import os
import shutil
import toml
from cryptography.fernet import Fernet
import zipfile

def generate_key():
    """Generate and save a key for encryption."""
    key = Fernet.generate_key()
    with open('compl_dist/secret.key', 'wb') as key_file:
        key_file.write(key)
    return key

def load_key(file_path):
    """Load the previously generated key."""
    return open(file_path, 'rb').read()

def encrypt_file(file_path, key):
    """Encrypt a file using the given key."""
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def archive(config_file):
    """Pack files into a custom encrypted archive based on TOML config."""
    config = toml.load(config_file)
    archive_name = config['archive']['name']
    if not archive_name.endswith('.compl'):
        archive_name += '.compl'
    
    # Ensure compl_dist directory exists
    if not os.path.exists('compl_dist'):
        os.makedirs('compl_dist')

    # Generate or load encryption key
    if not os.path.exists('compl_dist/secret.key'):
        key = generate_key()
        print("Encryption key created and saved as 'compl_dist/secret.key'.")
    else:
        key = load_key('compl_dist/secret.key')
        print("Using existing encryption key from 'compl_dist/secret.key'.")

    # Create temporary directory to hold files
    temp_dir = 'temp_archive'
    os.makedirs(temp_dir, exist_ok=True)

    # Copy files and folders to the temporary directory
    for file_entry in config['files']:
        path = file_entry['path']
        if path:
            if os.path.isfile(path):
                shutil.copy(path, temp_dir)
                encrypt_file(os.path.join(temp_dir, os.path.basename(path)), key)
            elif os.path.isdir(path):
                shutil.copytree(path, os.path.join(temp_dir, os.path.basename(path)))
                for root, _, files in os.walk(os.path.join(temp_dir, os.path.basename(path))):
                    for file in files:
                        encrypt_file(os.path.join(root, file), key)

    # Create the temporary zip archive
    temp_archive_name = f'{archive_name}.zip'
    shutil.make_archive(temp_archive_name.replace('.zip', ''), 'zip', temp_dir)

    # Rename the zip archive to .compl and move it to compl_dist
    os.rename(temp_archive_name, os.path.join('compl_dist', archive_name))
    
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    
    print(f"Archive created successfully: compl_dist/{archive_name}")
    print(f"Encryption key is stored in 'compl_dist/secret.key'.")

def decrypt_file(file_path, key):
    """Decrypt a file using the given key."""
    fernet = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

def decrypt_archive(key_file, archive_file, destination):
    """Decrypt and extract a custom encrypted archive based on the key."""
    key = load_key(key_file)
    
    # Ensure destination directory exists
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Extract the .compl archive
    temp_dir = 'temp_extracted'
    os.makedirs(temp_dir, exist_ok=True)
    
    with zipfile.ZipFile(archive_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Decrypt the files
    for root, _, files in os.walk(temp_dir):
        for file in files:
            decrypt_file(os.path.join(root, file), key)
    
    # Move the decrypted files to the destination
    for file_name in os.listdir(temp_dir):
        shutil.move(os.path.join(temp_dir, file_name), os.path.join(destination, file_name))

    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    
    print(f"Archive extracted and decrypted successfully to '{destination}'.")