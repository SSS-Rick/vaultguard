import sys

from vaultguard.crypto import KEY_FILE, generate_godly_keyfile
from vaultguard.vault import decrypt_file, encrypt_file


def print_banner():
    """Renders the ASCII art header."""
    print(r"""
V   V   A   U   U L     TTTTT  GGG  U   U   A   RRRR  DDDD  
V   V  A A  U   U L       T   G     U   U  A A  R   R D   D 
V   V AAAAA U   U L       T   G GG  U   U AAAAA RRRR  D   D 
 V V  A   A U   U L       T   G   G U   U A   A R  R  D   D 
  V   A   A  UUU  LLLLL   T    GGG   UUU  A   A R   R DDDD  
    Sovereign Quantum-Resistant Secret Sync [v1.0]
    """)

def main():
    """Main CLI entry point routing arguments to proper cryptographic functions."""
    print_banner()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  vaultguard init               - Generate Godly 512-byte quantum keyfile")
        print("  vaultguard encrypt [file]     - Encrypt target secret file into .vault.json")
        print("  vaultguard decrypt [output]   - Decrypt .vault.json back to plaintext")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    
    if action == "init":
        generate_godly_keyfile(KEY_FILE)
    elif action == "encrypt":
        target_file = sys.argv[2] if len(sys.argv) > 2 else ".env"
        encrypt_file(target_file)
    elif action == "decrypt":
        output_file = sys.argv[2] if len(sys.argv) > 2 else ".env"
        decrypt_file(output_file)
    else:
        print(f"[-] Unknown command: '{action}'")
        print("Run 'vaultguard' without arguments for usage instructions.")
        sys.exit(1)

if __name__ == "__main__":
    main()
