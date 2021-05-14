import json
import logging

from hvac import Client

logger = None


class KVstore:
    client = None
    kv_store = None
    transit = None

    def __init__(self, client, kv_store, transit):
        global logger
        logger = logging.LoggerAdapter(logging.getLogger(__name__),
                                       {'STAGE': 'KV Store'})
        logger.info(f'Getting KV data from mount={kv_store}')

        self.client = client
        self.kv_store = kv_store
        self.transit = transit

    def get_base_folder(self):
        """
        get the base folder
        :param client: the client to connect with
        :param kv_store: the kv_store from which to retrieve the folder
        :return: a folder object
        """

        logger.info("Getting secrets for mount: %s", self.kv_store)

        if not self.kv_store.endswith("/"):
            self.kv_store = self.kv_store + "/"

        folder = self.get_folder_content("", self.kv_store)

        return json.dumps(folder)

    def get_folder_content(self, path: str, mount_point: str):
        """
        get the list of content for a base folder
        :param client: the client to connect with
        :param path: the path in the kv_store to the entity in question
        :param mount_point:  the kv_store from which to retrieve the objects
        :return: a list of either folders or entities
        """
        keys = []
        content = {}
        try:
            keys = self.client.secrets.kv.v2.list_secrets(
                path=path,
                mount_point=mount_point
            )['data']['keys']
        except Exception as err:
            logger.exception("Error: %s", err)
            exit(1)
        logger.debug("Found a folder: " + mount_point + path)

        for key in keys:
            if key.endswith('/'):
                # this seems to be a folder
                folder = self.get_folder_content(path + key, mount_point)
                content[key] = folder
            else:
                # this seems to be an entity
                content[key] = self.get_entity(path, key, mount_point)
                # content.append(path + key)

        return content

    def get_entity(self, path: str, entity_name: str, mount_point: str):
        """
        get an entity object from  the api
        :param client: the client to connect with
        :param path: the path in the kv_store to the entity in question
        :param entity_name: the name (for easy inserting in the entity object)
        :param mount_point: the kv_store from which to retrieve the entity
        :return: an entity object
        """
        data = {}
        try:
            data = self.client.secrets.kv.v2.read_secret_version(
                path=path + "/" + entity_name,
                mount_point=mount_point
            )['data']
        except ValueError as err:
            logger.exception("Error: %s", err)
            exit(1)

        logger.debug("Found an entity %s with ", str(data['data'].keys()))

        try:
            data = {'path': path, 'name': entity_name, 'data': data['data']}
            data_js = json.dumps(data)

            return self.transit.encrypt(data_js)
        except Exception as err:
            logger.exception(f'Error: {err}')
            exit(1)
