import getpass
import hashlib
import os
import sys
import time

from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

VAULT_DIR = ".vaultguard"
KEY_FILE = os.path.join(VAULT_DIR, "vault.key")
SALT_CONSTANT = b"vaultguard_quantum_salt_v1"

def generate_godly_keyfile(key_path=KEY_FILE):
    """
    Generates a true 512-byte quantum-resistant keyfile using human typing entropy,
    nanosecond CPU timing jitter, system randomness, and multi-round hashing (SHA3-512 + Blake2b).
    """
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    print("[*] Initializing Godly 512-Byte Quantum-Resistant Keyfile...")
    print("[*] Please type random sentences, gibberish, and smash keys for maximum entropy generation:")
    
    start_time = time.time_ns()
    user_input = getpass.getpass("Entropy seed input: ")
    end_time = time.time_ns()
    
    # Gather multi-source entropy
    urand_bytes = os.urandom(256)
    time_seed = str(end_time - start_time).encode('utf-8')
    user_bytes = user_input.encode('utf-8')
    
    raw_entropy = urand_bytes + time_seed + user_bytes
    
    # Layered cryptographic mixing (Multi-algorithm hashing to eliminate biases)
    h1 = hashlib.sha3_512(raw_entropy).digest()
    h2 = hashlib.blake2b(raw_entropy, digest_size=64).digest()
    h3 = hashlib.sha512(raw_entropy + h1).digest()
    h4 = hashlib.sha3_512(raw_entropy + h2).digest()
    
    intermediate_key = h1 + h2 + h3 + h4 # 256 bytes
    
    h5 = hashlib.sha3_512(intermediate_key).digest()
    h6 = hashlib.blake2b(intermediate_key, digest_size=64).digest()
    h7 = hashlib.sha512(intermediate_key + h5).digest()
    h8 = hashlib.sha3_512(intermediate_key + h6).digest()
    
    godly_512_bytes = intermediate_key + h5 + h6 + h7 + h8 # Exactly 512 bytes
    
    with open(key_path, "wb") as f:
        f.write(godly_512_bytes[:512])
        
    print(f"[+] Godly 512-byte keyfile successfully generated at {key_path}")

def load_keyfile(key_path=KEY_FILE) -> bytes:
    """
    Loads the 512-byte binary keyfile from disk with validation checks.
    """
    if not os.path.exists(key_path):
        print(f"[-] Error: Keyfile not found at {key_path}. Run 'vaultguard init' first.")
        sys.exit(1)
        
    with open(key_path, "rb") as f:
        key_data = f.read()
        
    if len(key_data) != 512:
        print("[-] Error: Keyfile corruption detected (invalid length).")
        sys.exit(1)
        
    return key_data

def derive_aes_key(key_data: bytes) -> bytes:
    """
    Derives a memory-hard 256-bit (32 byte) AES key from the 512-byte keyfile 
    using Argon2id to prevent ASIC/GPU parallel brute-force attacks.
    """
    kdf = Argon2id(
        salt=SALT_CONSTANT,
        length=32,
        iterations=3,
        lanes=4,
        memory_cost=65536,
    )
    return kdf.derive(key_data)
