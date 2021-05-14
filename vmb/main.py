#!/usr/bin/env python
import json
import logging
import os

from hvac import Client

from vmb.kvstore import KVstore
from vmb.transit import Transit

from . import __version__, cfg

logger = logging.LoggerAdapter(logging.getLogger(__name__), {'STAGE': 'Main'})
logger.info(f"Starting vmb {__version__}")


def write_to_disk(path_to_write, data):
    try:
        with open(path_to_write, "w+") as fd:
            fd.write(data)
    except Exception as e:
        logger.exception(f'Error on path {path_to_write}: {e}')
        exit(1)


def main():

    logger.info("Trying to login with Token")
    logger.debug("Debug enabled")
    try:
        client = Client(
           url=os.environ['VAULT_ADDR'],
           token=os.environ['VAULT_TOKEN']
        )
        client.is_authenticated()
    except Exception as err:
        logger.exception("Token Login failed: %s", err)
        exit(2)

    transit = Transit(client=client, encryption_key='backup', mount='transit')
    kv = KVstore(client, cfg['kv_path'], transit=transit)

    data = kv.get_base_folder()
    write_to_disk(cfg['out_file'], data)
    logger.info(f"Finished encrypting and writting data to {cfg['out_file']}")

    exported_key = transit.backup_key()
    write_to_disk(cfg['backup_key'], exported_key)
    logger.info(f"Finished encrypting and writting data to {cfg['backup_key']}")


if __name__ == "__main__":
    main()
