# Disclaimer
This is not an official HashiCorp tool and its currently in POC stage

# What is it
Its an utility to backup the contents of a KV-v2 secret engine from a HashiCorp Vault using its **Transit secret engine**

The idea is that we can move the data in json format while being encrypted at rest storing the key somewhere else.

# How to use it

## Clone this repository
```
$ git clone https://github.com/bruj0/vault-kv-backup.git
```
## Optional: Use the provided docker-compose to start Vault
```
$ cd docker
$ docker-compose up -d
$ export VAULT_ADDR="http://127.0.0.:8300"
$ vault operator init -key-shares=1 -key-threshold=1
$ vault operator unseal <unseal key>
```
Save the unseal keys and root token for later use somewhere.

It is configured to use a filesystem storage in the directory `docker/data` and the configuration from `docker/config/vault.hcl`

## Enable the transit engine in Vault

```
$ vault secrets enable transit
$ vault write -f transit/keys/backup
```

## Set the environment variables

```
$ export VAULT_ADDR="http://127.0.0.:8300"
$ export VAULT_TOKEN=<your token>
$ python -m vmb.main encrypted.json
2019-11-25 16:09:52,329 [Main][INFO]
Starting vmb 0.0.1

2019-11-25 16:09:52,329 [Main][INFO]
Trying to login with Token

2019-11-25 16:09:52,342 [Transit encryption][INFO]
Starting transit encryption with key=backup mount=transit

2019-11-25 16:09:52,342 [KV Store][INFO]
Getting KV data from mount=secrets

2019-11-25 16:09:52,343 [KV Store][INFO]
Getting secrets for mount: secrets

2019-11-25 16:09:52,727 [Main][INFO]
Finished encrypting and writing data to encrypted.json

2019-11-25 16:09:52,727 [Main][INFO]
Encryption used key:
eyJwb2xpY3kiOnsibmFtZSI6ImJhY2t1cCIsImtleXMiOnsiMSI6eyJrZXkiOiJpaWdxS2dielFrMVgrN2tT...fV19fQo=
```

This will give you 2 things:
1. A file in json with all the encrypted key->value text, ie:

```json
[
    "vault:v1:mcjbiVnSbXDr11mQgFQwvYS5w/+u9s/gKMB7m4KrUL1S...G8kBI4n6XeAZv/c",
    "vault:v1:BC7SlJw26l4U3csa/CKYrR5yVXD1s09RBX5N1JykLnuG4GMOEF495qLDcIn3OY1BMMdBqGrBfHb9W/...",
]
```
1. The text representation of Transit key used as returned by the `export` API: https://www.vaultproject.io/api/secret/transit/index.html#export-key and can be used to restore it.

The idea is to keep the data encrypted and the key in different physical places in case one is breached. 

### TODO
* Automation of included Vault instance
* Restoring
* Packaging to pypi
* Configuration