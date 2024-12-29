import pytest
from unittest.mock import patch, Mock
from main import SamsungArtController

@pytest.fixture
def controller(mock_samsung_tv):
    """Create a controller instance with mocked TV"""
    with patch('main.SamsungTVWS', return_value=mock_samsung_tv):
        return SamsungArtController("192.168.1.100")

def test_check_art_mode_support(controller):
    """Test art mode support check"""
    assert controller.check_art_mode_support() is True

def test_upload_image_success(controller):
    """Test successful image upload"""
    with patch('builtins.open', mock_open(read_data=b"fake_image_data")):
        result = controller.upload_image_to_tv("fake_image.jpg")
        assert result is True

def test_clean_old_art(controller):
    """Test cleaning old art"""
    controller.clean_old_art()
    
    # Verify delete was called for each MY* content_id
    art = controller.tv.art()
    assert art.delete.call_count == 2  # We have 2 mock MY* items

def test_set_latest_art(controller):
    """Test setting latest art"""
    result = controller.set_latest_art()
    
    # Should select MY002 as it's the highest number
    assert result == 'MY002'
    controller.tv.art().select_image.assert_called_once_with('MY002') 