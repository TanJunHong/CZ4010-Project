# CZ4010 Applied Cryptography Course Project - BoHack (Password Management Tool)

> Note: This password manager tool was created as a project and is NOT intended for actual use.
> Please use an established, preferably open source password manager to store important passwords as they are likely to be audited by security experts.

## Group Members

- Tan Jun Hong
- Lim Xiao Wei

## Motivation

According to Dr Tay Kian Boon, there are many incorrect applications of cryptography in the real world. For instance,
Nadia's paper found that there are keys generated in real life that have insufficient entropy due to faulty
implementations. As such, there are many minefields to be aware of.
<br>In order to gain a deeper understanding of cryptography, it is crucial to apply these concepts, preferably on a
project. As such, we decided to create a secure and authenticated password management tool, which will give a deeper
insights on the inner workings.

## Research

### Choosing a password hashing library

We began searching for a password hashing library that meets the following criteria:

- Well documented and transparent, so we can understand the mechanics behind and verify that it is secure
- Widely used and open source, which makes it more reliable and likely to be tested by security experts
- Frequently updated, in order to keep up with the latest best security practices
- Compatible with Python, since that is the language we are using

[**Passlib**](https://passlib.readthedocs.io/en/stable/index.html) is eventually chosen as it fulfills the
considerations mentioned above.

[**PyCryptodome**](https://pycryptodome.readthedocs.io/en/latest/index.html) is also used as Passlib does not support
AES.

### Choosing the hash function

After choosing the password hashing library, we need to choose the hash functions. These are the criteria we are looking
for:

- Secure and deterministic, which means it uses a CSPRF
- Widely used and tested
- No known major vulnerabilities as of the time of writing

We decided on the following hash functions:

#### [**passlib.crypto.digest.pbkdf2_hmac()**](https://passlib.readthedocs.io/en/stable/lib/passlib.crypto.digest.html)

It is a PBKDF v2.0 using HMAC. It is used to generate the vault key, which is used to decrypt the vault. This function
is used for vault key instead of pbkdf2_sha256 is because we are able to set the vault key length to meet the
requirements of AES.

#### [**pbkdf2_sha256**](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.pbkdf2_digest.html)

This class implements a generic PBKDF2-HMAC-SHA256-based password hash. It will run through the pbkdf2_hmac function
mentioned above, as well as a PRF build from HMAC and the respective message digest. It is used to generate the
authentication key, which is used to retrieve the vault from the database.

#### [**scrypt**](https://pycryptodome.readthedocs.io/en/latest/src/protocol/kdf.html)

scrypt is a password-based key derivation function created by Colin Percival. In addition to being computationally
expensive, it is also memory intensive and therefore more secure against the risk of custom ASICs. It is used to
generate the MAC key.

#### [**Poly1305**](https://pycryptodome.readthedocs.io/en/latest/src/hash/poly1305.html)

Poly1305 is a fast Carter-Wegman MAC algorithm created by Daniel J. Bernstein. It requires a 32-byte secret key, a
16-byte nonce, and a symmetric cipher. The MAC tag is always 16 bytes long. It is used to generate the MAC tag to verify
the vault's integrity.

### Choosing the ciphers

These are the criteria we are looking for:

- Secure and deterministic, which means it uses a CSPRF
- Widely used and tested
- No known major vulnerabilities as of the time of writing

#### [**AES**](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html)

AES is chosen as it fulfills the considerations mentioned above. Specifically, we are using CBC mode of operation. It is
used to encrypt the whole vault.

#### [**ChaCha20**](https://pycryptodome.readthedocs.io/en/latest/src/cipher/chacha20.html)

ChaCha20 is chosen to use with Poly1305. ChaCha20 with Poly1305 is now standardized in RFC 7905. It is used to generate
the MAC tag.

### Choosing the database

These are the criteria we are looking for:

- High uptime and ran by reputable company
- Automatically handles authentication, so we do not need to handle it (Leave it to experts)
- Good documentation
- Widely used and tested

[**Google Firebase**](https://firebase.google.com/) is eventually chosen as it fulfills the considerations mentioned
above. The documentations state that scrypt algorithm is used for the password hashing. scrypt is a PBKDF specifically
designed to make it costly to perform large-scale custom hardware attacks by requiring large amounts of memory.

### Choosing the cryptographically secure library

We need to choose a library that is cryptographically secure for the generation of secure passwords. These are the
criteria we are looking for:

- Cryptographically secure, for generating cryptographically strong random numbers
- Written and approved by security experts
- Widely used and well documented
- Compatible with Python

[**secrets**](https://docs.python.org/3/library/secrets.html) is eventually chosen as it fulfils the considerations
mentioned above.

### Generating cryptographically secure secrets

After choosing the functions, we need to figure out how to effectively use them. We researched on how other existing
password managers worked, and borrowed their concepts. One of the videos we referenced from is [**How Password Managers
Work - Computerphile**](https://www.youtube.com/watch?v=w68BBPDAWr8)

#### Generating vault key

To generate the vault key, we used (email | password) as the plaintext, and (password | UUID) as salt. We referenced the
above video for the plaintext. As for the salt, we need something *unique* so that nobody has computed the resulting
hash value before. UUIDs have to be generated uniquely for each user, and it is different each time it is generated for
the same user. As such, they are unique enough to be used as salt. We concatenate password in front of it, so it has a
higher chance of avoiding collisions.

#### Generating authentication key

To generate the authentication key, we used (vault key | password) as the plaintext, and (UUID | email) as salt. The
explanation is similar to that of generating the vault key. We have to make sure we are not reusing the key or the salt,
which is why we made use of the vault key.

#### Generating MAC key

To generate the MAC key, we used (UUID | vault key) as the plaintext, and (password | authentication key) as salt. The
explanation is similar to that of generating the vault key. We have to make sure we are not reusing the key or the salt,
which is why we made use of the vault key and the authentication key.

#### Generating secure passwords

To generate the password, we first create a list of all characters (alphanumeric and symbols) based on what is selected
by the user. We then use secrets to pick a character from the list. This is repeated for the desired length (capped at
64 characters). Since secrets module is cryptographically secure, it offers independent generation of numbers, and have
equal chance of being any character, making the password unpredictable. To ensure that it contains the type of
characters selected, a check is done after generation, and the password generation process is repeated if the condition
is not fulfilled.

Previously, we have implemented Feistel rounds as a password generator. This idea came about as we found that Feistel
rounds is an elegant and clean method which offers both substitution and permutations, which mixes the generated
password, potentially making it more unpredictable. However, we decide to scrap it as we are unsure of the possible
weaknesses in design due to the lack of expertise. Moreover, due to the short length of password, it is difficult to
test if the randomness is cryptographically secure.

## Design

There are two things in mind when it comes to our design - convenience and security Since we are storing passwords, it
is important to make our system as secure as possible, while ensuring ease of use. If the password management tool is
not easy to use, it defeats the purpose and the users may resort to weak methods to store their passwords.

### Convenience

#### Remote storage

To ensure ease of use, we decided to store the vaults on a remote server, as compared to a local storage. This way, the
user can run the program on a different machine and is still able to retrieve their passwords easily. For this function,
we used Google Firebase's Realtime Database to store our passwords.

#### Clipboard

Since passwords are often complex, we allow users to copy the stored password into a clipboard to use it on the website.
This reduces the chance of incorrect input, and is much faster, so the user does not need to keep the vault open as
long. The clipboard will automatically expire in 10s, and it will be replaced by an empty string. This allows for more
security, in case the user forgets to clear the password from the clipboard. For maximum security, we recommend users to
disable clipboard history.

#### Password History

To aid users in choosing a password, we decided to display the last 10 generated passwords. This way, users can view
previously generated passwords. Moreover, if a user forgets to save his/her newly generated password, he/she can still
retrieve it easily. Upon reaching 10 passwords, the oldest password will be removed.

### Security

Security is our utmost priority. We have to ensure that even if the database is leaked, the attackers have no way of
knowing decrypting the vaults and knowing the owner of the vaults. Here are some ways to ensure this:

#### Confidentially

- We use AES-CBC 256-bit encryption for vault data, and PBKDF2 SHA-256 to derive the vault key and authentication key.
  Only encrypted data is transmitted, and the database only stores encrypted data.
- The vault key never leaves the client, and as such it is impossible to sniff and intercept the vault key.
- The authentication key is sent to the server to retrieve the corresponding vault. Since the authentication key is
  generated using a strong hash function, anyone who has access to the vault data in the database has no idea who the
  vault belongs to.
- When displaying a website's login information, the password is masked out initially, to prevent people nearby from
  seeing it.
- When comparing passwords (i.e. check if old passwords are being used), we use the built-in `verify()` function
  provided by the libraries instead of `==`. This ensures a "constant time" equality check, which mitigates timing
  attacks.
- Variables that contains sensitive information are immediately deleted with `del` after usage.
- We make use of cryptographic libraries instead of writing our own, as they are maintained by cryptography experts and
  are likely to be more reliable.

#### Integrity

- We generate a MAC tag which can be used to check if the vault has been tampered with. If it is tampered, the user will
  be notified and logged out.
- scrypt is used to generate the secret key for MAC, and Poly1305 is used to generate the MAC tag itself.

### Speed

#### Entire vault encrypted as a whole

Due to the fact that the entire vault is being encrypted/decrypted as a whole, it may not be the most efficient method.
We have thought of encrypting each website as its own, and make use of CBC to encrypt the next block. However, it hides
way more information as compared to encrypting per website, since it is not that obvious how many websites are in the
entire vault.
<br>Furthermore, we may have to encrypt the website link itself, in order to hide from attacker which website the login
information belongs to. This means that we have to decrypt all website links when we want to use the vault, and then
decrypt the login information when the user uses it. Not only that, once we modify the vault, we have to re-encrypt the
whole vault, since a change in a block cascades the changes throughout. As a result, we found that the performance gain
is minimal, and it is way more complex to implement.
<br>Also, it is easy to "step on minefields" when it comes to encrypting each account by website, since we must be very
careful in handling the keys and initialization vectors for each encryption. It is much easier to get it wrong, and any
wrong usage will make the vault vulnerable. As such, we decided to go with the entire vault being encrypted/decrypted as
a whole.

## Development

### Python

#### Integrated Development Environment

- **Pycharm** -> For development of this application

#### Libraries

- **passlib** -> For hashing/comparisons of old passwords, as well as generating vault key and authentication key, using
  PBKDF2 SHA-256
- **pycryptodome** -> For encryption using AES-CBC 256-bit
- **Pyrebase4** -> Pyrebase with updated dependencies, to connect to Google Firebase (Uses pycryptodome as well)
- **ttkthemes** -> Themes for Tkinter
- **secrets** -> For generating cryptographically strong random numbers in selecting characters in password, as well as
  round key for Feistel rounds

### Google Firebase

- **Realtime Database** -> Cloud-hosted NoSQL database, for access to vault anywhere

## Use of the code

Please ensure you have Python 3.10 installed. (Only tested in Python 3.10, may work in other versions)

1. Clone this repository
2. From the root folder, run `pip install -r requirements.txt`
3. Navigate to the `pw_tool` folder
4. Run `main.py`. You should see the following screen ![Login Screen](https://github.com/TanJunHong/CZ4010-Project/blob/main/Login%20Screen.png)
5. Register for an account, and you are ready to go!

## Limitations

### Immutable String in Python

Strings in python are immutable, so there is a chance the password is still in memory even after calling `del`. There is
the possibility the operating system will swap the whole memory page ut to disk, where it could sit for months. However,
since this requires an attack on the client, we consider the risk of this attack minimal. If the attacker has access to
the client, there are more serious things to worry about.

## Glossary

- **CS** - Cryptographically Secure
- **PRF** - Pseudo-Random Function
- **PBKDF** - Password-Based Key Derivation
- **HMAC** - Hash-Based Message Authentication Code
- **SHA** - Secure Hash Algorithms
- **MAC** - Message Authentication Code
- **AES** - Advanced Encryption Standard
- **CBC** - Cipher-Block Chaining
- **UUID** - User Universally Unique Identifier

## Precautions

This password management tool securely encrypts your passwords but this security is only as strong as the weakest
component. Follow these basic guidelines to ensure that your vault is safe even if your passwords are exposed:

- Do not reuse your password
- Use a highly-varied set of different characters (alphanumeric, symbols, spaces)
    * Best if it is generated through a reputable password management tool (or ours!)
- Use sufficiently long password
- Do not include personal information or words in the password
- Never share your password, not even with your most trusted friends!
