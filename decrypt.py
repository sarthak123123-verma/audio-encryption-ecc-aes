
import wave
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from tinyec import registry
from tinyec.ec import Point


def load_encrypted_files():
    """Load the encrypted audio and encrypted AES key from disk."""
    with open("encrypted_audio.bin", "rb") as f:
        encrypted_audio = f.read()
    with open("encrypted_key.bin", "rb") as f:
        encrypted_key = f.read()
    print("[✔] Encrypted files loaded.")
    return encrypted_audio, encrypted_key


def load_params():
    """
    Parse params.txt to retrieve:
      - IV used in AES encryption
      - Ephemeral public key point (for ECDH)
      - Recipient's private key (demo only — never store this in production)
      - Original WAV audio parameters
    """
    with open("params.txt", "r") as f:
        lines = f.readlines()

    iv              = bytes.fromhex(lines[0].strip())
    ephem_x, ephem_y = map(int, lines[1].strip().split(","))
    private_key     = int(lines[2].strip())
    audio_params = eval(lines[3].strip(), {"_wave_params": wave._wave_params})   # Restore namedtuple from string

    print("[✔] Parameters loaded from params.txt.")
    return iv, ephem_x, ephem_y, private_key, audio_params


def ecc_recover_aes_key(encrypted_key, private_key, ephem_x, ephem_y):
    """
    Recover the original AES key using ECDH.

    The sender used:  shared_secret = ephemeral_priv * recipient_public
    We compute:       shared_secret = recipient_private * ephemeral_public
    Both yield the same point because ECC scalar multiplication is commutative
    in this way (ECDH property).
    """
    curve           = registry.get_curve('brainpoolP256r1')
    ephemeral_pub   = Point(curve, ephem_x, ephem_y)

    shared_secret    = private_key * ephemeral_pub
    shared_key_bytes = shared_secret.x.to_bytes(32, 'big')

    # Reverse the XOR to recover the original AES key
    aes_key = bytes(a ^ b for a, b in zip(encrypted_key, shared_key_bytes))

    print("[✔] AES key successfully recovered via ECC (ECDH).")
    return aes_key


def aes_decrypt(encrypted_audio, aes_key, iv):
    """Decrypt the audio frames using AES-256 CFB with the recovered key and IV."""
    cipher     = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor  = cipher.decryptor()
    decrypted  = decryptor.update(encrypted_audio) + decryptor.finalize()
    print("[✔] Audio frames decrypted successfully.")
    return decrypted


def save_output_audio(decrypted_frames, audio_params, output_filename="output.wav"):
    """Write the decrypted frames back into a valid WAV file."""
    with wave.open(output_filename, "wb") as audio_file:
        audio_file.setparams(audio_params)
        audio_file.writeframes(decrypted_frames)
    print(f"[✔] Decrypted audio saved → {output_filename}")


def main():
    print("=" * 55)
    print("  Audio Decryption — ECC + AES Hybrid Scheme")
    print("=" * 55)

    # Step 1: Load encrypted data from disk
    encrypted_audio, encrypted_key = load_encrypted_files()

    # Step 2: Load all parameters needed for decryption
    iv, ephem_x, ephem_y, private_key, audio_params = load_params()

    # Step 3: Recover the AES key using ECC (ECDH)
    aes_key = ecc_recover_aes_key(encrypted_key, private_key, ephem_x, ephem_y)

    # Step 4: Decrypt audio frames using AES-256 CFB
    decrypted_audio = aes_decrypt(encrypted_audio, aes_key, iv)

    # Step 5: Save the reconstructed audio
    save_output_audio(decrypted_audio, audio_params)

    print("\n" + "=" * 55)
    print("  Decryption complete! ✔")
    print("  Open output.wav to verify the restored audio.")
    print("=" * 55)


if __name__ == "__main__":
    main()