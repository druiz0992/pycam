import pytest
from unittest.mock import MagicMock, patch
from pycam.api.tapo import PytapoClient
from pycam.schemas import (
    Info,
    VideoQuality,
    VideoSpecs,
    VideoCapability,
    DayNightMode,
    VideoBitrate,
    VideoBitrateType,
    VideoEncodeType,
    VideoResolution,
)
from pycam.config.config import CameraConfig

FAKE_BASIC_INFO = {
    "device_info": {
        "basic_info": {
            "device_type": "SMART.IPCAMERA",
            "device_model": "C510W",
            "sw_version": "1.2.1 Build 250919 Rel.39196n",
            "hw_version": "2.0",
            "is_cal": True,
        }
    }
}

FAKE_VIDEO_QUALITY = {
    "video": {
        "main": {
            "quality": "5",
            "bitrate": "1228",
            "frame_rate": "65551",
            "encode_type": "H264",
            "resolution": "2304*1296",
            "bitrate_type": "vbr",
            "default_bitrate": "1228",
        }
    }
}

FAKE_VIDEO_CAPABILITY = {
    "video_capability": {
        "main": {
            "encode_types": ["H264", "H265"],
            "frame_rates": ["65551", "65556", "65561"],
            "bitrates": ["256", "512", "1024", "1228", "2048"],
            "bitrate_types": ["cbr", "vbr"],
            "resolutions": ["2304*1296", "1920*1080", "1280*720", "640*360"],
            "qualitys": ["1", "3", "5"],
        }
    }
}

FAKE_DAYNIGHT = "auto"
FAKE_IMAGE_FLIP = True


@pytest.fixture
def temp_config_file(tmp_path):
    yaml_content = """
host: 192.168.1.42
user:
  camera: admin123
  cloud: admin
port: 554
flip_image: true
daynight_mode: night
video_quality: high
start_position:
   pan: 0.0
   tilt: 0.0
"""
    f = tmp_path / "config.yaml"
    f.write_text(yaml_content)
    return f


@pytest.fixture
def mock_tapo(monkeypatch):
    """Patch pytapo.Tapo and inject fake responses."""
    monkeypatch.setenv("PASSWORD_CAMERA", "fake_camera_pass")
    monkeypatch.setenv("PASSWORD_CLOUD", "fake_cloud_pass")

    with patch("pycam.api.tapo.Tapo") as MockTapo:
        instance = MockTapo.return_value
        instance.getBasicInfo.return_value = FAKE_BASIC_INFO
        instance.getVideoQualities.return_value = FAKE_VIDEO_QUALITY
        instance.getVideoCapability.return_value = FAKE_VIDEO_CAPABILITY
        instance.getDayNightMode.return_value = FAKE_DAYNIGHT
        instance.getImageFlipVertical.return_value = FAKE_IMAGE_FLIP
        yield instance


def test_get_info(mock_tapo, temp_config_file) -> None:
    config = CameraConfig(config_path=str(temp_config_file))
    client = PytapoClient(config)
    info: Info = client.get_info()

    assert info["device_model"] == "C510W"
    assert info["is_calibrated"] is True
    assert info["sw_version"].startswith("1.2.1")
    assert info["hw_version"].startswith("2.0")


def test_get_video_specs(mock_tapo, temp_config_file) -> None:
    config = CameraConfig(config_path=str(temp_config_file))
    client = PytapoClient(config)
    vq: VideoSpecs = client.get_video_specs()

    assert vq["bitrate"] == VideoBitrate.BR_1228
    assert vq["resolution"] == VideoResolution.RES_SUPER_HD
    assert vq["quality"] == VideoQuality(5)
    assert vq["frame_rate"] == 65551
    assert vq["encode_type"] == VideoEncodeType.H264
    assert vq["bitrate_type"] == VideoBitrateType.VBR
    assert vq["default_bitrate"] == 1228


def test_get_video_capabilities(mock_tapo, temp_config_file) -> None:
    config = CameraConfig(config_path=str(temp_config_file))
    client = PytapoClient(config)
    vc: VideoCapability = client.get_video_capabilities()
    assert VideoEncodeType.H264 in vc["encode_types"]
    assert VideoResolution.RES_SUPER_HD in vc["resolutions"]
    assert VideoQuality.HIGH in vc["qualitys"]
    assert 65551 in vc["frame_rates"]
    assert VideoBitrate.BR_256 in vc["bitrates"]
    assert VideoBitrateType.VBR in vc["bitrate_types"]


def test_get_daynight_mode(mock_tapo, temp_config_file) -> None:
    config = CameraConfig(config_path=str(temp_config_file))
    client = PytapoClient(config)
    mode = client.get_daynight_mode()
    assert mode == DayNightMode.AUTO


def test_is_image_flipped(mock_tapo, temp_config_file) -> None:
    config = CameraConfig(config_path=str(temp_config_file))
    client = PytapoClient(config)
    flipped = client.is_image_flipped()
    assert flipped is True
