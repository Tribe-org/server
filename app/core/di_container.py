from dependency_injector import containers, providers
from dependency_injector.providers import Configuration

from app.repositories.meeting.continuous_meeting_repository import (
    ContinuousMeetingRepository,
)
from app.repositories.meeting.meeting_repository import MeetingRepository
from app.repositories.meeting.mission_meeting_repository import (
    MissionMeetingRepository,
)
from app.services.meeting_service import MeettingService


class Container(containers.DeclarativeContainer):
    config = Configuration()

    meeting_repository = providers.Singleton(MeetingRepository)
    mission_meeting_repository = providers.Singleton(MissionMeetingRepository)
    continuouns_meeting_repository = providers.Singleton(
        ContinuousMeetingRepository
    )

    meeting_service = providers.Singleton(
        MeettingService,
        meeting_repo=meeting_repository,
        mission_repo=mission_meeting_repository,
        countinuouns_repo=continuouns_meeting_repository,
    )
