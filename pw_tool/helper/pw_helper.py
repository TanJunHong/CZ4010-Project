import passlib.context

vault_iv = bytes("zg4cPx@Tr^6U", "utf8")
auth_iv = bytes("lP5Vm*EyorW6", "utf8")

context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], pbkdf2_sha256__default_rounds=100000)

vault_key = None
