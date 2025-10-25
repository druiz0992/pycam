from typing import Optional, Callable, TypeVar
import time

from pycam.config.config import RuntimeConfig
from .api.api import CameraAPI
from .errors import CommandError, AuthenticationError
from .schemas import Info, VideoSpecs, VideoCapability, DayNightMode
from .config.config import CameraConfig
from .utils import clamp
from .calibration import CameraCalibration

R = TypeVar("R")


class Camera:
    """
    Generic camera wrapper.

    Can control any camera implementing the CameraAPI interface.
    """

    def __init__(
        self, api: CameraAPI, config: CameraConfig, calib_path: Optional[str] = None
    ):
        """
        api: an instance of a concrete CameraAPI implementation (e.g., PytapoClient)
        settings: optional CameraSettings to apply on initialization
        """
        self._api = api
        self._config = config

        self._tilt = 90.0
        self._pan = 360.0

        self._init_camera()

        if calib_path:
            self._calibration = CameraCalibration.from_yaml(calib_path)
        else:
            width, height = self._get_resolution()
            self._calibration = CameraCalibration.default(width, height)

    @property
    def calibration(self) -> CameraCalibration:
        return self._calibration

    @property
    def tilt(self) -> float:
        return self._tilt

    @property
    def pan(self) -> float:
        return self._pan

    ### Config
    def get_config(self) -> RuntimeConfig:

        return RuntimeConfig.from_config(self._config)

    ### API
    # --- Info / status methods ---
    def get_info(self) -> Info:
        """Returns basic camera information including device_model, sw_version, hw_version..."""
        return self._api.get_info()

    def get_video_specs(self) -> VideoSpecs:
        """Returns video configuration information such as encoding type, frame rate or bitrate"""
        return self._api.get_video_specs()

    def get_video_capabilities(self) -> VideoCapability:
        """Returns video configuration options"""
        return self._api.get_video_capabilities()

    def get_daynight_mode(self) -> DayNightMode:
        """Returns DayNightMode (nigh vision or day)"""
        return self._api.get_daynight_mode()

    # --- Motor control ---
    def move_motor(self, pan: float, tilt: float):
        """Command motor to move in specicied pan and tilt angles (degrees)"""
        pan = clamp(self._pan, pan, 0.0, 360.0)
        tilt = clamp(self._tilt, tilt, 0.0, 90)
        self._pan += pan
        self._tilt += tilt

        self._safe_call(self._api.move_motor, pan, tilt)

    def calibrate_motor(self):
        """Run motor calibration routine"""
        self._api.calibrate_motor()

    def reboot(self):
        """Reboot camera"""
        self._api.reboot()

    def is_image_flipped(self) -> bool:
        """Returns if image is flipped"""
        return self._api.is_image_flipped()

    def flip_image(self, flag: bool) -> None:
        """Command to configure DayNight mode"""
        self._api.flip_image(flag)

    def set_daynight_mode(self, mode: DayNightMode):
        """Command to configure DayNight mode"""
        self._api.set_daynight_mode(mode)

    def get_url(self) -> str:
        """Get RTSP url"""
        return self._api.get_url(self._config)

    ### INTERNAL

    def _get_resolution(self) -> tuple[int, int]:
        info = self._api.get_video_specs()
        resolution = info.get("resolution")
        if resolution:
            width, height = map(int, resolution.value.split("*"))
        else:
            width, height = 0, 0
        return width, height

    def _safe_call(self, fn: Callable[..., R], *args, **kwargs) -> Optional[R]:
        try:
            return fn(*args, **kwargs)
        except CommandError as e:
            return None
        except AuthenticationError as e:
            raise

    def _init_camera(self):
        self._api.flip_image(self._config.flip_image)
        self._api.set_daynight_mode(self._config.daynight_mode)

        self.move_motor(-360.0, -90)
        time.sleep(5)

        start_position = self._config.start_position
        self.move_motor(start_position["pan"], start_position["tilt"])
