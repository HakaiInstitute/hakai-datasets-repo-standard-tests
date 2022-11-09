import unittest
import os
import pandas as pd


# Load data dictionary
data_dictionary_path = "data-dictionary.csv"


def read_data_dictionary():
    if os.path.exists(data_dictionary_path):
        return pd.read_csv(data_dictionary_path)


class TestDataDictionary(unittest.TestCase):
    def test_variable_dictionary_readable(self):
        """Try to read the data dictionary if available."""
        df_vars = read_data_dictionary()
        if df_vars is None:
            return
        df_vars = read_data_dictionary()

    def test_variable_dictionary_columns_available(self):
        df_vars = read_data_dictionary()
        if df_vars is None:
            return
        missing_variables = [
            var
            for var in ["variable", "long_name", "units", "standard_name"]
            if var not in df_vars
        ]
        assert (
            not missing_variables
        ), f"{data_dictionary_path} is missing the following variables {missing_variables}"

    def test_variables_units(self):
        pass

    def test_variables_standard_name(self):
        """Review standard_names"""
        df_vars = read_data_dictionary()
        if df_vars is None:
            return
        standard_name_table = "https://cfconventions.org/Data/cf-standard-names/79/src/cf-standard-name-table.xml"
        df_standard_name = pd.read_xml(standard_name_table)
        unmatched_standard_names = [
            standard_name
            for standard_name in df_vars["standard_name"].dropna().to_list()
            if standard_name not in df_standard_name["id"]
        ]
        assert (
            not unmatched_standard_names
        ), f"The following standard_names arent't listed within the standard_name table {standard_name_table}"
