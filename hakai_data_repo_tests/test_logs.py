import logging
import unittest
from glob import glob

import pandas as pd

logger = logging.getLogger(__name__)
instrument_log_mandatory_variables = ["instrument_sn", "instrument_model"]
station_log_mandatory_variables = ["station", "latitude", "longitude"]

def review_mandatory_variables(df,mandatory_variables):
    missing_variables = [variable for variable in mandatory_variables if variable not in df]
    assert not missing_variables, f"Missing mandatory variables: {missing_variables}"


def review_coordinates(df):
    assert "latitude" in df and "longitude" in df, "Missing coordinate variable latitude or longitude"
    if "latitude" in df:
        assert df.query("latitude<-90").empty, "Invalid latitude range below -90"
        assert df.query("latitude>90").empty, "Invalid latitude range above 90"
    if "longitude" in df:
        assert df.query("longitude<-180").empty, "Invalid latitude range above 90"
        assert df.query("latitude>180").empty, "Invalid latitude range above 90"
    

def review_time_variables(df,time_variables):
    for variable in time_variables:
        if variable not in df:
            continue
        _ = pd.to_datetime(df[variable])

class TestInstrumentLog(unittest.TestCase):
    
    def test_instrument_log(self):
        """Test instrument-log.csv file by reading file, parsing dates
        and making sure that the mandatory columns are available"""
        logs = glob(r"instrument-log.csv", recursive=True)
        if not logs:
            return
        # Parse log
        df = pd.read_csv(logs[0])

        # Test Data format
        review_mandatory_variables(df,instrument_log_mandatory_variables)
        review_time_variables(df,["deployment_time",'retrievel_time'])
        review_coordinates(df)

    def test_station_log(self):
        """Test station-log.csv file by reading file, parsing dates
        and making sure that the mandatory columns are available"""
        logs = glob(r"station-log.csv")
        if not logs:
            return

        # Parse log
        df = pd.read_csv(logs[0])

        # Review mandatory variables
        review_mandatory_variables(df,station_log_mandatory_variables)
        review_time_variables(df,['commission_time','decommissioned_time'])
        review_coordinates(df)
