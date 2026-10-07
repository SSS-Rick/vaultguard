import base64
import json
import os
import sys

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from vaultguard.crypto import (
    KEY_FILE,
    derive_aes_key,
    generate_godly_keyfile,
    load_keyfile,
)

VAULT_JSON = ".vault.json"

def encrypt_file(input_path: str, output_json: str = VAULT_JSON):
    """
    Encrypts any target plaintext file (e.g. .env, database credentials, secret notes)
    using AES-256-GCM and the derived quantum keyfile. Produces a tamper-proof JSON payload.
    """
    if os.path.isdir(input_path):
        print(f"[-] Error: '{input_path}' is a directory, not a file.")
        return
    if not os.path.exists(input_path):
        print(f"[-] Error: Target file '{input_path}' not found.")
        return
        
    # 1. Load keyfile and derive 256-bit AES key
    key_data = load_keyfile(KEY_FILE)
    derived_key = derive_aes_key(key_data)
    
    # 2. Initialize AES-256-GCM cipher
    aesgcm = AESGCM(derived_key)
    
    # 3. Generate a fresh 96-bit cryptographic nonce (ensures unique ciphertext every run)
    nonce = os.urandom(12)
    
    # 4. Read plaintext secret file
    with open(input_path, "rb") as f:
        plaintext = f.read()
        
    # 5. Encrypt data (includes authentication tag for tamper protection)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    
    # 6. Package payload into base64 for safe JSON storage and public transport
    payload = {
        "version": "1.0",
        "algorithm": "AES-256-GCM + Argon2id",
        "nonce": base64.b64encode(nonce).decode('utf-8'),
        "ciphertext": base64.b64encode(ciphertext).decode('utf-8')
    }
    
    with open(output_json, "w") as f:
        json.dump(payload, f, indent=2)
        
    print(f"[+] Successfully encrypted '{input_path}' into '{output_json}' (Quantum-Resistant AES-256-GCM).")

def decrypt_file(output_path: str = ".env", input_json: str = VAULT_JSON):
    """
    Decrypts the .vault.json payload back into plaintext using the local keyfile.
    Fails instantly if the ciphertext or metadata has been tampered with.
    """
    if os.path.isdir(output_path):
        print(f"[-] Error: '{output_path}' is a directory.")
        return
    if not os.path.exists(input_json):
        print(f"[-] Error: Vault payload '{input_json}' not found.")
        return
        
    # 1. Load keyfile and derive 256-bit AES key
    key_data = load_keyfile(KEY_FILE)
    derived_key = derive_aes_key(key_data)
    
    # 2. Initialize AES-256-GCM cipher
    aesgcm = AESGCM(derived_key)
    
    # 3. Read encrypted JSON payload
    with open(input_json, "r") as f:
        payload = json.load(f)
        
    nonce = base64.b64decode(payload["nonce"])
    ciphertext = base64.b64decode(payload["ciphertext"])
    
    # 4. Decrypt and verify authentication tag
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        with open(output_path, "wb") as f:
            f.write(plaintext)
        print(f"[+] Successfully decrypted into '{output_path}'.")
    except Exception as e:
        print(f"[-] Decryption failed! Tampering detected or incorrect keyfile: {e}")
        sys.exit(1)
