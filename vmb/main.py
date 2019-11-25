#!/usr/bin/env python
import logging
from logging import getLogger

import sys, os, getopt
from pprint import pformat
from . import cfg
from . import __version__
from vmb.kvstore import KVstore
from vmb.transit import Transit
import json
from hvac import Client

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

    transit = Transit(client = client , encryption_key = 'backup',mount = 'transit')
    kv = KVstore(client,'secrets',transit=transit)

    data = kv.get_base_folder()
    try: 
      data=json.dumps(data[0],indent=4)
    except Exception as err:
      logger.exception(f'Error converting to JSON: {err}')
      exit(1)

    write_to_disk(cfg['out_file'],data)

    exported_key = transit.backup_key()
    
    logger.debug(f"Finished getting data:\n{data}")
    logger.info(f"Finished encrypting and writting data to {cfg['out_file']}")
    logger.info(f'Encryption used key:\n{exported_key}')



if __name__== "__main__":
  main()