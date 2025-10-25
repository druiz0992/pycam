import os
from typing import Optional, cast


class CameraSecretsError(Exception):
    """Raised when a required camera secret is missing."""


class CameraSecrets:
    """
    Generic camera secrets (host, user, password, etc.)

    Raises CameraSecretsError if any required field is empty.
    """

    def __init__(self, password_camera: str = "", password_cloud: str = ""):
        # Load from arguments or environment
        self.password_camera: str = password_camera or os.getenv("PASSWORD_CAMERA", "")
        self.password_cloud: str = password_cloud or os.getenv("PASSWORD_CLOUD", "")

        # Validate that nothing is empty
        missing = [
            name
            for name, value in {
                "password_camera": self.password_camera,
                "password_cloud": self.password_cloud,
            }.items()
            if not value
        ]

        if missing:
            raise CameraSecretsError(
                f"Missing required camera secrets: {', '.join(missing)}"
            )
