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
 [Shutdown some processes before encrypting files to ensure no write lock is present](https://securityaffairs.co/wordpress/103030/malware/sodinokibi-ransomware-new-feature.html)  
 [Get C&C server via unusual mechanism](https://www.zdnet.com/google-amp/article/astaroth-malware-hides-command-servers-in-youtube-channel-descriptions/)

# **Encryption Mechanism**
    encrypt all user files with AES-256-CBC.
    Random AES key and IV for each file.
    encrypt AES keys with locally generated public key RSA-2048.
    encrypt locally generated private key with RSA-2048 common public key.
   
    
    