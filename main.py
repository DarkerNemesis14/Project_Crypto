from src.crypto import CaesarCipher, AffineCipher, PlayfairCipher, HillCipher


with open("keys/hill.txt", 'r') as file:
    key = [list(map(int, line.split())) for line in file.read().split('\n')]

crypt = HillCipher(key)

with open("plain.txt", 'r') as file:
    plain = file.read()

with open("cipher.txt", 'w') as file:
    file.write(crypt.encrypt(plain))

with open("cipher.txt", 'r') as file:
    cipher = file.read()

with open("plain.txt", 'w') as file:
    file.write(crypt.decrypt(cipher))

print(plain, cipher)
print(crypt.crack_key(plain, cipher))