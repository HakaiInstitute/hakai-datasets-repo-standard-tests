import logging
import unittest
from glob import glob

import pandas as pd

logger = logging.getLogger(__name__)
instrument_log_mandatory_variables = ["instrument_sn", "instrument_model"]
station_log_mandatory_variables = ["station", "latitude", "longitude"]


class TestInstrumentLog(unittest.TestCase):
    def test_instrument_log(self):
        """Test instrument-log.csv file by reading file, parsing dates
        and making sure that the mandatory columns are available"""
        logs = glob(r"instrument-log.csv", recursive=True)
        if not logs:
            return
        # Parse log
        df = pd.read_csv(logs[0])

        # Review mandatory variables
        for var in instrument_log_mandatory_variables:
            if var not in df:
                logger.exception("instrument-log is missing mandatory variable %s", var)

        # Test Data format
        if "deployment_time" in df:
            df["deployment_time"] = pd.to_datetime(df["deployment_time"])

        if "retrieval_time" in df:
            df["retrieval_time"] = pd.to_datetime(df["retrieval_time"])

    def test_station_log(self):
        """Test station-log.csv file by reading file, parsing dates
        and making sure that the mandatory columns are available"""
        logs = glob(r"stations-log.csv")
        if not logs:
            return

        # Parse log
        df = pd.read_csv(logs[0])

        # Review mandatory variables
        for var in station_log_mandatory_variables:
            if var not in df:
                logger.exception("station-log is missing mandatory variable %s", var)

        # Test Data format
        if "commission_time" in df:
            df["commission_time"] = pd.to_datetime(df["commission_time"])

        if "decommissioned_time" in df:
            df["decommissioned_time"] = pd.to_datetime(df["decommissioned_time"])
