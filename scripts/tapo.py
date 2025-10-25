from pycam.wrappers.tapo_camera import TapoCamera
import sys
import traceback


def main():
    camera = TapoCamera(config_path="./scripts/config.yaml", env_path="./scripts/.env")

    print(camera.get_url())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected Error {e}")
        traceback.print_exc()
        sys.exit(1)
