import base64
import json

import Crypto
import passlib.context
import passlib.crypto.digest
import passlib.hash

import pw_tool.helper.fb_helper
import pw_tool.helper.ui_helper

# Randomly generated using BitWarden's Password Generator
# TODO: Set minimum password strength
# TODO: Check if salt can be fixed, if not generate salt using uuid + password (Remember to delete variable)
# https://crypto.stackexchange.com/questions/34642/security-implication-of-deriving-key-with-fixed-salt-for-files-authentication
# https://crypto.stackexchange.com/questions/50174/can-pbkdf2-be-used-with-a-fixed-salt-to-give-a-deterministic-slow-hash
# Note that the good practice would be either to derive the salt in a deterministic way (from the username, for example)
vault_salt = bytes("zg4cPx@Tr^6U", "utf8")
auth_salt = bytes("lP5Vm*EyorW6", "utf8")

context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], pbkdf2_sha256__default_rounds=100000)

vault_key = b""

vault = {}


def generate_vault_key(secret):
    """Generates vault key with secret
    Generates vault key to lock the vault. This value never leaves the client.
    """
    global vault_key
    vault_key = passlib.crypto.digest.pbkdf2_hmac(digest="sha256", secret=secret, salt=vault_salt, rounds=1000000,
                                                  keylen=16)
    del secret


def update_vault(website, username, password, old_value=None):
    """Updates vault with new entry
    """
    old_passwords = []
    if old_value is not None:
        old_passwords = vault[website]["old_passwords"]

        for old_password in old_passwords:
            if passlib.hash.pbkdf2_sha256.verify(secret=password, hash=old_password):
                return False

        if password != old_value["password"]:
            old_passwords.append(passlib.hash.pbkdf2_sha256.hash(secret=old_value["password"]))

    vault[website] = {"username": username, "password": password, "old_passwords": old_passwords}
    upload_vault()

    del old_passwords
    del website
    del username
    del password
    del old_value

    return True


def delete_from_vault(website):
    """Deletes entry from vault
    """
    del vault[website]
    upload_vault()


def load_vault():
    """Retrieves vault from firebase and store it in client
    """
    data = pw_tool.helper.fb_helper.database.child("vault").child(
        pw_tool.helper.fb_helper.auth_key.split("$")[-1].replace(".", "")).get(
        token=pw_tool.helper.fb_helper.user["idToken"])
    if data.val() is not None:
        result = json.loads(s=data.val())
        initialization_vector = base64.b64decode(s=result["iv"])
        ciphertext = base64.b64decode(s=result["ct"])
        cipher = Crypto.Cipher.AES.new(key=bytes(pw_tool.helper.vault_helper.vault_key),
                                       mode=Crypto.Cipher.AES.MODE_CBC, iv=initialization_vector)
        vault_bytes = Crypto.Util.Padding.unpad(padded_data=cipher.decrypt(ciphertext=ciphertext),
                                                block_size=Crypto.Cipher.AES.block_size)
        pw_tool.helper.vault_helper.vault = json.loads(s=vault_bytes.decode(encoding="utf-8"))

        del data
        del result
        del initialization_vector
        del ciphertext
        del cipher
        del vault_bytes


def upload_vault():
    """Uploads vault to firebase
    """
    vault_bytes = json.dumps(obj=vault).encode(encoding="utf-8")
    cipher = Crypto.Cipher.AES.new(key=bytes(vault_key), mode=Crypto.Cipher.AES.MODE_CBC)
    ciphertext_bytes = cipher.encrypt(
        plaintext=Crypto.Util.Padding.pad(data_to_pad=vault_bytes, block_size=Crypto.Cipher.AES.block_size))

    initialization_vector = base64.b64encode(s=cipher.iv).decode(encoding="utf-8")
    ciphertext = base64.b64encode(s=ciphertext_bytes).decode(encoding="utf-8")
    result = json.dumps(obj={"iv": initialization_vector, "ct": ciphertext})

    pw_tool.helper.fb_helper.database.child("vault").child(
        pw_tool.helper.fb_helper.auth_key.split("$")[-1].replace(".", "")).set(data=result,
                                                                               token=pw_tool.helper.fb_helper.user[
                                                                                   "idToken"])

    pw_tool.helper.ui_helper.vault_page.refresh_page()

    del vault_bytes
    del cipher
    del ciphertext_bytes
    del initialization_vector
    del ciphertext
    del result


def delete_vault(auth_key):
    """Deletes entry from vault
    """
    pw_tool.helper.fb_helper.database.child("vault").child(auth_key.split("$")[-1].replace(".", "")).remove(
        token=pw_tool.helper.fb_helper.user["idToken"])


def destroy_variables():
    """Destroys variables from client side
    Called when logging out.
    """
    global vault_key
    global vault
    pw_tool.helper.fb_helper.auth_key = None
    pw_tool.helper.ui_helper.vault_page = None
    vault_key = b""
    vault = {}
