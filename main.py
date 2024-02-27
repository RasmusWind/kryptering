#!./env/bin/python
import random
import re
import os
CAESAR_PLACES = 4
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

ALPHA_MIN = 65
ALPHA_MAX = 90
ALPHA_LENGTH = 26

freq_norm = {
    "A":0.64297,
    "B":0.11746,
    "C":0.21902,
    "D":0.33483,
    "E":1.00000,
    "F":0.17541,
    "G":0.15864,
    "H":0.47977,
    "I":0.54842,
    "J":0.01205,
    "K":0.06078,
    "L":0.31688,
    "M":0.18942,
    "N":0.53133,
    "O":0.59101, 
    "P":0.15187,
    "Q":0.00748,
    "R":0.47134,
    "S":0.49811,
    "T":0.71296,
    "U":0.21713,
    "V":0.07700,
    "W":0.18580,
    "X":0.01181,
    "Y":0.15541,
    "Z":0.00583,
}


def encrypt(raw_input, places=CAESAR_PLACES):
    input = str(raw_input).upper()
    encrypted_input = ""
    spaces_indexes = []
    for ind, char in enumerate(input):
        if char == " ":
            spaces_indexes.append(ind)
            continue
        try:
            char_index = ord(char)
        except ValueError:
            continue
        new_index = char_index + places

        if new_index > ALPHA_MAX:
            new_index -= ALPHA_LENGTH
        encrypted_input += chr(new_index)
    for si in spaces_indexes:
        encrypted_input = f"{encrypted_input[:si]} {encrypted_input[si:]}"
    return encrypted_input


def decrypt(encrypted_input, places=CAESAR_PLACES):
    input = str(encrypted_input).upper()
    stripped_input = ""
    for char in input:
        if char == " " or char in ALPHABET:
            stripped_input += char
    decrypted_input = ""
    spaces_indexes = []
    for ind, char in enumerate(input):
        if char == " ":
            spaces_indexes.append(ind)
            continue
        try:
            char_index = ord(char)
        except ValueError:
            continue
        new_index = char_index - places

        if new_index < ALPHA_MIN:
            new_index += ALPHA_LENGTH
        decrypted_input += chr(new_index)
    for si in spaces_indexes:
        decrypted_input = f"{decrypted_input[:si]} {decrypted_input[si:]}"
    return decrypted_input


def ol_encrypt(raw_input, places=CAESAR_PLACES):
    return "".join([ALPHABET[new_index] if new_index < len(ALPHABET) else ALPHABET[new_index-len(ALPHABET)] for new_index in [ALPHABET.index(char)+places for char in str(raw_input).replace(" ", "_")]])


def ol_decrypt(encrypted_input, places=CAESAR_PLACES):
    return "".join([ALPHABET[new_index] if new_index > 0 else ALPHABET[new_index+len(ALPHABET)] for new_index in [ALPHABET.index(char)-places for char in str(encrypted_input)]]).replace("_", " ")


def unicode_encrypt(raw_input, places=CAESAR_PLACES):
    input = str(raw_input)
    encrypted_input = ""
    for char in input:
        chr_index = ord(char)
        encrypted_input += chr(chr_index+places)
    return encrypted_input


def unicode_decrypt(encrypted_input, places=CAESAR_PLACES):
    input = str(encrypted_input)
    decrypted_input = ""
    for char in input:
        chr_index = ord(char)
        decrypted_input += chr(chr_index-places)
    return decrypted_input


def unicode_ol_encrypt(raw_input, places=CAESAR_PLACES):
    return "".join(chr(ord(char)+places) for char in str(raw_input))


def unicode_ol_decrypt(encrypted_input, places=CAESAR_PLACES):
    return "".join(chr(ord(char)-places) for char in str(encrypted_input))


def decrypted_text_deviation(decrypted_text):
    d = {}
    total_sum = 0
    for letter in decrypted_text:
        if letter.upper() not in ALPHABET:
            continue
        total_sum += freq_norm[letter.upper()]
        if letter.upper() not in d:
            d[letter.upper()] = 1
        else:
            d[letter.upper()] += 1
    
    new_d = {}
    
    max_value = 0
    for k,v in d.items():
        if v > max_value:
            max_value = v

    for k, v in d.items():
        deviation_num = v/max_value
        new_d[k] = deviation(freq_norm[k], deviation_num)
    
    return sum(new_d.values()), total_sum

        
def deviation(from_num, to_num):
    if from_num < to_num:
        return to_num - from_num
    return from_num - to_num


def decrypt_text(encrypted_str:str) -> tuple[int, str, int]:
    deviations = []
    for i in range(len(ALPHABET)):
        dec = decrypt(encrypted_str, i)
        dev = decrypted_text_deviation(dec)
        deviations.append((dev, dec, i))
    deviations = sorted(deviations, key=lambda x: x[0])
    
    return deviations[0]


def decrypt_local_song(path):
    input_str = ""
    with open(path, "r") as f:
        lines = f.readlines()
        line = " ".join(lines)
        line = re.sub(r'[^a-zA-Z ]+', '', line)
        input_str = line.upper()
    
    return decrypt_text(input_str)


def encrypt_local_song(path, places=None):
    input_str = standardize_local_text(path)
    
    if places is None:
        places = random.randrange(0, len(ALPHABET)-1)
    encrypted_str = encrypt(input_str, places)
    new_name = path.replace(".txt", "").replace("/","").replace(".","")
    print(new_name)
    with open(f'{new_name}_encrypted.txt', "w") as f:
        f.write(encrypted_str)
    return encrypted_str


def standardize_local_text(path):
    input_str = ""
    with open(path, "r") as f:
        lines = f.readlines()
        line = " ".join(lines)
        line = re.sub(r'[^a-zA-Z ]+', '', line)
        line = line.replace("\n", "")
        input_str = line.upper()
    return input_str


if __name__ == "__main__":
    songs = os.listdir("./encrypted_songs")
    for song in songs:
        deviation_num, text, shift = decrypt_local_song(f"./encrypted_songs/{song}")
        print(text)
        print(shift)
        print()