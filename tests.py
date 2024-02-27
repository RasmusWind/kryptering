#!./env/bin/python
import unittest
from vigenere import vigenere_decrypt, vigenere_encrypt

class CryptationTest(unittest.TestCase):    
    def vigenere_test(self):
        key = "HANS"
        text = "SO CLOSE NO MATTER HOW FAR COULDNT BE MUCH MORE FROM THE HEART FOREVER TRUST IN WHO WE ARE AND NOTHING ELSE MATTERS NEVER OPENED MYSELF THIS WAY LIFE IS OURS WE LIVE IT OUR WAY ALL THESE WORDS I DONT JUST SAY AND NOTHING ELSE MATTERS TRUST I SEEK AND I FIND IN YOU EVERY DAY FOR US SOMETHING NEW OPEN MIND FOR A DIFFERENT VIEW AND NOTHING ELSE MATTERS NEVER CARED FOR WHAT THEY DO NEVER CARED FOR WHAT THEY KNOW AND I KNOW SO CLOSE NO MATTER HOW FAR COULDNT BE MUCH MORE FROM THE HEART FOREVER TRUSTING WHO WE ARE AND NOTHING ELSE MATTERS"
        encrypted_string = vigenere_encrypt(text, key)
        decrypted_string = vigenere_decrypt(encrypted_string, key)
        self.assertEqual(text.upper(), decrypted_string)
    
    def vigenere_test2(self):
        key = "OCULORHINOLARINGOLOGY"
        text = "attacking tonight"
        encrypted_string = vigenere_encrypt(text, key)
        decrypted_string = vigenere_decrypt(encrypted_string, key)
        self.assertEqual(text.upper(), decrypted_string)

    def test(self):
        self.vigenere_test()
        self.vigenere_test2()

if __name__ == "__main__":
    unittest.main()