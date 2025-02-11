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
    
    channel = channel_pb2.Channel()
    channel.ParseFromString(binary_data)

    module_settings = channel_pb2.ModuleSettings()
    module_settings.ParseFromString(binary_data)

    channel_settings = channel_pb2.ChannelSettings()
    channel_settings.ParseFromString(binary_data)

    print(f"Deserialized Channel:\n {channel}")
    print(f"Deserialized Channel Settings:\n {channel_settings}")
    print(f"Deserialized Module Settings:\n {module_settings}")

    print(f"Channel Number: {channel.settings.channel_num}")
    print(f"Channel Name: {channel_settings.name}")
    print(f"Channel PSK: {util.pskToString(channel_settings.psk)}")
    print(f"Channel ID: {channel_settings.id}")

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
