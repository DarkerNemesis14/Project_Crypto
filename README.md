# Project_Crypto
A simple python-based cryptography project for encrypting and decrypting text using custom keys.

## Contents
- **`main.py`** – Main script to run encryption/decryption workflows.
- **`src/`** – Storage python modules implementing cryptographic functions and helpers.
- **`keys/`** – Storage for generated keys.
- **`texts/`** – Storage for input and output files.

## Features
- Encrypt plaintext to ciphertext  
- Decrypt ciphertext back to plaintext  
- Simple key management for cryptographic workflows  
- Easy to extend with additional algorithms

## Requirements
- Python 3.7 or higher  
- **No additional packages required**

## Project Structure
```bash
Project_Crypto/
├── keys/
│   └── (key files)
├── src/
│   └── (crypto modules)
├── texts/
│   └── (text files)
├── main.py
└── README.md
```

## Usage
- Write your plaintext in `text/plain.txt`
- Write the keys in the `keys/` directory
- Run the program: `python main.py`
- Outputs will be saved in `texts/` directory