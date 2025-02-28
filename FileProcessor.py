# RBI Baseball 3 - ROM Modifier
# Chet Collins
# November 2013

import time
import binascii

class FileProcessor():
    """ Provides ability to read from, and write to csv files
    """
    output = "output.csv"
    input = "static/2013_roster_v1.4.csv"

    def convert_csv(self,player):
        """
        @param player: A Batter or Pitcher
        @return: a csv-style string representing a Player
        """
        return ",".join(player.split('\t'))

    def write_output(self, data, filename):
        """
        @param data: text to be written - typically for .csv files
        @return:
        """
        with open(filename, "w+") as output_file:
            output_file.write(data)
            output_file.close()

    def read_csv_file(self, csv_file):
        with open(csv_file,"r") as input_file:
            return [line.rstrip() for line in input_file]

    def write_nes_file(self,data, filename):
        with open(filename, "wb") as f:
            nes_file = data.rstrip("'").lstrip("b'")
            #print(nes_file)
            f.write(binascii.unhexlify(nes_file))
            f.close()

    def write_error_log(self,data):
        """
        @param data: the error data to be written
        @return:
        """
        with open(time.strftime("%Y-%m-%d_%H-%M-%S") + "-error-log", "wb") as error_log:
            error_log.write(data)
            error_log.close()

