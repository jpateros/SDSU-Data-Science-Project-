from datetime import datetime
import time
import json
import requests
import numpy as np
import pandas as pd

class OpenDotaAPI():
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.last_match_id = 0

    def _call(self, url, parameters, tries= 2):
        for i in range(tries):
            try:
                if self.verbose: print("Sending API request... ", end="", flush=True)
                resp = requests.get(url, params= parameters, timeout= 20)
                load_resp = json.loads(resp.text)
                if self.verbose: print("done")
                return load_resp
            except Exception as e:
                print("failed. Trying again in 5s")
                print(e)
                time.sleep(5)
        else:
            ValueError("Unable to connect to OpenDota API")
      
    def get_recent_pro_matches(self, use_last_match = False):
        params = dict()
        if use_last_match:
            params['less_than_match_id'] = self.last_match_id
        url = "https://api.opendota.com/api/proMatches"
        matches = self._call(url, params)
        print(matches)
        self.last_match_id = min([item['match_id'] for item in matches])
        return matches

    # # Return a list of 100 recent matches; save smaller match_id
    # def get_recent_matches(self, use_last_match = False):
    #     params = dict()
    #     if use_last_match:
    #         params['less_than_match_id'] = self.last_match_id
    #     url = "https://api.opendota.com/api/publicMatches"
    #     matches = self._call(url, params)
    #     self.last_match_id = min([item['match_id'] for item in matches])
    #     return matches

    # Return a dictionary with match information
    def get_match_info(self, match_id):
        url = "https://api.opendota.com/api/matches/" + str(match_id)
        return self._call(url, None)

    # Return a list with player's match history (previous matches)
    def get_player_matches_history(self, account_id):
        url = "https://api.opendota.com/api/players/{}/matches".format(account_id)
        return self._call(url, None)

    # Get a dictionary with overall benchmarks given account id (kills, deaths, gpm...)
    def get_player_totals(self, account_id, hero_id = None):
        params = {'sort': 1}
        if hero_id: params['hero_id'] = hero_id
        url = "https://api.opendota.com/api/players/{}/totals".format(int(account_id))
        return self._call(url, params)

    # Return wins and losses for a given account id
    def get_player_win_loss(self, account_id, hero_id = None):
        if hero_id:
            params = {'hero_id': hero_id}
        else:
            params = None
        url = "https://api.opendota.com/api/players/{}/wl".format(account_id)
        resp = self._call(url, params)
        return resp['win'], resp['lose']
    