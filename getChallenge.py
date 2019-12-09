#!/usr/bin/env python3

import sys
import math
import pprint

pp = pprint.PrettyPrinter(indent=4)

from problems import *
from teams import *
from chair_result import *
from jury_result import *
from rules import *

fight_number = int(sys.argv[1])
round_number = int(sys.argv[2])

reported_problems = {}

for t in list(teams.keys()):
    reported_problems.update({
        t : []
        })

for f in range(0, fight_number):
    max_round = 3

    if f == ( fight_number - 1 ):
        max_round = round_number-1

    for r in range(0, max_round):
        this_problem = chair_result_fights[f]["rounds"][r]["problem"]
        this_rep_team = chair_result_fights[f]["team_order"][r]
        reported_problems[this_rep_team].append(this_problem)

reporter_team = chair_result_fights[fight_number-1]["team_order"][round_number-1]
print("Team " + reporter_team + " reported already " + str(reported_problems[reporter_team]))
print("Out of " + str(teams[reporter_team]["problems"]))
