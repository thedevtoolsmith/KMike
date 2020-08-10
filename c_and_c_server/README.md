## **Server Layout and Functionality**
    /initialise => This endpoint generates bitcoin address for each victim
    /decrypt => The ransomware will hit this endpoint after making payment to verify the payment and decrypt the RSA keys

## **File Structure and Explanation**
    c_and_c_server => The command and control server
      |
      |_ asymmetric_encryption.py => Defintions related to RSA 
      |_ db.py => Functions related to database operations
      |_ payment.py => Bitcoin address generation and payment verification
      |_ server.py => The server code with helper functions for decryption
      |_ utils.py => Driver script for processing requests
      |_ validation.py => Validate request parameters

## **Points to note**
* The bitcoin payment verification implements the payment checking logic but returns true irrespective of the payment status for testing.