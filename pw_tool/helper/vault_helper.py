import base64
import json

import Crypto.Cipher.AES
import Crypto.Cipher.ChaCha20
import Crypto.Hash.Poly1305
import Crypto.Util.Padding
import passlib.context
import passlib.crypto.digest
import passlib.hash

import pw_tool.helper.fb_helper
import pw_tool.helper.ui_helper

context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], pbkdf2_sha256__default_rounds=100000)
vault_key = default_vault_key = b""
vault = default_vault = {"vault": {}, "pw_gen_hist": []}


def generate_vault_key(secret, salt):
    """Generates vault key with secret and salt
    Generates vault key to lock the vault. This value never leaves the client.
    """
    global vault_key

    vault_key = passlib.crypto.digest.pbkdf2_hmac(digest="sha256", secret=secret, salt=salt, rounds=1000000, keylen=32)

    del secret
    del salt


def add_gen_pw(password):
    """Adds generated password to history
    This is done in case user forgets to save their generated passwords.
    It will only store the last 5 passwords.
    """
    vault["pw_gen_hist"].insert(0, password)
    while len(vault["pw_gen_hist"]) > 5:
        vault["pw_gen_hist"].pop(len(vault["pw_gen_hist"]) - 1)
    upload_vault()


def clear_gen_history():
    """Clears generated password from history
    """
    vault["pw_gen_hist"] = []
    upload_vault()


def update_vault(website, username, password, old_value=None):
    """Updates vault with new entry
    """
    old_passwords = []
    if old_value is not None:
        old_passwords = vault["vault"][website]["old_passwords"]

        for old_password in old_passwords:
            if passlib.hash.pbkdf2_sha256.verify(secret=password, hash=old_password):
                return False

        if password != old_value["password"]:
            old_passwords.append(passlib.hash.pbkdf2_sha256.hash(secret=old_value["password"]))

    del old_value

    vault["vault"][website] = {"username": username, "password": password, "old_passwords": old_passwords}
    upload_vault()

    del old_passwords
    del website
    del username
    del password

    return True


def delete_from_vault(website):
    """Deletes entry from vault
    """
    del vault["vault"][website]

    upload_vault()


def download_vault():
    """Retrieves vault from firebase and store it in client
    """
    global vault

    data = pw_tool.helper.fb_helper.database.child("vault").child(
        pw_tool.helper.fb_helper.auth_key.split("$")[-1].replace(".", "")).get(
        token=pw_tool.helper.fb_helper.user["idToken"])

    vault = decrypt_vault(data=data)

    del data


def upload_vault():
    """Uploads vault to firebase
    """
    pw_tool.helper.fb_helper.database.child("vault").child(
        pw_tool.helper.fb_helper.auth_key.split("$")[-1].replace(".", "")).set(data=encrypt_vault(),
                                                                               token=pw_tool.helper.fb_helper.user[
                                                                                   "idToken"])

    pw_tool.helper.ui_helper.vault_page.refresh_page()


def decrypt_vault(data):
    """Decrypts vault and returns decrypted vault
    """
    if data.val() is None:
        return default_vault

    result = json.loads(s=data.val())

    del data

    initialization_vector = base64.b64decode(s=result["iv"])
    ciphertext = base64.b64decode(s=result["ct"])
    nonce = base64.b64decode(s=result["nonce"])
    tag = base64.b64decode(s=result["tag"])

    del result

    try:
        Crypto.Hash.Poly1305.new(key=pw_tool.helper.fb_helper.mac_key, nonce=nonce, cipher=Crypto.Cipher.ChaCha20,
                                 data=ciphertext).verify(mac_tag=tag)
    except ValueError:
        return False

    del nonce
    del tag

    cipher = Crypto.Cipher.AES.new(key=bytes(vault_key), mode=Crypto.Cipher.AES.MODE_CBC, iv=initialization_vector)
    vault_bytes = Crypto.Util.Padding.unpad(padded_data=cipher.decrypt(ciphertext=ciphertext),
                                            block_size=Crypto.Cipher.AES.block_size)

    del initialization_vector
    del ciphertext
    del cipher

    return json.loads(s=vault_bytes.decode(encoding="utf-8"))


def encrypt_vault():
    """Encrypts vault and returns encrypted vault
    """
    vault_bytes = json.dumps(obj=vault).encode(encoding="utf-8")

    cipher = Crypto.Cipher.AES.new(key=bytes(vault_key), mode=Crypto.Cipher.AES.MODE_CBC)
    ciphertext_bytes = cipher.encrypt(
        plaintext=Crypto.Util.Padding.pad(data_to_pad=vault_bytes, block_size=Crypto.Cipher.AES.block_size))
    initialization_vector = base64.b64encode(s=cipher.iv).decode(encoding="utf-8")
    ciphertext = base64.b64encode(s=ciphertext_bytes).decode(encoding="utf-8")

    del vault_bytes
    del cipher

    mac = Crypto.Hash.Poly1305.new(key=pw_tool.helper.fb_helper.mac_key, cipher=Crypto.Cipher.ChaCha20,
                                   data=ciphertext_bytes)
    nonce = base64.b64encode(s=mac.nonce).decode(encoding="utf-8")
    tag = base64.b64encode(s=mac.digest()).decode(encoding="utf-8")

    del ciphertext_bytes
    del mac

    return json.dumps(obj={"iv": initialization_vector, "ct": ciphertext, "nonce": nonce, "tag": tag})


def delete_vault(auth_key):
    """Deletes entry from vault
    """
    pw_tool.helper.fb_helper.database.child("vault").child(auth_key.split("$")[-1].replace(".", "")).remove(
        token=pw_tool.helper.fb_helper.user["idToken"])

    del auth_key


def destroy_variables():
    """Destroys variables from client side
    Called when logging out.
    """
    global vault_key
    global vault

    pw_tool.helper.fb_helper.auth_key = pw_tool.helper.fb_helper.mac_key = pw_tool.helper.ui_helper.vault_page = None
    vault_key = default_vault_key
    vault = default_vault
