import passlib.context

site_wide_salt = bytes("CZ4010", "utf8")

context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256",
                                       pbkdf2_sha256__default_rounds=50000)