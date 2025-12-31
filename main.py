from src.crypto import CaesarCipher, AffineCipher, PlayfairCipher, HillCipher

# Caesar cipher tests
key_caesar = int(open("keys/caesar.txt", 'r').readline())

crypt_caesar = CaesarCipher(key_caesar)

plain_caesar = open("texts/plain.txt", 'r').readline()

open("texts/cipher_caesar.txt", 'w').write(crypt_caesar.encrypt(plain_caesar))

cipher_caesar = open("texts/cipher_caesar.txt", 'r').read()

open("texts/plain_caesar.txt", 'w').write(crypt_caesar.decrypt(cipher_caesar))


# Affine cipher tests
key_affine = tuple(map(int, open("keys/affine.txt", 'r').readline().split()))

crypt_affine = AffineCipher(key_affine)

plain_affine = open("texts/plain.txt", 'r').read()

open("texts/cipher_affine.txt", 'w').write(crypt_affine.encrypt(plain_affine))

cipher_affine = open("texts/cipher_affine.txt", 'r').read()

open("texts/plain_affine.txt", 'w').write(crypt_affine.decrypt(cipher_affine))


# Playfair cipher tests
key_playfair = open("keys/playfair.txt", 'r').readline()

crypt_playfair = PlayfairCipher(key_playfair)

plain_playfair = open("texts/plain.txt", 'r').read()

open("texts/cipher_playfair.txt", 'w').write(crypt_playfair.encrypt(plain_playfair))

cipher_playfair = open("texts/cipher_playfair.txt", 'r').read()

open("texts/plain_playfair.txt", 'w').write(crypt_playfair.decrypt(cipher_playfair))


# Hill cipher tests
key_hill = [list(map(int, line.split())) for line in open("keys/hill.txt", 'r').read().split('\n')]

crypt_hill = HillCipher(key_hill)

plain_hill = open("texts/plain.txt", 'r').read()

open("texts/cipher_hill.txt", 'w').write(crypt_hill.encrypt(plain_hill))

cipher_hill = open("texts/cipher_hill.txt", 'r').read()

open("texts/plain_hill.txt", 'w').write(crypt_hill.decrypt(cipher_hill))

open("texts/key_hill.txt", "w").write("\n".join(" ".join(map(str, row)) for row in crypt_hill.crack_key(plain_hill, cipher_hill)))