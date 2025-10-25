from dataclasses import dataclass, asdict
import numpy as np
import yaml
import cv2
from typing import Any, Dict
import glob


@dataclass
class CameraCalibration:
    """Camera intrinsic and distortion parameters."""

    width: int
    height: int
    distortion_model: str
    K: np.ndarray  # 3x3 intrinsic matrix
    D: np.ndarray  # 1xN distortion coefficients (usually 5)
    R: np.ndarray  # 3x3 rectification matrix
    P: np.ndarray  # 3x4 projection matrix

    @classmethod
    def default(cls, width: int, height: int) -> "CameraCalibration":
        """Default uncalibrated pinhole model."""
        fx = fy = 1000.0
        cx, cy = width / 2.0, height / 2.0
        return cls(
            width=width,
            height=height,
            distortion_model="plumb_bob",
            K=np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]]),
            D=np.zeros((5,)),
            R=np.eye(3),
            P=np.array([[fx, 0, cx, 0], [0, fy, cy, 0], [0, 0, 1, 0]]),
        )

    @classmethod
    def from_yaml(cls, path: str) -> "CameraCalibration":
        """Load calibration data from a YAML file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(
            width=data["width"],
            height=data["height"],
            distortion_model=data["distortion_model"],
            K=np.array(data["K"]).reshape(3, 3),
            D=np.array(data["D"]),
            R=np.array(data["R"]).reshape(3, 3),
            P=np.array(data["P"]).reshape(3, 4),
        )

    def to_yaml(self, path: str):
        """Export calibration data to YAML."""
        data: Dict[str, Any] = {
            "width": self.width,
            "height": self.height,
            "distortion_model": self.distortion_model,
            "K": self.K.flatten().tolist(),
            "D": self.D.flatten().tolist(),
            "R": self.R.flatten().tolist(),
            "P": self.P.flatten().tolist(),
        }
        with open(path, "w") as f:
            yaml.safe_dump(data, f)

    def to_dict(self) -> Dict[str, Any]:
        """Return as serializable dictionary."""
        return {
            "width": self.width,
            "height": self.height,
            "distortion_model": self.distortion_model,
            "K": self.K.tolist(),
            "D": self.D.tolist(),
            "R": self.R.tolist(),
            "P": self.P.tolist(),
        }


def compute_calibration(images_glob: str, board_size=(9, 6), square_size=0.024):
    objp = np.zeros((board_size[0] * board_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0 : board_size[0], 0 : board_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints = []

    images = glob.glob(images_glob)
    for fname in images:
        img = cv2.imread(fname)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, board_size)
        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

    ret, K, D, rvecs, tvecs = cv2.calibrateCamera(  # type: ignore[call-overload]
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    width, height = gray.shape[::-1]
    R = np.eye(3)
    P = np.hstack((K, np.zeros((3, 1))))

    return CameraCalibration(width, height, "plumb_bob", K, D, R, P)
