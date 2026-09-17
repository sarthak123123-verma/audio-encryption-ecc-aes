import wave
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from tinyec import registry
import secrets


def read_audio(filename):
    """Read a WAV audio file and return its parameters and raw frame data."""
    with wave.open(filename, "rb") as audio_file:
        params = audio_file.getparams()
        frames = audio_file.readframes(audio_file.getnframes())
    print(f"[✔] Audio file '{filename}' loaded successfully.")
    print(f"    Channels   : {params.nchannels}")
    print(f"    Frame rate : {params.framerate} Hz")
    print(f"    Frames     : {params.nframes}")
    return params, frames


def aes_encrypt(frames):
    """
    Encrypt audio frames using AES-256 in CFB mode.
    Returns the encrypted data along with the key and IV used.
    """
    aes_key = os.urandom(32)   # 256-bit AES key
    iv      = os.urandom(16)   # 128-bit Initialization Vector

    cipher     = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor  = cipher.encryptor()
    encrypted  = encryptor.update(frames) + encryptor.finalize()

    print("[✔] Audio frames encrypted with AES-256 (CFB mode).")
    return encrypted, aes_key, iv


def ecc_encrypt_key(aes_key):
    """
    Protect the AES key using Elliptic Curve Diffie-Hellman (ECDH).

    Steps:
      1. Generate a recipient ECC key pair (private + public).
      2. Generate a random ephemeral key pair for this session.
      3. Compute a shared secret via ECDH.
      4. XOR the AES key with the shared secret to produce the encrypted key.
    """
    curve = registry.get_curve('brainpoolP256r1')

    # Recipient key pair (in real use, public_key is shared openly)
    private_key = secrets.randbelow(curve.field.n)   #na
    public_key  = private_key * curve.g  #pa=na*G

    # Ephemeral key pair (generated fresh per session)
    ephemeral_priv   = secrets.randbelow(curve.field.n)
    ephemeral_pub    = ephemeral_priv * curve.g #e_priv*G

    # Shared secret derived from ECDH
    shared_secret    = ephemeral_priv * public_key #e_priv*Pa
    shared_key_bytes = shared_secret.x.to_bytes(32, 'big')

    # Encrypt the AES key by XOR-ing with the shared secret bytes
    encrypted_aes_key = bytes(a ^ b for a, b in zip(aes_key, shared_key_bytes))

    print("[✔] AES key encrypted using ECC (brainpoolP256r1 curve, ECDH).")
    return private_key, ephemeral_pub, encrypted_aes_key


def save_encrypted_audio(encrypted_audio):
    """Save the AES-encrypted audio bytes to a binary file."""
    with open("encrypted_audio.bin", "wb") as f:
        f.write(encrypted_audio)
    print("[✔] Encrypted audio saved → encrypted_audio.bin")


def save_encrypted_key(encrypted_key):
    """Save the ECC-protected AES key to a binary file."""
    with open("encrypted_key.bin", "wb") as f:
        f.write(encrypted_key)
    print("[✔] Encrypted AES key saved → encrypted_key.bin")


def save_params(iv, ephemeral_pub, private_key, audio_params):
    """
    Save all parameters needed for decryption into params.txt.
    
    NOTE: In a real-world system, private_key would NEVER be stored here.
          It is saved in this demo only so the decryption script can run
          standalone without a separate key management system.
    """
    with open("params.txt", "w") as f:
        f.write(f"{iv.hex()}\n")
        f.write(f"{ephemeral_pub.x},{ephemeral_pub.y}\n")
        f.write(f"{private_key}\n")
        f.write(str(audio_params) + "\n")
    print("[✔] Decryption parameters saved → params.txt")
    print("\n    ⚠  Note: private_key is stored in params.txt for demo purposes only.")
    print("       In production, the private key must be kept secret.")


def main():
    print("=" * 55)
    print("  Audio Encryption — ECC + AES Hybrid Scheme")
    print("=" * 55)

    # Step 1: Read input audio
    audio_params, raw_frames = read_audio("input.wav")

    # Step 2: Encrypt audio data with AES-256
    encrypted_audio, aes_key, iv = aes_encrypt(raw_frames)

    # Step 3: Protect the AES key using ECC (ECDH)
    private_key, ephemeral_pub, encrypted_aes_key = ecc_encrypt_key(aes_key)

    # Step 4: Persist all encrypted outputs
    save_encrypted_audio(encrypted_audio)
    save_encrypted_key(encrypted_aes_key)
    save_params(iv, ephemeral_pub, private_key, audio_params)

    print("\n" + "=" * 55)
    print("  Encryption complete! ✔")
    print("  Output files: encrypted_audio.bin, encrypted_key.bin, params.txt")
    print("=" * 55)


if __name__ == "__main__":
    main()