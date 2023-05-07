import os
import time
from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes

def encrypt_file(filename):
    # generate 128-bit key using get_random_bytes()
    key = get_random_bytes(16)

    # read file to be encrypted
    with open(filename, 'rb') as file:
        data = file.read()

    # pad the data to a multiple of the block size of Blowfish cipher
    block_size = Blowfish.block_size
    pad_size = block_size - len(data) % block_size
    data += pad_size.to_bytes(1, 'big') * pad_size

    # encrypt the data using the key and CBC mode
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    start_time = time.time()
    ciphertext = cipher.encrypt(data)
    encryption_time = time.time() - start_time

    # record the original size and encrypted size of the file
    initial_size = os.path.getsize(filename)
    encrypted_size = len(ciphertext)

    # write encrypted data to a new file with '.enc' extension
    encrypted_filename = filename + '.enc'
    with open(encrypted_filename, 'wb') as file:
        file.write(cipher.iv + ciphertext)

    # return the key, encrypted filename, initial size, encrypted size, and encryption time
    return key, encrypted_filename, initial_size, encrypted_size, encryption_time


def decrypt_file(filename, key):
    # read encrypted data from the input file
    with open(filename, 'rb') as file:
        encrypted_data = file.read()

    # separate the IV from the ciphertext
    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]

    # decrypt the data using the key, IV, and CBC mode
    cipher_dec = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    start_time = time.time()
    decrypted_data = cipher_dec.decrypt(ciphertext)
    decryption_time = time.time() - start_time

    # Unpad the decrypted data and write it to a new file with '.dec' extension
    decrypted_data = decrypted_data[:-decrypted_data[-1]]
    decrypted_filename = filename[:-4] + '.dec'
    with open(decrypted_filename, 'wb') as file:
        file.write(decrypted_data)

    # Return the decryption time
    return decryption_time


# Define a list of file extensions to be encrypted
extensions = ['.pdf', '.txt', '.mp3', '.docx']

# Get the number of times to run the encryption from the user
num_runs = int(input("How many times would you like to run the encryption? "))

# Loop through the encryption and decryption process for each file
for _ in range(num_runs):
    print(f"--- Run {_+1} ---")
    for extension in extensions:
        for filename in os.listdir():
            if filename.endswith(extension):
                # Encrypt the file and record the metrics
                key, encrypted_filename, initial_size, encrypted_size, encryption_time = encrypt_file(filename)
                decryption_time = decrypt_file(encrypted_filename, key)

                # Write the metrics to a file
                with open('Blowfish_encryption_metrics.txt', 'a') as file:
                    file.write(f"{filename}, {initial_size}, {encrypted_size}, {encryption_time}, {decryption_time}\n")

# Print a message indicating that the process is complete
print("Process complete.")
