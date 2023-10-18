import pandas as pd

class DataPreprocessing():
    def __init__(self):
        # Initialize tables as empty dataframes
        self.items_selected = pd.DataFrame()

    def get_hero_starting_items_lane(self, match):
        hero_items_dict = {}
        players = match["players"]
        hero_lane_dict = {}    
        if match is not None:
            for player in players:
                purchase_log = player["purchase_log"]
                pre_game_items = []
                if purchase_log is not None:
                    for items in purchase_log:
                        if items["time"] < 0:
                            pre_game_items.append(items["key"])
                        
                    hero_id = player["hero_id"]
                    hero_items_dict[hero_id] = pre_game_items
                    hero_lane_dict[hero_id] = player["lane"]
            
            # Find the maximum length of the item lists
            max_length = max(len(lst) for lst in hero_items_dict.values())
            
            # Fill missing values with None
            hero_items_dict = {k: v + [None] * (max_length - len(v)) for k, v in hero_items_dict.items()}
            
            # Create the DataFrame
            df = pd.DataFrame.from_dict(hero_items_dict, orient='index').fillna('')

            # Reset the index
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'hero_id'}, inplace=True)

            self.items_selected = self.items_selected._append(df, ignore_index=True)
            
            print(self.items_selected)
            self.items_selected.to_csv("data.csv")
            
            
    def get_all_current_match_tables(self, match_details):
            """ Get all tables from a current match, except the previous matches. """
            if match_details is not None:
                # self.get_match(match_details)
                # self.get_draft_timings(match_details)
                self.get_hero_starting_items_lane(match_details)