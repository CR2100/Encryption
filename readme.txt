Padding is added to the input data in block ciphers to ensure that the data is a multiple of the block size required by the specific encryption algorithm. Block ciphers like AES and Blowfish process data in fixed-size blocks, typically 128 bits (16 bytes) for AES and 64 bits (8 bytes) for Blowfish.

When the input data is not a multiple of the block size, it needs to be padded to fit the block size. Padding serves two main purposes:

Ensures that the data can be processed by the block cipher without errors, as the algorithm expects input data to be a multiple of the block size.
Provides an unambiguous way to remove the padding after decryption, so the original data can be restored without any extra bytes.
There are different padding schemes available, like PKCS#7, ANSI X.923, and ISO/IEC 7816-4. In the provided encryption scripts, a simple padding method is used, where the padding byte represents the number of padding bytes added. This method ensures that the padding can be easily removed after decryption by looking at the last byte of the decrypted data and removing that many bytes from the end.

It's important to note that padding is not required for all encryption algorithms. For example, RSA doesn't require padding in the same way block ciphers do, as it is not a block cipher. However, padding is often used with RSA for security reasons, to prevent certain attacks on the algorithm.


AES-128 is considered roughly equivalent in security to a 3072-bit RSA key.
AES-192 is considered roughly equivalent in security to a 7680-bit RSA key.
AES-256 is considered roughly equivalent in security to a 15360-bit RSA key.

based on this new info,
need to choose these:
RSA: 3072 bits (approximately equivalent to AES-128)
AES: 128 bits
Blowfish: 128 bits (Blowfish can support key sizes up to 448 bits, but 128 bits is considered secure enough and maintains a similar security level as the other two algorithms)
