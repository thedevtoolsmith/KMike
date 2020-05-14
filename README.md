# **About**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The (name not decided yet) ransomware is a functional, industrial grade ransomware targeting Windows systems that I have decided to create for learning about the inner workings of ransomware.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It is written in Python, contrary to C or C++ which is supposed to be the languages for malware programming. Frankly, I chose Python because it was too much of a hassle to set up the development environment in my Macbook  

# **Feature List:**
    ~~Encrypt, Decrypt Files~~  
    ~~Delete Original Files~~  
    Show ransom message  
    Auto Payment Verification  
    The ransom note should persist across restarts  
    Privilege escalation  
    Communicate via Tor  
    Sandbox Evasion  
    AV Evasion  
    Obfuscate Code  
    Multithreading/multiprocessing to speed up encryption  
    [`Shutdown some processes before encrypting files to ensure no write lock is present`](https://securityaffairs.co/wordpress/103030/malware/sodinokibi-ransomware-new-feature.html)  
    [`Get C&C server via unusual mechanism`](https://www.zdnet.com/article/astaroth-malware-hides-command-servers-in-youtube-channel-descriptions/)

# **Encryption Mechanism**
    encrypt all user files with AES-256-CBC.
    Random AES key and IV for each file.
    encrypt AES keys with locally generated public key RSA-2048.
    encrypt locally generated private key with RSA-2048 common public key.
   
# **File Structure and Explanation**
    |
    |_ransomware => Ransomware related stuff
    |   |
    |   |_  __init__.py => Make python file a package, no content here
    |   |_  __main__.py => Driver file which specifies the files to be encrypted and calls required functions
    |   |_  asymmetric_encryption.py => Contains definitions related to RSA encryption, key generation, padding and decryption
    |   |_  decrypt_files.py => Has functions which decrypt files and keys 
    |   |_  encrypt_files.py => Has functions which encrypt files and keys
    |   |_  symmetric_encryption.py => Contains defintions related to AES encryption, decryption and padding
    |   |_  utils.py => Helper functions needed to perfrom common tasks
    |
    |_README.md => Contians general info about the project