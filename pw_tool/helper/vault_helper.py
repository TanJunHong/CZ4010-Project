import base64
import json

import Crypto
import passlib.context

import pw_tool.helper.firebase_helper

vault_iv = bytes("zg4cPx@Tr^6U", "utf8")
auth_iv = bytes("lP5Vm*EyorW6", "utf8")

context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], pbkdf2_sha256__default_rounds=100000)

vault_key = b""

vault = {}


def update_vault(website, username, password):
    vault[website] = {"username": username, "password": password}
    upload_vault()


def delete_from_vault(website):
    del vault[website]
    upload_vault()


def upload_vault():
    vault_bytes = json.dumps(obj=vault).encode(encoding="utf-8")
    cipher = Crypto.Cipher.AES.new(key=bytes(vault_key), mode=Crypto.Cipher.AES.MODE_CBC)
    ciphertext_bytes = cipher.encrypt(
        Crypto.Util.Padding.pad(data_to_pad=vault_bytes, block_size=Crypto.Cipher.AES.block_size))

    initialization_vector = base64.b64encode(s=cipher.iv).decode(encoding="utf-8")
    ciphertext = base64.b64encode(s=ciphertext_bytes).decode(encoding="utf-8")
    result = json.dumps({"iv": initialization_vector, "ct": ciphertext})

    pw_tool.helper.firebase_helper.database.child("vault").child(
        pw_tool.helper.firebase_helper.auth_key.split("$")[-1].replace(".", "")).set(result)
