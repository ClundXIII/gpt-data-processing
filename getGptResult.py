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

do_finale = False

fight_number = int(sys.argv[1])

if len(sys.argv) >= 3 and sys.argv[2] == "f":
    do_finale = True

if do_finale:
    print("running until finale")
else:
    print("running until fight " + sys.argv[1])

print("")

if len(chair_result_fights) < fight_number:
    print("chair_result_fights needs at least " + str(fight_number) + " fights!")
    exit(1)
if len(juror_result_fights) < fight_number:
    print("juror_result_fights needs at least " + str(fight_number) + " fights!")
    exit(1)

longest_teamname_len = -1

print("Teams: ")
team_keys = list(teams.keys())
for t in range(0, len(teams)):
    print("  team #" + str(t) + ":")
    print("    name: " + teams[team_keys[t]]["name"] + " from " + teams[team_keys[t]]["location"])
    if len(teams[team_keys[t]]["name"]) > longest_teamname_len:
        longest_teamname_len = len(teams[team_keys[t]]["name"])
    print("    problems: ")
    for p in range(0, len(teams[team_keys[t]]["problems"])):
        print("      problem #" + "{: >2}".format(teams[team_keys[t]]["problems"][p]) + ": " + problems[teams[team_keys[t]]["problems"][p]])


print()
print()

fights_result = {
    "single_fights" : [
    ],
    "team_result" : {}
}

team_shortnames = list(teams.keys())
for i in range(0, len(team_shortnames)):
    fights_result["team_result"].update({
        (team_shortnames[i]) : {
            "score" : 0,
            "bonus" : 0    # DAVON BONUS. Nicht additiv
        }})

def get_column(data, column):

    result = []

    for i in range(0, len(data)):
        result.append(data[i][column])

    return result

for f in range(0, fight_number):
    print("fight #" + str(f+1))
    print("  team order:      1st round 2nd round 3rd round")

    if chair_result_fights[f]["team_order"] != juror_result_fights[f]["team_order"]:
        print("team order for juror and chair result is not the same!")
        exit(2)

    teamA = teams[chair_result_fights[f]["team_order"][0]]
    teamB = teams[chair_result_fights[f]["team_order"][1]]
    teamC = teams[chair_result_fights[f]["team_order"][2]]

    this_round_teams = [teamA, teamB, teamC]
    this_round_team_short = [
        chair_result_fights[f]["team_order"][0],
        chair_result_fights[f]["team_order"][1],
        chair_result_fights[f]["team_order"][2]
    ]

    print("    A: " + ("{: >" + str(longest_teamname_len) + "}").format(teamA["name"]) + " : " + team_order_placements[0][0] + " " + team_order_placements[0][1] + " " + team_order_placements[0][2])
    print("    B: " + ("{: >" + str(longest_teamname_len) + "}").format(teamB["name"]) + " : " + team_order_placements[1][0] + " " + team_order_placements[1][1] + " " + team_order_placements[1][2])
    print("    C: " + ("{: >" + str(longest_teamname_len) + "}").format(teamC["name"]) + " : " + team_order_placements[2][0] + " " + team_order_placements[2][1] + " " + team_order_placements[2][2])

    this_fight = {
        "rounds" : [],
        "score"  : {
            this_round_team_short[0] : 0,
            this_round_team_short[1] : 0,
            this_round_team_short[2] : 0
        },
        "bonus"  : {
            this_round_team_short[0] : 0,
            this_round_team_short[1] : 0,
            this_round_team_short[2] : 0
        }
    }

    for r in range(0, 3):
        print("  processing round #" + str(r+1))

        this_round = chair_result_fights[f]["rounds"][r]

        jury_amount = len(this_round["reporter"])

        reporter_data = sorted(this_round["reporter"])
        opponent_data = sorted(this_round["opponent"])
        reviewer_data = sorted(this_round["reviewer"])

        jury_data_rep = sorted(get_column(juror_result_fights[f]["rounds"][r], 0))
        jury_data_opp = sorted(get_column(juror_result_fights[f]["rounds"][r], 1))
        jury_data_rev = sorted(get_column(juror_result_fights[f]["rounds"][r], 2))

        if jury_data_rep != reporter_data:
            print("error: JURY DATA DOES NOT MATCH JUROR DATA for reporter!")
            exit(11)
        if jury_data_opp != opponent_data:
            print("error: JURY DATA DOES NOT MATCH JUROR DATA for opponent!")
            exit(12)
        if jury_data_rev != reviewer_data:
            print("error: JURY DATA DOES NOT MATCH JUROR DATA for reviewer!")
            exit(13)

        reporter_team = this_round_teams[team_order_placement_position[r]["reporter"]]
        opponent_team = this_round_teams[team_order_placement_position[r]["opponent"]]
        reviewer_team = this_round_teams[team_order_placement_position[r]["reviewer"]]

        reporter_team_short = this_round_team_short[team_order_placement_position[r]["reporter"]]
        opponent_team_short = this_round_team_short[team_order_placement_position[r]["opponent"]]
        reviewer_team_short = this_round_team_short[team_order_placement_position[r]["reviewer"]]

        print("    reporter team: " + reporter_team["name"] + " with Problem #" + str(this_round["problem"]) + " " + problems[this_round["problem"]])
        reporter_grade = getGrade(reporter_data, jury_amount)
        print("      grade: " + str(reporter_grade))
        print("      adding grade x3: " + str(reporter_grade*3))
        this_fight["score"][reporter_team_short] += reporter_grade*3

        print("    opponent team: " + opponent_team["name"])
        opponent_grade = getGrade(opponent_data, jury_amount)
        print("      grade: " + str(reporter_grade))
        print("      adding grade x2: " + str(reporter_grade*2))
        this_fight["score"][opponent_team_short] += opponent_grade*2

        print("    reviewer team: " + reviewer_team["name"])
        reviewer_grade = getGrade(reviewer_data, jury_amount)
        print("      grade: " + str(reporter_grade))
        print("      adding grade x1: " + str(reporter_grade*1))
        this_fight["score"][reviewer_team_short] += reviewer_grade*1

        this_round = {
            "problem"  : this_round["problem"],
            "reporter" : {
                "team"    : reporter_team_short,
                "grade"   : reporter_grade
            },
            "opponent" : {
                "team"    : opponent_team_short,
                "grade"   : opponent_grade
            },
            "reviewer" : {
                "team"    : reviewer_team_short,
                "grade"   : reviewer_grade
            }
        }
        this_fight["rounds"].append(this_round)

    fights_result["single_fights"].append(this_fight)

    bonus_points_first = {
        "name" : [],
        "points" : -1
    }

    bonus_points_second = {
        "name" : [],
        "points" : -1
    }

    for t in this_round_team_short:
        print("  calculating PF result for team " + t)

        # rounding with floating point is quite tricky
        # we will use a crutch to make sure we do round up 0.005 to 0.01:
        # aka using fixed-point arithmetic

        grade = this_fight["score"][t]

        grade_temp = grade * 10000

        if ((int(grade_temp) % 100) > 49) and ((int(grade_temp) % 100) < 51):
            print("!!!!!!!! WARNING: do manual confirmation of this grade !!!!!!")

        if int(grade_temp) % 100 > 50:
            grade = math.ceil(grade*100)
        else:
            grade = math.floor(grade*100)

        print("    receives " + str(grade) + "/100 points")

        fights_result["team_result"][t]["score"] += grade
        this_fight["score"][t] = grade/100

        if grade == bonus_points_first["points"]:
            bonus_points_first["name"].append(t)
        if grade > bonus_points_first["points"]:
            bonus_points_second["points"] = bonus_points_first["points"]
            bonus_points_second["name"] = bonus_points_first["name"]

            bonus_points_first["points"] = grade
            bonus_points_first["name"] = [t]
        elif grade == bonus_points_second["points"]:
            bonus_points_second["name"].append(t)
        elif grade > bonus_points_second["points"]:
            bonus_points_second["points"] = grade
            bonus_points_second["name"] = [t]

    if len(bonus_points_first["name"]) == 1:
        print("  Best Team this round " + bonus_points_first["name"][0] + " receives 2 bonus points because of " + str(bonus_points_first["points"]))
        fights_result["team_result"][bonus_points_first["name"][0]]["score"] += 2.0
        fights_result["team_result"][bonus_points_first["name"][0]]["bonus"] += 2.0
        this_fight["bonus"][bonus_points_first["name"][0]] += 2.0
        this_fight["score"][bonus_points_first["name"][0]] += 2.0

        second_places_count = len(bonus_points_second["name"])
        for second_place_team in bonus_points_second["name"]:
            print("  Second best Team this round " + second_place_team + " receives " + str(1/second_places_count) + " bonus point because of " + str(bonus_points_second["points"]))
            fights_result["team_result"][second_place_team]["score"] += 1/second_places_count
            fights_result["team_result"][second_place_team]["bonus"] += 1/second_places_count
            this_fight["bonus"][second_place_team] += 1/second_places_count
            this_fight["score"][second_place_team] += 1/second_places_count
    else:
        first_places_count = len(bonus_points_first["name"])
        for score_team in bonus_points_first["name"]:
            print("  Best Team this round " + score_team + " receives " + str(3/first_places_count) + " bonus points because of " + str(bonus_points_first["points"]))
            fights_result["team_result"][score_team]["score"] += 3/first_places_count
            fights_result["team_result"][score_team]["bonus"] += 3/first_places_count
            this_fight["bonus"][score_team] += 3/first_places_count
            this_fight["score"][score_team] += 3/first_places_count


print()
print()
print("Result:")
pp.pprint(fights_result)
print()
print()

if do_finale:
    # do finale
    print("Calculating Bonus points for finale")

print("<h1>GPT Results</h1>")

for f in range(0, fight_number):

    thisFight = fights_result["single_fights"][f]

    print("<h2>Physics fight " + str(f+1) + "</h2>")
    print("<table><tr><th>Round</th><th>Problem</th><th>Role</th><th>Team</th><th>Grade</th></tr>")

    this_fight_rounds = thisFight["rounds"]
    for r in range(0, len(this_fight_rounds)):
        this_r = this_fight_rounds[r]
        print("<tr><td>" + str(r+1) + "</td><td>" + str(this_r["problem"]) + ". " + problems[this_r["problem"]] + "</td><td>Reporter</td><td>" + teams[this_r["reporter"]["team"]]["name"] + "</td><td>" + str(round(this_r["reporter"]["grade"]*100)/100) + "</td></tr>")
        print("<tr><td></td><td></td><td>Opponent</td><td>" + teams[this_r["opponent"]["team"]]["name"] + "</td><td>" + str(round(this_r["opponent"]["grade"]*100)/100) + "</td></tr>")
        print("<tr><td></td><td></td><td>Reviewer</td><td>" + teams[this_r["reviewer"]["team"]]["name"] + "</td><td>" + str(round(this_r["reviewer"]["grade"]*100)/100) + "</td></tr>")


    print("</table>")
    print("<br/>")
    print("<h3>Team Result from this Fight</h3>")
    thisFightTeams = list(fights_result["single_fights"][f]["score"].keys())
    for t in thisFightTeams:
        print("<b>" + teams[t]["name"] + "</b> : " + str(fights_result["single_fights"][f]["score"][t]))
        if fights_result["single_fights"][f]["bonus"][t] > 0:
            print(" (including " + str(fights_result["single_fights"][f]["bonus"][t]) + " bonus points)")
        print("<br/>")

