from pathlib import Path

# Project Root

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data Directories

DATA_DIR = PROJECT_ROOT / "data"

IMAGE_DIR = DATA_DIR / "images"

XML_DIR = DATA_DIR / "xml"

SIGNATURE_DIR = DATA_DIR / "signatures"

DATABASE_DIR = DATA_DIR / "database"

OUTPUT_DIR = DATA_DIR / "output"

LOG_DIR = PROJECT_ROOT / "logs"

TEST_IMAGE_DIR = DATA_DIR / "test_images"

# Database

DATABASE_PATH = DATABASE_DIR / "attendance.db"

# GUI

WINDOW_WIDTH = 1400

WINDOW_HEIGHT = 850

PREVIEW_WIDTH = 900

PREVIEW_HEIGHT = 650

THEME = "dark"

COLOR_THEME = "blue"

# Image Processing

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff"
}

DEFAULT_THRESHOLD = 127

MAX_BINARY_VALUE = 255

GAUSSIAN_KERNEL = (5, 5)

MEDIAN_KERNEL = 5

# Logging

LOG_FILE = LOG_DIR / "system.log"

LOG_LEVEL = "INFO"