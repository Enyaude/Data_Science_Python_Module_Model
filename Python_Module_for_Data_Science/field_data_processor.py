# Copy in your class including the ingest_sql_data and  method here
import pandas as pd
from data_ingestion import create_db_engine, query_data, read_from_web_CSV
import logging


### START FUNCTION

class FieldDataProcessor:
    """
    A class for processing field data from various sources.
    """

    def __init__(self, config_params, logging_level="INFO"):  
        """
        Initialize the FieldDataProcessor class.

        Parameters:
        - logging_level (str): The logging level to set for the class. Options are 'DEBUG', 'INFO', 'NONE' (default: 'INFO').
        """
        self.db_path = config_params['db_path']
        self.sql_query = config_params['sql_query']
        self.columns_to_rename = config_params['columns_to_rename']
        self.values_to_rename = config_params['values_to_rename']
        self.weather_map_data = config_params['weather_mapping_csv']

        # Add the rest of your class code here
        self.initialize_logging(logging_level)

        # We create empty objects to store the DataFrame and engine in
        self.df = None
        self.engine = None
        
    # This method enables logging in the class.
    def initialize_logging(self, logging_level):
        """
        Set up logging for the FieldDataProcessor instance.

        Parameters:
        - logging_level (str): The logging level to set for the instance. Options are 'DEBUG', 'INFO', 'NONE'.
        """
        logger_name = __name__ + ".FieldDataProcessor"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False  # Prevents log messages from being propagated to the root logger

        # Set logging level
        if logging_level.upper() == "DEBUG":
            log_level = logging.DEBUG
        elif logging_level.upper() == "INFO":
            log_level = logging.INFO
        elif logging_level.upper() == "NONE":  # Option to disable logging
            self.logger.disabled = True
            return
        else:
            log_level = logging.INFO  # Default to INFO

        self.logger.setLevel(log_level)

        # Only add handler if not already added to avoid duplicate messages
        if not self.logger.handlers:
            ch = logging.StreamHandler()  # Create console handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

        # Use self.logger.info(), self.logger.debug(), etc.


    # let's focus only on this part from now on
    def ingest_sql_data(self):
        """
        Ingest data from an SQL database using the specified SQL query.

        This method connects to the SQL database using the provided database path,
        executes the SQL query to retrieve the data, and assigns the result to the
        DataFrame attribute of the FieldDataProcessor instance.

        Returns:
        - pandas.DataFrame: The DataFrame containing the retrieved data.

        Raises:
        - Exception: If there is an error connecting to the database or executing the query.
        """
        self.engine = create_db_engine(self.db_path)
        self.df = query_data(self.engine, self.sql_query)
        self.logger.info("Sucessfully loaded data.")
        return self.df
    
    def rename_columns(self):
        """
        Rename columns in the DataFrame according to the specified mapping.

        This method renames columns in the DataFrame based on the provided mapping
        stored in the `columns_to_rename` attribute. It temporarily renames one of
        the columns to avoid naming conflicts during the renaming process.

        Returns:
        - None: The DataFrame is modified in place.

        Raises:
        - KeyError: If the columns specified in `columns_to_rename` do not exist in the DataFrame.
        """
        # Extract the columns to rename from the configuration
        column1, column2 = list(self.columns_to_rename.keys())[0], list(self.columns_to_rename.values())[0]       

        # Temporarily rename one of the columns to avoid a naming conflict
        temp_name = "__temp_name_for_swap__"
        while temp_name in self.df.columns:
            temp_name += "_"

        self.logger.info(f"Swapped columns: {column1} with {column2}")

        # Perform the swap
        self.df = self.df.rename(columns={column1: temp_name, column2: column1})
        self.df = self.df.rename(columns={temp_name: column2})

    def apply_corrections(self, column_name='Crop_type', abs_column='Elevation'):
        """
        Apply corrections to specified columns in the DataFrame.

        This method applies corrections to the specified column in the DataFrame.
        It updates the absolute values of the specified column and performs value
        replacement in the specified column based on the mapping provided in
        `values_to_rename` attribute.

        Args:
        - column_name (str): The name of the column to apply value corrections to. Defaults to 'Crop_type'.
        - abs_column (str): The name of the column to compute absolute values for. Defaults to 'Elevation'.

        Returns:
        - None: The DataFrame is modified in place.

        Raises:
        - KeyError: If the column specified in `column_name` or `abs_column` does not exist in the DataFrame.
        """
        self.df[abs_column] = self.df[abs_column].abs()
        self.df[column_name] = self.df[column_name].apply(lambda crop: self.values_to_rename.get(crop, crop))

    def weather_station_mapping(self):
        """
        Read the weather station mapping data from a web CSV file.

        This method reads the weather station mapping data from a CSV file hosted on the web.
        The CSV file contains information about the mapping between field IDs and weather stations.

        Returns:
        - pandas.DataFrame: The DataFrame containing the weather station mapping data.

        Raises:
        - Exception: If there is an error reading the CSV data from the web.
        """
        df = read_from_web_CSV(self.weather_map_data)
        return df
    
    def process(self):
        """
        Process the data by ingesting SQL data, renaming columns, and applying corrections.

        This method orchestrates the data processing pipeline by performing the following steps:
        1. Ingest SQL data: Load data from a SQL database using the provided SQL query.
        2. Rename columns: Rename columns in the DataFrame based on the provided configuration.
        3. Apply corrections: Apply corrections to specific columns in the DataFrame.

        This method should be called after initializing the object and configuring necessary parameters.

        Returns:
        - None

        """
        self.ingest_sql_data()
        self.rename_columns()
        self.apply_corrections()
        
### END FUNCTION