from pycam.schemas import (
    DayNightMode,
    Info,
    VideoCapability,
    VideoSpecs,
    VideoBitrateType,
    VideoBitrate,
    VideoEncodeType,
    VideoResolution,
    VideoQuality,
)


def test_daynight_mode_values() -> None:
    assert DayNightMode.NIGHT.value == "on"
    assert DayNightMode.DAY.value == "off"
    assert DayNightMode.AUTO.value == "auto"


def test_info_typeddict() -> None:
    info: Info = {
        "device_model": "Tapo C200",
        "sw_version": "1.0.0",
        "hw_version": "1.0",
        "is_calibrated": True,
    }
    assert info["device_model"] == "Tapo C200"
    assert isinstance(info["is_calibrated"], bool)


def test_video_quality_typeddict() -> None:
    vq: VideoSpecs = {
        "bitrate": VideoBitrate.BR_1024,
        "default_bitrate": VideoBitrate.BR_2048,
        "bitrate_type": VideoBitrateType.CBR,
        "frame_rate": 30,
        "encode_type": VideoEncodeType.H264,
        "resolution": VideoResolution.RES_1080P,
        "quality": VideoQuality(5),
    }
    assert vq["resolution"] == VideoResolution.RES_1080P


def test_video_capability_typeddict() -> None:
    vc: VideoCapability = {
        "bitrates": [VideoBitrate.BR_1024, VideoBitrate.BR_512],
        "bitrate_types": [VideoBitrateType.CBR, VideoBitrateType.VBR],
        "frame_rates": [15, 30, 60],
        "encode_types": [VideoEncodeType.H264, VideoEncodeType.H265],
        "resolutions": [
            VideoResolution.RES_1080P,
            VideoResolution.RES_360P,
            VideoResolution.RES_720P,
        ],
        "qualitys": [VideoQuality(1), VideoQuality(3), VideoQuality(5)],
    }
    assert VideoResolution.RES_SUPER_HD not in vc["resolutions"]
