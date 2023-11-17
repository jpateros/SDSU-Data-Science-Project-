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
    df = pd.read_csv('large_amounts_of_data.csv')
    i = 0
    match_df = pd.read_csv("2022_Match_IDs.csv")
    match_ids = match_df["match_id"].iloc[20000:21000]
    while True:
        
        for recent_match in match_ids:
            match_details = api.get_match_info(recent_match)

            if match_details is not None:
                table = data.get_all_current_match_tables(match_details)
            if table is not None:
                if not (table.isna().any().any()) and not(table.shape[1] < 44) and not (recent_match in df[['MatchID']].values):
                    file_path = 'large_amounts_of_data.csv'
                    if os.path.isfile(file_path):
                        # Append the DataFrame to the existing CSV file without overwriting
                        table.to_csv(file_path, index=False, mode='a', header=False)  # Set header=False to avoid writing column headers
                        print(table)
                    else:
                        # If the file doesn't exist, create a new CSV file
                        table.to_csv(file_path, index=False)  
                
def filter_matches(matches_list):
    return list(filter(lambda m: _filter_function(m), matches_list))

def _filter_function(match):
    if match['duration'] < 1000 or match['duration'] > 4200:
        return False
    else:
        return True

if __name__ == "__main__":
    main()