"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import os
import random
import sys
import zlib
from getpass import getpass

import numpy as np
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.padding import PKCS7
from PIL import Image


def encrypt_data(data, public_key):
    """
    Encrypts data using a hybrid RSA-AES scheme.

    Generates a random AES session key, derives a symmetric key via PBKDF2,
    encrypts the data with AES-CBC, and encrypts the session key with RSA-OAEP.
    """
    session_key = os.urandom(32)
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
        backend=default_backend()
    )
    key = kdf.derive(session_key)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    padder = PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_session_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_session_key, salt, iv, encrypted_data


def decrypt_data(encrypted_session_key, salt, iv, encrypted_data, private_key):
    """
    Decrypts data encrypted by encrypt_data().

    Decrypts the RSA-encrypted session key, derives the AES key via PBKDF2,
    then decrypts the data using AES-CBC.
    """
    session_key = private_key.decrypt(
        encrypted_session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200000,
        backend=default_backend()
    )
    key = kdf.derive(session_key)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = \
        decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = \
        unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data


def compute_seed_from_image_dimensions(image_path):
    """
    Generates a deterministic seed based on image dimensions
    """
    with Image.open(image_path) as img:
        width, height = img.size
    return width + height


def hide_file_in_png(image_path, file_to_hide,
                     output_image_path, public_key_path):
    """
    Hides and encrypts a file within an image using LSB steganography
    """
    with open(public_key_path, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    seed = compute_seed_from_image_dimensions(image_path)
    prng = random.Random(seed)

    img = Image.open(image_path)
    if img.mode not in ['RGB', 'RGBA', 'P', 'L']:
        raise ValueError(
            "Image mode must be RGB, RGBA, P (palette-based), "
            "or L (grayscale).")

    if img.mode == 'P' or img.mode == 'L':
        img = img.convert('RGB')

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    host_format = img.format
    if host_format is None:
        file_extension = os.path.splitext(image_path)[1].lower()
        extension_to_format = {
            '.tga': 'TGA',
            '.png': 'PNG',
            '.bmp': 'BMP',
            '.tif': 'TIFF',
            '.tiff': 'TIFF',
        }
        host_format = extension_to_format.get(file_extension)

    supported_formats = {'TGA', 'TIFF', 'BMP', 'PNG'}
    if host_format not in supported_formats:
        raise ValueError(f"Unsupported image format: {host_format}")
    pixels = np.array(img)
    with open(file_to_hide, 'rb') as f:
        file_bytes = f.read()
    compressed_data = zlib.compress(file_bytes)

    encrypted_session_key, salt, iv, encrypted_data = encrypt_data(
        compressed_data, public_key
    )
    filename = os.path.basename(file_to_hide).encode()
    filename_size = len(filename)

    data_to_encode = (filename_size.to_bytes(4, 'big') + filename +
                      encrypted_session_key + salt + iv + encrypted_data)
    file_size = len(data_to_encode)
    num_pixels_required = file_size * 8
    if num_pixels_required > pixels.size // 4:
        raise ValueError("Image is not large enough to hide the file.")

    pixel_indices = list(range(pixels.size // 4))
    prng.shuffle(pixel_indices)

    for i in range(64):
        idx = pixel_indices[i]
        bit = (file_size >> (63 - i)) & 0x1
        pixel_val = pixels[idx // pixels.shape[1], idx % pixels.shape[1], 0]
        if (pixel_val & 0x1) != bit:
            pixels[idx // pixels.shape[1], idx % pixels.shape[1], 0] ^= 0x1

    for i, byte in enumerate(data_to_encode):
        for bit in range(8):
            idx = pixel_indices[64 + i * 8 + bit]
            pixel_val = pixels[idx // pixels.shape[1],
                               idx % pixels.shape[1], 0]
            expected_bit = (byte >> (7 - bit)) & 0x1
            if (pixel_val & 0x1) != expected_bit:
                pixels[idx // pixels.shape[1], idx % pixels.shape[1], 0] ^= 0x1
    if os.path.exists(output_image_path):
        overwrite = input(f"The file '{output_image_path}' "
                          f"already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Extraction cancelled.")
            return
    new_img = Image.fromarray(pixels, 'RGBA')

    if host_format == 'PNG':
        new_img.save(output_image_path, format='PNG', optimize=True)
    elif host_format == 'BMP':
        new_img.save(output_image_path, format='BMP', optimize=True)
    elif host_format == 'TGA':
        new_img.save(output_image_path, format='TGA', optimize=True)
    elif host_format == 'TIFF':
        new_img.save(output_image_path, format='TIFF', optimize=True)
    else:
        raise ValueError(f"Unsupported image format: {host_format}")

    print(
        f"File '{file_to_hide}' has been successfully "
        f"hidden in '{output_image_path}'."
    )


def extract_file_from_png(image_path, output_file_path, private_key_path):
    """
    Extracts and decrypts a hidden file from a stego-image
    """
    passphrase = getpass("Enter the private key passphrase: ")
    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=passphrase.encode(),
            backend=default_backend()
        )
    encrypted_session_key_size = private_key.key_size // 8
    seed = compute_seed_from_image_dimensions(image_path)
    prng = random.Random(seed)
    img = Image.open(image_path)
    if img.mode not in ['RGB', 'RGBA']:
        raise ValueError("Image must be in RGB or RGBA format.")
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    pixels = np.array(img)
    flat_pixels = pixels.flatten()
    channel_multiplier = 4

    file_size = 0
    for i in range(64):
        pixel_bit = flat_pixels[i * channel_multiplier] & 0x1
        file_size = (file_size << 1) | pixel_bit
    num_bytes_to_extract = file_size
    extracted_bytes = []

    pixel_indices = list(range(pixels.size // 4))
    prng.shuffle(pixel_indices)

    file_size = 0
    for i in range(64):
        idx = pixel_indices[i]
        file_size = (file_size << 1) | (pixels[idx // pixels.shape[1],
                                               idx % pixels.shape[1], 0] & 0x1)

    num_bytes_to_extract = file_size

    extracted_bytes = []
    for i in range(num_bytes_to_extract):
        byte = 0
        for bit in range(8):
            idx = pixel_indices[64 + i * 8 + bit]
            byte = (byte << 1) | (pixels[idx // pixels.shape[1],
                                         idx % pixels.shape[1], 0] & 0x1)
        extracted_bytes.append(byte)
    data_to_decode = bytes(extracted_bytes)

    filename_size = int.from_bytes(data_to_decode[:4], 'big')
    filename = data_to_decode[4:4 + filename_size].decode()
    offset = 4 + filename_size
    key_end = offset + encrypted_session_key_size
    encrypted_session_key = data_to_decode[offset:key_end]

    salt_start = offset + encrypted_session_key_size
    salt_end = salt_start + 16
    salt = data_to_decode[salt_start:salt_end]

    iv_start = offset + encrypted_session_key_size + 16
    iv_end = iv_start + 16
    iv = data_to_decode[iv_start:iv_end]
    encrypted_data = data_to_decode[offset + encrypted_session_key_size + 32:]
    decrypted_data = decrypt_data(
        encrypted_session_key,
        salt, iv, encrypted_data,
        private_key)
    decompressed_data = zlib.decompress(decrypted_data)
    if not output_file_path:
        output_file_path = os.path.join(os.getcwd(), filename)

    if os.path.exists(output_file_path):
        overwrite = input(
            f"The file '{output_file_path}' already exists. "
            f"Overwrite? (y/n): "
        ).lower()
        if overwrite != 'y':
            print("Extraction cancelled.")
            return
    with open(output_file_path, 'wb') as f:
        f.write(decompressed_data)

    print(f"File extracted to {output_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description='SecretPixel - Advanced Steganography Tool',
        epilog="Example commands:\n"
               "  Hide: python secret_pixel.py hide host.png secret.txt "
               "mypublickey.pem output.png\n"
               "  Extract: python secret_pixel.py extract carrier.png "
               "myprivatekey.pem [extracted.txt]",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command')

    hide_parser = subparsers.add_parser(
        'hide', help='Hide a file inside an image',
        epilog="Example: python secret_pixel.py hide host.png secret.txt "
               "mypublickey.pem output.png",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    hide_parser.add_argument('host', type=str, help='Path to the host image')
    hide_parser.add_argument(
        'secret', type=str, help='Path to the secret file to hide'
    )
    hide_parser.add_argument(
        'pubkey', type=str, help='Path to the public key for encryption'
    )
    hide_parser.add_argument(
        'output', type=str, help='Path to the output image with embedded data'
    )
    extract_parser = subparsers.add_parser(
        'extract', help='Extract a file from an image',
        epilog="Example: python secret_pixel.py extract carrier.png  "
               "myprivatekey.pem [extracted.txt]",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    extract_parser.add_argument(
        'carrier', type=str,
        help='Path to the image with embedded data'
    )
    extract_parser.add_argument(
        'privkey', type=str,
        help='Path to the private key for decryption'
    )

    extract_parser.add_argument(
        'extracted', nargs='?', type=str, default=None,
        help='Path to save the extracted secret file '
             '(optional, defaults to the original filename)'
    )
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.command == 'hide':
        hide_file_in_png(args.host, args.secret, args.output, args.pubkey)
    elif args.command == 'extract':
        output_file_path = args.extracted if args.extracted else None
        extract_file_from_png(args.carrier, output_file_path, args.privkey)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
