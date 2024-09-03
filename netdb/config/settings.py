from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from util.exception import NetDBException


class _Settings(BaseSettings):
    """
    NetDB global settings. Intended to be loaded once into its container (see below)
    at FastAPI initialization time. Not indended to be accessed directly.
    """

    # Mongod host and port
    mongo_url: str

    # Mongod DB name
    db_name: str = 'netdb'

    # This requires a mongodb relica set
    transactions: bool = False

    # Used for instances on proxy minions and only need reads.
    read_only: bool = False

    # Used for overrides table. Must not confict with column names.
    override_table: str = 'override'

    # Overrides status
    overrides_enabled: bool = True

    model_config = SettingsConfigDict(env_file=".env")


class NetdbSettings:
    """
    Threadsafe container for NetDB settings. Returns copies of the NetDB settings
    (_settings) object.
    """

    __settings__: Optional[_Settings] = None

    @classmethod
    def initialize(cls):
        """
        Initialize the container by loading the global settings object and saving it
        inside the container.
        """
        cls.__settings__ = _Settings()

    @classmethod
    def get_settings(cls) -> _Settings:
        """
        Return a copy of the NetDB global settings.
        """
        if cls.__settings__ is None:
            raise NetDBException(
                code=500,
                message='get_settings() called on uninitialized NetdbSettings container.',
            )

        return cls.__settings__.model_copy(deep=True)
