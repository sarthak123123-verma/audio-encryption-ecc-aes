# Audio Encryption System — ECC + AES Hybrid Cryptography

A Python-based hybrid encryption system that combines AES-256 symmetric encryption with Elliptic Curve Diffie-Hellman (ECDH) key exchange to securely encrypt and decrypt WAV audio files.

## Overview

This project demonstrates a hybrid cryptographic architecture similar to the approach used in modern secure communication protocols.

The system combines:

- AES-256 for symmetric data encryption
- ECDH for asymmetric key exchange
- Ephemeral ECC key pairs for forward secrecy
- WAV file processing for lossless audio encryption and decryption

## Cryptographic Architecture

The encryption pipeline uses:

```text
Input WAV
    │
    ▼
AES-256 Encryption
    │
    ▼
Encrypted Audio
    │
    │
    └── AES key established through ECDH
              │
              ▼
        Ephemeral ECC Keys

The use of ephemeral ECC key pairs means a new key exchange can be performed for each session, providing forward secrecy.

Technologies Used

* Python
* AES-256
* ECDH
* Elliptic Curve Cryptography
* brainpoolP256r1
* WAV audio processing

Project Structure

audio_ecc_project/
├── encrypt.py
├── decrypt.py
├── params.txt
├── input.wav
├── encrypted_audio.bin
├── encrypted_key.bin
└── output.wav

encrypt.py

Handles the encryption process and generation of the encrypted output.

decrypt.py

Handles decryption and reconstruction of the original audio file.

Validation

The decrypted WAV file was compared against the original input using structured output comparison.

The decrypted output was validated as bit-for-bit identical to the original WAV file, confirming lossless recovery.

Key Concepts Demonstrated

* Hybrid cryptography
* Symmetric encryption
* Elliptic Curve Cryptography
* ECDH key exchange
* Forward secrecy
* Secure key management
* Binary file encryption
* Data integrity validation

Purpose

This project was developed to understand how symmetric and asymmetric cryptographic techniques can be combined into a practical secure communication architecture.

The design was influenced by the hybrid cryptographic model used in TLS/SSL.
