import argparse
from compilemaster.index import archive, decrypt_archive

def main():
    parser = argparse.ArgumentParser(description='Pack files into a custom encrypted archive or unpack an existing one.')
    parser.add_argument('-b', '--build', help='Path to the TOML configuration file', required=False)
    parser.add_argument('-e', '--key', help='Path to the encryption key file', required=False)
    parser.add_argument('-f', '--file', help='Path to the custom archive file (for extraction)', required=False)
    parser.add_argument('-d', '--destination', help='Path to the folder where the archive should be extracted', default='.')
    args = parser.parse_args()

    if args.build:
        archive(args.build)
    elif args.key and args.file:
        decrypt_archive(args.key, args.file, args.destination)
    else:
        print("Error: You must provide both -e (key) and -f (file) arguments to decrypt an archive.")
        print("Or provide -b (build) argument to create a new archive.")

if __name__ == "__main__":
    main()
