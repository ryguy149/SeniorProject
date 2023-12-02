#File for constant varriabes present in the program
#if therte is not enough input text the feature number needs to be lowered
import random

FEATURE_NUMBER = 55

subredditList = ["buildapc", "gaming", "politics", "shortstories", "witcher", "Showerthoughts", "worldnews", "todayilearned", "mildlyintresting", "soccer", "india"]

#SUBREDIT_SELECTION = random.choice(subredditList)
#print(SUBREDIT_SELECTION)
SUBREDIT_SELECTION = "buildapc"

AMMOUNT_TEXT = 0

NUMBEROFPULLS = 10

def init():
    global redditBool
    redditBool = False