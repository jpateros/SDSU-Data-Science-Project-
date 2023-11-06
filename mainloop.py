from OpenDotaAPI import OpenDotaAPI
from DataPreProcess2 import DataPreprocessing
import time
import json 
import pandas as pd

def main(sleep_time = 2):
    api = OpenDotaAPI(verbose= True)
    data = DataPreprocessing()
    recent_matches = filter_matches(api.get_recent_pro_matches())
    df = pd.DataFrame()
    i = 0
    for recent_match in recent_matches:
        time.sleep(sleep_time)
        match_details = api.get_match_info(recent_match['match_id'])
        if match_details is not None:
            table = data.get_all_current_match_tables(match_details)
        
        df = pd.concat([df, table])
        if i % 10 == 0:
            print(df)
        i = i + 1
        if i >= 1000:
            break
            
        # Specify the file path where you want to save the CSV file
    file_path = '1000_matches.csv'

    # Write the DataFrame to a CSV file
    df.to_csv(file_path, index=False)  # Set index=False if you don't want to save the DataFrame's index


def filter_matches(matches_list):
    return list(filter(lambda m: _filter_function(m), matches_list))

def _filter_function(match):
    if match['duration'] < 1000 or match['duration'] > 4200:
        return False
    else:
        return True

if __name__ == "__main__":
    main()