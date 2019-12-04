#!/bin/env python3

team_order_placements = [
    ["reporter", "reviewer", "opponent"], # position A 1st round, 2nd round, 3rd round
    ["opponent", "reporter", "reviewer"], # B
    ["reviewer", "opponent", "reporter"]  # C
]

team_order_placement_position = [
    {# 1st round. Reporter Team is team A
        "reporter" : 0,
        "opponent" : 1,
        "reviewer" : 2
    },
    {# 2nd round
        "reviewer" : 0,
        "reporter" : 1,
        "opponent" : 2
    },
    {# 3rd round
        "opponent" : 0,
        "reviewer" : 1,
        "reporter" : 2
    } 
]


def getGrade(data, jury_amount):

    if len(data) != jury_amount:
        print("DATA LENGTH DOES NOT MATCH JURY AMOUNT OF FIRST GRADE!!")
        exit(3)

    data = sorted(data)
    print("      score: " + str(data))

    # remove scores based on amount of jurors
    if jury_amount == 5 or jury_amount == 6:
        print("      removing lowest score")
        data.pop(0)
    elif jury_amount >= 7:
        amountToRemove = math.ceil((jury_amount/4))
        print("      removing " + str(amountToRemove) + " scores")
        for i in range(0, math.floor(amountToRemove/2)):
            data.pop(0)
            data.pop(len(data)-1)
        if (amountToRemove % 2) != 0:
            data.pop(0)
    else:
        print("      no score to be removed")

    print("      score: " + str(data))
    grade = sum(data)
    grade /= len(data)

    return grade
