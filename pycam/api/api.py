from abc import ABC, abstractmethod
from typing import Optional

from ..schemas import (
    DayNightMode,
    Info,
    VideoSpecs,
    VideoCapability,
)
from ..config.config import CameraConfig


class CameraAPI(ABC):
    """Abstract interface for any camera implementation."""

    @abstractmethod
    def get_info(self) -> Info: ...

    @abstractmethod
    def get_video_specs(self) -> VideoSpecs: ...

    @abstractmethod
    def get_video_capabilities(self) -> VideoCapability: ...

    @abstractmethod
    def move_motor(self, pan: float, tilt: float) -> bool: ...

    @abstractmethod
    def calibrate_motor(self): ...

    @abstractmethod
    def reboot(self): ...

    @abstractmethod
    def set_daynight_mode(self, mode): ...

    @abstractmethod
    def get_daynight_mode(self) -> DayNightMode: ...

    @abstractmethod
    def is_image_flipped(self) -> bool: ...

    @abstractmethod
    def flip_image(self, flag: bool): ...

    @abstractmethod
    def get_url(self, config: Optional[CameraConfig]) -> str: ...
