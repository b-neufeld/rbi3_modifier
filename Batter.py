# RBI Baseball 3 - ROM Modifier
# Chet Collins
# November 2013

# a representation of a batter from RBI3


class Batter(object):
    """ A representation of an RBI3 Batter
    """
    def __init__(self,offset,lineup_pos,name,stance,batting_avg,home_runs,
                 contact,power1,power2,speed,position,switch):
        self.offset = offset
        self.lineup_pos = lineup_pos
        self.name = name
        self.stance = stance
        self.batting_avg = batting_avg
        self.home_runs = home_runs
        self.contact = contact
        self.power1 = power1
        self.power2 = power2
        self.power = power1 + (power2*256)
        self.speed = speed
        self.position = position
        self.switch = switch

    def __str__(self):
        """
        @return: a string representation of a batter
        """
        #(str(hex(self.offset//2)) + '\t'+
        return str(self.lineup_pos) + '\t'+ \
            self.name.strip() + '\t'+ \
            str(self.stance) + '\t'+ \
            str(self.batting_avg) + '\t'+ \
            str(self.home_runs) + '\t'+ \
            str(self.contact) + '\t'+ \
            str(self.power) + '\t'+ \
            str(self.speed) + '\t'+ \
            str(self.position) + '\t'+ \
            str(self.switch) + '\n' \





