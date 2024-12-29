import pytest
from unittest.mock import Mock
import os
import sys

# Add the parent directory to the path so we can import the main modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_openai():
    """Mock OpenAI client fixture"""
    mock = Mock()
    # Setup mock response for image generation
    mock.images.generate.return_value = Mock(
        data=[Mock(url="http://fake-image-url.com/image.png")]
    )
    return mock

@pytest.fixture
def mock_samsung_tv():
    """Mock Samsung TV fixture"""
    mock = Mock()
    # Setup basic mock responses
    mock.art.return_value.supported.return_value = True
    mock.art.return_value.available.return_value = [
        {'content_id': 'MY001', 'title': 'Test Art 1'},
        {'content_id': 'MY002', 'title': 'Test Art 2'}
    ]
    return mock

@pytest.fixture
def mock_requests_get():
    """Mock requests.get fixture"""
    mock = Mock()
    mock.status_code = 200
    mock.raw.decode_content = True
    return mock 