class CaesarCipher:
    def __init__(self, key = 3):
        self.key = key
        
    def encrypt(self, plain_text: str) -> str:
        cipher_text = ''.join(chr((ord(char) - 97 + self.key) % 26 + 65) if char.isalpha() else char for char in plain_text.lower())

        return cipher_text
    
    def decrypt(self, cipher_text: str) -> str:
        plain_text = ''.join(chr((ord(char) - 65 - self.key) % 26 + 97) if char.isalpha() else char for char in cipher_text.upper())

        return plain_text


class AffineCipher:
    def __init__(self, key = (9,2)):
        self.key = key
        
    def encrypt(self, plain_text: str) -> str:
        cipher_text = ''.join(chr((self.key[0] * (ord(char) - 97) + self.key[1]) % 26 + 65) if char.isalpha() else char for char in plain_text.lower())

        return cipher_text
    
    def decrypt(self, cipher_text: str) -> str:
        plain_text = ''.join(chr((pow(self.key[0], -1, 26) * (ord(char) - 65 - self.key[1])) % 26 + 97) if char.isalpha() else char for char in cipher_text.upper())

        return plain_text


class PlayfairCipher:
    def __init__(self, key = "MONARCHY"):
        self.keymatrix = self.__create_keymatrix(key)

    def __create_keymatrix(self, key: str) -> tuple:
        key = ''.join(dict.fromkeys(key.upper()))
        keylist = [char for char in key]
        keylist.extend(chr(enc) for enc in range(ord('A'), ord('Z') + 1) if chr(enc) not in keylist)
        keylist.remove('J')
        keymatrix = tuple([tuple(keylist[i:i+5]) for i in range(0, 25, 5)])

        return keymatrix
    
    def __create_digrams(self, text: str) -> list:
        digram = []
        i = 0
        while i < len(text):
            first = text[i]
            second = text[i+1] if i+1 < len(text) else "X"
            digram.append(first + ("X" if first==second else second))
            i += 1 if first==second else 2
        return digram
    
    def __find_position(self, char: str) -> tuple:
        position = next((i, j) for i in range(5) for j in range(5) if self.keymatrix[i][j] == char)
        return position
    
    def __remove_x(self, text: list) -> None:
        i = 1
        while i < len(text)-1:
            if text[i] == "X" and text[i-1] == text[i+1]:
                del text[i]
            else:
                i += 1

    def encrypt(self, plain_text: str) -> str:
        symbols = [(i, plain_text[i]) for i in range(len(plain_text)) if not plain_text[i].isalpha()]
        plain_text = ''.join([char for char in plain_text if char.isalpha()]).upper().replace("J", "I")
        
        digrams = self.__create_digrams(plain_text)
        cipher_text = []
        for first, second in digrams:
            r1, c1 = self.__find_position(first)
            r2, c2 = self.__find_position(second)
            cipher_text += (self.keymatrix[r1][(c1 - 1) % 5] + self.keymatrix[r1][(c2 - 1) % 5] if r1 == r2 else self.keymatrix[(r1 - 1) % 5][c1] + self.keymatrix[(r2 - 1) % 5][c2] if c1 == c2 else self.keymatrix[r1][c2] + self.keymatrix[r2][c1])
        for pos, sym in symbols:
            cipher_text.insert(pos, sym)
        cipher_text = ''.join(cipher_text)

        return cipher_text
    
    def decrypt(self, cipher_text: str) -> str:
        symbols = [(i, cipher_text[i]) for i in range(len(cipher_text)) if not cipher_text[i].isalpha()]
        cipher_text = ''.join([char for char in cipher_text if char.isalpha()]).upper().replace("J", "I")
        
        digrams = [cipher_text[i:i+2] for i in range(0, len(cipher_text), 2)]
        plain_text = []
        for first, second in digrams:
            r1, c1 = self.__find_position(first)
            r2, c2 = self.__find_position(second)
            plain_text += (self.keymatrix[r1][(c1 + 1) % 5] + self.keymatrix[r1][(c2 + 1) % 5] if r1 == r2 else self.keymatrix[(r1 + 1) % 5][c1] + self.keymatrix[(r2 + 1) % 5][c2] if c1 == c2 else self.keymatrix[r1][c2] + self.keymatrix[r2][c1])
        for pos, sym in symbols:
            plain_text.insert(pos, sym)
        self.__remove_x(plain_text)
        plain_text = ''.join(plain_text)
        
        return plain_text.lower()


class HillCipher:
    def __init__(self, key = [[5,8],[17,13]]):
        self.key = key
    
    def __to_enctext(self, text: str) -> list:
        return [ord(char) - 65 for char in text]

    def __to_text(self, enctext: list) -> list:
        return [chr(n + 65) for n in enctext]

    def __mod_product(self, A: list, v: list) -> list:
        u = [(v[0]*A[0][0] + v[1]*A[1][0]) % 26, (v[0]*A[0][1] + v[1]*A[1][1]) % 26]

        return u
    
    def __mod_matmul(self, A: list, B: list) -> list:
        C = [[(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % 26, (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % 26],[(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % 26, (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % 26]]

        return C

    def __inverse_mat(self, mat: list) -> list:
        det = (mat[0][0]*mat[1][1] - mat[0][1]*mat[1][0]) % 26
        det_inv = pow(det, -1, 26)
        mat_inverse = [[(mat[1][1]*det_inv) % 26, (-mat[0][1]*det_inv) % 26], [(-mat[1][0]*det_inv) % 26, (mat[0][0]*det_inv) % 26]]

        return mat_inverse
    
    def __try_crack(self, plain_mat: list, cipher_mat: list):
        try:
            plain_mat_inv = self.__inverse_mat(plain_mat)
            key = self.__mod_matmul(plain_mat_inv, cipher_mat)
            return key
        except:
            return None

    def encrypt(self, plain_text: str) -> str:
        symbols = [(i, plain_text[i]) for i in range(len(plain_text)) if not plain_text[i].isalpha()]
        plain_text = ''.join([char for char in plain_text if char.isalpha()]).upper()
        
        plain_enc = self.__to_enctext(plain_text)
        if len(plain_enc) % 2:
            plain_enc.append(23)
        cipher_enc = []
        for i in range(0, len(plain_enc), 2):
            cipher_enc.extend(self.__mod_product(self.key, plain_enc[i:i+2]))
        cipher_list = self.__to_text(cipher_enc)
        for pos, sym in symbols:
            cipher_list.insert(pos, sym)
        cipher_text = ''.join(cipher_list)

        return cipher_text

    def decrypt(self, cipher_text: str) -> str:
        key_inverse = self.__inverse_mat(self.key)

        symbols = [(i, cipher_text[i]) for i in range(len(cipher_text)) if not cipher_text[i].isalpha()]
        cipher_text = ''.join([char for char in cipher_text if char.isalpha()]).upper()

        cipher_enc = self.__to_enctext(cipher_text)
        plain_enc = []
        for i in range(0, len(cipher_enc), 2):
            plain_enc.extend(self.__mod_product(key_inverse, cipher_enc[i:i+2]))
        plain_list = self.__to_text(plain_enc)
        for pos, sym in symbols:
            plain_list.insert(pos, sym)
        plain_text = ''.join(plain_list)

        return plain_text.lower()

    def crack_key(self, plain_text: str, cipher_text: str):
        plain_text = ''.join([char for char in plain_text if char.isalpha()]).upper()
        plain_enc = self.__to_enctext(plain_text)
        cipher_text = ''.join([char for char in cipher_text if char.isalpha()]).upper()
        cipher_enc = self.__to_enctext(cipher_text)

        for i in range(0,len(plain_enc)-3,2):
            plain_mat = [[plain_enc[i],plain_enc[i+1]],[plain_enc[i+2],plain_enc[i+3]]]
            cipher_mat = [[cipher_enc[i],cipher_enc[i+1]],[cipher_enc[i+2],cipher_enc[i+3]]]
            key = self.__try_crack(plain_mat, cipher_mat)
            if key: break

        return key
