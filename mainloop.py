from OpenDotaAPI import OpenDotaAPI
from DataPreProcess import DataPreprocessing
import time
import json 

def main(sleep_time = 2):
    api = OpenDotaAPI(verbose= True)
    data = DataPreprocessing()
    recent_matches = filter_matches(api.get_recent_pro_matches())
    
    for recent_match in recent_matches:
        time.sleep(sleep_time)
        match_details = api.get_match_info(recent_match['match_id'])
        if match_details is not None:
            data.get_all_current_match_tables(match_details)
        # Get previous matches for all players with valid account ids
        # players_with_account = data.players[data.players['account_id'] > 0]
        # for i, player in players_with_account.iterrows():
        #     time.sleep(sleep_time)
        #     full_match_history = api.get_player_matches_history(player['account_id'])
        #     if full_match_history:
        #         data.get_previous_matches(match_details['match_id'], player['account_id'],
        #         full_match_history, match_details['start_time'])
    return data


def filter_matches(matches_list):
    return list(filter(lambda m: _filter_function(m), matches_list))

def _filter_function(match):
    if match['duration'] < 1000 or match['duration'] > 4200:
        return False
    else:
        return True

if __name__ == "__main__":
    main()