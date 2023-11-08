import pandas as pd

class DataPreprocessing():
    def __init__(self):
        self.dict_of_dict = {}
        self.list_of_dictionaries = []
        self.match_id = None
        self.valid_df = True
    
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
            
            max_length = 0  # Initialize max_length to 0

            for lst in hero_items_dict.values():
                if lst:  # Check if the list is not empty
                    max_length = max(max_length, len(lst))

            # Now you can fill missing values with None
            hero_items_dict = {k: v + [None] * (max_length - len(v)) for k, v in hero_items_dict.items()}
            
            for key in hero_lane_dict:
                if hero_lane_dict[key] == None:
                    self.valid_df = False
                self.dict_of_dict[key].update({"Lane" : hero_lane_dict[key]})
            
            # print(hero_items_dict)
            for key in hero_items_dict:
                self.dict_of_dict[key].update({
                                            "smoke_of_deceit" : 0,
                                            "boots" : 0,
                                            "flask" : 0,
                                            "blood_grenade" : 0,
                                            "clarity" : 0,
                                            "enchanted_mango" : 0,
                                            "branches" : 0,
                                            "magic_stick" : 0,
                                            "faerie_fire" : 0,
                                            "circlet" : 0,
                                            "gauntlets" : 0,
                                            "ward_observer" : 0,
                                            "tango" : 0,
                                            "ward_sentry" : 0,                                            
                                            "slippers" : 0,
                                            "quelling_blade" : 0,
                                            "ring_of_protection" : 0,
                                            "magic_wand" : 0,
                                            "mantle" : 0,
                                            "crown" : 0,
                                            "chainmail" : 0,
                                            "blight_stone" : 0,
                                            "robe" : 0,
                                            "wraith_band" : 0,
                                            "gloves" : 0,
                                            "infused_raindrops" : 0,
                                            "blades_of_attack" : 0,
                                            "orb_of_venom" : 0,
                                            "tpscroll" : 0,
                                            "fluffy_hat" : 0,
                                            "ring_of_regen" : 0,
                                            "sobi_mask" : 0,
                                            "null_talisman" : 0,
                                            "buckler" : 0,
                                            "headdress" : 0,
                                            "ring_of_basilius" : 0,
                                            "wind_lace" : 0,
                                            "boots_of_elves" : 0,
                                            "dust" : 0,
                                            "bracer" : 0
                                        })
                if hero_items_dict[key] is not None:
                    for index, item in enumerate(hero_items_dict[key]):
                        if item is not None:
                            value = self.dict_of_dict[key][item] + 1     
                            if item == None:
                                self.valid_df = False                   
                            self.dict_of_dict[key].update({item : value})
                
    def get_draft_timings(self, match):
        """get the order of heroes picked in a match"""

        timings = match['draft_timings']
        timings = self.clean_draft_timings(timings)
        # print("############### Draft Timings")
        heroes = []
        if timings is not None:
            for item in timings:
                heroes.append(item["hero_id"]) 
    
        for index, id in enumerate(heroes):
            self.dict_of_dict[id].update({"Order" : index})
            if index == None:
                self.valid_df = False
        # print(self.dict_of_dict)
        for key in self.dict_of_dict:
            self.dict_of_dict[key].update({"MatchID" : self.match_id})
        
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
        self.dict_of_dict =  {key: {"Hero ID": key} for key, value in team_dict.items()}
        for key in self.dict_of_dict:
            self.dict_of_dict[key].update({"Team": team_dict[key]})
        
            
    def get_all_current_match_tables(self, match_details):
        """ Get all tables from a current match, except the previous matches. """
        if match_details is not None:
            self.match_id = match_details["match_id"]
            # self.get_match(match_details)
            self.get_teams(match_details)
            self.get_draft_timings(match_details)
            self.get_hero_starting_items_lane(match_details)
            # print(self.dict_of_dict)
            return self.create_data_frame()

    def create_data_frame(self):
        first_key = list(self.dict_of_dict.keys())[0]
        first_dict = self.dict_of_dict[first_key]

        df = pd.DataFrame([first_dict], index=[self.match_id])
        i = 0
        for key in self.dict_of_dict:
            if i != 0:
                df2 = pd.DataFrame(self.dict_of_dict[key], index=[self.match_id])
                # print(df2)
                df = pd.concat([df, df2])            
            i = i + 1
        if self.valid_df:
            return df
        else:
            #we had some sort invalid entry we dont want to include the match at all
            return None
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