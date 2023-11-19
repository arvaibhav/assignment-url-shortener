import os
from typing import Optional

from .base import BaseConfig


class GlobalConfig:
    _config_instance: Optional[BaseConfig] = None

    @property
    def config(self):
        if self._config_instance is None:
            env = os.getenv("APP_ENVIRONMENT", "staging").lower()
            if env == "production":
                from .production import Config
                self._config_instance = Config()
            else:
                from .staging import Config
                self._config_instance = Config()

        return self._config_instance


APP_CONFIG: BaseConfig = GlobalConfig().config
