# RBI Baseball 3 - ROM Modifier
# Chet Collins
# November 2013

from Values import *
from Batter import *
from Pitcher import *
from PlayerNames import *
from TeamsData import *
from FileProcessor import *

class PlayerEditHelper():
    """ Player editing helper functions
    """
    def batter_convert(self, batter):
        """
        Convert a batter to an equivalent hex string
        @param batter: Batter to convert
        @return: a Batter converted from hex
        """
        return self.hex_format(batter.lineup_pos,2) + \
        PlayerNames().alpha_to_hex(batter.name[:6]) + \
        self.hex_format(batter.stance,2) + \
        self.hex_format(batter.batting_avg-111,2) + \
        self.hex_format(batter.home_runs,2) + \
        self.hex_format(batter.contact,2) + \
        self.hex_format(batter.power1,2) + \
        self.hex_format(batter.power2,2) + \
        self.hex_format(batter.speed,2) + \
        self.hex_format(batter.position,2) + \
        self.hex_format(batter.switch,2) + \
        PlayerNames().alpha_to_hex(batter.name[6:])

    def pitcher_convert(self, pitcher):
        """
        Convert a Pitcher to an equivalent hex string
        @param pitcher: Pitcher to convert
        @return: a Pitcher converted from hex
        OLD line: self.hex_format(pitcher.era,2) + \
        """
        #to do: this is where an ERA lookup has to happen... given a decimal ERA, look up the best hex.
        return self.hex_format(pitcher.staff_pos,2) + \
        PlayerNames().alpha_to_hex(pitcher.name[:6]) + \
        self.hex_format(pitcher.sinker_val,1) + \
        self.hex_format(pitcher.style,1) + \
        ERA_helper().decimal_era_to_hex(pitcher.era) + \
        self.hex_format(pitcher.sink_spd,2) + \
        self.hex_format(pitcher.reg_spd,2) + \
        self.hex_format(pitcher.fast_spd,2) + \
        self.hex_format(pitcher.left_curve,1) + \
        self.hex_format(pitcher.right_curve,1)+ \
        self.hex_format(pitcher.stamina,2) + \
        self.hex_format(pitcher.cpu_field1,2) + \
        self.hex_format(pitcher.cpu_field2,2)+ \
        PlayerNames().alpha_to_hex(pitcher.name[6:])

    def create_batter(self,data,offset):
        """
        create a Batter from ROM file
        @param data: hex Batter data
        @param offset: starting address in ROM file
        @return: a new Batter
        """
        lineup_pos = self.hex_to_int(data,0,2)
        name = PlayerNames().hex_to_alpha(data[2:14]+data[32:36])
        stance = self.hex_to_int(data,14,16)
        batting_avg = 111+self.hex_to_int(data,16,18)
        home_runs = self.hex_to_int(data,18,20)
        contact = self.hex_to_int(data,20,22)
        power1 = self.hex_to_int(data,22,24)
        power2 = self.hex_to_int(data,24,26)
        speed = self.hex_to_int(data,26,28)
        position = self.hex_to_int(data,28,30)
        switch = self.hex_to_int(data,30,32)
        return Batter(offset,lineup_pos,name,stance,batting_avg,home_runs,contact,
                      power1, power2,speed,position,switch)

    def create_pitcher(self,data,offset,era_table):
        """
        create a Pitcher from ROM file
        @param data: hex Pitcher data
        @param offset: starting address in ROM file
        @param era_table: an array of all possible ERA values, read from the ROM file. Not efficient but hey.
        @return: a new Pitcher
        """
        staff_pos = self.hex_to_int(data,0,2)
        name = PlayerNames().hex_to_alpha(data[2:14]+data[32:36])
        sinker_val = self.hex_to_int(data,14,15)
        style = self.hex_to_int(data,15,16)
        era = self.hex_to_ERA(data,16,18,era_table)
        sink_spd = self.hex_to_int(data,18,20)
        reg_spd = self.hex_to_int(data,20,22)
        fast_spd = self.hex_to_int(data,22,24)
        left_curve = self.hex_to_int(data,24,25)
        right_curve = self.hex_to_int(data,25,26)
        stamina = self.hex_to_int(data,26,28)
        cpu_field1 = self.hex_to_int(data,28,30)
        cpu_field2 = self.hex_to_int(data,30,32)
        return Pitcher(offset,staff_pos,name,sinker_val,style,era,sink_spd,reg_spd,
                       fast_spd,left_curve,right_curve,stamina,cpu_field1,cpu_field2)

    def get_team_id(self,player):
        """
        @param player: the Player whose team id we are looking for
        @return: the Players team id
        """
        for key,team in TeamsData().values.items():
            if isinstance(player,Pitcher):
                if team.pitcher_offset <= player.offset < team.pitcher_offset+(PLAYER_LEN*PITCHERS_PER_TEAM):
                    return team.team_id
            elif isinstance(player,Batter):
                if team.batter_offset <= player.offset < team.batter_offset+(PLAYER_LEN*BATTERS_PER_TEAM):
                    return team.team_id

    def get_pitcher_offset(self, team_id, staff_pos):
        """
        @param team_id: the team id of the Pitcher
        @param staff_pos: the staff position of the Pitcher
        @return: the offset where the Pitcher is to be written
        """
        return TeamsData().values[str(team_id)].pitcher_offset + (staff_pos - STAFF_POS_START)*PLAYER_LEN

    def get_team_initials(self,team_id):
        """
        @param team_id: the team id of a team
        @return: the initials of the team
        """
        return TeamsData().values[str(team_id)].team_text

    def get_rom_year(self, data):
        """
        @return: return "base year" of the ROM, as two integers (0-9, 0-9)
        two integers will make writing the reverse function much easier
        """
        # length for get_substring_nonplayer is 4 since we're looking for 2 hex pairs
        hex_digit_1 = PlayerEditHelper().get_substring_nonplayer(data, BASE_YEAR_P1_A, 2)
        hex_digit_2 = PlayerEditHelper().get_substring_nonplayer(data, BASE_YEAR_P1_A + 2, 2)
        # get the integer representations based on the hex
        digit_1 = YEAR_LOOKUP_INT[YEAR_LOOKUP_HEX.index(hex_digit_1)]
        digit_2 = YEAR_LOOKUP_INT[YEAR_LOOKUP_HEX.index(hex_digit_2)]
        return digit_1, digit_2

    def get_team_uniform_colours(self,data,team_id):
        """
        @param team_id: the team id of a team
        @return: a tab-delimited string of the three uniform values.
        """
        offset_int = self.get_team_uniform_colour_offset(team_id)
        value = PlayerEditHelper().get_substring_nonplayer(data,offset_int,UNIFORM_DATA_LEN)
        return value[:2] + "\t" + \
               value[2:-2] + "\t" + \
               value[-2:]

    def get_team_uniform_colour_offset(self,team_id):
        """
        @param team_id: the team id of a team
        @return: the integer offset of the uniform colours
        """
        return int(str(TeamsData().values[str(team_id)].outline).replace("h",""),16)*2

    def get_team_error_percent(self,data,team_id):
        """
        @param team_id: the team id of a team
        @param data: the self.data data object from PlayerEditor.py
        @return: the error percentage of a team
        """
        # strip off "h", convert to an offset
        offset_int = self.get_team_error_offset(team_id)
        value = PlayerEditHelper().get_substring_nonplayer(data,offset_int, ERROR_PCT_LEN)
        value = float(int(value,HEX_BASE))/255*100
        value = str("%.2f" % value)
        return value

    def get_team_error_offset(self,team_id):
        """
        @param team_id: the team id of a team
        @return: the integer offset of a team
        """
        return int(str(TeamsData().values[str(team_id)].team_error).replace("h",""),HEX_BASE)*2

    def get_batter_offset(self, team_id, lineup_pos):
        """
        @param team_id: the team id of the Batter
        @param lineup_pos: the lineup position of the Batter
        @return: the offset where the Batter is to be written
        """
        return TeamsData().values[str(team_id)].batter_offset + lineup_pos*PLAYER_LEN

    def hex_to_int(self,data,start,end):
        """
        Convert a hex value to an integer
        @param data: the hex string containing data
        @param start: start index
        @param end: end index
        @return: the integer value
        """
        return int(data[start:end],HEX_BASE)

    def hex_format(self,value,precision):
        """
        format a hex string to conform to ROM file standards
        @param value: hex string to be formatted
        @param precision: number of decimal places
        @return: a formatted hex string
        """
        return str(hex(value)).lstrip('0x').zfill(precision).upper()

    def hex_to_ERA(self,data,start,end,era_table):
        """
        take a hex ERA value, convert to int and perform the lookup on the 2 ERA tables
        @param data: the hex string containing data
        @param start: start index
        @param end: end index
        returns: A 3-digit ERA in the form 1.23
        Basically the same as hex_to_int but a little fancier
        ALSO: kind of inefficient passing the whole ERA table to each and every pitcher,
              but I'm not a smart man, Jenny...... Jembleee....., Jambourine...........
        """
        return era_table[int(data[start:end], 16)]

    def invalid_entry(self,data):
        """
        Test for a valid entry
        @param data: the entry to be tested
        @return: if line contains valid data
        """
        return int(data,HEX_BASE) == 0

    def get_substring(self,data,offset):
        """
        @param data: the source from which to extract the substring
        @param offset: the starting offset
        @return: a substring containing a player
        """
        return data[offset:offset+PLAYER_LEN]

    def get_substring_nonplayer(self,data,offset,length):
        """
        get_substring is set up to only grab something by player length...
        this function can grab something by any length
        @param data: the source from which to extract the substring
        @param offset: the starting offset
        @param length: the length to offset
        @return: a substring containing a player
        """
        return data[offset:offset+length]

    def name_check(self,data):
        """
        check that a name is properly padded with spaces
        see http://stackoverflow.com/questions/5676646/fill-out-a-python-string-with-spaces
        """
        return data.ljust(NAME_LEN)
