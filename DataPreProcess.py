import pandas as pd
import numpy as np

class DataPreprocessing():
    def __init__(self):
        # Initialize tables as empty dataframes
        self.matches = pd.DataFrame()
        self.players = pd.DataFrame()
        self.chat = pd.DataFrame()
        self.objectives = pd.DataFrame()
        self.advantages = pd.DataFrame()
        self.events = pd.DataFrame()
        self.abilities = pd.DataFrame()
        self.wards = pd.DataFrame()
        self.previous_matches = pd.DataFrame()


    def get_match(self, match):
        """ Get general information from the match and append to self.matches. """
        
        # fields = ['match_id', 'match_seq_num', 'patch', 'region', 'start_time', 'duration',
        #     'game_mode', 'skill', 'first_blood_time', 'barracks_status_dire',
        #     'barracks_status_radiant', 'tower_status_dire', 'tower_status_radiant',
        #     'dire_score', 'radiant_score', 'radiant_win']

        fields = ['match_id']

        proc_match = {key: [match[key]] for key in fields}
        self.matches = self.matches._append(pd.DataFrame(proc_match), ignore_index= True)
        # print(self.matches)
   
    def get_players_events(self, match):
        """ Get events for each player (kills, runes, bb and purchases) and append to self.events. """
        events = []
        for player in match['players']:
            if player['buyback_log']: # Player's Buybacks
                for bb in player['buyback_log']:
                    tmp = {
                        'match_id': match['match_id'],
                        'account_id': player['account_id'],
                        'player_slot': player['player_slot'],
                        'hero_id': player['hero_id'],
                        'time': bb['time'],
                        'key': np.nan,
                        'event': 'buyback'
                    }
                    events.append(tmp.copy())
            if player['kills_log']: # Player's kills on enemy heroes
                for kill in player['kills_log']:
                    tmp = {
                        'match_id': match['match_id'],
                        'account_id': player['account_id'],
                        'player_slot': player['player_slot'],
                        'hero_id': player['hero_id'],
                        'time': kill['time'],
                        'key': kill['key'],
                        'event': 'kill'
                    }
                    events.append(tmp.copy())
            if player['runes_log']: # Runes picked
                for rune in player['runes_log']:
                    tmp = {
                        'match_id': match['match_id'], 
                        'account_id': player['account_id'], 
                        'player_slot': player['player_slot'],
                        'hero_id': player['hero_id'], 
                        'time': rune['time'],
                        'key': rune['key'],
                        'event': 'rune'
                    }
                    events.append(tmp.copy())
            if player['purchase_log']:
                for item in player['purchase_log']: # Items purchased
                    tmp = {
                        'match_id': match['match_id'],
                        'account_id': player['account_id'],
                        'player_slot': player['player_slot'],
                        'hero_id': player['hero_id'],
                        'time': item['time'],
                        'key': item['key'],
                        'event': 'purchase'
                    }
                    events.append(tmp.copy())
        if events:
            self.events = self.events._append(pd.DataFrame(events), ignore_index= True)

    def get_draft_timings(self, match):
        """get the order of heroes picked in a match"""

        timings = match['draft_timings']
        # print(timings)
        timings = self.clean_draft_timings(timings)
        
        return timings

    def clean_draft_timings(self, timings):
        retval = []
        if timings is not None:
            for item in timings:
                if item['pick'] == True:
                    retval.append(item)
            # print(retval)
            return retval

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
                            #append to pre_game_items
                            pre_game_items.append(items)
                        
                    #add new entry to items_dict
                    hero_id = player["hero_id"]
                    hero_items_dict[hero_id] = pre_game_items
                    hero_lane_dict[hero_id] = player["lane"]
            # print(hero_items_dict)
            print(hero_lane_dict)
            return hero_items_dict, hero_lane_dict

    # https://liquipedia.net/dota2/MediaWiki:Dota2webapi-heroes.json

    def get_players(self, match):
        """ Get match information for each player and append to self.players dataframe. """
        
        fields = ['player_slot', 'account_id', 'hero_id', 'kills', 'deaths',
            'assists', 'last_hits', 'denies', 'gold_per_min', 'xp_per_min',
            'gold_spent', 'hero_damage', 'hero_healing', 'tower_damage',
            'level', 'party_size', 'item_0', 'item_1', 'item_2', 'item_3',
            'item_4', 'item_5', 'camps_stacked', 'creeps_stacked', 'obs_placed', 'sen_placed',
            'purchase_tpscroll', 'rune_pickups', 'roshans_killed', 'towers_killed', 'win']

        players = []
        for item in match['players']:
            player = {'match_id': match['match_id']}
            for field in fields:
                if field in item:
                    player[field] = item[field]
                else:
                    player[field] = np.nan
            players.append(player.copy())
        if players:
            self.players = self.players._append(pd.DataFrame(players), ignore_index= True)
            # print(self.players)

    def get_all_current_match_tables(self, match_details):
        """ Get all tables from a current match, except the previous matches. """
        self.get_match(match_details)
        self.get_players(match_details)
        # self.get_match_chat(match_details)
        # self.get_match_objectives(match_details)
        # self.get_match_advantages(match_details)
        # self.get_ability_upgrades(match_details)
        self.get_players_events(match_details)
        # self.get_wards(match_details)
        self.get_draft_timings(match_details)
        self.get_hero_starting_items_lane(match_details)
 
    # def get_match_chat(self, match):
    #     """ Get match chat and save to self.chat dataframe. """
    #     fields = ['match_id', 'time', 'type', 'key', 'slot', 'player_slot']
    #     messages = []
    #     if match['chat']:
    #         for item in match['chat']:
    #             message = {'match_id': match['match_id']}
    #             for field in fields:
    #                 message[field] = item[field]
    #             messages.append(message.copy())
    #         if messages:
    #             self.chat = self.chat._append(pd.DataFrame(messages), ignore_index= True)

    # def get_match_objectives(self, match):
    #     """ Get game objectives like Roshan and towers and append to self.objectives dataframe. """
    #     fields = ['time', 'type', 'unit', 'key', 'slot', 'player_slot']
    #     objectives = []
    #     if match['objectives']:
    #         for item in match['objectives']:
    #             obj = {'match_id': match['match_id']}
    #             for field in fields:
    #                 if field in item:
    #                     obj[field] = item[field]
    #                 else:
    #                     obj[field] = np.nan
    #             objectives.append(obj.copy())
    #     if objectives:
    #         self.objectives = self.objectives._append(pd.DataFrame(objectives), ignore_index= True)

    # def get_match_advantages(self, match):
    #     """ Get radiant gold and xp advantage for each minute and append to self.advantages dataframe. """
    #     advantages = []
    #     if match['radiant_gold_adv']:  # Gold advantage (gold_or_xp = 0)
    #         for i, value in enumerate(match['radiant_gold_adv']):
    #             adv = {
    #                 'match_id': match['match_id'],
    #                 'minute': i,
    #                 'gold_or_xp': 0,
    #                 'value': int(value)
    #             }
    #             advantages.append(adv.copy())
    #     if match['radiant_xp_adv']:  # XP advantage (gold_or_xp = 1)
    #         for i, value in enumerate(match['radiant_xp_adv']):
    #             adv = {
    #                 'match_id': match['match_id'],
    #                 'minute': i,
    #                 'gold_or_xp': 1,
    #                 'value': int(value)
    #             }
    #             advantages.append(adv.copy())
    #     if advantages:
    #         self.advantages = self.advantages._append(pd.DataFrame(advantages), ignore_index= True)

    # def get_previous_matches(self, current_match_id, player_account_id, player_previous_matches,
    #                          current_match_start_time):
    #     """ Append all previous matches before match_start_time from a given account id. """
        
    #     previous_matches = []
    #     fields = ['match_id', 'player_slot', 'radiant_win', 'duration', 'game_mode',
    #               'lobby_type', 'start_time', 'version', 'hero_id', 'kills', 'deaths',
    #               'assists', 'skill', 'leaver_status', 'party_size']

    #     for item in player_previous_matches:
    #         previous_match = {'current_match_id': current_match_id, 'account_id': player_account_id}
    #         for field in fields:
    #             previous_match[field] = item[field]
    #         previous_matches.append(previous_match.copy())

    #     df = pd.DataFrame(previous_matches)
    #     # Avoid future games
    #     df = df[df['start_time'] < current_match_start_time]
    #     self.previous_matches = self.previous_matches._append(df, ignore_index= True)


    # def get_ability_upgrades(self, match):
    #     """ Get skill upgrades for each player. Columns goes from 1 to 25 for each possible skill upgrade. """
    #     ability_upgrades = []
    #     for player in match['players']:
    #         if player['ability_upgrades_arr']:
    #             tmp = {
    #                 'match_id': match['match_id'],
    #                 'account_id': player['account_id'],
    #                 'player_slot': player['player_slot'],
    #                 'hero_id': player['hero_id'],
    #             }
    #             for i in range(25):
    #                 tmp['skill_upgrade_' + str(i + 1)] = np.nan
    #             for i, value in enumerate(player['ability_upgrades_arr']):
    #                 tmp['skill_upgrade_' + str(i + 1)] = value
    #             ability_upgrades.append(tmp.copy())
    #     if ability_upgrades:
    #         self.abilities = self.abilities._append(pd.DataFrame(ability_upgrades), ignore_index= True)

    # def get_wards(self, match):
    #     """ Get time, position, slot and hero for each ward placed and append to self.wards dataframe. """
    #     wards = []
    #     for player in match['players']:
    #         if player['obs_log']:  # Observer wards (type = 0)
    #             for item in player['obs_log']:
    #                 ward = {
    #                     'match_id': match['match_id'], 'account_id': player['account_id'],
    #                     'player_slot': player['player_slot'], 'hero_id': player['hero_id'],
    #                     'time': item['time'], 'x': item['x'], 'y': item['y'], 'type': 0
    #                 }
    #                 wards.append(ward.copy())
    #         if player['sen_log']:  # Sentry wards (type = 1)
    #             for item in player['sen_log']:
    #                 ward = {
    #                     'match_id': match['match_id'], 'account_id': player['account_id'],
    #                     'player_slot': player['player_slot'], 'hero_id': player['hero_id'],
    #                     'time': item['time'], 'x': item['x'], 'y': item['y'], 'type': 1
    #                 }
    #                 wards.append(ward.copy())
    #     if wards:
    #         self.wards = self.wards._append(pd.DataFrame(wards), ignore_index= True)
