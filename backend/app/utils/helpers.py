from pathlib import Path


def format_file_size(size_bytes: int) -> float:
    
    # Convert bytes to MB.
    return round(size_bytes / (1024 * 1024), 2)


def ensure_directory(path: Path):

    # Create directory if it does not exist.
    path.mkdir(parents=True, exist_ok=True)


def get_extension(file_path: str) -> str:
    
    # Return file extension in lowercase.
    return Path(file_path).suffix.lower()