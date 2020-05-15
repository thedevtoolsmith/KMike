## **Encryption Mechanism**
    Encrypt all user files with AES-256-CBC.
    Random AES key and IV for each file.
    Encrypt AES keys with locally generated public key RSA-2048.
    Encrypt locally generated private key with RSA-2048 common public key.
       

## **File Structure and Explanation**
    |
    |_  ransomware => Ransomware related stuff
    |     |
    |     |_  __init__.py => Make python file a package
    |     |_  __main__.py => Driver file which specifies the files to be encrypted and calls required functions
    |     |_  asymmetric_encryption.py => Contains definitions related to RSA
    |     |_  decrypt_files.py => Has functions which decrypt files and keys 
    |     |_  encrypt_files.py => Has functions which encrypt files and keys
    |     |_  symmetric_encryption.py => Contains defintions related to AES
    |     |_  utils.py => Helper functions needed to perform common tasks
    |
    |_  README.md => Contians general info about the project