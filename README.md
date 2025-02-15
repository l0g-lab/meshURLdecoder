# Tool to decode a provided Meshtastic channel URL

### How to use

1. Create a python local environment
   ```bash
   python3 -m venv .venv
   ```
2. Activate pyenv
   ```bash
   source .venv/bin/activate
   ```
3. Install requirements
   ```bash
   pip3 install -r requirements.txt
   ```
4. Run the script, providing the Meshtastic URL with the `-u` argument:
   ```bash
   python3 meshURLdecoder.py -u https://meshtastic.org/e/?add=true#...
   ```
