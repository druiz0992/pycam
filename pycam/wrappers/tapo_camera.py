from dotenv import load_dotenv
from typing import Optional
import sys
import traceback
import os

from pycam.config.config import CameraConfig
from pycam.api.tapo import PytapoClient
from pycam.camera import Camera
from pycam.errors import AuthenticationError, ConnectionError


class TapoCamera(Camera):
    """
    TapoCamera wrapper: automatically loads .env, config, API, and Camera.
    """

    def __init__(self, config_path: str, env_path: str):
        """Initializes TapoCamera."""
        # Load .env file
        if env_path is None:
            env_path = os.path.join(os.getcwd(), ".env")

        if os.path.exists(env_path):
            load_dotenv(dotenv_path=env_path)
        else:
            self._die()

        try:
            config = CameraConfig(config_path)
        except Exception as e:
            self._die()

        try:
            api = PytapoClient(config)
        except ConnectionError as e:
            self._die()
        except AuthenticationError as e:
            self._die()

        # Initialize base Camera
        super().__init__(api, config)

    def _die(self):
        traceback.print_exc()
        sys.exit(1)
