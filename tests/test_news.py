import pytest
from unittest.mock import patch
from news import get_prompt

def test_get_prompt_success():
    """Test successful API response from Perplexity"""
    mock_response = {
        "choices": [{
            "message": {
                "content": "Test news summary"
            }
        }]
    }
    
    with patch('news.requests.post') as mock_post:
        # Setup mock response
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.status_code = 200
        
        result = get_prompt("What's the news today?")
        
        # Verify result
        assert result == "Test news summary"
        
        # Verify API was called correctly
        mock_post.assert_called_once()
        args = mock_post.call_args
        assert "api.perplexity.ai" in args[0][0]

def test_get_prompt_api_failure():
    """Test API failure handling"""
    with patch('news.requests.post') as mock_post:
        # Setup mock to simulate API failure
        mock_post.side_effect = Exception("API Error")
        
        result = get_prompt("What's the news today?")
        
        # Verify failure handling
        assert result is None 