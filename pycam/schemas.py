from typing import TypedDict, List
from enum import Enum, IntEnum, IntFlag


class VideoEncodeType(Enum):
    H264 = "H264"
    H265 = "H265"


class VideoBitrate(IntFlag):
    BR_256 = 256
    BR_512 = 512
    BR_1024 = 1024
    BR_1228 = 1228
    BR_2048 = 2048


class VideoResolution(Enum):
    RES_SUPER_HD = "2304*1296"
    RES_1080P = "1920*1080"
    RES_720P = "1280*720"
    RES_360P = "640*360"


class VideoBitrateType(Enum):
    CBR = "cbr"
    VBR = "vbr"


class DayNightMode(Enum):
    NIGHT = "on"
    DAY = "off"
    AUTO = "auto"

    @classmethod
    def _missing_(cls, value):
        lookup = {
            "night": "on",
            "day": "off",
        }
        if isinstance(value, str):
            key = value.lower()
            if key in lookup:
                return cls(lookup[key])
        raise ValueError(f"Invalid DayNightMode value: {value}")


class VideoQuality(IntEnum):
    LOW = 1
    MID = 3
    HIGH = 5


class Info(TypedDict):
    device_model: str
    sw_version: str
    hw_version: str
    is_calibrated: bool


class VideoSpecs(TypedDict):
    bitrate: VideoBitrate
    default_bitrate: VideoBitrate
    bitrate_type: VideoBitrateType
    frame_rate: int
    encode_type: VideoEncodeType
    resolution: VideoResolution
    quality: int


class VideoCapability(TypedDict):
    encode_types: List[VideoEncodeType]
    frame_rates: List[int]
    bitrates: List[VideoBitrate]
    bitrate_types: List[VideoBitrateType]
    resolutions: List[VideoResolution]
    qualitys: List[int]
