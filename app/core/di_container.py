from dependency_injector import containers, providers
from dependency_injector.providers import Configuration

from app.services.meeting_service import MeettingService


class Container(containers.DeclarativeContainer):
    config = Configuration()

    meeting_service = providers.Singleton(MeettingService)
