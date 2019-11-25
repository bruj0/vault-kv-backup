import os
import logging
import base64
from hvac import Client


logger = logging.LoggerAdapter(logging.getLogger(__name__), {'STAGE': 'Transit encryption'})

class Transit:
    client = None
    encryption_key = None
    mount = None
    def __init__(self,client,encryption_key,mount):
        self.client = client
        self.encryption_key = encryption_key
        self.mount = mount
        logger.info(f'Starting transit encryption with key={encryption_key} mount={mount}')
    
    def encrypt(self,data):
        #logger.debug(f'Trying to base64 encode\n{data}')

        try:
            data_b64=base64.b64encode(data.encode())
            data_sb64=str(data_b64,"utf-8")
            #logger.debug(f'data in b64:\n{data_sb64}')
        except Exception as err:
            logger.exception(f'Error: {err}')
            exit(1)

        try:
            encrypt_data_response = self.client.secrets.transit.encrypt_data(
                name=self.encryption_key,
                mount_point=self.mount,
                plaintext=data_sb64,
            )
            ciphertext = encrypt_data_response['data']['ciphertext']
            logger.debug(f'Encrypted response:\n{encrypt_data_response}')
            #logger.info('Encrypted plaintext ciphertext is: {cipher}'.format(cipher=ciphertext))
            return ciphertext
        except Exception as err:
            logger.exception(f'Error: {err}')
            exit(1)

    def backup_key(self):
        self.client.secrets.transit.update_key_configuration(
            name=self.encryption_key,
            exportable=True,
            allow_plaintext_backup=True,
        )

        backup_key_response = self.client.secrets.transit.backup_key(
            name=self.encryption_key,
        )

        backed_up_key = backup_key_response['data']['backup']
        return backed_up_key