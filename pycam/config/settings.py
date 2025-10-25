import yaml
from pathlib import Path
from ..schemas import DayNightMode, VideoQuality

DEFAULT_HOST = "127.0.0.1"
DEFAULT_USER = "admin"
DEFAULT_PORT = 554
DEFAULT_FLIP_IMAGE = True
DEFAULT_DAYNIGHT_MODE = "day"
DEFAULT_VIDEO_QUALITY = "high"
DEFAULT_INITIAL_TILT = 0.0
DEFAULT_INITIAL_PAN = 0.0


class CameraSettings:
    """
    Generic camera settings loaded from YAML.
    """

    def __init__(self, path: str):
        self.path = Path(path)
        self.load()

    def load(self):
        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found: {self.path}")

        with open(self.path, "r") as f:
            data = yaml.safe_load(f)

        self.host = data.get("host", DEFAULT_HOST)
        users = data.get("user", {})
        self.user_camera = users.get("camera", DEFAULT_USER)
        self.user_cloud = users.get("cloud", DEFAULT_USER)
        self.port = data.get("port", DEFAULT_PORT)
        self.flip_image = bool(data.get("flip_image", DEFAULT_FLIP_IMAGE))
        self.daynight_mode = DayNightMode(
            "off" if data.get("daynight_mode", DEFAULT_DAYNIGHT_MODE) == "day" else "on"
        )
        self.video_quality = VideoQuality(
            5 if data.get("video_quality", DEFAULT_VIDEO_QUALITY) == "high" else 1
        )

        self.start_position = data.get(
            "start_position", {"pan": DEFAULT_INITIAL_PAN, "tilt": DEFAULT_INITIAL_TILT}
        )
