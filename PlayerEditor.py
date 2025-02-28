# RBI Baseball 3 - ROM Modifier
# Chet Collins
# November 2013



from PlayersData import *
from Validator import *
import binascii
import time
import re
game_file = ""      # see comments on this var in __init__

class PlayerEditor():
    """ Provides the ability to convert players to and from their hex strings, and update players on the ROM file
    """
    def __init__(self,filename):
        # open the ROM file - changed to read in binary mode, so we can open a .nes file. Also changed to read-only.
        with open(filename, "rb") as my_file:
            # str(binascii.hexlify()) creates a text string of hex, as if we'd opened a .txt file.
            # the rstrip and lstrip take out the binary "b" prefix and single quote marks that get added
            # upper() will make all of the hex uppercase; this plays nice with the character lookup
            self.data = str(binascii.hexlify(my_file.read())).rstrip("'").lstrip("b'").upper()
            #print(self.data)
            # global variables are bad, any smart ideas to get this filename to the replace_player() function?
            global game_file
            game_file = filename

        # loading players from initial ROM data
        self.players = PlayersData(self.data)

    def __str__(self):
        """
        @return: list of all Pitchers and Batters
        """
        return self.display_batters() + self.display_pitchers() + self.display_team_params() \
               + self.display_rom_base_year()

    def display_pitchers(self):
        """
        @return: A list of Pitchers in order
        """
        data = ":(pitchers)DONT CHANGE,lineup# DONT CHANGE,Name,SinkerVal,Stance,ERA," \
               "SinkSpd,RegSpd,FastSpd,LCurve,RCurve,Stamina,CPU1,CPU2\n"
        # commenting out the archive teams so they don't clutter up the .csv export file
        # can always remove this comment in the future.
        """
        i = PITCHER_S1
        while i < PITCHER_E1:
            if not PlayerEditHelper().invalid_entry(PlayerEditHelper().get_substring(self.data,i)):
                data += FileProcessor().convert_csv(
                    str(PlayerEditHelper().get_team_id(self.players.pitchers[i])) + "\t" + str(self.players.pitchers[i]))
            i += PLAYER_LEN
        """
        i = PITCHER_S2
        while i < PITCHER_E2:
            if not PlayerEditHelper().invalid_entry(PlayerEditHelper().get_substring(self.data,i)):
                data += FileProcessor().convert_csv(
                    str(PlayerEditHelper().get_team_id(self.players.pitchers[i])) + "\t" + str(self.players.pitchers[i]))
            i += PLAYER_LEN
        return data

    def display_batters(self):
        """
        @return: A list of Batters in order
        """
        data = ":(batters)DONT CHANGE,lineup# DONT CHANGE,Name,Stance,BA,HR,Contact," \
               "Power,Speed,FieldingPos,Switch\n"
        # commenting out the archive teams so they don't clutter up the .csv export file
        # can always remove this comment in the future.
        """
        i = BATTER_S1
        while i < BATTER_E1:
            data += FileProcessor().convert_csv(
                str(PlayerEditHelper().get_team_id(self.players.batters[i])) + "\t" + str(self.players.batters[i]))
            i += PLAYER_LEN
        """
        i = BATTER_S2
        while i < BATTER_E2:
            data += FileProcessor().convert_csv(
                str(PlayerEditHelper().get_team_id(self.players.batters[i])) + "\t" + str(self.players.batters[i]))
            i += PLAYER_LEN
        return data

    def display_team_params(self):
        """
        @return: A list of team parameters like error %, uniform colour options,
        """
        data = ":(team_params)TeamID DONT CHANGE,Initials DONT CHANGE,OutlineCol(00-3F),PantsCol(00-3F)," \
               "JerseyCol(00-3F),TeamErrorPct(to nearest 0.39)\n"
        # loop through teams 31 to 60. In the future we can change this to 1-60.
        i = 31
        while i <= 60:
            data += FileProcessor().convert_csv(
                str(i) + "\t" +
                str(PlayerEditHelper().get_team_initials(str(i))) + "\t" +
                str(PlayerEditHelper().get_team_uniform_colours(self.data,str(i))) + "\t" + \
                str(PlayerEditHelper().get_team_error_percent(self.data, str(i))) + "\n")
            i += 1
        return data

    def display_rom_base_year(self):
        """
        @return: a single two-digit value (00-99) for the "base" year that is displayed in the ROM
        re.sub takes out a pair of parenthesis from the get_rom_year return string.
        """
        data = ":(ROM_year) Digit 1 (0-9), Digit 2 (0-9)\n"
        data += FileProcessor().convert_csv(
            re.sub('[(\')]', '', str(PlayerEditHelper().get_rom_year(self.data))) + "\n"
        )
        return data

    def write_file(self, file_path):
        FileProcessor().write_output(self.__str__(), file_path)

    def write_game_file(self, filename):
        FileProcessor().write_nes_file(self.data, filename)

    def import_new_data(self, csv_file):
        """
        Read in all Pitcher and Batter data from csv file
        @return:
        """
        new_data = FileProcessor().read_csv_file(csv_file)


        for line in new_data:
            if ":(batters)" in line:

                read_in = "bats"
            if ":(pitchers)" in line:
                read_in = "pitch"
            if ":(team_params)" in line:
                read_in = "team_params"
            if ":(ROM_year)" in line:
                read_in = "rom_year"

            if read_in == "bats" and ":(batters)" not in line:
                # split the .csv line into a small array
                values = [x.strip() for x in line.split(',')]

                if not is_valid_batter(values):
                    #TO DO write error log
                    for text in is_valid_batter(values):
                        print(text)
                else:
                    #print("Valid batter found!\n")
                    self.valid_batter_from_csv(values)

            if read_in == "pitch" and ":(pitchers)" not in line:
                # split the .csv line into a small array
                values = [x.strip() for x in line.split(',')]

                if not is_valid_pitcher(values):
                    for text in is_valid_pitcher(values):
                        print(text)
                else:
                    #print("Valid pitcher found!\n")
                    self.valid_pitcher_from_csv(values)

            if read_in == "team_params" and ":(team_params)" not in line:
                # split the .csv line into a small array
                values = [x.strip() for x in line.split(',')]
                self.valid_team_from_csv(values)
                # TODO: FIX VALIDATION LATER
                """
                if not is_valid_team(values):
                    for text in is_valid_team(values):
                        print(text)
                else:
                    print("Valid team found!\n")
                    self.valid_team_from_csv(values)
                """

            if read_in == "rom_year" and ":(ROM_year)" not in line:
                # split the .csv line into a small array - this will be two values, one for each digit
                values = [x.strip() for x in line.split(',')]
                # validation - if both values are in the list of valid year digits (as strings)
                if values[0] in YEAR_LOOKUP_INT and values[1] in YEAR_LOOKUP_INT:
                    self.valid_base_year_from_csv(values)
                # else, set values equal to the current year and go.
                else:
                    values = [str(time.strftime("%y")[:1]), str(time.strftime("%y")[-1:])]
                    self.valid_base_year_from_csv(values)

        # re-initialize self.players based on new players
        self.players = PlayersData(self.data)

    def valid_team_from_csv(self, values):
        """
        take valid team data and insert it into the ROM file.
        TO DO: clean this up a little bit.
        """
        uniform_offset = PlayerEditHelper().get_team_uniform_colour_offset(int(values[0]))
        self.replace_nonplayer_data(str(values[2]).rjust(2,'0') +
                                    str(values[3]).rjust(2,'0') +
                                    str(values[4]).rjust(2,'0'), uniform_offset)
        error_pct_offset = PlayerEditHelper().get_team_error_offset(int(values[0]))

        # TO DO: turn this logic into a function
        int_error = int(round(float(values[5])/100*255,0))
        error_hex = PlayerEditHelper().hex_format(int_error,2)
        self.replace_nonplayer_data(error_hex,error_pct_offset)

    def valid_base_year_from_csv(self, values):
        """
        There are a few places in the ROM where we have to update the year.
        """
        hex_digit_1 = YEAR_LOOKUP_HEX[(YEAR_LOOKUP_INT.index(values[0]))]
        hex_digit_2 = YEAR_LOOKUP_HEX[(YEAR_LOOKUP_INT.index(values[1]))]
        # replace P1 base year in two locations
        self.replace_nonplayer_data(hex_digit_1 + hex_digit_2, BASE_YEAR_P1_A)
        self.replace_nonplayer_data(hex_digit_1 + hex_digit_2, BASE_YEAR_P1_B)
        # replace P2 base year in two locations
        self.replace_nonplayer_data(hex_digit_1 + hex_digit_2, BASE_YEAR_P2_A)
        self.replace_nonplayer_data(hex_digit_1 + hex_digit_2, BASE_YEAR_P2_B)
        # replace "second line" year in two locations (one digit per location)
        self.replace_nonplayer_data(hex_digit_1, BASE_YEAR_CHAR_1)
        self.replace_nonplayer_data(hex_digit_2, BASE_YEAR_CHAR_2)

    def valid_pitcher_from_csv(self, values):
        # check for what teamID and decide what offset to use
        self.update_player(Pitcher(PlayerEditHelper().get_pitcher_offset(int(values[0]), int(values[1])),
                    int(values[1]), PlayerEditHelper().name_check(values[2]), int(values[3]), int(values[4]),
                    float(values[5]), int(values[6]), int(values[7]), int(values[8]), int(values[9]),
                    int(values[10]), int(values[11]), int(values[12]), int(values[13])))

    def valid_batter_from_csv(self, values):
        # check for what teamID and decide what offset to use
        self.update_player(Batter(PlayerEditHelper().get_batter_offset(int(values[0]), int(values[1])),
                    int(values[1]), PlayerEditHelper().name_check(values[2]), int(values[3]), int(values[4]),
                    int(values[5]), int(values[6]), int(values[7])%256, int(values[7])//256, int(values[8]),
                    int(values[9]), int(values[10])))

    def replace_nonplayer_data(self,string,offset):
        """
        @param string: Player to be replaced in the ROM file
        @param offset: address within the ROM file
        @param length: length of string to be replaced
        @return:
        """
        length = len(str(string))
        offset = int(offset)
        string = str(string)
        self.data = self.data[0:offset] + string + self.data[offset+length:]

    def replace_player(self,string,offset):
        """
        @param string: Player to be replaced in the ROM file
        @param offset: address within the ROM file
        @return:
        """
        #remove print after debugging
        #print(str(offset)+" "+string)
        self.data = self.data[0:offset] + string + self.data[offset+PLAYER_LEN:]
        #print(self.data[offset:offset+PLAYER_LEN])

    def update_player(self,player):
        """
        Update a player and write to ROM file
        @param player: Player to be updated
        @return:
        """
        update_string = ""
        if isinstance(player,Batter):
            #print('Batter found!')
            update_string = PlayerEditHelper().batter_convert(player)
        elif isinstance(player,Pitcher):
            update_string = PlayerEditHelper().pitcher_convert(player)
            #print('Pitcher found!')
        self.replace_player(update_string,player.offset)






