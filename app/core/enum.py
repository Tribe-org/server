from enum import StrEnum


class MeetingTopic(StrEnum):
    """모임 주제 Enum"""

    FOOD = "food"  # 음식
    TRAVEL = "travel"  # 여행
    SPORTS_ACTIVITY = "sports-activity"  # 스포츠/활동
    CULTURE_ART = "culture-art"  # 문화/예술
    SELF_DEVELOPMENT = "self-development"  # 자기계발
    GAME = "game"  # 게임
    BEAUTY_FASHION = "beauty-fashion"  # 뷰티/패션
    VOLUNTEER = "volunteer"  # 봉사활동


class MeetingType(StrEnum):
    """모임 유형 Enum"""

    MISSION = "mission"  # 미션
    CONTINUOUS = "continuous"  # 지속형 모임


class MeetingPlace(StrEnum):
    """미팅 장소 유형 Enum"""

    ONLINE = "online"  # 온라인
    OFFLINE = "offline"  # 오프라인


class GoalFrequency(StrEnum):
    """미팅 주기 유형 Enum"""

    DAILY = "daily"  # 매일
    WEEKLY = "weekly"  # 매주
    MONTHLY = "monthly"  # 매달


class CertificationType(StrEnum):
    """인증 유형 Enum"""

    TEXT = "text"  # 텍스트
    IMAGE = "image"  # 이미지
    TEXT_WITH_IMAGE = "text_with_image"  # 텍스트 + 이미지


class GenderRestriction(StrEnum):
    """성별 제한 유형 Enum"""

    MALE = "male"  # 남성
    FEMALE = "female"  # 여성
    NONE = "none"  # 제한 없음


class AgeRestriction(StrEnum):
    """나이 제한 유형 Enum"""

    NONE = "none"  # 제한 없음
    TWENTIES = "twenties"  # 20대
    THIRTIES = "thirties"  # 30대
    FORTIES = "forties"  # 40대
    FIFTYS_AND_OVER = "fifties_and_over"  # 50대 이상
