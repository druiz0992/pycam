from .camera import Camera
from .api.api import CameraAPI
from .api.tapo import PytapoClient
from .schemas import Info, VideoQuality, VideoCapability, DayNightMode
from .errors import CameraError, CommandError, ConnectionError, AuthenticationError
from .wrappers.tapo_camera import TapoCamera

from .config.secrets import CameraSecrets
from .config.settings import CameraSettings
from .config.config import CameraConfig

# Clean namespace for `from camera import *`
__all__ = [
    "Camera",
    "TapoCamera",
    "CameraAPI",
    "CameraConfig",
    "PytapoClient",
    "Info",
    "VideoQuality",
    "VideoCapability",
    "DayNightMode",
    "CameraError",
    "CommandError",
    "ConnectionError",
    "AuthenticationError",
    "CameraSecrets",
    "CameraSettings",
]
