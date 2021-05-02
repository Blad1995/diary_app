import logging
import os as os
import sys
from typing import Optional

import structlog
import structlog_pretty
import yaml as yaml


class DiaryConfig:
    _config_path = "config.yml"
    dir_path: Optional[str] = None
    first_use: Optional[bool] = None
    owner_credentials_file_name: Optional[str] = None
    date_format: Optional[str] = None
    natural_date_format: Optional[str] = None
    data_extension: Optional[str] = None
    _keys = []
    logger = None

    @classmethod
    def load(cls, config_path = "./"):
        cls.configure_logger()
        cls.logger = structlog.getLogger()
        with open(os.path.join(config_path, cls._config_path), mode="r") as f:
            cfg = yaml.safe_load(f)
        if not cfg:
            raise RuntimeError("Cannot find config file.")
        cls._keys = set(cfg.keys())

        for key in cls._keys:
            try:
                setattr(cls, key, cfg[key])
            except KeyError as ke:
                cls.logger.error("config.loading.unknown_key", key=key)
                raise RuntimeError(f"Config file has been corrupted.") from ke
        cls.logger.info("config.loading.success", keys=cls._keys)

    @classmethod
    def save(cls):
        cfg = {key: value for key, value in cls.__dict__.items() if key in cls._keys}
        try:
            with open(cls._config_path, "w") as f:
                yaml.safe_dump(data=cfg, stream=f)
        except IOError as e:
            cls.logger.error(f"config.writing.io_error", path=cls._config_path)
            raise e

    @classmethod
    def configure_logger(cls):
        debug_processors = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog_pretty.NumericRounder(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(pad_event=25),
        ]

        structlog.configure(
            processors=debug_processors,
            logger_factory=structlog.PrintLoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=structlog.threadlocal.wrap_dict(dict),
        )
