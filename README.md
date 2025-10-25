# PyCam

**PyCam** is a lightweight and extensible Python framework for controlling IP cameras through a unified interface.  
Currently it supports **TP-Link Tapo cameras** via the [`pytapo`](https://github.com/JurajNyiri/pytapo) library — and provides structured configuration, error handling, and a clean abstraction layer for integrating camera systems into robotics or cloud-based pipelines.

- **Generic camera abstraction** — one interface for all supported cameras.  
- **Secrets and configuration management** — separate `.env` secrets from YAML configs.  
- **Modular architecture** — easily extend with new camera APIs.  


## Usage

```python
from pycam.wrappers.tapo_camera import TapoCamera
import sys


def main():
    camera = TapoCamera(
        config_path="./scripts/config.yaml",
        env_path="./scripts/.env"
    )

    print(camera.get_url())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected Error {e}")
        sys.exit(1)
```

## Configuration
Two different configuration files are requires:
- `.env` file with secrets.
```bash
# PASSWORD_CAMERA is the password configured via Tapo App. Settings ->  Advanced Configuration -> Camera Account
PASSWORD_CAMERA=password123  
# PASSWORD_CLOUD is the password configure when subscribing to Tapo App
PASSWORD_CLOUD=cyxRos-0jekqa-dorxaz
```
- `yaml` file with additional configuration parameters
```yaml
host: 192.168.1.42
user:
  camera: admin123
  cloud: admin
# RTSP streaming port
port: 554
# Mirror image vertically in case camera is positioned upside down
flip_image: true  # true, false
daynight_mode: day # day, night
# Starting camera position (in angles)
start_position:
   pan: 10.0
   tilt: 25.0
```

## API
The following API has been defined for the camera
```python
    def get_info(self) -> Info:
        """ Returns basic camera information including device_model, sw_version, hw_version..."""

    def get_video_specs(self) -> VideoSpecs:
        """ Returns video configuration information such as encoding type, frame rate or bitrate"""

    def get_video_capabilities(self) -> VideoCapability:
        """ Returns video configuration options"""

    def get_daynight_mode(self) -> DayNightMode:
        """ Returns DayNightMode (nigh vision or day)"""

    def move_motor(self, pan: float, tilt: float):
        """ Command motor to move in specicied pan and tilt angles (degrees)"""

    def calibrate_motor(self):
        """ Run motor calibration routine"""

    def reboot(self):
        """ Reboot camera"""

    def is_image_flipped(self) -> bool:
        """ Returns if image is flipped """

    def flip_image(self, flag: bool) -> None:
        """ Command to flip image"""

    def set_daynight_mode(self, mode: DayNightMode):
        """ Command to configure DayNight mode"""

    def get_url(self) -> str:
        """ Get RTSP url"""
```

## Notes
- When camera is initialized, the configured options are sent to the camera (flip, day/night vision, starting position).
- Camera starts pointing down and to the left. This position corresponds to a `pan` and `tilt` angle of 0 degress. `pan` is between 0 (all to the left) and 360 degrees (all to the right). `tilt` is between 0 (pointing down) and 90 degrees (pointing up).