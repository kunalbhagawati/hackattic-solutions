import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


# Could have gone with https://pydantic-docs.helpmanual.io/, but seemed like overkill for this project.
# Will replace this if it becomes too cumbersome to maintain.
@dataclass
class Config:
    """Global config object for the running program."""

    access_token: str
    postgres__port: int
    postgres__password: str
    postgres__username: str
    postgres__dbname: str
    backup_restore__container_name: str

    @classmethod
    def from_env(cls):
        """Builds an instance from the loaded dotenv settings."""

        return cls(access_token=os.environ['ACCESS_TOKEN'],
                   postgres__port=int(os.environ['POSTGRES__PORT']),
                   postgres__password=os.environ['POSTGRES__PASSWORD'],
                   postgres__username=os.environ['POSTGRES__USERNAME'],
                   postgres__dbname=os.environ['POSTGRES__DBNAME'],
                   backup_restore__container_name=os.environ['BACKUP_RESTORE__CONTAINER_NAME'])


config = Config.from_env()
