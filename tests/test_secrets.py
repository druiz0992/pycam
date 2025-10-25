import pytest
from pycam.config.secrets import CameraSecrets, CameraSecretsError


def test_camera_secrets_success(monkeypatch):
    # Set environment variables
    monkeypatch.setenv("PASSWORD_CAMERA", "pass_cam")
    monkeypatch.setenv("PASSWORD_CLOUD", "pass_cloud")

    secrets = CameraSecrets()

    assert secrets.password_camera == "pass_cam"
    assert secrets.password_cloud == "pass_cloud"


def test_camera_secrets_missing(monkeypatch):
    # Clear env variables
    monkeypatch.delenv("PASSWORD_CAMERA", raising=False)
    monkeypatch.delenv("PASSWORD_CLOUD", raising=False)

    with pytest.raises(CameraSecretsError) as excinfo:
        CameraSecrets()

    assert "Missing required camera secrets" in str(excinfo.value)
