from typing import Optional, cast
from enum import IntFlag

from pytapo import Tapo

from .api import CameraAPI
from ..errors import AuthenticationError, CommandError, handle_errors
from ..schemas import (
    Info,
    VideoQuality,
    VideoSpecs,
    VideoCapability,
    DayNightMode,
    VideoEncodeType,
    VideoBitrate,
    VideoResolution,
    VideoBitrateType,
)
from ..config.config import CameraConfig


class CameraPosition(IntFlag):
    DOWN = 270
    UP = 90
    LEFT = 180
    RIGHT = 0


class PytapoClient(CameraAPI):
    """Wrapper around pytapo."""

    @handle_errors(error_type=AuthenticationError)
    def __init__(self, config: CameraConfig):
        self._client = Tapo(config.host, config.user_cloud, config.password_cloud)

    @handle_errors()
    def get_info(self) -> Info:
        data = cast(dict, self._client.getBasicInfo())
        basic = data["device_info"]["basic_info"]
        info: Info = {
            "device_model": basic["device_model"],
            "sw_version": basic["sw_version"],
            "hw_version": basic["hw_version"],
            "is_calibrated": basic["is_cal"],
        }
        return info

    @handle_errors()
    def get_video_specs(self) -> VideoSpecs:
        data = cast(dict, self._client.getVideoQualities())
        video = data["video"]["main"]
        return {
            "bitrate": VideoBitrate(int(video["bitrate"])),
            "default_bitrate": VideoBitrate(int(video["default_bitrate"])),
            "bitrate_type": VideoBitrateType(video["bitrate_type"]),
            "frame_rate": int(video["frame_rate"]),
            "encode_type": VideoEncodeType(video["encode_type"]),
            "resolution": VideoResolution(video["resolution"]),
            "quality": VideoQuality(int(video["quality"])),
        }

    @handle_errors()
    def get_video_capabilities(self) -> VideoCapability:
        data = cast(dict, self._client.getVideoCapability())
        capabilities = data["video_capability"]["main"]
        return {
            "bitrates": [
                VideoBitrate(int(bitrate)) for bitrate in capabilities["bitrates"]
            ],
            "bitrate_types": [
                VideoBitrateType(bitrate_type)
                for bitrate_type in capabilities["bitrate_types"]
            ],
            "frame_rates": [
                int(frame_rate) for frame_rate in capabilities["frame_rates"]
            ],
            "encode_types": [
                VideoEncodeType(encode_type)
                for encode_type in capabilities["encode_types"]
            ],
            "resolutions": [
                VideoResolution(resolution)
                for resolution in capabilities["resolutions"]
            ],
            "qualitys": [
                VideoQuality(int(quality)) for quality in capabilities["qualitys"]
            ],
        }

    @handle_errors()
    def move_motor(self, pan: float, tilt: float) -> bool:
        try:
            self._client.moveMotor(pan, tilt)
            return True
        except CommandError as e:
            pass
        return False

    @handle_errors()
    def calibrate_motor(self):
        self._client.calibrateMotor()

    @handle_errors()
    def reboot(self):
        self._client.reboot()

    @handle_errors()
    def set_daynight_mode(self, mode: DayNightMode):
        self._client.setDayNightMode(mode.value)

    @handle_errors()
    def get_daynight_mode(self) -> DayNightMode:
        return DayNightMode(self._client.getDayNightMode())

    @handle_errors()
    def is_image_flipped(self) -> bool:
        return bool(self._client.getImageFlipVertical())

    @handle_errors()
    def flip_image(self, flag: bool):
        self._client.setImageFlipVertical(flag)

    def get_url(self, config: Optional[CameraConfig]) -> str:
        if config is None:
            return ""
        user = config.user_camera
        pwd = config.password_camera
        port = config.port
        host = config.host
        stream = "stream1" if config.video_quality == VideoQuality.HIGH else "stream2"

        return f"rtsp://{user}:{pwd}@{host}:{port}/{stream}"
