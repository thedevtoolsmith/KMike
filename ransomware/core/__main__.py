import logging
from core.gui import start_menu

logging.basicConfig(
    format="%(asctime)s %(module)s %(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# TODO: Add explicit garbage collection
# TODO: Show proper error messages in GUI

def main():
    app = start_menu.tkinterApp() 
    app.mainloop()


if __name__ == "__main__":
    main()
    
