# VaultGuard (`vaultguard`)

Sovereign, quantum-resistant, zero-SaaS secret sync CLI tool.
                              <mark>basicly encript any txt file<mark/>

## Philosophy
- **safe storage:** you can save your password on any public space and no one would be able to decrypt or read it except with your key.
- **Zero-SaaS:** No third-party servers holding your keys.
- **Quantum-Resistant:** Uses Godly 512-byte keyfiles combined with Argon2id and AES-256-GCM.
- **License:** GNU General Public License v3.0 (GPLv3).

## Installation

### 1. Create and Activate a Virtual Environment (Recommended)
Before installing, it's best to isolate your environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. For Developers (Editable / Local Install)
Install VaultGuard in editable mode so it links directly to your active virtual environment and code changes apply instantly:
```bash
pip install -e .
```

### 3. For Users (Standard Install)
To install it as a standard package into your environment:
```bash
pip install .
```

> **Note:** Make sure your user local binary directory (`~/.local/bin`) is included in your system's `PATH` so you can run the `vaultguard` command globally. You can add it by appending this to your `~/.bashrc` or `~/.zshrc`:
> ```bash
> export PATH="$HOME/.local/bin:$PATH"
> ```

## Usage
1. Initialize your quantum keyfile:
   ```bash
   vaultguard init
   ```
2. Encrypt your `.env` file:
   ```bash
   vaultguard encrypt .env
   ```
3. Decrypt your `.env` file:
   ```bash
   vaultguard decrypt .env
   ```
