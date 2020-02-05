import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s -  %(levelname)s -  %(message)s')
# import sys
# key1, key2, encode, decode = sys.stdin.read().split()
key1, key2, encode_text , decode_text = 'abcd','?%^8','abacabadaba','#*%*d*%'

key = (key1,key2)
def encode_key(key):
    encode_key = {}
    for i in range(len(key1)):
        encode_key.update({key[0][i]:key[1][i]})
    return encode_key
def decode_key(key):
    decode_key = {}
    for i in range(len(key1)):
        decode_key.update({key[1][i]:key[0][i]})
    return decode_key

def encode(key,text):
    encode_text = encode_key(key)
    encoded = ''
    for i in text:
        encoded += encode_text[i]
    return encoded

def decode(key,text):
    decode_text = decode_key(key)
    decoded = ''
    for i in text:
        decoded += decode_text[i]
    return decoded

print(encode(key,encode_text))
print(decode(key,decode_text))




