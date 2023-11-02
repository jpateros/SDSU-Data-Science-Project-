import pandas as pd

class DataPreprocessing():
    def __init__(self):
        # Initialize tables as empty dataframes
        self.items_selected = pd.DataFrame()
        self.draft_timings = pd.DataFrame()
        self.teams = pd.DataFrame()
        self.lane_position = pd.DataFrame()

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
            print("########################### ITEMS SELECTED")
            print(self.items_selected)
            self.items_selected.to_csv("data.csv")
            
            self.lane_position = self.lane_position._append(pd.DataFrame(hero_lane_dict, index=[0]), ignore_index=True)
            print('############################# LANE POSITIONS')
            print(self.lane_position)
    def get_draft_timings(self, match):
        """get the order of heroes picked in a match"""

        timings = match['draft_timings']
        timings = self.clean_draft_timings(timings)
        print("############### Draft Timings")
        heroes = []
        if timings is not None:
            for item in timings:
                heroes.append(item["hero_id"]) 
        self.draft_timings = self.draft_timings._append(pd.DataFrame(heroes), ignore_index=True)
        print(self.draft_timings)
        # return heroes

    def clean_draft_timings(self, timings):
        retval = []
        if timings is not None:
            for item in timings:
                if item['pick'] == True:
                    retval.append(item)
            return retval
    
    def get_teams(self, match):
        players = match["players"]
        team_dict = {}
        if match is not None:
            for player in players:
                hero_id = player["hero_id"]
                team_dict[hero_id] = player["isRadiant"]
        # print('############ Team dictionary')
        # print(team_dict)

        self.teams = self.teams._append(pd.DataFrame([team_dict]), ignore_index=True)
        print('############ Team dictionary')
        print(self.teams)
        # return team_dict
            
    def get_all_current_match_tables(self, match_details):
            """ Get all tables from a current match, except the previous matches. """
            if match_details is not None:
                # self.get_match(match_details)
                self.get_teams(match_details)
                self.get_draft_timings(match_details)
                self.get_hero_starting_items_lane(match_details)


                """
                        hero id | team | order | lane | item 1 | item 2| ... | item 12
                row 1   123       true   0       1
                row 2
                row 3
                row 4
                row 5
                row 6
                ...
                row 10 
                """