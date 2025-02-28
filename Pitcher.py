# RBI Baseball 3 - ROM Modifier
# Chet Collins
# November 2013

from Values import *

class Pitcher(object):
    """  A representation of a Pitcher from RBI3
    """

    def __init__(self,offset,staff_pos,name,sinker_val,style,era,sink_spd,reg_spd,fast_spd,
                 left_curve,right_curve,stamina,cpu_field1,cpu_field2):
        self.offset = offset
        self.staff_pos = staff_pos
        self.name = name
        self.sinker_val = sinker_val
        self.style = style
        self.era = era
        self.sink_spd = sink_spd
        self.reg_spd = reg_spd
        self.fast_spd = fast_spd
        self.left_curve = left_curve
        self.right_curve = right_curve
        self.stamina = stamina
        self.cpu_field1 = cpu_field1
        self.cpu_field2 = cpu_field2

    def __str__(self):
        """
        @return: a string representation of a pitcher
        """
        #(str(hex(self.offset//2)) + '\t'+
        return str(self.staff_pos) + '\t'+ \
            self.name.strip() + '\t'+ \
            str(self.sinker_val) + '\t'+ \
            str(self.style) + '\t'+ \
            str(self.era) + '\t'+ \
            str(self.sink_spd) + '\t'+ \
            str(self.reg_spd) + '\t'+ \
            str(self.fast_spd) + '\t'+ \
            str(self.left_curve) + '\t'+ \
            str(self.right_curve) + '\t'+ \
            str(self.stamina) + '\t'+ \
            str(self.cpu_field1) + '\t'+ \
            str(self.cpu_field2)+ '\n'


class ERA_helper(dict):
    """
    This is a function that helps turn .csv-supplied ERA values into valid hex values.
    A reverse dictionary-style function is not really required, since the lookup is easy.
    Brahm Neufeld Dec 31 2013
    """
    filename = ROOT_DIRECTORY + "data_files/era_lookup_table.txt"

    def __init__(self):
        """
        load values from file
        key = hex corresponding to ERA lookup logic
        value = decimal ERA value
        @return:
        """
        super(ERA_helper,self).__init__()
        with open(self.filename) as my_file:
            for line in my_file:
                key, value = line.partition("\t")[::2]
                self.__setitem__(str(key).strip(), float(value))

    def __setitem__(self, key, value):
        """
        Two-way dictionary functions
        @param key: lookup key/value
        @param value: lookup key/value
        @return: the key or value
        """
        #dict.__setitem__(self, key, value)
        # I don't think we need a 2-way dictionary here - uncommenting this breaks
        dict.__setitem__(self, value, key)

    def decimal_era_to_hex(self, decimal_era):
        """
        take a decimal ERA and return the nearest hex value based on the era_lookup_table
        (the era_lookup_table should match what is in the ROM file)
        thanks stackoverflow http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-some-value/12141207#12141207
        """
        #given a bunch of ERA keys, look up the hex value
        value = min(self.keys(), key=lambda x:abs(x-decimal_era))
        # return the value
        return str(self.get(value))
