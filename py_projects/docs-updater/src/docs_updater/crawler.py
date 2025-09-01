"""Documentation crawler using crawl4ai."""

from dataclasses import dataclass
import re
from urllib.parse import urljoin, urlparse

from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import httpx
from loguru import logger
from pydantic import BaseModel


class Link(BaseModel):
    """Represents a link found on a page."""

    url: str
    text: str


class URLResult(BaseModel):
    """Result from crawling a URL."""

    url: str
    html: str
    markdown: str
    links: list[Link] = []


@dataclass
class MarkdownFile:
    """Represents a markdown file to download."""

    url: str
    path: str
    content: str = ""


async def _handle_web_content(url: str, verbose: bool = False) -> URLResult:
    """Fetch and parse web content using crawl4ai."""
    browser_config = BrowserConfig(
        browser_type="chromium",
        headless=True,
        verbose=verbose,
        user_agent_mode="random",
        java_script_enabled=True,
        extra_args=["--disable-blink-features=AutomationControlled", "--disable-web-security"],
    )
    run_config = CrawlerRunConfig(
        scan_full_page=True,
        user_agent_mode="random",
        cache_mode=CacheMode.DISABLED,
        markdown_generator=DefaultMarkdownGenerator(),
        verbose=verbose,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=url,
            config=run_config,
        )

    links: list[Link] = []
    seen_urls: set[str] = set()
    combined_link_data = result.links.get("internal", []) + result.links.get("external", [])  # type: ignore
    for link_data in combined_link_data:
        href = link_data.get("href", "")
        if href and href not in seen_urls:
            seen_urls.add(href)
            link = Link(
                url=href,
                text=link_data.get("title", "") or link_data.get("text", ""),
            )
            links.append(link)

    url_result = URLResult(
        url=url,
        html=result.html or "",  # type: ignore
        markdown=result.markdown or "",  # type: ignore
        links=links,
    )
    return url_result


async def get_github_files(repo_url: str) -> list[MarkdownFile]:
    """Get markdown files from a GitHub repository."""
    # Parse GitHub URL to get owner and repo
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    owner = path_parts[0]
    repo = path_parts[1]

    # Default branch could be specified in URL after /tree/
    branch = "main"
    subpath = ""

    if len(path_parts) > 2 and path_parts[2] == "tree" and len(path_parts) > 3:
        branch = path_parts[3]
        if len(path_parts) > 4:
            subpath = "/".join(path_parts[4:])

    # Use GitHub API to get repository contents
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    files: list[MarkdownFile] = []

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
            response.raise_for_status()

            data = response.json()
            tree = data.get("tree", [])

            for item in tree:
                if item["type"] == "blob":
                    path = item["path"]

                    # Filter to only markdown files
                    if path.endswith((".md", ".mdx")):
                        # If subpath is specified, only include files under that path
                        if subpath and not path.startswith(subpath):
                            continue

                        # Remove subpath prefix if present
                        display_path = path[len(subpath) :].lstrip("/") if subpath else path

                        # Construct raw content URL
                        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"

                        files.append(MarkdownFile(url=raw_url, path=display_path))

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                # Try with master branch if main doesn't exist
                if branch == "main":
                    api_url = api_url.replace("/main?", "/master?")
                    response = await client.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
                    response.raise_for_status()

                    data = response.json()
                    tree = data.get("tree", [])

                    for item in tree:
                        if item["type"] == "blob":
                            path = item["path"]

                            if path.endswith((".md", ".mdx")):
                                if subpath and not path.startswith(subpath):
                                    continue

                                display_path = path[len(subpath) :].lstrip("/") if subpath else path
                                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{path}"

                                files.append(MarkdownFile(url=raw_url, path=display_path))
                else:
                    raise
            else:
                raise

    return sorted(files, key=lambda f: f.path)


async def crawl_docs(url: str) -> list[MarkdownFile]:
    """Crawl a documentation website and find markdown pages."""
    logger.info(f"Crawling documentation from: {url}")

    # Fetch the main page
    result = await _handle_web_content(url)

    files: list[MarkdownFile] = []
    seen_urls: set[str] = set()

    # Add the main page if it has content
    if result.markdown.strip():
        parsed = urlparse(url)
        filename = parsed.path.strip("/").replace("/", "_") or "index"
        if not filename.endswith(".md"):
            filename += ".md"
        files.append(MarkdownFile(url=url, path=filename, content=result.markdown))
        seen_urls.add(url)

    # Filter links to find potential documentation pages
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    for link in result.links:
        link_url = link.url

        # Make absolute URL if relative
        if not link_url.startswith(("http://", "https://")):
            link_url = urljoin(url, link_url)

        # Skip if already seen
        if link_url in seen_urls:
            continue

        # Skip external links (different domain)
        if not link_url.startswith(base_url):
            continue

        # Skip non-documentation links
        skip_patterns = [
            r"#",  # Anchors
            r"\.(jpg|jpeg|png|gif|svg|ico|pdf|zip|tar|gz|exe|dmg)$",  # Binary files
            r"/signin|/login|/signup|/register|/auth",  # Auth pages
            r"/search\?",  # Search queries
            r"github\.com|twitter\.com|facebook\.com|linkedin\.com",  # Social media
        ]

        if any(re.search(pattern, link_url, re.IGNORECASE) for pattern in skip_patterns):
            continue

        # Include if it looks like a documentation page
        include_patterns = [
            r"/docs/",
            r"/documentation/",
            r"/guide/",
            r"/tutorial/",
            r"/reference/",
            r"/api/",
            r"/manual/",
            r"\.md$",
            r"\.mdx$",
        ]

        if any(re.search(pattern, link_url, re.IGNORECASE) for pattern in include_patterns):
            # Generate a reasonable file path
            parsed = urlparse(link_url)
            path = parsed.path.strip("/")

            # Clean up the path
            if not path:
                path = "index"

            # Ensure .md extension
            if not path.endswith((".md", ".mdx")):
                path += ".md"

            # Replace slashes with underscores for flat structure
            path = path.replace("/", "_")

            files.append(MarkdownFile(url=link_url, path=path))
            seen_urls.add(link_url)

    return sorted(files, key=lambda f: f.path)


async def fetch_single_file(url: str) -> str:
    """Fetch content of a single file."""
    # Check if it's a raw GitHub URL
    if "raw.githubusercontent.com" in url:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text

    # Otherwise, use crawl4ai to get the markdown
    result = await _handle_web_content(url)
    return result.markdown
