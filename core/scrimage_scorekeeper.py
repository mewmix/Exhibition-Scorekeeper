import json
import time
import os
from pprint import pprint
from core.point_matrix import eightball_points_matrix, nineball_loser_points_matrix, nineball_skill_level_points

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
    def __init__(self, player1_name, player2_name, game="eightball", break_shot=True, break_and_run=False, current_shooter=None, inning_total=0, lag_winner=None, eightball_rack_count=1, eightball_pocketing_context=None,
                 inning_count_at_rack_start=0, rack_breaking_player=None, match_winner=None, current_shooter_defensive_shot=0,
                 match_start_timestamp=time.time(), match_start_human_readable=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), match_end_timestamp=None, game_log_iterator=0, game_log={}):
        
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.game = game
        self.break_shot_taken = break_shot
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
        game_state = {
            "player1_name": self.player1_name,
            "player2_name": self.player2_name,
            "game": self.game,
            "break_shot": self.break_shot_taken,
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

    @staticmethod
    def from_json(json_str):
        game_state = json.loads(json_str)
        return EightballGame(**game_state)

    def lag_for_the_break(self, lag_winner):
        if lag_winner not in [self.player1_name, self.player2_name]:
            raise ValueError('Invalid lag winner')
        
        self.lag_winner = lag_winner
        self.rack_breaking_player = lag_winner
        self.current_shooter = lag_winner
        self.game_log[self.game_log_iterator] = f'{lag_winner} wins the lag and will break'
        self.game_log_iterator += 1

    def take_break_shot(self, ball_pocketed=None):
        if not self.break_shot_taken:
            raise ValueError('Break shot already taken')

        self.break_shot_taken = False
        self.game_log[self.game_log_iterator] = f'{self.current_shooter} takes the break shot'
        self.game_log_iterator += 1

        if ball_pocketed is not None:
            try:
                ball_pocketed = int(ball_pocketed)
            except ValueError:
                raise ValueError('Invalid ball number')

        if ball_pocketed == 8:
            self.match_winner = self.current_shooter
            self.game_log[self.game_log_iterator] = f'{self.current_shooter} wins the game by pocketing the 8-ball on the break'
        elif ball_pocketed == 0:
            opponent = self.player1_name if self.current_shooter == self.player2_name else self.player2_name
            self.match_winner = opponent
            self.game_log[self.game_log_iterator] = f'{self.current_shooter} scratches on the break. {opponent} wins the game'
        elif ball_pocketed is not None:
            self.game_log[self.game_log_iterator] = f'{self.current_shooter} pockets ball {ball_pocketed} on the break'
        else:
            self.switch_turn()
            self.game_log[self.game_log_iterator] = f'No balls pocketed on the break. Turn switches to {self.current_shooter}'

        self.game_log_iterator += 1
        if self.is_game_over():
            self.end_game()

    def pocket_ball(self, ball_number):
        if not (1 <= ball_number <= 15):
            raise ValueError('Invalid ball number')

        if self.match_winner:
            raise ValueError('The game is already over')

        if ball_number == 8:
            self.match_winner = self.current_shooter
        elif ball_number == 0:
            self.switch_turn()
            self.current_shooter_defensive_shot += 1
        else:
            if self.current_shooter == self.player1_name:
                self.eightball_pocketing_context = 'player1'
            elif self.current_shooter == self.player2_name:
                self.eightball_pocketing_context = 'player2'

        self.game_log[self.game_log_iterator] = f'Player {self.current_shooter} pocketed ball {ball_number}'
        self.game_log_iterator += 1
        self.switch_turn()
        if self.is_game_over():
            self.end_game()

    def switch_turn(self):
        if self.current_shooter == self.player1_name:
            self.current_shooter = self.player2_name
        else:
            self.current_shooter = self.player1_name

    def is_game_over(self):
        if self.match_winner:
            return True
        return False

    def end_game(self):
        self.match_end_timestamp = time.time()
        self.game_log[self.game_log_iterator] = f'Player {self.current_shooter} wins the game'
        self.game_log_iterator += 1


class NineballGame:
    def __init__(self, game="nineball", break_shot=True, break_and_run=False, current_shooter=None, inning_total=0, lag_winner=None, nineball_rack=[1, 2, 3, 4, 5, 6, 7, 8, 9], nineball_rack_count=0,
                inning_count_at_rack_start=0, rack_breaking_player=None, dead_balls=[], player_1_balls_pocketed=[], player_2_balls_pocketed=[], match_winner=None):
        
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

    def to_json(self):
        game_state = {
            "game": self.game,
            "break_shot": self.break_shot,
            "break_and_run": self.break_and_run,
            "current_shooter": self.current_shooter,
            "inning_total": self.inning_total,
            "lag_winner": self.lag_winner,
            "nineball_rack": self.nineball_rack,
            "nineball_rack_count": self.nineball_rack_count,
            "inning_count_at_rack_start": self.inning_count_at_rack_start,
            "rack_breaking_player": self.rack_breaking_player,
            "dead_balls": self.dead_balls,
            "player_1_balls_pocketed": self.player_1_balls_pocketed,
            "player_2_balls_pocketed": self.player_2_balls_pocketed,
            "match_winner": self.match_winner
        }
        return json.dumps(game_state)

    @staticmethod
    def from_json(json_str):
        game_state = json.loads(json_str)
        return NineballGame(**game_state)
