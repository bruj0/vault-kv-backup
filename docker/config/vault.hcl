storage "file" {
  path = "/vault/data"
}
listener "tcp" {
  #address          = "127.0.0.1:8200"
  address          = "0.0.0.0:8200"
  tls_disable      = "true"
  
}
ui = true
cluster_name = "Backup"