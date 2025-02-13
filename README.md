# Auto proxy
The purpose of this tool is to anonymize your whole network and avoid DNS leaks
The script has functions that configuring the files automatically.
# Usage
git clone https://github.com/CyberMafiaPH/autoproxy

cd autoproxy

sudo apt install proxychains4 && sudo apt install tor

sudo python3 autoproxy.py

proxychains4 firefox https://ifconfig.me
