import enum


class MeetingType(enum.Enum):
    # 지속형
    CONTINUOUS = "continuous"
    # 미션형
    MISSION = "mission"


class GenderType(enum.Enum):
    # 남성
    M = "M"
    # 여성
    F = "F"
    # 확인불가
    U = "U"


class FeedType(enum.Enum):
    # 텍스트
    TEXT = "text"
    # 이미지
    IMAGE = "image"