import os
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# define the encryption function for each file type
def encrypt_file(filename):
    # set the encryption key
    key = get_random_bytes(16) # this is a 128 bit key

    # set the block size for the encryption
    block_size = 16

    # read in the file
    with open(filename, 'rb') as file:
        data = file.read()

    # get the initial file size
    initial_size = len(data)

    # pad the data so that it is a multiple of the block size
    pad_size = block_size - len(data) % block_size
    data += pad_size.to_bytes(1, 'big') * pad_size

    # initialize the AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC)

    # encrypt the data
    start_time = time.time()
    ciphertext = cipher.encrypt(data)
    encryption_time = time.time() - start_time

    # get the encrypted file size
    encrypted_size = len(ciphertext)

    # write the encrypted data to a new file
    encrypted_filename = filename + '.enc'
    with open(encrypted_filename, 'wb') as file:
        file.write(ciphertext)

    # decrypt the data
    cipher = AES.new(key, AES.MODE_CBC)
    start_time = time.time()
    plaintext = cipher.decrypt(ciphertext)
    decryption_time = time.time() - start_time

    # remove padding from decrypted data
    plaintext = plaintext[:-pad_size]

    # write the decrypted data to a new file
    decrypted_filename = filename + '.dec'
    with open(decrypted_filename, 'wb') as file:
        file.write(plaintext)

    # write the metrics to a file
    with open('encryption_metrics.txt', 'a') as file:
        file.write(f"{filename}, {initial_size}, {encrypted_size}, {encryption_time}, {decryption_time}\n")


# get user input for number of times to run encryption and decryption process
num_runs = int(input("Enter the number of times to run the encryption and decryption process: "))

# define the file extensions to be encrypted
extensions = ['.pdf', '.txt', '.mp3', '.docx']

# get all files in the current directory with the specified extensions and run encryption and decryption process
for i in range(num_runs):
    print(f"--- Run {i+1} ---")
    for extension in extensions:
        for filename in os.listdir():
            if filename.endswith(extension):
                encrypt_file(filename)
print("Process complete.")
