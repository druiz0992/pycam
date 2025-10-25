from ..schemas import DayNightMode, VideoQuality
from .secrets import CameraSecrets
from .settings import CameraSettings
from dataclasses import dataclass


class CameraConfig:
    """
    Container for camera secrets and settings.
    """

    def __init__(self, config_path: str = "config.yaml"):
        # Load secrets
        self.secrets = CameraSecrets()

        # Load settings
        self.settings = CameraSettings(config_path)

    @property
    def host(self) -> str:
        return self.settings.host

    @property
    def user_camera(self) -> str:
        return self.settings.user_camera

    @property
    def user_cloud(self) -> str:
        return self.settings.user_cloud

    @property
    def password_camera(self) -> str:
        return self.secrets.password_camera

    @property
    def password_cloud(self) -> str:
        return self.secrets.password_cloud

    @property
    def port(self) -> int:
        return self.settings.port

    @property
    def flip_image(self) -> bool:
        return self.settings.flip_image

    @property
    def daynight_mode(self) -> DayNightMode:
        return self.settings.daynight_mode

    @property
    def video_quality(self) -> VideoQuality:
        return self.settings.video_quality

    @property
    def start_position(self):
        return self.settings.start_position


@dataclass
class RuntimeConfig:
    """Runtime configuration of the camera (post-loaded from CameraConfig)."""

    host: str
    port: int
    flip_image: bool
    daynight_mode: DayNightMode

    @classmethod
    def from_config(cls, cfg) -> "RuntimeConfig":
        """Factory method to build from a CameraConfig-like object."""
        return cls(
            host=cfg.host,
            port=cfg.port,
            flip_image=cfg.flip_image,
            daynight_mode=cfg.daynight_mode,
        )
