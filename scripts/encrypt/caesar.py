from scytale.ciphers import Caesar


if __name__ == '__main__':
    plaintext = input('Plaintext: ')
    key = int(input('Key: '))
    ciphertext = Caesar(key=key).encrypt(plaintext)
    print(f'Ciphertext: {ciphertext}')
