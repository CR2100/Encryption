import os
import time
from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes

# Define the encryption function for each file type
def encrypt_file(filename):
    # Set the encryption key
    key = get_random_bytes(16)

    # Read in the file
    with open(filename, 'rb') as file:
        data = file.read()

    # Set the block size for the encryption
    block_size = Blowfish.block_size

    # Pad the data so that it is a multiple of the block size
    pad_size = block_size - len(data) % block_size
    data += pad_size.to_bytes(1, 'big') * pad_size

    # Initialize the Blowfish cipher in CBC mode
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)

    # Encrypt the data
    start_time = time.time()
    ciphertext = cipher.encrypt(data)
    encryption_time = time.time() - start_time

    # Get the initial and encrypted file size
    initial_size = os.path.getsize(filename)
    encrypted_size = len(ciphertext)

    # Write the encrypted data to a new file
    encrypted_filename = filename + '.enc'
    with open(encrypted_filename, 'wb') as file:
        file.write(cipher.iv + ciphertext)

    # Decrypt the data
    with open(encrypted_filename, 'rb') as file:
        encrypted_data = file.read()

    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]

    cipher_dec = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted_data = cipher_dec.decrypt(ciphertext)

    # Remove the padding from the decrypted data
    decrypted_data = decrypted_data[:-decrypted_data[-1]]

    # Write the decrypted data to a new file
    decrypted_filename = filename + '.dec'
    with open(decrypted_filename, 'wb') as file:
        file.write(decrypted_data)

# ... (the beginning part of the script remains unchanged)

    # Decrypt the data
    with open(encrypted_filename, 'rb') as file:
        encrypted_data = file.read()

    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]

    cipher_dec = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    start_time = time.time()
    decrypted_data = cipher_dec.decrypt(ciphertext)
    decryption_time = time.time() - start_time

    # ... (the rest of the script remains unchanged)

    # Write the metrics to a file
    with open('Blowfish_encryption_metrics.txt', 'a') as file:
        file.write(f"{filename}, {initial_size}, {encrypted_size}, {encryption_time}, {decryption_time}\n")

# ... (the rest of the script remains unchanged)


# Define the file extensions to be encrypted
extensions = ['.pdf', '.txt', '.mp3', '.docx']

# Get the number of times to run the encryption
num_runs = int(input("How many times would you like to run the encryption? "))

# Run the encryption and decryption for each file type and repeat as many times as specified
for _ in range(num_runs):
    print(f"--- Run {_+1} ---")
    for extension in extensions:
        for filename in os.listdir():
            if filename.endswith(extension):
                encrypt_file(filename)
print("Process complete.")
