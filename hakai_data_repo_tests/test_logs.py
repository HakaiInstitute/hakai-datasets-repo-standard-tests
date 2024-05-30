import logging
import unittest
from glob import glob

import pandas as pd

logger = logging.getLogger(__name__)
instrument_log_mandatory_variables = ["instrument_sn", "instrument_model"]
station_log_mandatory_variables = ["station", "latitude", "longitude"]


def read_logs(log_path):
    logs = glob(log_path)
    if logs:
        return pd.read_csv(logs[0])


def review_mandatory_variables(df, mandatory_variables):
    missing_variables = [
        variable for variable in mandatory_variables if variable not in df
    ]
    assert not missing_variables, f"Missing mandatory variables: {missing_variables}"


def review_coordinates(df):
    assert ("latitude" in df and "longitude" in df) or (
        "latitude" not in df and "longitude" not in df
    ), "Missing coordinate variable latitude or longitude"
    if "latitude" in df:
        assert df.query("latitude<-90").empty, "Invalid latitude range below -90"
        assert df.query("latitude>90").empty, "Invalid latitude range above 90"
    if "longitude" in df:
        assert df.query("longitude<-180").empty, "Invalid latitude range above 90"
        assert df.query("latitude>180").empty, "Invalid latitude range above 90"


def review_time_variables(df, time_variables):
    for variable in time_variables:
        if variable not in df:
            continue
        _ = pd.to_datetime(df[variable])


class TestInstrumentLog(unittest.TestCase):
    # Test Data format
    def test_instrument_log_mandatory_variables(self):
        """Test instrument-log.csv file to make sure that the mandatory columns are available"""
        df = read_logs("instrument-log.csv")
        if df is None:
            return
        review_mandatory_variables(df, instrument_log_mandatory_variables)

    def test_instrument_log_time_variables(self):
        """Test instrument-log.csv file by parsing dates"""
        df = read_logs("instrument-log.csv")
        if df is None:
            return
        review_time_variables(df, ["deployment_time", "retrievel_time"])

    def test_instrument_log_coordinates_variables(self):
        """Test instrument-log.csv file and confirm that coordinate variables are in the correct range"""
        df = read_logs("instrument-log.csv")
        if df is None:
            return
        review_coordinates(df)


class TestStationLog(unittest.TestCase):
    def test_station_log_mandatory_variables(self):
        """Test station-log.csv file to make sure that the mandatory columns are available"""
        df = read_logs("station-log.csv")
        if df is None:
            return
        review_mandatory_variables(df, station_log_mandatory_variables)

    def test_station_log_time_variables(self):
        """Test station-log.csv file by parsing dates"""
        df = read_logs("station-log.csv")
        if df is None:
            return
        review_time_variables(df, ["commission_time", "decommissioned_time"])

    def test_station_log_coordinates_variables(self):
        """Test station-log.csv file and confirm that coordinate variables are in the correct range"""
        df = read_logs("station-log.csv")
        if df is None:
            return
        review_coordinates(df)

    def test_station_log_empty_station(self):
        df = read_logs("station-log.csv")
        if df is None:
            return
        assert (
            not df["station"].isna().any()
        ), f"station-log.csv contains rows with no station assigned:\n{df.loc[df['station'].isna()]}"


class TestLogs(unittest.TestCase):
    def test_for_duplicated_columns(self):
        df_instrument = read_logs("instrument-log.csv")
        df_station = read_logs("station-log.csv")
        if df_instrument is None or df_station is None:
            return
        duplicated_columns = set(df_instrument.columns) & set(df_station.columns) - {
            "station",
        }
        assert (
            len(duplicated_columns) == 0
        ), f"Duplicated columns exists between station-log and instrument-log: {duplicated_columns}"
