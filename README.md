# Classic Cipher Client

A Python command-line tool that provides a unified interface for classic ciphers: Caesar, Affine, Playfair, and Hill. It uses `argparse` subcommands for encryption/decryption, and the Hill cipher additionally supports `crack` to recover a 2x2 key from known plaintext–ciphertext pairs. 

## Requirements
- Python 3.7+ (standard library only). 

## Quick start
Show help:
```bash
python main.py -h
```
## Cipher modes
```bash
python main.py hill -h
```
## Unified CLI Interface
All cipher operations follow the same general command pattern:
`python main.py <cipher> <mode> [options]`
- cipher: The algorithm to use (caesar, affine, playfair, or hill).
- mode: The operation mode (enc for encryption, dec for decryption).
- [options]: Cipher-specific parameters such as keys, input files, and output files.

## HillCipher usage (2x2)
### Encrypt:

```bash
python main.py hill enc --key 3 2 8 5 -f texts/plain.txt -o texts/cipher_hill.txt
```
### Decrypt:

```bash
python main.py hill dec --key 3 2 8 5 -f texts/cipher_hill.txt -o texts/plain_hill.txt
```
### Crack key (known-plaintext):

```bash
python main.py hill crack --plain-file texts/plain.txt --ctext-file texts/cipher_hill.txt -o keys/hill_cracked.txt
```
## Project structure
```
Project_Crypto/
├── keys/     # Key files (including cracked keys)
├── src/      # Cipher implementations
├── texts/    # Sample input/output texts
└── main.py   # CLI entry point
```