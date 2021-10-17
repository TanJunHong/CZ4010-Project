import base64
import json

import Crypto
import passlib.context
import passlib.crypto.digest

import pw_tool.helper.firebase_helper
import pw_tool.helper.ui_helper

# Randomly generated using BitWarden's Password Generator
vault_iv = bytes("zg4cPx@Tr^6U", "utf8")
auth_iv = bytes("lP5Vm*EyorW6", "utf8")

context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], pbkdf2_sha256__default_rounds=100000)

vault_key = b""

vault = {}


def generate_vault_key(secret):
    global vault_key
    vault_key = passlib.crypto.digest.pbkdf2_hmac(digest="sha256", secret=secret, salt=vault_iv, rounds=1000000,
                                                  keylen=16)


def update_vault(website, username, password):
    vault[website] = {"username": username, "password": password}
    upload_vault()


def delete_from_vault(website):
    del vault[website]
    upload_vault()


def load_vault():
    data = pw_tool.helper.firebase_helper.database.child("vault").child(
        pw_tool.helper.firebase_helper.auth_key.split("$")[-1].replace(".", "")).get()
    if data.val() is not None:
        result = json.loads(s=data.val())
        initialization_vector = base64.b64decode(s=result["iv"])
        ciphertext = base64.b64decode(s=result["ct"])
        cipher = Crypto.Cipher.AES.new(key=bytes(pw_tool.helper.vault_helper.vault_key),
                                       mode=Crypto.Cipher.AES.MODE_CBC, iv=initialization_vector)
        vault_bytes = Crypto.Util.Padding.unpad(padded_data=cipher.decrypt(ciphertext=ciphertext),
                                                block_size=Crypto.Cipher.AES.block_size)
        pw_tool.helper.vault_helper.vault = json.loads(s=vault_bytes.decode(encoding="utf-8"))


def upload_vault():
    vault_bytes = json.dumps(obj=vault).encode(encoding="utf-8")
    cipher = Crypto.Cipher.AES.new(key=bytes(vault_key), mode=Crypto.Cipher.AES.MODE_CBC)
    ciphertext_bytes = cipher.encrypt(
        Crypto.Util.Padding.pad(data_to_pad=vault_bytes, block_size=Crypto.Cipher.AES.block_size))

    initialization_vector = base64.b64encode(s=cipher.iv).decode(encoding="utf-8")
    ciphertext = base64.b64encode(s=ciphertext_bytes).decode(encoding="utf-8")
    result = json.dumps(obj={"iv": initialization_vector, "ct": ciphertext})

    pw_tool.helper.firebase_helper.database.child("vault").child(
        pw_tool.helper.firebase_helper.auth_key.split("$")[-1].replace(".", "")).set(result)

    pw_tool.helper.ui_helper.vault_page.refresh_page()


def destroy_variables():
    global vault_key
    global vault
    pw_tool.helper.firebase_helper.auth_key = None
    pw_tool.helper.ui_helper.vault_page = None
    vault_key = b""
    vault = {}
