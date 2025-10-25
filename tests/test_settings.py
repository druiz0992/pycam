import tempfile
import yaml
from pycam.config.settings import CameraSettings
from pycam.schemas import DayNightMode, VideoQuality


def test_camera_settings_loading():
    # Prepare a temporary YAML config
    config_data = {
        "host": "192.168.1.42",
        "user": {"camera": "admin123", "cloud": "admin"},
        "port": 554,
        "flip_image": True,
        "daynight_mode": "night",
        "video_quality": "high",
        "start_position": {"pan": 10.5, "tilt": 20.0},
    }

    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp_file:
        yaml.dump(config_data, tmp_file)
        tmp_file_path = tmp_file.name

    # Load settings
    settings = CameraSettings(tmp_file_path)

    # Assert fields loaded correctly
    assert settings.host == "192.168.1.42"
    assert settings.user_camera == "admin123"
    assert settings.user_cloud == "admin"
    assert settings.port == 554
    assert settings.flip_image is True
    assert settings.daynight_mode == DayNightMode.NIGHT
    assert settings.video_quality == VideoQuality.HIGH
    assert settings.start_position["pan"] == 10.5
    assert settings.start_position["tilt"] == 20.0
