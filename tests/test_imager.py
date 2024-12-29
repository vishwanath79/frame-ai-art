import pytest
from unittest.mock import patch, mock_open
from imager import generate_image

def test_generate_image_success(mock_openai, mock_requests_get):
    """Test successful image generation"""
    with patch('imager.OpenAI', return_value=mock_openai), \
         patch('imager.requests.get', return_value=mock_requests_get), \
         patch('builtins.open', mock_open()):
        
        # Test image generation
        result = generate_image("test prompt")
        
        # Verify results
        assert result is not None
        filename, filepath = result
        assert filename.endswith('.png')
        assert filepath.startswith('images/')
        
        # Verify OpenAI was called correctly
        mock_openai.images.generate.assert_called_once_with(
            model='dall-e-3',
            prompt="test prompt",
            quality='hd',
            n=1
        )

def test_generate_image_request_failure():
    """Test image generation when request fails"""
    with patch('imager.OpenAI') as mock_openai, \
         patch('imager.requests.get') as mock_get:
        
        # Setup mock to simulate request failure
        mock_get.return_value.status_code = 404
        
        # Test image generation
        result = generate_image("test prompt")
        
        # Verify failure
        assert result is None 