import json
import time
import os
from pprint import pprint
from point_matrix import eightball_points_matrix, nineball_loser_points_matrix, nineball_skill_level_points

class PlayerStats:
    """This class will be used to create Player Profiles (no auth), for both eightball and nineball. This will serve as the record, recording scores for specific matches will not happen in the function."""
    def __init__(self, player_name, lag_won = 0,
                 
                eightball_player_skill_level= 0, eightball_racks_to_win = 0, eightball_inning_total = 0,
                eightball_matches_played = 0, eightball_matches_won = 0, eightball_win_percentage = 0,
                eightball_racks_won = 0, eightball_points_total = 0, eightball_points_per_match = 0, eightball_points_available = 0,
                eightball_defensive_shot_total = 0, eightball_defensive_shot_average = 0,
                eightball_eight_on_the_break = 0, eightball_break_and_run = 0, eightball_mini_slam = 0,

                nineball_player_skill_level = 0, nineball_points_to_win = 0,
                nineball_inning_total = 0, nineball_matches_played = 0, nineball_matches_won = 0, nineball_win_percentage = 0,
                nineball_match_ball_count = 0, nineball_points_total = 0, nineball_points_per_match = 0, nineball_points_available = 0,
                nineball_defensive_shot_total = 0, nineball_defensive_shot_average = 0,
                nineball_nine_on_the_snap = 0, nineball_break_and_run = 0, nineball_mini_slam = 0):
        
        # Miscellaneous stats
        self.player_name = player_name
        self.lag_won = lag_won

        # Eightball stats
        self.eightball_player_skill_level = eightball_player_skill_level
        self.eightball_racks_to_win = eightball_racks_to_win
        self.eightball_inning_total = eightball_inning_total
        self.eightball_matches_played = eightball_matches_played
        self.eightball_matches_won = eightball_matches_won
        self.eightball_win_percentage = eightball_win_percentage
        self.eightball_racks_won = eightball_racks_won
        self.eightball_points_total = eightball_points_total
        self.eightball_points_per_match = eightball_points_per_match
        self.eightball_points_available = eightball_points_available
        self.eightball_defensive_shot_total = eightball_defensive_shot_total
        self.eightball_defensive_shot_average = eightball_defensive_shot_average
        self.eightball_eight_on_the_break = eightball_eight_on_the_break
        self.eightball_break_and_run = eightball_break_and_run
        self.eightball_mini_slam = eightball_mini_slam

        # Nineball stats
        self.nineball_player_skill_level = nineball_player_skill_level
        self.nineball_points_to_win = nineball_points_to_win
        self.nineball_inning_total = nineball_inning_total
        self.nineball_matches_played = nineball_matches_played
        self.nineball_matches_won = nineball_matches_won
        self.nineball_win_percentage = nineball_win_percentage
        self.nineball_match_ball_count = nineball_match_ball_count
        self.nineball_points_total = nineball_points_total
        self.nineball_points_per_match = nineball_points_per_match
        self.nineball_points_available = nineball_points_available
        self.nineball_defensive_shot_total = nineball_defensive_shot_total
        self.nineball_defensive_shot_average = nineball_defensive_shot_average
        self.nineball_nine_on_the_snap = nineball_nine_on_the_snap
        self.nineball_break_and_run = nineball_break_and_run
        self.nineball_mini_slam = nineball_mini_slam
    @staticmethod
    def update_player_matches_won(player_name, matches_won, game_type):
        with open("player_data.json", "r+") as file:
            data = json.load(file)
            if player_name in data:
                player_data = data[player_name]
                if game_type in player_data:
                    player_data[game_type]["eightball_matches_won"] += matches_won
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    return True
            return False
    def create_json_file_player_entry(self):
        """This function will create new entries for each player in the match IF, they don't already have an entry in the player_data.json"""
        
        # Load the json file creating the first intermediate dictionary
        with open("player_data.json") as file:
            json_player_data = json.load(file)

        # Look for player_name in the player_data.json file
        if not self.player_name in json_player_data:
            # Create second intermediate dictionary with all the same fields as the class
            new_player = {
                self.player_name:{
                    "lags_won": 0,
                    "eightball": {
                        "eightball_player_skill_level": self.eightball_player_skill_level,
                        "eightball_racks_to_win": self.eightball_racks_to_win,
                        "eightball_inning_total": self.eightball_inning_total,
                        "eightball_matches_played": self.eightball_matches_played,
                        "eightball_matches_won": self.eightball_matches_won,
                        "eightball_win_percentage": self.eightball_win_percentage,
                        "eightball_racks_won": self.eightball_racks_won,
                        "eightball_points_total": self.eightball_points_total,
                        "eightball_points_per_match": self.eightball_points_per_match,
                        "eightball_points_available": self.eightball_points_available,
                        "eightball_defensive_shot_total": self.eightball_defensive_shot_total,
                        "eightball_defensive_shot_average": self.eightball_defensive_shot_average,
                        "eightball_eight_on_the_break": self.eightball_eight_on_the_break,
                        "eightball_break_and_run": self.eightball_break_and_run,
                        "eightball_mini_slam": self.eightball_mini_slam,
                        "eightball_match_sn_history": []
                    },
                    "nineball": {
                        "nineball_player_skill_level": self.nineball_player_skill_level,
                        "nineball_points_to_win": self.nineball_points_to_win,
                        "nineball_inning_total": self.nineball_inning_total,
                        "nineball_matches_played": self.nineball_matches_played,
                        "nineball_matches_won": self.nineball_matches_won,
                        "nineball_win_percentage": self.nineball_win_percentage,
                        "nineball_points_total": self.nineball_points_total,
                        "nineball_points_per_match": self.nineball_points_per_match,
                        "nineball_points_available": self.nineball_points_available,
                        "nineball_defensive_shot_total": self.nineball_defensive_shot_total,
                        "nineball_defensive_shot_average": self.nineball_defensive_shot_average,
                        "nineball_nine_on_the_snap": self.nineball_nine_on_the_snap,
                        "nineball_break_and_run": self.nineball_break_and_run,
                        "nineball_mini_slam": self.nineball_mini_slam,
                        "nineball_points_history": []
                    }
                }
            }
        
            # Update the first intermediate dictionary with the second intermediate dictionary
            json_player_data.update(new_player)
        
        # Writing the updated data to the JSON file
        with open("player_data.json", "w") as file:
            json.dump(json_player_data, file, indent=4)

    def update_json_file_player_stats(self):
        """This function will write the stats of a match to a json file once the match is complete."""

        # Loading the JSON file
        with open("player_data.json") as file:
            json_player_data = json.load(file)

        # NINEBALL CALCULATIONS
        if current_match.game == "nineball":
            # This calculates the nineball win percentage
            self.nineball_win_percentage = (self.nineball_matches_won + json_player_data[self.player_name][current_match.game]["nineball_matches_won"]) / (self.nineball_matches_played + json_player_data[self.player_name][current_match.game]["nineball_matches_played"]) * 100
            if self.nineball_win_percentage.is_integer():
                self.nineball_win_percentage = int(self.nineball_win_percentage)

            # This calculates the nineball points per match percentage
            self.nineball_points_per_match = (self.nineball_points_total + json_player_data[self.player_name][current_match.game]["nineball_points_total"]) / (self.nineball_matches_played + json_player_data[self.player_name][current_match.game]["nineball_matches_played"])
            if self.nineball_points_per_match.is_integer():
                self.nineball_points_per_match = int(self.nineball_points_per_match)

            # This calculates the nineball points_available
            self.nineball_points_available = ((self.nineball_points_total + json_player_data[self.player_name][current_match.game]["nineball_points_total"]) / ((self.nineball_matches_played + json_player_data[self.player_name][current_match.game]["nineball_matches_played"]) * 20)) * 100
            if self.nineball_points_available.is_integer():
                self.nineball_points_available = int(self.nineball_points_available)

            # This calculates the nineball defensive shot average
            if self.nineball_defensive_shot_total > 0:
                self.nineball_defensive_shot_average = (self.nineball_defensive_shot_total + json_player_data[self.player_name][current_match.game]["nineball_defensive_shot_total"]) / (current_match.inning_total + json_player_data[self.player_name][current_match.game]["nineball_inning_total"]) * 100
                if self.nineball_defensive_shot_average.is_integer():
                    self.nineball_defensive_shot_average = int(self.nineball_defensive_shot_average)   

            # This checks for mini slams
            if self.nineball_break_and_run > 0 and self.nineball_nine_on_the_snap > 0:
                self.nineball_mini_slam += 1   
                
            # Add the player stats to the intermediate json file
            json_player_data[self.player_name]["lags_won"] = json_player_data[self.player_name]["lags_won"] + self.lag_won
            json_player_data[self.player_name][current_match.game]["nineball_player_skill_level"] = self.nineball_player_skill_level
            json_player_data[self.player_name][current_match.game]["nineball_points_to_win"] = self.nineball_points_to_win
            json_player_data[self.player_name][current_match.game]["nineball_inning_total"] += current_match.inning_total
            json_player_data[self.player_name][current_match.game]["nineball_matches_played"] += self.nineball_matches_played
            json_player_data[self.player_name][current_match.game]["nineball_matches_won"] += self.nineball_matches_won
            json_player_data[self.player_name][current_match.game]["nineball_win_percentage"] = self.nineball_win_percentage
            json_player_data[self.player_name][current_match.game]["nineball_points_total"] += self.nineball_points_total
            json_player_data[self.player_name][current_match.game]["nineball_points_per_match"] = self.nineball_points_per_match
            json_player_data[self.player_name][current_match.game]["nineball_points_available"] = self.nineball_points_available
            json_player_data[self.player_name][current_match.game]["nineball_defensive_shot_total"] += self.nineball_defensive_shot_total
            json_player_data[self.player_name][current_match.game]["nineball_defensive_shot_average"] = self.nineball_defensive_shot_average
            json_player_data[self.player_name][current_match.game]["nineball_nine_on_the_snap"] += self.nineball_nine_on_the_snap
            json_player_data[self.player_name][current_match.game]["nineball_break_and_run"] += self.nineball_break_and_run
            json_player_data[self.player_name][current_match.game]["nineball_mini_slam"] += self.nineball_mini_slam
            json_player_data[self.player_name][current_match.game]["nineball_points_history"].append(self.nineball_points_total)
        
        if current_match.game == "eightball":
            # This calculates the eightball win percentage
            self.eightball_win_percentage = (self.eightball_matches_won + json_player_data[self.player_name][current_match.game]["eightball_matches_won"]) / (self.eightball_matches_played + json_player_data[self.player_name][current_match.game]["eightball_matches_played"]) * 100
            if self.eightball_win_percentage.is_integer():
                self.eightball_win_percentage = int(self.eightball_win_percentage)

            # This calculates the eightball points per match percentage
            self.eightball_points_per_match = (self.eightball_points_total + json_player_data[self.player_name][current_match.game]["eightball_points_total"]) / (self.eightball_matches_played + json_player_data[self.player_name][current_match.game]["eightball_matches_played"])
            if self.eightball_points_per_match.is_integer():
                self.eightball_points_per_match = int(self.eightball_points_per_match)

            # This calculates the eightball points_available
            self.eightball_points_available = ((self.eightball_points_total + json_player_data[self.player_name][current_match.game]["eightball_points_total"]) / ((self.eightball_matches_played + json_player_data[self.player_name][current_match.game]["eightball_matches_played"]) * 3)) * 100
            if self.eightball_points_available.is_integer():
                self.eightball_points_available = int(self.eightball_points_available)

            # This calculates the eightball defensive shot average
            if self.eightball_defensive_shot_total > 0:
                self.eightball_defensive_shot_average = (self.eightball_defensive_shot_total + json_player_data[self.player_name][current_match.game]["eightball_defensive_shot_total"]) / (current_match.inning_total + json_player_data[self.player_name][current_match.game]["eightball_inning_total"]) * 100
                if self.eightball_defensive_shot_average.is_integer():
                    self.eightball_defensive_shot_average = int(self.eightball_defensive_shot_average)   

            # This checks for mini slams
            if self.eightball_break_and_run > 0 and self.eightball_eight_on_the_break > 0:
                self.eightball_mini_slam += 1   
                
            # Add the player stats to the intermediate json file
            json_player_data[self.player_name]["lags_won"] = json_player_data[self.player_name]["lags_won"] + self.lag_won
            json_player_data[self.player_name][current_match.game]["eightball_player_skill_level"] = self.eightball_player_skill_level
            json_player_data[self.player_name][current_match.game]["eightball_racks_to_win"] = self.eightball_racks_to_win
            json_player_data[self.player_name][current_match.game]["eightball_inning_total"] += current_match.inning_total
            json_player_data[self.player_name][current_match.game]["eightball_matches_played"] += self.eightball_matches_played
            json_player_data[self.player_name][current_match.game]["eightball_matches_won"] += self.eightball_matches_won
            json_player_data[self.player_name][current_match.game]["eightball_win_percentage"] = self.eightball_win_percentage
            json_player_data[self.player_name][current_match.game]["eightball_racks_won"] += self.eightball_racks_won
            json_player_data[self.player_name][current_match.game]["eightball_points_total"] = self.eightball_points_total
            json_player_data[self.player_name][current_match.game]["eightball_points_per_match"] = self.eightball_points_per_match
            json_player_data[self.player_name][current_match.game]["eightball_points_available"] = self.eightball_points_available
            json_player_data[self.player_name][current_match.game]["eightball_defensive_shot_total"] += self.eightball_defensive_shot_total
            json_player_data[self.player_name][current_match.game]["eightball_defensive_shot_average"] = self.eightball_defensive_shot_average
            json_player_data[self.player_name][current_match.game]["eightball_eight_on_the_break"] += self.eightball_eight_on_the_break
            json_player_data[self.player_name][current_match.game]["eightball_break_and_run"] += self.eightball_break_and_run
            json_player_data[self.player_name][current_match.game]["eightball_mini_slam"] += self.eightball_mini_slam
            json_player_data[self.player_name][current_match.game]["eightball_match_sn_history"].append(str(current_match.match_start_timestamp))
        
        # Writing the updated data to the JSON file
        with open("player_data.json", "w") as file:
            json.dump(json_player_data, file, indent=4)

# This section is used to create 'player profiles' class objects
player_1 = PlayerStats("Ryan Oswalt")
player_2 = PlayerStats("Peter Parker")

player_1.eightball_player_skill_level = 5
player_2.eightball_player_skill_level = 3

player_1.nineball_player_skill_level = 5
player_2.nineball_player_skill_level = 3

player_1.eightball_racks_to_win = eightball_points_matrix[player_1.eightball_player_skill_level][player_2.eightball_player_skill_level]["player_rack_count"]
player_2.eightball_racks_to_win = eightball_points_matrix[player_2.eightball_player_skill_level][player_1.eightball_player_skill_level]["player_rack_count"]

player_1.nineball_points_to_win = nineball_skill_level_points[player_1.nineball_player_skill_level]
player_2.nineball_points_to_win = nineball_skill_level_points[player_2.nineball_player_skill_level]


class EightballGame:
    """This class is used to score a game of eightball"""
    def __init__(self, game = "eightball", break_shot= True, break_and_run = False, current_shooter = None, inning_total = 0, lag_winner = None, eightball_rack_count = 1, eightball_pocketing_context = None,
                inning_count_at_rack_start = 0, rack_breaking_player = None, match_winner = None, current_shooter_defensive_shot = 0,
                match_start_timestamp = time.time(), match_start_human_readable = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), match_end_timestamp = None, game_log_iterator = 0, game_log = {}):
        
        self.game = game
        self.break_shot = break_shot
        self.break_and_run = break_and_run
        self.current_shooter = current_shooter
        self.inning_total = inning_total
        self.lag_winner = lag_winner
        self.eightball_rack_count = eightball_rack_count
        self.eightball_pocketing_context = eightball_pocketing_context
        self.inning_count_at_rack_start = inning_count_at_rack_start
        self.rack_breaking_player = rack_breaking_player
        self.current_shooter_defensive_shot = current_shooter_defensive_shot
        self.match_winner = match_winner
        self.match_start_timestamp = match_start_timestamp
        self.match_start_human_readable = match_start_human_readable
        self.match_end_timestamp = match_end_timestamp
        self.game_log_iterator = game_log_iterator
        self.game_log = game_log
    def to_json(self):
        # Convert the game state to a dict suitable for serialization
        game_state = {
            "game": self.game,
            "break_shot": self.break_shot,
            "break_and_run": self.break_and_run,
            "current_shooter": self.current_shooter,
            "inning_total": self.inning_total,
            "lag_winner": self.lag_winner,
            "eightball_rack_count": self.eightball_rack_count,
            "eightball_pocketing_context": self.eightball_pocketing_context,
            "inning_count_at_rack_start": self.inning_count_at_rack_start,
            "rack_breaking_player": self.rack_breaking_player,
            "current_shooter_defensive_shot": self.current_shooter_defensive_shot,
            "match_winner": self.match_winner,
            "match_start_timestamp": self.match_start_timestamp,
            "match_start_human_readable": self.match_start_human_readable,
            "match_end_timestamp": self.match_end_timestamp,
            "game_log_iterator": self.game_log_iterator,
            "game_log": self.game_log
        }
        return json.dumps(game_state)
    
    def ball_pocketed(self, ball_number):
        # Check if the ball number is valid (1 to 15)
        if not (1 <= ball_number <= 15):
            return json.dumps({'error': 'Invalid ball number'}), 400

        # Check if the game is still in progress
        if self.match_winner:
            return json.dumps({'error': 'The game is already over'}), 400

        # Update the game state to reflect the pocketed ball
        if ball_number == 8:
            # Special case: Pocketing the 8-ball
            if self.eightball_rack_count == 1:
                # If it's the first rack, pocketing the 8-ball wins the game
                self.match_winner = self.current_shooter
            else:
                # If it's not the first rack, pocketing the 8-ball is a foul
                self.switch_turn()  # Switch turn to the opponent
                self.current_shooter_defensive_shot += 1  # Increment defensive shot count
        elif ball_number == 0:
            # Special case: Pocketing the cue ball (scratch)
            self.switch_turn()  # Switch turn to the opponent
            self.current_shooter_defensive_shot += 1  # Increment defensive shot count
        else:
            # Regular ball pocketed
            if self.current_shooter == self.player1_name:
                self.eightball_pocketing_context = 'player1'
            elif self.current_shooter == self.player2_name:
                self.eightball_pocketing_context = 'player2'
        
        # Update other relevant game state attributes
        # For example, remove the pocketed ball from the table, update inning count, etc.

        # Log the action
        self.game_log[self.game_log_iterator] = f'Player {self.current_shooter} pocketed ball {ball_number}'
        self.game_log_iterator += 1

        # You may need to implement more complex logic based on your specific game rules

        # Update the turn
        self.switch_turn()

        # Check if the game is over (e.g., if a player has won)
        if self.is_game_over():
            self.end_game()
    @staticmethod
    def from_json(json_str):
        # Convert JSON string back to a dictionary
        game_state = json.loads(json_str)
        game = EightballGame(**game_state)
        return game
    
    def update_game_log(self, break_shot = False, inning = False, defensive_shot = False, rack_over = False, match_over = False, push_to_json_file=False, undo=False):
        """This method will update the game_log dictionary"""

        # Loading the JSON file
        with open("match_data.json") as file:
            json_match_data = json.load(file)

        if not push_to_json_file:
            # Create nested dictionary for each event in the match: lag, innings, defensive shots, rack over
            if not self.match_start_timestamp in self.game_log:
                self.game_log.update({
                    self.match_start_timestamp: {
                        "Game": self.game,
                        "Match Start": self.match_start_human_readable,
                        "Lag Winner": self.lag_winner,
                        "event_log": {self.game_log_iterator: {}}
                    }
                })
            else:
                if not undo:
                    self.game_log[self.match_start_timestamp]["event_log"].update({self.game_log_iterator: {}})
                else:
                    last_event = self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator]

            if break_shot:
                if undo:
                    self.game_log[self.match_start_timestamp]["event_log"](self.game_log_iterator).pop("break_shot")
                else:
                    self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator].update({
                        "inning_count": self.inning_total,
                        "break_shot": self.current_shooter
                    })
            elif inning:
                if undo:
                    self.game_log[self.match_start_timestamp]["event_log"](self.game_log_iterator).pop("inning_count")
                else:
                    if "defensive_shot" in list(self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator-1].keys()):
                        self.game_log_iterator -= 1
                        self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator].update({
                            "inning_count": self.inning_total,
                        })
                    else:
                        self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator].update({
                            "inning_count": self.inning_total,
                            "current_shooter": self.current_shooter
                        })
            elif defensive_shot:
                if undo:
                    self.game_log[self.match_start_timestamp]["event_log"](self.game_log_iterator).pop("defensive_shot")
                else:
                    self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator].update({
                        "inning_count": self.inning_total,
                        "defensive_shot": self.current_shooter
                    })
            elif rack_over:
                if undo:
                    self.game_log[self.match_start_timestamp]["event_log"](self.game_log_iterator).pop("rack_over")
                else:
                    if self.current_shooter == self.lag_winner and self.inning_total == self.inning_count_at_rack_start:
                        self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator].update({
                            "inning_count": self.inning_total,
                            "break_shot": self.current_shooter,
                            "rack_over": self.eightball_pocketing_context,
                        })
                    else:
                        self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator].update({
                            "inning_count": self.inning_total,
                            "current_shooter": self.current_shooter,
                            "rack_over": self.eightball_pocketing_context,
                        })
            elif match_over:
                if undo:
                    self.game_log[self.match_start_timestamp]["event_log"](self.game_log_iterator).pop("match_over")
                else:
                    self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator].update({
                        "inning_count": self.inning_total,
                        "rack_over": self.eightball_pocketing_context,
                        "match_winner": self.current_shooter
                    })

            if not undo:
                self.game_log_iterator += 1

        else:

            if push_to_json_file:
                json_match_data.update(self.game_log)
                with open("match_data.json", "w") as file:
                    json.dump(json_match_data, file, indent=4)
        
    def lag_for_the_break(self, lag_winner):
        """This method will set the lag winner for the match and the current shooter for the first inning."""
        # Create a list of the of all different case types, so case type doesn't matter
        lag_winner_list = [lag_winner, lag_winner.capitalize(), lag_winner.casefold(), lag_winner.lower(), lag_winner.swapcase(), lag_winner.title(), lag_winner.upper()]

        # Winner of the lag is the current shooter, so both are assigned the player that won the lag, and add 1 to the lag winner's profile under lag_won
        if player_1.player_name in lag_winner_list:
            self.current_shooter = player_1.player_name
            self.lag_winner = player_1.player_name
            player_1.lag_won += 1
            self.rack_breaking_player = self.current_shooter
        else:
            self.current_shooter = player_2.player_name
            self.lag_winner = player_2.player_name
            player_2.lag_won += 1
            self.rack_breaking_player = self.current_shooter

        if self.break_shot:
            self.update_game_log(break_shot=True)
        
        # Add 1 to self.eightball_rack_count
        self.eightball_rack_count += 1

    def defensive_shot(self, undo=False):
        """This method will be used to increase the defensive shot count for the current shooter"""
        if undo:
            if self.current_shooter == player_1.player_name:
                player_1.eightball_defensive_shot_total -= 1
            else:
                player_2.eightball_defensive_shot_total -= 1

            self.update_game_log(defensive_shot=True, undo=True)        
            self.current_shooter_defensive_shot = 0
        else:
            if self.current_shooter == player_1.player_name:
                player_1.eightball_defensive_shot_total += 1
            else:
                player_2.eightball_defensive_shot_total += 1

            self.current_shooter_defensive_shot = 1
            self.update_game_log(defensive_shot=True)        
            self.current_shooter_defensive_shot = 0

    def shooter_turn_over(self, undo=False):
        """This method will be used to increase the inning count"""
        if undo:
            if self.break_shot:
                self.update_game_log(break_shot=True, undo=True)
            else:
                self.update_game_log(inning=True, undo=True)

            # Check for the break_shot and change value to False
            if "break_shot" in self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator-1]:
                self.break_shot = False
            if self.inning_total != self.inning_count_at_rack_start and self.current_shooter in self.game_log[self.match_start_timestamp]["event_log"][self.game_log_iterator-1].values():
                self.break_and_run = True

            # When the player that lost the lag is done with their turn, add 1 to the inning count
            # Check if the self.current_shooter lost the lag, if they did, the inning is over, add 1 to self.inning_total
            if self.current_shooter != self.lag_winner:
                self.inning_total -= 1

            # Check which player is the self.current_shooter, and update the self.current_shooter to the other player
            if self.current_shooter == player_1.player_name:
                self.current_shooter = player_2.player_name
            else:
                self.current_shooter = player_1.player_name
        else:
            if self.break_shot:
                self.update_game_log(break_shot=True)
            else:
                self.update_game_log(inning=True)

            # Check for the break_shot and change value to False
            self.break_shot = False
            self.break_and_run = False

            # When the player that lost the lag is done with their turn, add 1 to the inning count
            # Check if the self.current_shooter lost the lag, if they did, the inning is over, add 1 to self.inning_total
            if self.current_shooter != self.lag_winner:
                self.inning_total += 1

            # Check which player is the self.current_shooter, and update the self.current_shooter to the other player
            if self.current_shooter == player_1.player_name:
                self.current_shooter = player_2.player_name
            else:
                self.current_shooter = player_1.player_name

    def rack_over(self, eight_on_the_break = False, break_and_run = False, made_eightball = False, scratched_on_eightball = False, eightball_in_wrong_pocket = False, made_eightball_early = False):
        """This method is used to reset the rack and will ultimately execute the json update at the end of the match"""
        # Check the manner in which the eightball was pocketed and update self.eightball_pocketing_context
        if eight_on_the_break:
            if self.inning_count_at_rack_start == self.inning_total and self.current_shooter == self.rack_breaking_player:
                self.game_log_iterator -= 1
            if self.current_shooter == player_1.player_name:
                player_1.eightball_eight_on_the_break += 1
                player_1.eightball_racks_won += 1
                self.eightball_pocketing_context = "eight on the break"
            else:
                player_2.eightball_eight_on_the_break += 1
                player_2.eightball_racks_won += 1
                self.eightball_pocketing_context = "eight on the break"
        elif break_and_run:
            if self.inning_count_at_rack_start == self.inning_total and self.current_shooter == self.rack_breaking_player:
                self.game_log_iterator -= 1
            if self.current_shooter == player_1.player_name:
                player_1.eightball_break_and_run += 1
                player_1.eightball_racks_won += 1
                self.eightball_pocketing_context = "break and run"
            else:
                player_2.eightball_break_and_run += 1
                player_2.eightball_racks_won += 1
                self.eightball_pocketing_context = "break and run"
        elif made_eightball:
            if self.current_shooter == player_1.player_name:
                player_1.eightball_racks_won += 1
                self.eightball_pocketing_context = "made the eightball"
            else:
                player_2.eightball_racks_won += 1
                self.eightball_pocketing_context = "made the eightball"
        elif scratched_on_eightball or eightball_in_wrong_pocket or made_eightball_early:
            if self.current_shooter == player_1.player_name:
                player_2.eightball_racks_won += 1
                self.eightball_pocketing_context = "scratched on the eight"
            else:
                player_1.eightball_racks_won += 1
                self.eightball_pocketing_context = "scratched on the eight"

        if self.eightball_pocketing_context == "break and run" or self.eightball_pocketing_context == "eight on the break":
            if self.game_log_iterator == 0 and self.break_shot:
                pass
            else:
                self.game_log_iterator += 1

        # Check for a match winner based PlayerStats class properties
        if player_1.eightball_racks_to_win == player_1.eightball_racks_won:
            self.match_winner = player_1.player_name
            player_1.eightball_matches_won += 1
            if player_2.eightball_racks_won == 0:
                player_1.eightball_points_total = 3
                player_2.eightball_points_total = 0
            elif player_2.eightball_racks_won + 1 == player_2.eightball_racks_to_win:
                player_1.eightball_points_total = 2
                player_2.eightball_points_total = 1
            else:
                player_1.eightball_points_total = 2
                player_2.eightball_points_total = 0
        elif player_2.eightball_racks_to_win == player_2.eightball_racks_won:
            self.match_winner = player_2.player_name
            player_2.eightball_matches_won += 1
            if player_1.eightball_racks_won == 0:
                player_2.eightball_points_total = 3
                player_1.eightball_points_total = 0
            elif player_1.eightball_racks_won + 1 == player_1.eightball_racks_to_win:
                player_2.eightball_points_total = 2
                player_1.eightball_points_total = 1
            else:
                player_2.eightball_points_total = 2
                player_1.eightball_points_total = 0

        # Check for a match winner, if None, reset properties to rack starting configuration
        if self.match_winner == None:
            self.inning_count_at_rack_start = self.inning_total
            self.rack_breaking_player = self.current_shooter
            self.eightball_rack_count += 1
            self.break_shot = True
            self.eightball_break_and_run = True
            self.update_game_log(rack_over=True)
        else:
            player_1.eightball_matches_played += 1
            player_2.eightball_matches_played += 1
            print(f"Match over, {self.match_winner} is the winner!")

            # Update json files
            self.match_end_timestamp = time.localtime()
            self.update_game_log(match_over=True)
            player_1.update_json_file_player_stats()
            player_2.update_json_file_player_stats()
            current_match.update_game_log(push_to_json_file=True)


class NineballGame:
    """This class is used to score a game of nineball"""
    def __init__(self, game = "nineball", break_shot= True, break_and_run = False, current_shooter = None, inning_total = 0, lag_winner = None, nineball_rack = [1, 2, 3, 4, 5, 6, 7, 8, 9], nineball_rack_count = 0,
                inning_count_at_rack_start = 0, rack_breaking_player = None, dead_balls = [], player_1_balls_pocketed = [], player_2_balls_pocketed = [], match_winner = None):
        
        self.game = game
        self.break_shot = break_shot
        self.break_and_run = break_and_run
        self.current_shooter = current_shooter
        self.inning_total = inning_total
        self.lag_winner = lag_winner
        self.nineball_rack = nineball_rack
        self.nineball_rack_count = nineball_rack_count
        self.inning_count_at_rack_start = inning_count_at_rack_start
        self.rack_breaking_player = rack_breaking_player
        self.dead_balls = dead_balls
        self.player_1_balls_pocketed = player_1_balls_pocketed
        self.player_2_balls_pocketed = player_2_balls_pocketed
        self.match_winner = match_winner
        
    def lag_for_the_break(self, lag_winner):
        """This method will set the lag winner for the match and the current shooter for the first inning."""
        # Create a list of the of all different case types, so case type doesn't matter
        lag_winner_list = [lag_winner, lag_winner.capitalize(), lag_winner.casefold(), lag_winner.lower(), lag_winner.swapcase(), lag_winner.title(), lag_winner.upper()]

        # Add 1 to self.nineball_rack_count
        self.nineball_rack_count += 1

        # Winner of the lag is the current shooter, so both are assigned the player that won the lag, and add 1 to the lag winner's profile under lag_won
        if player_1.player_name in lag_winner_list:
            self.current_shooter = player_1.player_name
            self.lag_winner = player_1.player_name
            player_1.lag_won += 1
            self.rack_breaking_player = self.current_shooter
        else:
            self.current_shooter = player_2.player_name
            self.lag_winner = player_2.player_name
            player_2.lag_won += 1
            self.rack_breaking_player = self.current_shooter

    def ball_pocketed(self, ball, dead = False):
        """This method is used to mark pocketed balls"""
        # Check for a nine_on_the_snap
        if self.break_shot and ball == 9 and not dead:
            if self.current_shooter == player_1.player_name:
                player_1.nineball_nine_on_the_snap += 1
            else:
                player_2.nineball_nine_on_the_snap += 1
        
        # Remove ball just pocketed self.nineball_rack
        self.nineball_rack.remove(ball)

        # Check if the pocketed ball is dead
        if dead:
            self.dead_balls.append(ball)
    
        # Check self.current_shooter so the ball can be applied to the correct player, the ball 9 is worth 2 points
        elif self.current_shooter == player_1.player_name:
            self.player_1_balls_pocketed.append(ball)
            if ball == 9:
                player_1.nineball_match_ball_count += 2
            else:
                player_1.nineball_match_ball_count += 1
                current_match.break_shot = False
        else:
            self.player_2_balls_pocketed.append(ball)
            if ball == 9:
                player_2.nineball_match_ball_count += 2
            else:
                player_2.nineball_match_ball_count += 1
                current_match.break_shot = False

        # Check for a break_and_run
        if ball == 9 and self.break_and_run and not self.break_shot and len(self.nineball_rack) == 0:
            if self.current_shooter == player_1.player_name:
                player_1.nineball_break_and_run += 1
            else:
                player_2.nineball_break_and_run += 1

        # Check the ball count for each player, and add 1 to the winner's profile
        if player_1.nineball_match_ball_count == player_1.nineball_points_to_win:
            self.match_winner = player_1.player_name
            player_1.nineball_matches_won += 1
            player_1.nineball_points_total = 20 - nineball_loser_points_matrix[player_2.nineball_player_skill_level][player_2.nineball_match_ball_count]
            player_2.nineball_points_total = nineball_loser_points_matrix[player_2.nineball_player_skill_level][player_2.nineball_match_ball_count]
        elif player_2.nineball_match_ball_count == player_2.nineball_points_to_win:
            self.match_winner = player_2.player_name
            player_2.nineball_matches_won += 1
            player_2.nineball_points_total = 20 - nineball_loser_points_matrix[player_1.nineball_player_skill_level][player_1.nineball_match_ball_count]
            player_1.nineball_points_total = nineball_loser_points_matrix[player_1.nineball_player_skill_level][player_1.nineball_match_ball_count]

        # Add 1 to each player's profile under nineball_matches_played and declare the winner of the match
        if self.match_winner != None:
            player_1.nineball_matches_played += 1
            player_2.nineball_matches_played += 1
            print(f"Match over, {self.match_winner} is the winner!")

        if ball == 9:
            current_match.rack_over()

    def defensive_shot(self):
        if self.current_shooter == player_1.player_name:
            player_1.nineball_defensive_shot_total += 1
        else:
            player_2.nineball_defensive_shot_total += 1

    def shooter_turn_over(self):
        """This method will be used to increase the inning count"""
        # Check for the break_shot and change value to False
        self.break_shot = False
        self.break_and_run = False

        # When the player that lost the lag is done with their turn, add 1 to the inning count
        # Check if the self.current_shooter lost the lag, if they did, the inning is over, add 1 to self.inning_total
        if self.current_shooter != self.lag_winner:
            self.inning_total += 1

        # Check which player is the self.current_shooter, and update the self.current_shooter to the other player
        if self.current_shooter == player_1.player_name:
            self.current_shooter = player_2.player_name
        else:
            self.current_shooter = player_1.player_name

    def rack_over(self):
        """This method is used to reset the rack"""
        self.inning_count_at_rack_start = self.inning_total
        self.rack_breaking_player = self.current_shooter
        self.nineball_rack_count += 1
        self.nineball_rack  = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.dead_balls = []
        self.break_shot = True
        self.break_and_run = True
        self.player_1_balls_pocketed = []
        self.player_2_balls_pocketed = []

