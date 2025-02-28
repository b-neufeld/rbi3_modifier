# web values
# ROOT_DIRECTORY - set to an empty string when running on a local machine.
# May also have to go around and switch to back/forward slashes depending on run environment :'(
ROOT_DIRECTORY = r'D:\Inetpub\vhosts\brahm.ca\httpdocs\rbi\\'
# for file_upload.py and csv_from_nes.py
UPLOAD_FOLDER = "http://www.brahm.ca/rbi/upload/"

# Constant address values and sizes
HEX_BASE = 16

# size of each player object
PLAYER_LEN = 36
NAME_LEN = 8
PITCHERS_PER_TEAM = 10
BATTERS_PER_TEAM = 14

# size of some team objects
ERROR_PCT_LEN = 2
UNIFORM_DATA_LEN = 6

# start and end addresses of Batter and Pitcher blocks
BATTER_S1 = int('0010',16)*2
BATTER_E1 = int('01D97',16)*2
BATTER_S2 = int('16010',16)*2
BATTER_E2 = int('17D98',16)*2
PITCHER_S1 = int('12010',16)*2
PITCHER_E1 = int('13D4F',16)*2
PITCHER_S2 = int('18010',16)*2
PITCHER_E2 = int('19D4F',16)*2

# start and end of ERA pitching tables (**2005/2013 ROM** - ROM file must be patched prior to running ERA changes)
ERA_DIGITS12_S1 = int('19D88',16)*2
ERA_DIGITS12_E1 = int('19E57',16)*2
ERA_DIGIT3_S1 = int('19F48',16)*2
ERA_DIGIT3_E1 = int('19FAF',16)*2

# offsets for base years in the file - ie, 90 in original, 05 in AndyB mod, 13 in our mod
# these years appear in the first line of the team select screen
BASE_YEAR_P1_A = int('986E',16)*2  # 2 bytes
BASE_YEAR_P1_B = int('98CB',16)*2  # 2 bytes
BASE_YEAR_P2_A = int('987E',16)*2  # 2 bytes
BASE_YEAR_P2_B = int('98D0',16)*2  # 2 bytes
# these years appear in the second line of the team select screen - when scrolling through archive teams.
BASE_YEAR_CHAR_1 = int('1482A',16)*2 # "9" in original - 1 byte
BASE_YEAR_CHAR_2 = int('14830',16)*2 # "0" in original - 1 byte. Increments mathematically.
# these are the arrays for year lookups
YEAR_LOOKUP_HEX = ["18", "19", "1A", "1B", "1C", "1D", "1E", "1F", "20", "21"]
YEAR_LOOKUP_INT = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Validation for Team, Pitcher, and Batters

# Team value ranges
TEAM_ID_MIN = 1
TEAM_ID_MAX = 60

# Pitcher value ranges
PITCHER_MIN = 0
STAFF_POS_START = 14
STAFF_POS_END = 23
PITCH_ABILITY_MAX = 15
STYLE_MAX = 3
PITCH_SPD_MAX = 255
STAMINA_MAX = 255

# Batter value ranges
BATTER_MIN = 0
LINEUP_POS_END = 13
STANCE_MAX = 1
BATTING_AVG_MAX = 366
HOME_RUN_MAX = 99
CONTACT_MAX = 99
POWER_MAX = 1100
SPEED_MAX = 255
FIELD_POS_MAX = 2
SWITCH_HITTER = 1


