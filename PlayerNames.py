# RBI Baseball 3 - ROM Modifier
# Chet Collins
# November 2013

from Values import *

class PlayerNames(dict):
    """ Two way map to relate alphanumeric characters and hex values
    """
    filename = ROOT_DIRECTORY + "data_files/player_name_map.txt"

    def __init__(self):
        """
        load dictionary values from file
        @return:
        """
        super(PlayerNames,self).__init__()
        with open(self.filename) as my_file:
            for line in my_file:
                key, value = line.partition("\t")[::2]
                self.__setitem__(str(key).strip(), str(value).strip())

    def __len__(self):
        """
        @return: the length of the dictionary
        """
        return dict.__len__(self)/2

    def __setitem__(self, key, value):
        """
        Two-way dictionary functions
        @param key: lookup key/value
        @param value: lookup key/value
        @return: the key or value
        """
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)

    def hex_to_alpha(self, hex_string):
        """
        Given a hex string, return the alphanumeric equivalent
        @param hex_string:
        @return: alphanumeric string
        """
        name = ""
        for (hex_part1,hex_part2) in zip(hex_string[0::2],hex_string[1::2]):
            hex_part1 += hex_part2
            if hex_part1 == "24":
                name += " "
            name += str(self.get(hex_part1))
        return name

    def alpha_to_hex(self, alpha_string):
        """
        Given an alpha string, return the hex equivalent
        @param alpha_string: the string to convert
        @return: hex string
        """
        name = ""
        for char in alpha_string:
            if char != " ":
                name += str(self.get(char))
            else:
                name += "24"
        return name




