#!/usr/bin/env python3

import sys
import argparse
import base64
import json
import re
from meshtastic.protobuf import admin_pb2, apponly_pb2, channel_pb2, localonly_pb2, mesh_pb2, portnums_pb2
from meshtastic import util

def decrypt_mesh_url(murl: str):
    """ Decode a provided URL into the meshtastic channel information """
    print(f"[+] provided URL: {murl}")

    data = re.search(r'#(.*)',  murl)
    binary_data = base64.urlsafe_b64decode(data.group(1) + '==')
    print(f"[+] Unserialized data: {binary_data}")
    
    #channel = channel_pb2.Channel()
    #channel.ParseFromString(binary_data)
    #module_settings = channel_pb2.ModuleSettings()
    #module_settings.ParseFromString(binary_data)
    #channel_settings = channel_pb2.ChannelSettings()
    #channel_settings.ParseFromString(binary_data)

    app_only = apponly_pb2.ChannelSet()
    app_only.ParseFromString(binary_data)

    psk_enabled = ord(app_only.settings[0].psk)
    
    print("---------------------------------------------------")
    print(f"[+] Decoded data:\n{app_only}")
    print("---------------------------------------------------")

    print(f"[+][+] Channel Number: {app_only.settings[1].id}")
    print(f"[+][+] Channel Name: {app_only.settings[1].name}")
    #print(f"[+][+] Channel PSK Enabled: {app_only.settings[0]}", end="")
    print(f"[+][+] Channel PSK Enabled: {psk_enabled}")
    if psk_enabled == 1:
        print(f"[+][+] Channel PSK: {util.pskToString(app_only.settings[1].psk)}")
        #print(f"Channel PSK: {app_only.settings[1].psk}")
    else:
        print(f"[+][+] PSK Disabled!!")
    #print(f"Lora Config: {app_only.lora_config}")

def main():
    parser = argparse.ArgumentParser(description="Meshtastic URL decoder.")
    parser.add_argument("-u", "--url", help="Define URL to decode")
    args = parser.parse_args()

    if args.url:
        decrypt_mesh_url(args.url)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
