import argparse
import sys
import math

from src.crypto import CaesarCipher, AffineCipher, PlayfairCipher, HillCipher

MODULUS = 26


def read_text_arg(text, text_file):
    if (text is None) == (text_file is None):
        raise ValueError("Provide exactly one of --text or --text-file.")
    if text_file:
        with open(text_file, "r", encoding="utf-8") as f:
            return f.read()
    return text


def read_any_text(text, text_file, label="text"):
    if (text is None) == (text_file is None):
        raise ValueError(f"Provide exactly one of --{label} or --{label}-file.")
    if text_file:
        with open(text_file, "r", encoding="utf-8") as f:
            return f.read()
    return text


def write_output(out, out_file):
    sys.stdout.write(out)
    if not out.endswith("\n"):
        sys.stdout.write("\n")

    if out_file:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(out)


def gcd(a, b):
    return math.gcd(a, b)


def validate_affine_key(a, modulus=MODULUS):
    if gcd(a, modulus) != 1:
        raise ValueError(f"Invalid Affine key: 'a' must be coprime with {modulus} (got a={a}).")


def parse_hill_key(key_file, key):
    if (key_file is None) == (key is None):
        raise ValueError("Provide exactly one of --key-file or --key (4 integers).")

    if key is not None:
        if len(key) != 4:
            raise ValueError("Hill --key must have exactly 4 integers: a b c d.")
        a, b, c, d = key
        return [[a, b], [c, d]]

    raw = open(key_file, "r", encoding="utf-8").read().strip()
    rows = [ln.split() for ln in raw.splitlines() if ln.strip()]
    key_matrix = [list(map(int, row)) for row in rows]

    if len(key_matrix) != 2 or any(len(r) != 2 for r in key_matrix):
        raise ValueError("Hill key file must be a 2x2 matrix like:\n3 2\n8 5")

    return key_matrix


def det_2x2(K):
    return K[0][0] * K[1][1] - K[0][1] * K[1][0]


def validate_hill_key_2x2(K, modulus=MODULUS):
    d = det_2x2(K) % modulus
    if gcd(d, modulus) != 1:
        raise ValueError(
            f"Invalid Hill key: det(K) mod {modulus} must be coprime with {modulus}. "
            f"Got det mod {modulus} = {d}."
        )


def add_common_io_flags(p):
    p.add_argument("-t", "--text", help="Input text (plaintext for enc, ciphertext for dec).")
    p.add_argument("-f", "--text-file", help="Read input text from file.")
    p.add_argument("-o", "--out", help="Also write result to this file (output is always printed).")


def build_parser():
    parser = argparse.ArgumentParser(prog="main.py", description="Classic cipher CLI")
    cipher_parsers = parser.add_subparsers(dest="cipher", required=True)

    # --- Caesar ---
    caesar = cipher_parsers.add_parser("caesar", help="Caesar cipher")
    caesar_ops = caesar.add_subparsers(dest="op", required=True)

    caesar_enc = caesar_ops.add_parser("enc", help="Encrypt with Caesar")
    add_common_io_flags(caesar_enc)
    caesar_enc.add_argument("-k", "--key", type=int, required=True)

    caesar_dec = caesar_ops.add_parser("dec", help="Decrypt with Caesar")
    add_common_io_flags(caesar_dec)
    caesar_dec.add_argument("-k", "--key", type=int, required=True)

    # --- Affine ---
    affine = cipher_parsers.add_parser("affine", help="Affine cipher")
    affine_ops = affine.add_subparsers(dest="op", required=True)

    affine_enc = affine_ops.add_parser("enc", help="Encrypt with Affine")
    add_common_io_flags(affine_enc)
    affine_enc.add_argument("--a", type=int, required=True, help="Multiplicative key a")
    affine_enc.add_argument("--b", type=int, required=True, help="Additive key b")

    affine_dec = affine_ops.add_parser("dec", help="Decrypt with Affine")
    add_common_io_flags(affine_dec)
    affine_dec.add_argument("--a", type=int, required=True)
    affine_dec.add_argument("--b", type=int, required=True)

    # --- Playfair ---
    playfair = cipher_parsers.add_parser("playfair", help="Playfair cipher")
    playfair_ops = playfair.add_subparsers(dest="op", required=True)

    playfair_enc = playfair_ops.add_parser("enc", help="Encrypt with Playfair")
    add_common_io_flags(playfair_enc)
    playfair_enc.add_argument("-k", "--key", required=True, help="Playfair keyword/key")

    playfair_dec = playfair_ops.add_parser("dec", help="Decrypt with Playfair")
    add_common_io_flags(playfair_dec)
    playfair_dec.add_argument("-k", "--key", required=True)

    # --- Hill ---
    hill = cipher_parsers.add_parser("hill", help="Hill cipher (2x2)")
    hill_ops = hill.add_subparsers(dest="op", required=True)

    hill_enc = hill_ops.add_parser("enc", help="Encrypt with Hill")
    add_common_io_flags(hill_enc)
    hill_enc.add_argument("--key-file", help="Path to 2x2 key matrix file.")
    hill_enc.add_argument("--key", nargs=4, type=int, help="2x2 key as 4 ints: a b c d")

    hill_dec = hill_ops.add_parser("dec", help="Decrypt with Hill")
    add_common_io_flags(hill_dec)
    hill_dec.add_argument("--key-file", help="Path to 2x2 key matrix file.")
    hill_dec.add_argument("--key", nargs=4, type=int, help="2x2 key as 4 ints: a b c d")

    # IMPORTANT: use --ctext/--ctext-file (NOT --cipher/--cipher-file) to avoid args.cipher collision
    hill_crack = hill_ops.add_parser("crack", help="Crack Hill 2x2 key from known plaintext/ciphertext")
    hill_crack.add_argument("--plain", help="Known plaintext (string).")
    hill_crack.add_argument("--plain-file", help="Known plaintext file.")
    hill_crack.add_argument("--ctext", help="Known ciphertext (string).")
    hill_crack.add_argument("--ctext-file", help="Known ciphertext file.")
    hill_crack.add_argument("-o", "--out", help="Also write recovered key matrix to file (always printed).")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.cipher == "caesar":
            text = read_text_arg(args.text, args.text_file)
            crypt = CaesarCipher(args.key)
            out = crypt.encrypt(text) if args.op == "enc" else crypt.decrypt(text)
            write_output(out, args.out)
            return

        if args.cipher == "affine":
            validate_affine_key(args.a)
            text = read_text_arg(args.text, args.text_file)
            crypt = AffineCipher((args.a, args.b))
            out = crypt.encrypt(text) if args.op == "enc" else crypt.decrypt(text)
            write_output(out, args.out)
            return

        if args.cipher == "playfair":
            text = read_text_arg(args.text, args.text_file)
            crypt = PlayfairCipher(args.key)
            out = crypt.encrypt(text) if args.op == "enc" else crypt.decrypt(text)
            write_output(out, args.out)
            return

        if args.cipher == "hill":
            if args.op == "enc":
                text = read_text_arg(args.text, args.text_file)
                key_matrix = parse_hill_key(args.key_file, args.key)
                validate_hill_key_2x2(key_matrix)
                crypt = HillCipher(key_matrix)
                out = crypt.encrypt(text)
                write_output(out, args.out)
                return

            if args.op == "dec":
                text = read_text_arg(args.text, args.text_file)
                key_matrix = parse_hill_key(args.key_file, args.key)
                validate_hill_key_2x2(key_matrix)
                crypt = HillCipher(key_matrix)
                out = crypt.decrypt(text)
                write_output(out, args.out)
                return

            if args.op == "crack":
                plain = read_any_text(args.plain, args.plain_file, label="plain")
                ctext = read_any_text(args.ctext, args.ctext_file, label="ctext")

                crypt = HillCipher([[1, 0], [0, 1]])  # dummy key; crack_key doesn't use it
                key = crypt.crack_key(plain, ctext)

                if not key:
                    raise ValueError("Could not crack key (no invertible plaintext block found).")

                key_text = "\n".join(" ".join(map(str, row)) for row in key)
                write_output(key_text, args.out)
                return

            raise ValueError(f"Unknown hill operation: {args.op}")

        parser.error("Unsupported command combination.")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
