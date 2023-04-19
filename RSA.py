import os
import time
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# define the encryption function for each file type
def encrypt_file_RSA(filename):
    # generate RSA keys
    key = RSA.generate(2048)

    # set the block size for the encryption
    block_size = 16

    # read in the file
    with open(filename, 'rb') as file:
        data = file.read()

    # pad the data so that it is a multiple of the block size
    pad_size = block_size - len(data) % block_size
    data += pad_size.to_bytes(1, 'big') * pad_size

    # initialize the RSA cipher in CBC mode
    cipher_rsa = PKCS1_OAEP.new(key)

    # initialize the AES cipher in CBC mode
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_CBC)

    # encrypt the session key with the RSA cipher
    start_time = time.time()
    encrypted_session_key = cipher_rsa.encrypt(session_key)
    encryption_time = time.time() - start_time

    # encrypt the data with the AES cipher
    ciphertext = cipher_aes.encrypt(data)

    # get the initial and encrypted file size
    initial_size = os.path.getsize(filename)
    encrypted_size = len(encrypted_session_key) + len(ciphertext)

    # write the encrypted data to a new file
    encrypted_filename = filename + '.enc'
    with open(encrypted_filename, 'wb') as file:
        file.write(encrypted_session_key)
        file.write(ciphertext)

# ... (the beginning part of the script remains unchanged)

    # write the metrics to a file
    with open('RSA_encryption_metrics.txt', 'a') as file:
        file.write(f"{filename}, {initial_size}, {encrypted_size}, {encryption_time}, ")

    # Decrypt the data
    cipher_rsa_dec = PKCS1_OAEP.new(key)
    start_time = time.time()
    decrypted_session_key = cipher_rsa_dec.decrypt(encrypted_session_key)
    decryption_time = time.time() - start_time

    cipher_aes_dec = AES.new(decrypted_session_key, AES.MODE_CBC)
    decrypted_data = cipher_aes_dec.decrypt(ciphertext)

    # remove padding from decrypted data
    pad_size = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad_size]

    # write the decrypted data to a new file
    decrypted_filename = filename + '.dec'
    with open(decrypted_filename, 'wb') as file:
        file.write(decrypted_data)

    # write decryption time to the file
    with open('RSA_encryption_metrics.txt', 'a') as file:
        file.write(f"{decryption_time}\n")

# ... (the rest of the script remains unchanged)


# define the file extensions to be encrypted
extensions = ['.pdf', '.txt', '.mp3', '.docx']

# prompt user for number of runs
num_runs = int(input("Enter the number of times to run the encryption algorithm: "))

for i in range(num_runs):
    print(f"--- Run {i+1} ---")

    # get all files in the current directory with the specified extensions
    for extension in extensions:
        for filename in os.listdir():
            if filename.endswith(extension):
                encrypt_file_RSA(filename)

print("Process complete.")
