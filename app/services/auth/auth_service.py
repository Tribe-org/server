from abc import ABC, abstractmethod


class AuthService(ABC):
    @abstractmethod
    def auth_start(self):
        pass

    @abstractmethod
    async def auth_callback(self, url: str, **kwargs):
        pass
