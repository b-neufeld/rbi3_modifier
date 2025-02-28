# RBI Baseball 3 - ROM Modifier
# Chet Collins
# November 2013

"""
TeamID
Team
Outline
Pitcher Pants
Jersey
Batter Offset
Pitcher Offset
Team Error%
Team Years
"""

from Team import *
from Values import *

class TeamsData(object):
    """ Contains data parameters for all RBI3 teams
    """
    filename = ROOT_DIRECTORY + "data_files/teams.txt"
    values = {}

    def __init__(self):
        """
        Loads Team values from file
        @return: a container of TeamsData
        """
        with open(self.filename) as teams_data:
            for line in teams_data:
                data_list = line.split(",")
                self.values.__setitem__(str(data_list[0]), Team(data_list))

    def __str__(self):
        """
        @return: a string representation of TeamsData
        """
        data = ""
        i = 1
        while i <= len(self.values):
            data += str(self.values[str(i)])
            i += 1
        return data
