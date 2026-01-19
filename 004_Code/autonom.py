import mdns


mdns_server = mdns.Server(wlan.ifconfig()[0], "pico-filter")
mdns_server.add_service("_http", "_tcp", 80)
mdns_server.start()