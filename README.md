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

[**Passlib**](https://passlib.readthedocs.io/en/stable/index.html) is eventually chosen as it fulfills the
considerations mentioned above.

### Choosing the hash function

After choosing the password hashing library, we need to choose the hash functions. These are the criteria we are looking
for:

- Secure, which means it uses a cryptographically secure pseudo-random number generator
- Widely used and tested
- No known major vulnerabilities as of the time of writing

We decided on the following hash functions:

#### [**passlib.crypto.digest.pbkdf2_hmac()**](https://passlib.readthedocs.io/en/stable/lib/passlib.crypto.digest.html)

It is a PBKDF v2.0 using HMAC. It is used to generate the vault key, which is used to decrypt the vault.
<br> This function is used for vault key instead of pbkdf2_sha256 is because we are able to set the vault key length to
meet the requirements of AES.

#### [**pbkdf2_sha256**](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.pbkdf2_digest.html)

This class implements a generic PBKDF2-HMAC-SHA256-based password hash. It will run through the pbkdf2_hmac function
mentioned above. It is used to generate the authentication key, which is used to retrieve the vault from the database.

### Choosing the encryption function

AES

## Design

Talk about convenience vs security

Remote storage on firebase realtime database

## Development

Use of salt, plaintext, aes
https://www.youtube.com/watch?v=w68BBPDAWr8

## Use of the code

Screenshot of code How to run the program

## Glossary

- **PBKDF** - Password-Based Key Derivation
- **HMAC** - Hash-Based Message Authentication Code
- **SHA** - Secure Hash Algorithms
- **AES** - Advanced Encryption Standard

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


