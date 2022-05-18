#This is a script that will generate an ethereum wallet then send it to server 

from cmath import exp
from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256
import requests
from threading import Thread
import random
import time

ip_addresses = []

def proxy_generator():
    response = requests.get("https://api.proxyscrape.com/?request=getproxies&proxytype=http&country=all&timeout=10000&ssl=yes&anonymity=all")
    for line in response.text.splitlines():
        ip_addresses.append(line)
    time.sleep(50)



def make_requests(url, private , public):
    random_proxy = random.choice(ip_addresses)
    r = requests.get(url, proxies={"http": random_proxy})
    if r.status_code!=200:
        time.sleep(5)
        return 0 
    elif r.status_code==200:
        if 'This address has transacted 0 times' not in r.text:
            print('VALID!'),print(private),print(public)
        else:pass


    
def main():
    time.sleep(2)
    while True:
        private_key = keccak_256(token_bytes(32)).digest()
        public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
        addr = keccak_256(public_key).digest()[-20:]
        make_requests('https://www.blockchain.com/eth/address/0x' + addr.hex(), private_key, addr)  
if __name__ == '__main__':
    Thread(target=proxy_generator).start()
    Thread(target=main).start()

    
