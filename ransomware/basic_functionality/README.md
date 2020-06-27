## **Encryption Mechanism**
    Encrypt all user files with AES-256-CBC.
    Random AES key and IV for each file.
    Encrypt AES keys with locally generated public key RSA-2048.
    Encrypt locally generated private key with RSA-2048 common public key.
       

## **File Structure and Explanation**
    basic_functionality => Encryption and Decryption related code
      |
      |_  __init__.py => Make python file a package
      |_  __main__.py => Driver file which specifies the files to be encrypted and calls required functions
      |_  asymmetric_encryption.py => Contains definitions related to RSA
      |_  comms.py => Has functions to communicate with the C&C server
      |_  decrypt_files.py => Has functions which decrypt files and keys 
      |_  encrypt_files.py => Has functions which encrypt files and keys
      |_  symmetric_encryption.py => Contains defintions related to AES
      |_  utils.py => Helper functions needed to perform common tasks

## **Points to note**
* The details such as file_path and AES initialization vector are base64 encoded before being written to disk because I ran into some exceptions while trying to store them as they were.
* The encrypted local private key is being sent as a base64 encoded string because bytes are not JSON serializable.
* All the base64 encoded data will be bytes, so the conversion to ASCII needs to be done before getting them as strings. ASCII was chosen because the `b64decode()` functioncan handle ASCII strings by default.
* The `encrypted_file_path` key in the dictionary in `encrypt_files()` utf-8 encoding happens because b64encode accepts only byte objects.