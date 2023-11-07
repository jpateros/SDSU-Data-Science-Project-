from OpenDotaAPI import OpenDotaAPI
from DataPreProcess2 import DataPreprocessing
import time
import json 
import pandas as pd
import os 

def main(sleep_time = 2):
    api = OpenDotaAPI(verbose= True)
    data = DataPreprocessing()
    # recent_matches = filter_matches(api.get_recent_pro_matches())
    df = pd.DataFrame()
    i = 0
    for i in range(1,10):
        recent_matches = filter_matches(api.get_recent_pro_matches())
        for recent_match in recent_matches:
            time.sleep(sleep_time)
            match_details = api.get_match_info(recent_match['match_id'])
            if match_details is not None:
                i = i + 1
                table = data.get_all_current_match_tables(match_details)
                
            if not (table.isna().any().any()) and not(table.shape[1] < 44):
                file_path = 'large_amounts_of_data.csv'
                if os.path.isfile(file_path):
                    # Append the DataFrame to the existing CSV file without overwriting
                    table.to_csv(file_path, index=False, mode='a', header=False)  # Set header=False to avoid writing column headers
                else:
                    # If the file doesn't exist, create a new CSV file
                    table.to_csv(file_path, index=False)  
                print(table)
            if i >= 10000:
                break

def filter_matches(matches_list):
    return list(filter(lambda m: _filter_function(m), matches_list))

def _filter_function(match):
    if match['duration'] < 1000 or match['duration'] > 4200:
        return False
    else:
        return True

if __name__ == "__main__":
    main()