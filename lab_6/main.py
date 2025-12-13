import argparse

from crypto_system import HybridCryptoSystem
from work_file import *


def main():
    paths = read_json("settings.json")

    main_parser = argparse.ArgumentParser()
    group = main_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", help="key generation mode", nargs='?', const=32, default=None, type=int,
                       choices=[16, 24, 32])
    group.add_argument("-enc", "--encryption", help="encryption mode", action="store_true")
    group.add_argument("-dec", "--decryption", help="decryption mode", action="store_true")

    main_parser.add_argument("--symmetric-key", help="path to symmetric key", default=paths["symmetric_key"])
    main_parser.add_argument("--secret-key", help="path to secret key", default=paths["secret_key"])
    main_parser.add_argument("--public-key", help="path to public key", default=paths["public_key"])

    args = main_parser.parse_args()

    args.generation_flag = args.generation is not None

    if args.generation_flag and args.generation is None:
        args.generation = 32

    match (args.generation_flag, args.encryption, args.decryption):
        case (True, False, False):
            key_size = args.generation
            h = HybridCryptoSystem(args.symmetric_key, args.secret_key, args.public_key)
            h.generate_keys(key_size)
        case (False, True, False):
            h = HybridCryptoSystem(args.symmetric_key, args.secret_key, args.public_key)
            h.encrypt(paths["initial_file"], paths["encrypted_file"])
        case (False, False, True):
            h = HybridCryptoSystem(args.symmetric_key, args.secret_key, args.public_key)
            h.decrypt(paths["encrypted_file"], paths["decrypted_file"])


if __name__ == '__main__':
    main()