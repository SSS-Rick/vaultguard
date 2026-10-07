from setuptools import find_packages, setup

setup(
    name="vaultguard",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "cryptography>=41.0.0",
    ],
    entry_points={
        "console_scripts": [
            "vaultguard=vaultguard.cli:main",
        ],
    },
    author="Jackdaw Collective",
    description="Sovereign Quantum-Resistant Secret Sync CLI",
    license="GPLv3",
)
