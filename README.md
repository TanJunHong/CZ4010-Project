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
- Compatible with Python 3, since that is the language we are using

[**Passlib**](https://passlib.readthedocs.io/en/stable/index.html) is eventually chosen for the as it fulfills the
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

It is a PBKDF v2.0 using HMAC. It is used to generate the vault key, which is used to decrypt the vault.
<br> This function is used for vault key instead of pbkdf2_sha256 is because we are able to set the vault key length to
meet the requirements of AES.

#### [**pbkdf2_sha256**](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.pbkdf2_digest.html)

This class implements a generic PBKDF2-HMAC-SHA256-based password hash. It will run through the pbkdf2_hmac function
mentioned above, as well as a PRF build from HMAC and the respective message digest. It is used to generate the
authentication key, which is used to retrieve the vault from the database.

### Choosing the encryption function

These are the criteria we are looking for:

- Secure and deterministic, which means it uses a CSPRF
- Widely used and tested
- No known major vulnerabilities as of the time of writing

[**AES**](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html) is eventually chosen as it fulfills the
considerations mentioned above. Specifically, we are using CBC mode of operation.

### Choosing the database

These are the criteria we are looking for:

- High uptime and ran by reputable company
- Automatically handles authentication, so we do not need to handle it (Leave it to experts)
- Good documentation
- Widely used and tested

[**Google Firebase**](https://firebase.google.com/) is eventually chosen as it fulfills the considerations mentioned
above. The documentations state that scrypt algorithm is used for the password hashing. scrypt is a PBKDF specifically
designed to make it costly to perform large-scale custom hardware attacks by requiring large amounts of memory.

## Design

There are two things in mind when it comes to our design - convenience and security Since we are storing passwords, it
is important to make our system as secure as possible, while ensuring ease of use. If the password management tool is
not easy to use, it defeats the purpose and the users may resort to weak methods to store their passwords.

### Convenience

To ensure ease of use, we decided to store the vaults on a remote server, as compared to a local storage. This way, the
user can run the program on a different machine and is still able to retrieve their passwords easily. For this function,
we used Google Firebase's Realtime Database to store our passwords.
<br>Also, since passwords are often complex, we allow users to copy the stored password into a clipboard to use it on
the website. This reduces the chance of incorrect input, and is much faster, so the user does not need to keep the vault
open as long. The clipboard will automatically expire in 10s, and it will be replaced by an empty string. This allows
for more security, in case the user forgets to clear the password from the clipboard. For maximum security, we recommend
users to disable clipboard history.

### Security

Security is our utmost priority. We have to ensure that even if the database is leaked, the attackers have no way of
knowing decrypting the vaults and knowing the owner of the vaults.
<br>To ensure this, we use AES-CBC 256-bit encryption for vault data, and PBKDF2 SHA-256 to derive the vault key and
authentication key. The database only stores encrypted data.
<br>The vault key never leaves the client, and as such it is impossible to sniff and intercept the vault key. The
authentication key is sent to the server to retrieve the corresponding vault. Since the authentication key is generated
using a strong hash function, anyone who has access to the vault data in the database has no idea who the vault belongs
to. The attacker will also not know how to decrypt the vault, since the key is kept in the client. **MORE**

## Development

Use of salt, plaintext, aes
https://www.youtube.com/watch?v=w68BBPDAWr8

## Use of the code

Screenshot of code How to run the program

## Glossary

- **CS** - Cryptographically Secure
- **PRF** - Pseudo-Random Function
- **PBKDF** - Password-Based Key Derivation
- **HMAC** - Hash-Based Message Authentication Code
- **SHA** - Secure Hash Algorithms
- **AES** - Advanced Encryption Standard
- **CBC** - Cipher-Block Chaining

---

## Encryption

XX

## Hash Verification

To authenticate the user, they are prompted to create a master password which is then stored using a SHA256 Hash
Function and is verified at login.

## Precautions

This password manager tool securely encrypts your password but this security is only as strong as the weakest component

- and this is very often the primary password used to lock and unlock your vault. Follow these basic guidelines to
  ensure that your vault is safe even if exposed:

* Choose a unique password that is not used elsewhere
* Use a highly-varied set of different characters (alphanumeric, symbols, spaces)
* Use long password (the longer the better)
* Do not include personal information or words in the password
* Never share your password


