# Audio Encryption System — ECC + AES Hybrid Cryptography

A Python-based hybrid cryptography project combining **AES-256-CFB** for audio encryption with **ECDH** using the **brainpoolP256r1** elliptic curve for AES key establishment.

## Overview

This project explores how symmetric and elliptic-curve cryptography can be combined to securely process binary audio data.

AES-256 is used for efficient encryption of the audio data, while ECDH is used to derive shared secret material for protecting the AES key.

## Architecture

```text
                Input WAV
                    │
                    ▼
              AES-256-CFB
                    │
                    ▼
            Encrypted Audio
                    │
                    │
                    ▼
          ECDH — brainpoolP256r1
                    │
                    ▼
             Shared Secret
                    │
                    ▼
            AES Key Protection
                    │
                    ▼
          Encrypted Key + Metadata

During decryption, the ECDH shared secret is reconstructed using the recipient’s private key and the ephemeral public key, allowing the AES key to be recovered and the original audio to be reconstructed.

Key Features

* AES-256-CFB encryption for WAV audio data
* ECDH key establishment using brainpoolP256r1
* Fresh ephemeral ECC key pair for each encryption session
* Binary audio encryption and reconstruction
* Bit-for-bit validation of decrypted output

Technologies

* Python
* AES-256-CFB
* ECDH
* Elliptic Curve Cryptography
* brainpoolP256r1
* cryptography
* tinyec
* wave

Project Structure

audio_ecc_project/
├── encrypt.py
├── decrypt.py
├── README.md
└── requirements.txt

encrypt.py

Handles AES encryption, ECC key generation, ECDH shared-secret computation, and encrypted output generation.

decrypt.py

Reconstructs the shared secret, recovers the AES key, decrypts the audio, and reconstructs the WAV file.

Validation

The decrypted WAV output was compared against the original input and validated as bit-for-bit identical, confirming correct and lossless recovery through the implemented encryption/decryption pipeline.

Security Considerations

This is an educational implementation, not a production cryptosystem.

The current version:

* Uses XOR-based AES key protection rather than a dedicated KDF such as HKDF.
* Uses AES-CFB, which does not provide authenticated encryption.
* Uses simplified private-key storage for demonstration purposes.
* Does not authenticate the ECDH key exchange.

These are deliberate areas for future improvement rather than claims of production security.

Future Improvements

* HKDF-based key derivation
* AES-GCM authenticated encryption
* Authenticated ECDH
* Secure private-key management
* Safer metadata serialization