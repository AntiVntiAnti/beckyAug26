from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import os
import shutil
from typing import List, Union
import tracker_config as tkc
from logger_setup import logger

user_dir = os.path.expanduser('~')
db_path = os.path.join(os.getcwd(), tkc.DB_NAME)  # Database Name
target_db_path = os.path.join(user_dir, tkc.DB_NAME)  # Database Name


def initialize_database() -> None:
    """
    Initializes the database by creating a new database file or copying an existing one.

    If the target database file doesn't exist, it checks if the source database file exists.
    If the source database file exists, it copies it to the target location.
    If the source database file doesn't exist, it creates a new database file using the 'QSQLITE' driver.

    Returns:
        None

    Raises:
        Exception: If there is an error creating or copying the database file.
    """
    try:
        if not os.path.exists(target_db_path):
            if os.path.exists(db_path):
                shutil.copy(db_path, target_db_path)
            else:
                db: QSqlDatabase = QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName(target_db_path)
                if not db.open():
                    logger.error("Error: Unable to create database")
                db.close()
    except Exception as e:
        logger.error("Error: Unable to create database", str(e))


class DataManager:
    
    def __init__(self,
                 db_name: str = target_db_path) -> None:
        """
        Initializes the DataManager object and opens the database connection.

        Args:
            db_name (str): The path to the SQLite database file.

        Raises:
            Exception: If there is an error opening the database.

        """
        try:
            self.db: QSqlDatabase = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(db_name)
            
            if not self.db.open():
                logger.error("Error: Unable to open database")
            logger.info("DB INITIALIZING")
            self.query: QSqlQuery = QSqlQuery()
            self.setup_tables()
        except Exception as e:
            logger.error(f"Error: Unable to open database {e}", exc_info=True)
    
    def setup_tables(self) -> None:
        """
        Sets up the necessary tables in the database.

        This method calls the setup_beck_table_aug_8() and setup_altman_table() methods to create the required tables in the database.
        """
        self.setup_beck_table_aug_8()

    def setup_beck_table_aug_8(self) -> None:
        """
        Sets up the 'beck_table_aug_8' in the database if it doesn't already exist.

        This method creates a table named 'beck_table_aug_8' in the database with the following columns:
        - id: INTEGER (Primary Key, Autoincrement)
        - beck_date: TEXT
        - beck_time: TEXT
        - sadness: INTEGER
        - outlook: INTEGER
        - guilt: INTEGER
        - solitude: INTEGER
        - hygiene: INTEGER
        - decisiveness: INTEGER
        - effort: INTEGER
        - interest: INTEGER
        - pessimism: INTEGER
        - victimhood: INTEGER
        - sleep: INTEGER
                
        If the table already exists, this method does nothing.

        Returns:
            None
        """
        if not self.query.exec(f"""
                        CREATE TABLE IF NOT EXISTS beck_table_aug_8 (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        beck_date TEXT,
                        beck_time TEXT,
                        b_slider INTEGER,
                        b_slider_2 INTEGER,
                        b_slider_3 INTEGER,
                        b_slider_4 INTEGER,
                        b_slider_5 INTEGER,
                        b_slider_6 INTEGER,
                        b_slider_7 INTEGER,
                        b_slider_8 INTEGER,
                        b_slider_9 INTEGER,
                        b_slider_10 INTEGER,
                        b_slider_11 INTEGER,
                        b_slider_12 INTEGER,
                        b_slider_13 INTEGER,
                        b_slider_14 INTEGER,
                        b_slider_15 INTEGER,
                        b_slider_16 INTEGER,
                        b_slider_17 INTEGER,
                        b_slider_18 INTEGER,
                        b_slider_19 INTEGER,
                        b_slider_20 INTEGER,
                        b_slider_21 INTEGER,
                        beck_summary INTEGER
                        )"""):
            logger.error(f"Error creating table: beck_table_aug_8",
                         self.query.lastError().text())
    
    def insert_into_beck_table_aug_8(self,
                               beck_date: str,
                               beck_time: str,
                               b_slider: int,
                               b_slider_2: int,
                               b_slider_3: int,
                               b_slider_4: int,
                               b_slider_5: int,
                               b_slider_6: int,
                               b_slider_7: int,
                               b_slider_8: int,
                               b_slider_9: int,
                               b_slider_10: int,
                               b_slider_11: int,
                               b_slider_12: int,
                               b_slider_13: int,
                               b_slider_14: int,
                               b_slider_15: int,
                               b_slider_16: int,
                               b_slider_17: int,
                               b_slider_18: int,
                               b_slider_19: int,
                               b_slider_20: int,
                               b_slider_21: int,
                               beck_summary: int
                               ) -> None:
        sql: str = f"""INSERT INTO beck_table_aug_8(
        beck_date, beck_time, b_slider, b_slider_2, b_slider_3, b_slider_4, b_slider_5, b_slider_6,
        b_slider_7, b_slider_8, b_slider_9, b_slider_10, b_slider_11, b_slider_12,
        b_slider_13, b_slider_14, b_slider_15, b_slider_16, b_slider_17, b_slider_18,
        b_slider_19, b_slider_20, b_slider_21, beck_summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        bind_values: List[Union[str, int]] = [
            beck_date, beck_time, b_slider, b_slider_2, b_slider_3, b_slider_4, b_slider_5, b_slider_6,
            b_slider_7, b_slider_8, b_slider_9, b_slider_10, b_slider_11, b_slider_12,
            b_slider_13, b_slider_14, b_slider_15, b_slider_16, b_slider_17, b_slider_18,
            b_slider_19, b_slider_20, b_slider_21, beck_summary
        ]
        try:
            self.query.prepare(sql)
            for value in bind_values:
                self.query.addBindValue(value)
            if sql.count('?') != len(bind_values):
                raise ValueError(f"""Mismatch: beck_table_aug_8 Expected {sql.count('?')}
                    bind values, got {len(bind_values)}.""")
            if not self.query.exec():
                logger.error(
                    f"Error inserting data: beck_table_aug_8 - {self.query.lastError().text()}")
        except ValueError as e:
            logger.error(f"ValueError beck_table_aug_8: {e}")
        except Exception as e:
            logger.error(f"Error during data insertion: beck_table_aug_8 {e}", exc_info=True)


def close_database(self) -> None:
    """
    Closes the database connection if it is open.

    This method checks if the database connection is open and closes it if it is.
    If the connection is already closed or an error occurs while closing the
    connection, an exception is logged.

    Raises:
        None

    Returns:
        None
    """
    try:
        logger.info("if database is open")
        if self.db.isOpen():
            logger.info("the database is closed successfully")
            self.db.close()
    except Exception as e:
        logger.exception(f"Error closing database: {e}")
