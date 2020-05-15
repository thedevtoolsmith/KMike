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


## **License**
    The project at this time is not allowed to be modified or used by anyone
      

## **Acknowledgments**
 * [Encryption Scheme - Tarcísio Marinho](https://medium.com/@tarcisioma/ransomware-encryption-techniques-696531d07bb9)  
   ```
   This blog post helped me with deciding the encryption scheme used and the accompanying repo helped me with solving the problem of encrypting the locally generated RSA public key   
   ```