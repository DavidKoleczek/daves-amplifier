from pathlib import Path

from dotenv import load_dotenv


def load_root_dotenv():
    load_dotenv(Path(__file__).parents[4] / ".env")
