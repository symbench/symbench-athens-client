from pathlib import Path


def get_test_file_path(filename):
    """Given a filename prepend it with the correct test data location"""
    return str(Path(__file__).resolve().parent / "assets" / filename)
