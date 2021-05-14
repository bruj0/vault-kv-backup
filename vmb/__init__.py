
import getopt
import logging
import os
import sys
from logging import getLogger
from logging.config import dictConfig
from pprint import pformat, pprint

from pkg_resources import get_distribution

from vmb.args import ArgParser


def get_config():
    args, remaining = ArgParser().parse_known_args()
    vargs = vars(args)

    return {
        'log_file': vargs.pop("log_to_file"),
        'out_file': vargs.pop("out_file"),
        'global_cfg': vargs.pop("global_cfg", {}),
        'debug': vargs.pop("debug"),
        'dry_run': vargs.pop("dry_run"),
        'backup_key': vargs.pop("backup_key"),
        'kv_path': vargs.pop("kv_path")
    }

__version__ = get_distribution('vmb').version
cfg = get_config()

if cfg["debug"] is True:
    log_level = "DEBUG"
else:
    log_level = "INFO"

# Basic logging config that will print out useful information
log_cfg = {
    "version": 1,
    'disable_existing_loggers': False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(STAGE)s][%(levelname)s]\n%(message)s\n",
            "style": "%",
        },
        "debug": {
            "format": "%(asctime)s [%(STAGE)s][%(levelname)s] (%(name)s:%(lineno)d)\n%(message)s\n",
            "style": "%",
        }
    },
    "handlers": {
        "to_stdout": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        "nothing": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "vmb": {"handlers": ["to_stdout"], "level": log_level},
        "__main__": {"handlers": ["to_stdout"], "level": log_level},
    }
}

if log_level == "DEBUG":
    log_cfg['handlers']['to_stdout']['formatter'] = 'debug'

if "log_to_file" in cfg:
    log_cfg["handlers"].update(
        {
            "to_file": {
                "class": "logging.FileHandler",
                "filename": cfg["log_file"],
                "formatter": "default",
            }
        }
    )
    log_cfg["loggers"]["vmb"]["handlers"].append("to_file")
else:
    log_cfg["loggers"]["vmb"]["handlers"].append("to_stdout")


dictConfig(log_cfg)
