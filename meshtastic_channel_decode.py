#!/usr/bin/env python3

import sys
import argparse
import base64
import json
import re

def decrypt_mesh_url(murl: str):
    """ Decode a provided URL into the meshtastic channel information """
    print(f"[+] provided URL: {murl}")

    data = re.search(r'#(.*)',  murl)
    binary_data = base64.urlsafe_b64decode(data.group(1) + '==')
    settings_data = binary_data.decode('utf-8', errors='ignore')
    print(f"[+] Unserialized data: {settings_data}")

    return binary_data

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
