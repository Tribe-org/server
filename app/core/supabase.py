import os
from .config import Config
from supabase import create_client, Client



class Supabase:
    _instance = None
    _initialized = False

    # Singleton pattern
    def __new__(cls):
        """
        Returns the single instance of the class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            self._initialized = True

