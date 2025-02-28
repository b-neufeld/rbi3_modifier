# RBI Baseball 3 - ROM Modifier
# Chet Collins
# November 2013

from PlayerEditHelper import *

class PlayersData():
    """ Abstraction of the list of all Pitchers and Batters
        And ERA tables
    """
    pitchers = {}
    batters = {}
    era_table = {}

    def __init__(self,data):
        self.load_players(data)

    def get_era_tables(self, data):
        """
        Load all ERA tables from the ROM file and format properly
        @param data: data from the ROM file
        @param start: start address
        @param end: end address
        208: number of possible ERA values based on table size in 2005/2013 ROM
        """
        era_table_12 = data[ERA_DIGITS12_S1:ERA_DIGITS12_E1+2]
        era_table_3 = data[ERA_DIGIT3_S1:ERA_DIGIT3_E1+2]

        # for each ERA value (208 total based on dimensions of table...
        for offset in range(0, era_table_3.__len__()):
            # build a valid 3-digit ERA, including period, of the form 1.23, and store in array object
            self.era_table[offset] = era_table_12[offset*2]+'.'+era_table_12[offset*2+1]+era_table_3[offset]
        # uncomment for testing.
        #print(self.era_table)

    def get_pitcher_block(self,data,start,end):
        """
        Load all Pitchers from ROM file
        @param start: start address
        @param end: end address
        @return:
        ERA table is passed to create_pitcher
        """
        for offset in range(start,end,PLAYER_LEN):
            if not PlayerEditHelper().invalid_entry(PlayerEditHelper().get_substring(data,offset)):
                self.pitchers[offset] = PlayerEditHelper().create_pitcher(PlayerEditHelper().get_substring(data,offset),
                                                                          offset,self.era_table)

    def get_batter_block(self, data, end, start):
        """
        Load all Batters from ROM file
        @param data: data from the ROM file
        @param start: start address
        @param end: end address
        @return:
        """
        for offset in range(start,end,PLAYER_LEN):
            self.batters[offset] = PlayerEditHelper().create_batter(PlayerEditHelper().get_substring(data,offset),offset)

    def load_players(self,data):
        """
        Load players from their defined memory addresses
        @return:
        """
        # loading era tables - must be before pitchers.
        self.get_era_tables(data)

        # loading batters
        self.get_batter_block(data, BATTER_E1, BATTER_S1)
        self.get_batter_block(data, BATTER_E2, BATTER_S2)
        #print("Batters: "+str(len(self.batters)))

        # loading pitchers
        self.get_pitcher_block(data,PITCHER_S1,PITCHER_E1)
        self.get_pitcher_block(data,PITCHER_S2,PITCHER_E2)
        #print("Pitchers: "+str(len(self.pitchers)))
