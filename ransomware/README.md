## Installation
**Setup the server before running the ransomware**  
The project can be run in Python 3.6 and above.

Clone the repository
```
git clone https://github.com/Suryak-5328/KMike.git
```

Navigate to the c_and_c_server folder in the cloned repository
```
cd KMike/ransomware
```

[Create a python virtual environment](https://docs.python.org/3/tutorial/venv.html)
```
python -m venv venv
```

Activate the virtual environment
```
source venv/bin/activate
```

Install the required packages 
```
pip install -r requirements.txt
```

## Building the exe
To be filled

## Usage
Run the program
```
python -m core
```

## **Encryption Mechanism**
    Encrypt all user files with AES-256-CBC.
    Random AES key and IV for each file.
    Encrypt AES keys with locally generated public key RSA-2048.
    Encrypt locally generated private key with RSA-2048 common public key.
       

## **File Structure and Explanation**
    ransomware => Ransomware code
      |
      |_ executable.py => Entrypoint for making code into executable
      |_ core => Ransomware code
          |
          |_ comms => Server communication code
              |
              |_ bitcoin_address.py => Sends request for bitcoin address generation to the server after encryption
              |_ cnc_generator.py => Generates a list of domains for communication
              |_ decrypt.py => Sends request to verify payment and decrypt data
          |
          |_ crypto => Definitions related to encryption and decryption
              |
              |_ asymmetric_encryption.py => Contains definitions related to RSA
              |_ symmetric_encryption.py => Contains defintions related to AES
          |
          |_ gui => GUI related stuff
              |
              |_ start_menu.py => Definitions related to GUI windows
          |
          |_ utils => Helper functions needed to perform common tasks
              |
              |_ file_ops.py => File read write operations
              |_ generators.py => Generates RSA key pair and client ID
              |_ statistics.py => Collects various statistics about the infected machine
          |
          |_ __main__.py => Driver file which specifies the files to be encrypted and calls required functions
          |_ decrypt_files.py => Has functions which decrypt files and keys 
          |_ encrypt_files.py => Has functions which encrypt files and keys


## **Points to note**
* The details such as file_path and AES initialization vector are base64 encoded before being written to disk because I ran into some exceptions while trying to store them as they were.
* The encrypted local private key is being sent as a base64 encoded string because bytes are not JSON serializable.
* All the base64 encoded data will be bytes, so the conversion to ASCII needs to be done before getting them as strings. ASCII was chosen because the `b64decode()` functioncan handle ASCII strings by default.
* The `encrypted_file_path` key in the dictionary in `encrypt_files()` utf-8 encoding happens because b64encode accepts only byte objects.
* Some of the file encryption details are split into parts, encrypted and stored in a list when they are too large to be encrypted as a whole.