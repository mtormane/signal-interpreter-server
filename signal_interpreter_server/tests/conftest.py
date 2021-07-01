import os
import pytest


@pytest.fixture
def file_path():
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(curr_dir, "integration", "fixtures", "test_basic.json")


@pytest.fixture
def bad_file_path():
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(curr_dir, "integration", "fixtures", "fake_db.json")
