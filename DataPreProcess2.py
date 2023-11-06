import pandas as pd

class DataPreprocessing():
    def __init__(self):
        # Initialize tables as empty dataframes
        # TODO: change these to become empty dictionaries
        # then at the end condense everything into a dataframe
        # self.items_selected = pd.DataFrame()
        # self.draft_timings = pd.DataFrame()
        # self.teams = pd.DataFrame()
        # self.lane_position = pd.DataFrame()
        self.dict_of_dict = {}
        self.list_of_dictionaries = []

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
            
            
    def get_draft_timings(self, match):
        """get the order of heroes picked in a match"""

        timings = match['draft_timings']
        timings = self.clean_draft_timings(timings)
        print("############### Draft Timings")
        heroes = []
        if timings is not None:
            for item in timings:
                heroes.append(item["hero_id"]) 
    
        for index, id in enumerate(heroes):
            self.dict_of_dict[id].update({"Time" : index})
        print(self.dict_of_dict)
        
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
                team_dict[hero_id] = int(player["isRadiant"])
        
        self.dict_of_dict =  {key: {"Team": value} for key, value in team_dict.items()}
        
            
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

                """
                import pandas as pd

                # Define the data for the columns
                data = {
                    'Column1': [1, 2, 3, 4, 5],
                    'Column2': ['A', 'B', 'C', 'D', 'E'],
                    'Column3': [10.1, 20.2, 30.3, 40.4, 50.5]
                }
                data = [
                row 1: {"hero_id": 123, "team": True, "order": 0, "lane": 1}, etc. 
                row 2: {"hero_id": 123, "team": True, "order": 0, "lane": 1},
                ]

                1. First insert all heros id into 10 different dictionarys
                2. Name the dictionary by hero id
                3. Go into the dicitonary with that hero id and insert the rest of the items
                4. Append to the lists when done 

                5. Erase old dictionaries when finishing an entire match
                6. Loop again


                # Create the dataframe
                df = pd.DataFrame(data)

                # Print the dataframe
                print(df)

                """