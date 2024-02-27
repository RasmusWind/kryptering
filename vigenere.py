#!./env/bin/python
from main import ALPHABET, decrypted_text_deviation, encrypt, decrypt
from multiprocessing import Process
import multiprocessing
import time

def find_key_char(key, index_counter, subtraction_num):
    count = index_counter - subtraction_num
    if count >= len(key):
        subtraction_num = index_counter
        count = index_counter - subtraction_num
    key_char = key[count]
    if key_char not in ALPHABET:
        return find_key_char(key, index_counter+1, subtraction_num)
    return (key_char, index_counter, subtraction_num)


def vigenere_encrypt(string_to_encrypt, key):
    key = key.upper().replace(" ", "")
    string_to_encrypt = string_to_encrypt.upper()
    encrypted_string = ""
    subtraction_num = 0
    index_counter = 0
    for ste_char in string_to_encrypt:
        if ste_char not in ALPHABET:
            encrypted_string += ste_char
            continue

        key_char, index_counter, subtraction_num = find_key_char(key, index_counter, subtraction_num)

        key_char_index = ALPHABET.index(key_char)
        
        new_char = encrypt(ste_char, key_char_index)
        encrypted_string += new_char
        index_counter += 1
    return encrypted_string


def vigenere_decrypt(string_to_decrypt, key):
    key = key.upper().replace(" ", "")
    string_to_decrypt = string_to_decrypt.upper()
    decrypted_string = ""
    subtraction_num = 0
    index_counter = 0
    for ste_char in string_to_decrypt:
        if ste_char not in ALPHABET:
            decrypted_string += ste_char
            continue
        
        key_char, index_counter, subtraction_num = find_key_char(key, index_counter, subtraction_num)

        key_char_index = ALPHABET.index(key_char)
        new_char = decrypt(ste_char, key_char_index)
        decrypted_string += new_char
        index_counter += 1
    return decrypted_string


def increment_key(key, increment_index=-1):
    key_copy = key[:]
    try:
        if key[increment_index] == ALPHABET[-1]:
            key_copy_split = [*key_copy]
            key_copy_split[increment_index] = "A"
            key_copy = "".join(key_copy_split)
            return increment_key(key_copy, increment_index-1)
        else:
            key_copy_split = [*key_copy]
            key_copy_split[increment_index] = ALPHABET[ALPHABET.index(key_copy[increment_index]) + 1]
            key_copy = "".join(key_copy_split)
    except IndexError:
        key_copy = "A" + key_copy
    
    return key_copy


def vigenere_brute_force(string_to_decrypt, key_range, result, r_index):
    process_time = time.time()
    current_key = key_range[0]
    tries = []
    
    while current_key != key_range[1]:
        decrypted_string = vigenere_decrypt(string_to_decrypt, current_key)
        deviation, summer = decrypted_text_deviation(decrypted_string)
        tries.append((deviation, summer, decrypted_string, current_key))
        print(f"Key:{current_key}", end="\r")
        current_key = increment_key(current_key)
    
    result[r_index] = sorted(tries, key=lambda x: x[0])[:20]
    print(f"Process: {r_index} took: {time.time()-process_time}")

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    t1 = time.time()
    string_to_encrypt = "This is an english text that is supposed to be tested by my brute force decryption"
    key = "HANS"
    encrypted_string = vigenere_encrypt(string_to_encrypt, key)
    threads = [None] * 13
    return_list = manager.list([None] * 13)

    threads[0] = Process(target=vigenere_brute_force, args=(encrypted_string, ("A", "BBBB"), return_list, 0))
    threads[1] = Process(target=vigenere_brute_force, args=(encrypted_string, ("BBBB", "DDDD"), return_list, 1))
    threads[2] = Process(target=vigenere_brute_force, args=(encrypted_string, ("DDDD", "FFFF"), return_list, 2))
    threads[3] = Process(target=vigenere_brute_force, args=(encrypted_string, ("FFFF", "HHHH"), return_list, 3))
    threads[4] = Process(target=vigenere_brute_force, args=(encrypted_string, ("HHHH", "JJJJ"), return_list, 4))
    threads[5] = Process(target=vigenere_brute_force, args=(encrypted_string, ("JJJJ", "LLLL"), return_list, 5))
    threads[6] = Process(target=vigenere_brute_force, args=(encrypted_string, ("LLLL", "NNNN"), return_list, 6))
    threads[7] = Process(target=vigenere_brute_force, args=(encrypted_string, ("NNNN", "PPPP"), return_list, 7))
    threads[8] = Process(target=vigenere_brute_force, args=(encrypted_string, ("PPPP", "RRRR"), return_list, 8))
    threads[9] = Process(target=vigenere_brute_force, args=(encrypted_string, ("RRRR", "TTTT"), return_list, 9))
    threads[10] = Process(target=vigenere_brute_force, args=(encrypted_string, ("TTTT", "VVVV"), return_list, 10))
    threads[11] = Process(target=vigenere_brute_force, args=(encrypted_string, ("VVVV", "XXXX"), return_list, 11))
    threads[12] = Process(target=vigenere_brute_force, args=(encrypted_string, ("XXXX", "AAAAA"), return_list, 12))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    final_res = []

    for result in return_list:
        if result:
            for r in result:
                final_res.append(r)
    
    final_res = sorted(final_res, key=lambda x: x[0])[:50]

    for best_try in final_res:
        print(best_try)

    final_res = sorted(final_res, key=lambda x: x[2], reverse=True)
    print("FINAL:", final_res[0])
    print("TOOK:", time.time()-t1)