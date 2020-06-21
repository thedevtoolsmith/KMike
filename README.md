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
 * Basic Funcionality
    * ~~Encrypt, Decrypt Files~~  
    * ~~Delete Original Files~~
    * Show ransom message
    * Make the python code into an executable
 * Write a C&C server
    * Auto Payment Verification
    * Communicate via Tor
 * Evasion Techniques
    * Sandbox Evasion  
    * AV Evasion  
    * Obfuscate Code
 * Nice-to-have Features
    * Privilege escalation     
    * The ransom note should persist across restarts  
    * Multithreading/multiprocessing to speed up encryption
    * [`Get C&C server via unusual mechanism`](https://www.zdnet.com/article/astaroth-malware-hides-command-servers-in-youtube-channel-descriptions/)  
    * [`Shutdown some processes before encrypting files to ensure no write lock is present`](https://securityaffairs.co/wordpress/103030/malware/sodinokibi-ransomware-new-feature.html)  
 


## **License**
    The project is distributed under GNU GPL 3.0
      

## **Acknowledgments**
 * [Encryption Scheme - Tarcísio Marinho](https://medium.com/@tarcisioma/ransomware-encryption-techniques-696531d07bb9)  
   ```
   This blog post helped me with deciding the encryption scheme used and the accompanying repo helped me with solving the problem of encrypting the locally generated RSA public key   
   ```