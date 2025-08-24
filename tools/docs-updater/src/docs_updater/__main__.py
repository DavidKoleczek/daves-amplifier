"""Entry point for docs-updater."""

from pathlib import Path
from typing import ClassVar
from urllib.parse import urlparse

from loguru import logger
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, LoadingIndicator, Tree
from textual.widgets.tree import TreeNode

from docs_updater.crawler import MarkdownFile, crawl_docs, get_github_files


class FileSelectionScreen(Screen):
    """Screen for selecting files to download."""

    CSS = """
    #file-tree {
        height: 75%;
        border: solid $primary;
        margin: 1 0;
    }
    
    .button-row {
        margin: 2 0;
        align: center middle;
        height: 3;
    }
    
    #selection-count {
        color: $text-muted;
        text-style: italic;
    }
    """

    def __init__(self, files: list[MarkdownFile], folder_name: str):
        super().__init__()
        self.files = files
        self.folder_name = folder_name
        self.selected_files: set[str] = set()

    def compose(self) -> ComposeResult:
        """Create the UI for file selection."""
        yield Header()
        yield Container(
            Label("Select files to download (click to toggle selection):", classes="title"),
            ScrollableContainer(
                Tree("Files"),
                id="file-tree",
            ),
            Label("0 files selected", id="selection-count", classes="status-label"),
            Horizontal(
                Button("Select All", id="select-all", variant="primary"),
                Button("Deselect All", id="deselect-all"),
                Button("Download Selected", id="download", variant="success"),
                Button("Cancel", id="cancel", variant="error"),
                classes="button-row",
            ),
            id="main-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Populate the tree with files."""
        tree = self.query_one(Tree)
        tree.show_root = False
        self._build_tree(tree)
        self.update_selection_count()

    def _build_tree(self, tree: Tree) -> None:
        """Build the file tree structure."""
        path_nodes: dict[str, TreeNode] = {}

        for file in self.files:
            parts = file.path.split("/")
            parent_node = tree.root

            # Build directory path
            for i, part in enumerate(parts[:-1]):
                current_path = "/".join(parts[: i + 1])
                if current_path not in path_nodes:
                    node = parent_node.add(f"📁 {part}")
                    path_nodes[current_path] = node
                parent_node = path_nodes[current_path]

            # Add file as leaf
            if parts:  # Safety check
                parent_node.add_leaf(f"📄 {parts[-1]}", data=file)

    def update_selection_count(self) -> None:
        """Update the selection count label."""
        count_label = self.query_one("#selection-count", Label)
        selected = len(self.selected_files)
        total = len(self.files)

        if selected == 0:
            count_label.update("No files selected")
        elif selected == total:
            count_label.update(f"All {total} files selected")
        else:
            count_label.update(f"{selected} of {total} files selected")

    def _get_file_label(self, file: MarkdownFile, selected: bool) -> str:
        """Get the label for a file node."""
        filename = file.path.split("/")[-1]
        return f"✅ 📄 {filename}" if selected else f"📄 {filename}"

    def _toggle_node_selection(self, node: TreeNode) -> None:
        """Toggle selection for a node and all its children."""
        if node.data and isinstance(node.data, MarkdownFile):
            file = node.data
            if file.url in self.selected_files:
                self.selected_files.remove(file.url)
                node.set_label(self._get_file_label(file, False))
            else:
                self.selected_files.add(file.url)
                node.set_label(self._get_file_label(file, True))

        # Recursively toggle children
        for child in node.children:
            self._toggle_node_selection(child)

    def _update_all_nodes(self, node: TreeNode, select: bool) -> None:
        """Update selection state for all nodes."""
        if node.data and isinstance(node.data, MarkdownFile):
            file = node.data
            if select:
                self.selected_files.add(file.url)
            else:
                self.selected_files.discard(file.url)
            node.set_label(self._get_file_label(file, select))

        for child in node.children:
            self._update_all_nodes(child, select)

    @on(Tree.NodeHighlighted)
    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        """Update node appearance on highlight."""
        if event.node.data and isinstance(event.node.data, MarkdownFile):
            file = event.node.data
            selected = file.url in self.selected_files
            event.node.set_label(self._get_file_label(file, selected))

    @on(Tree.NodeSelected)
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Toggle file selection on click."""
        self._toggle_node_selection(event.node)
        self.update_selection_count()

    @on(Button.Pressed, "#select-all")
    def action_select_all(self) -> None:
        """Select all files."""
        tree = self.query_one(Tree)
        self._update_all_nodes(tree.root, select=True)
        self.update_selection_count()

    @on(Button.Pressed, "#deselect-all")
    def action_deselect_all(self) -> None:
        """Deselect all files."""
        tree = self.query_one(Tree)
        self._update_all_nodes(tree.root, select=False)
        self.update_selection_count()

    @on(Button.Pressed, "#download")
    async def action_download(self) -> None:
        """Download selected files."""
        if not self.selected_files:
            self.notify("No files selected", severity="warning")
            return

        selected = [f for f in self.files if f.url in self.selected_files]
        self.app.pop_screen()

        if isinstance(self.app, DocsUpdaterApp):
            await self.app.download_files(selected, self.folder_name)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """Cancel and return to main screen."""
        self.app.pop_screen()


class DocsUpdaterApp(App):
    """A Textual app for updating documentation."""

    CSS = """
    #main-container {
        padding: 1;
    }

    .title {
        text-style: bold;
        margin: 1 0;
    }

    Input {
        margin: 1 0;
    }

    Button {
        margin: 1 2;
    }

    LoadingIndicator {
        margin: 2;
    }

    .status-label {
        margin: 1;
        text-align: center;
    }
    """

    BINDINGS: ClassVar = [
        ("escape", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        """Create the main UI."""
        yield Header()
        yield Container(
            Label("Enter URL (GitHub repo or documentation website):", classes="title"),
            Input(
                placeholder="https://github.com/user/repo or https://docs.example.com",
                id="url-input",
            ),
            Label("Enter folder name (will be saved to ai_context/docs/<name>):", classes="title"),
            Input(
                placeholder="my-docs",
                id="folder-input",
            ),
            Button("Fetch Documentation", id="fetch-btn", variant="primary"),
            id="main-container",
        )
        yield Footer()

    def _get_inputs(self) -> tuple[str, str] | None:
        """Get and validate input values."""
        url_input = self.query_one("#url-input", Input)
        folder_input = self.query_one("#folder-input", Input)

        url = url_input.value.strip()
        folder_name = folder_input.value.strip()

        if not url:
            self.notify("Please enter a URL", severity="error")
            return None

        if not folder_name:
            self.notify("Please enter a folder name", severity="error")
            return None

        return url, folder_name

    def _show_loading(self, message: str) -> None:
        """Show loading indicator with message."""
        container = self.query_one("#main-container", Container)
        container.mount(LoadingIndicator())
        container.mount(Label(message, classes="status-label"))

    def _hide_loading(self) -> None:
        """Remove loading indicator and status label."""
        container = self.query_one("#main-container", Container)
        for widget in container.query("LoadingIndicator, .status-label"):
            widget.remove()

    @on(Button.Pressed, "#fetch-btn")
    def on_fetch_pressed(self) -> None:
        """Handle fetch button press."""
        inputs = self._get_inputs()
        if inputs:
            url, folder_name = inputs
            self.fetch_documentation(url, folder_name)

    @work(exclusive=True)
    async def fetch_documentation(self, url: str, folder_name: str) -> None:
        """Fetch documentation from the URL."""
        self._show_loading("Fetching documentation...")

        try:
            # Determine if GitHub URL
            parsed = urlparse(url)
            is_github = "github.com" in (parsed.hostname or "")

            # Fetch files based on URL type
            files = await (get_github_files(url) if is_github else crawl_docs(url))

            self._hide_loading()

            if not files:
                self.notify("No markdown files found", severity="warning")
                return

            # Show file selection screen
            self.push_screen(FileSelectionScreen(files, folder_name))

        except Exception as e:
            logger.error(f"Error fetching documentation: {e}")
            self.notify(f"Error: {e!s}", severity="error")
            self._hide_loading()

    async def download_files(self, files: list[MarkdownFile], folder_name: str) -> None:
        """Download and save selected files."""
        self._show_loading(f"Downloading {len(files)} files...")

        try:
            # Create output directory
            output_dir = Path.cwd() / "ai_context" / "docs" / folder_name
            output_dir.mkdir(parents=True, exist_ok=True)

            # Download each file
            for file in files:
                file_path = output_dir / file.path
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Fetch content if not already available
                if not file.content:
                    from docs_updater.crawler import fetch_single_file

                    file.content = await fetch_single_file(file.url)

                # Save file
                file_path.write_text(file.content)
                logger.info(f"Saved: {file_path}")

            self._hide_loading()

            message = f"Successfully downloaded {len(files)} files to ai_context/docs/{folder_name}"
            self.notify(message, severity="information")
            logger.info(message)

        except Exception as e:
            logger.error(f"Error downloading files: {e}")
            self.notify(f"Error: {e!s}", severity="error")
            self._hide_loading()


def main() -> None:
    """Main entry point."""
    app = DocsUpdaterApp()
    app.run()


if __name__ == "__main__":
    main()
