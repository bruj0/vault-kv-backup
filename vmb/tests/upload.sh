#!/bin/bash -x

jq -c '.[]' $1 | while read i; do
    id=$( echo $i | jq -r '.id')
    #echo $i
    curl -v  --request POST --header "X-Vault-Token: $VAULT_TOKEN" --data "{ \"data\": $i }" http://127.0.0.1:8300/v1/secrets/data/$2/$id
done