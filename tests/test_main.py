import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import main

def test_load_config_env_vars(monkeypatch):
    monkeypatch.setenv('NASA_APOD_API_KEY', 'testkey')
    monkeypatch.setenv('WINDOWS_SAVE_DIR', '/tmp')
    api_key, windows_save_dir = main.load_config()
    assert api_key == 'testkey'
    assert windows_save_dir == Path('/tmp')

def test_load_config_missing(monkeypatch):
    monkeypatch.delenv('NASA_APOD_API_KEY', raising=False)
    monkeypatch.setenv('WINDOWS_SAVE_DIR', '/tmp')
    with pytest.raises(ValueError):
        main.load_config()

def test_process_data_image():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'media_type': 'image',
        'hdurl': 'https://example.com/image.jpg',
        'explanation': 'Test explanation'
    }
    with patch('main.requests.get') as mock_get:
        mock_img_resp = MagicMock()
        mock_img_resp.content = b'data'
        mock_img_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_img_resp
        filename, image_response, explanation, media_type = main.process_data(mock_response)
        assert filename == 'image.jpg'
        assert image_response == mock_img_resp
        assert explanation == 'Test explanation'
        assert media_type == 'image'

def test_process_data_non_image():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'media_type': 'video',
        'explanation': 'Test explanation'
    }
    filename, image_response, explanation, media_type = main.process_data(mock_response)
    assert filename == ''
    assert image_response is None
    assert explanation == 'Test explanation'
    assert media_type == 'video'
