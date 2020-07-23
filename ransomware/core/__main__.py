import logging
from core.gui import start_menu

logging.basicConfig(
    format="%(asctime)s %(module)s %(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# TODO: Find a better way to store the configuration variables
# TODO: Solve the relative path issue while acessing files
# TODO: Add exception handling
# TODO: Implement Windows file traversal logic
# TODO: Add explicit garbage collection
# TODO: Add double encryption protection


def main():
    app = start_menu.tkinterApp() 
    app.mainloop()


if __name__ == "__main__":
    main()
    
