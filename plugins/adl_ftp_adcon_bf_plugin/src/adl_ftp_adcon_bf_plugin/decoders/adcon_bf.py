import logging

import pandas as pd
from adl_ftp_plugin.registries import FTPDecoder
from adl_ftp_plugin.utils import get_dates_to_now

logger = logging.getLogger(__name__)


class AdconBFDecoder(FTPDecoder):
    """
    This class represents a decoder for the Adcon data format.
    """
    
    type = "adcon_bf"
    compat_type = "adcon_bf"
    display_name = "ADCON FTP Burkina Faso"
    
    def get_matching_files(self, station_link, files):
        # get all the initial matching files
        matching_files = super().get_matching_files(station_link, files)
        
        # get the dates we need to check
        dates = get_dates_to_now(date_granularity=station_link.date_granularity,
                                 timezone=station_link.timezone,
                                 from_date=station_link.start_date,
                                 as_string=True,
                                 str_format="%Y%m%d")
        
        # sample filename 0-854-0-004-20250216.txt
        # filter the matching files by date
        matching_files = [file for file in matching_files if any(date in file for date in dates)]
        
        return matching_files
    
    def decode(self, file_path):
        df = pd.read_csv(file_path, delimiter="\t", decimal=",", dtype={"Heure": str})
        
        non_data_val_cols = ["Code station", "Date", "Heure"]
        
        # convert non-date columns to float
        for column in df.columns:
            if column not in non_data_val_cols:
                df[column] = df[column].astype(str).str.replace(',', '.', regex=False)
                df[column] = pd.to_numeric(df[column], errors='coerce')
        
        # convert date and time columns to datetime
        
        # date format like 20251702
        date_time_str = df["Date"].astype(str) + df["Heure"].astype(str)
        
        df["TIMESTAMP"] = pd.to_datetime(date_time_str, format="%Y%d%m%H%M")
        df = df.where(pd.notna(df), None)
        
        records = df.to_dict(orient="records", )
        
        return {
            "values": records
        }
