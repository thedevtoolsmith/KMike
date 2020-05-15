## **NAME NOT DECIDED**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The (name not decided yet) ransomware is a functional, industrial grade ransomware targeting Windows systems that I have decided to create for learning about the inner workings of ransomware.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It is written in Python, contrary to C or C++ which is supposed to be the languages for malware programming.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Python was chosen because it was too much of a hassle to set up the C development environment in my Macbook and I have no intention of deploying the malware, so the performance and size do not matter.   


## **Getting Started**
Instructions on how to go about setting up in your local machine  

### Prerequistes
To be filled

### Installing/Building
To be filled


## **Feature List:**
 * ~~Encrypt, Decrypt Files~~  
 * ~~Delete Original Files~~  
 * Show ransom message  
 * Auto Payment Verification  
 * The ransom note should persist across restarts  
 * Make the python code into an executable
 * Privilege escalation  
 * Communicate via Tor  
 * Sandbox Evasion  
 * AV Evasion  
 * Obfuscate Code  
 * Multithreading/multiprocessing to speed up encryption  
 * [`Shutdown some processes before encrypting files to ensure no write lock is present`](https://securityaffairs.co/wordpress/103030/malware/sodinokibi-ransomware-new-feature.html)  
 * [`Get C&C server via unusual mechanism`](https://www.zdnet.com/article/astaroth-malware-hides-command-servers-in-youtube-channel-descriptions/)
 

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


## **License**
    The project at this time is not allowed to be modified or used by anyone
      

## **Acknowledgments**
 * [Encryption Scheme - Tarcísio Marinho](https://medium.com/@tarcisioma/ransomware-encryption-techniques-696531d07bb9)  
   ```
   This blog post helped me with deciding the encryption scheme used and the accompanying repo helped me with solving the problem of encrypting the locally generated RSA public key   
   ```