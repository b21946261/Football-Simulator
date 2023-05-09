import pandas as pd
import data


dummyCounter = 0
'''
The list of all the teams in Turkish League and the list of excel files that stores the data about their players.
'''
TurkishLeague = ["Alanyaspor", "Ankaragücü", "Antalyaspor", "Beşiktaş", "Çaykur Rizespor", "Denizlispor",
                 "Fenerbahçe", "Galatasaray SK", "Gazişehir Gaziantep", "Gençlerbirliği", "Göztepe SK",
                 "İstanbul Başakşehir", "Kasımpaşa", "Kayserispor", "Konyaspor",
                 "Sivasspor", "Trabzonspor", "Yeni Malatyaspor"]
tslFiles = [f"Spor Toto Super League/{i}.xlsx" for i in TurkishLeague]


class Team:
    # All of the formations as a dictionary. Class variable.
    f_4_2 = {"GK": "", "RB": "", "LB": "", "CB1": "", "CB2": "",
             "RW": "", "LW": "", "CM1": "", "CM2": "", "ST1": "", "ST2": ""}

    five_3_2 = {"GK": "", "RB": "", "LB": "", "CB1": "", "CB2": "", "CB3": "",
                "CM1": "", "CM2": "", "CAM": "", "ST1": "", "ST2": ""}

    f_4312 = {"GK": "", "RB": "", "LB": "", "CB1": "", "CB2": "",
              "RM": "", "LM": "", "CM": "", "CAM": "", "ST1": "", "ST2": ""}

    liv_433 = {"GK": "", "RB": "", "LB": "", "CB1": "", "CB2": "",
               "LW": "", "RW": "", "CDM": "", "CM1": "", "CM2": "", "ST": ""}

    f_4231 = {"GK": "", "RB": "", "LB": "", "CB1": "", "CB2": "",
              "RW": "", "LW": "","CM1": "", "CM2": "","CAM": "", "ST": ""}

    off_4141 = {"GK": "", "RB": "", "LB": "", "CB1": "", "CB2": "",
                "RW": "", "LW": "","CDM": "", "CAM1": "", "CAM2": "", "ST": ""}

    def_4141 = {"GK": "", "RB": "", "LB": "", "CB1": "", "CB2": "",
                "RM": "", "LM": "", "CDM": "", "CM1": "", "CM2": "", "ST": ""}
    formation = [f_4_2, f_4312, liv_433, f_4231, off_4141, def_4141]  # five_3_2 may be added later
    positions = ["GK", "CB", "RB", "LB", "CM", "CDM", "CAM", "RM", "RW", "LM", "LW", "ST"]

    def __init__(self, name):
        self.name = name
        self.players = []
        self.formation = {}  # [position]: (player, player's name)
        self.lineup = {}  # [position]: (player's name)
        self.allFormations = []  # (formation, avg rating)
        self.defenceTactic = {"Defence Width": bool, "Offside Tactic": bool, "Defence Line": int, "GK how to play in": list}
        self.attackTactic = {"Attack Width": int, "Attack From": int, "Creativity": list,
                             "Crossing": bool, "Attacking Backs": bool, "Tempo": int, "Dribbling": list}
        self.main = int
        self.offensePoint = int
        self.counterPoint = int
        self.defencePoint = int
        self.goalScored = 0
        self.goalConceded = 0
        self.averageGoals = self.goalScored - self.goalConceded
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.points = (self.wins * 3) + self.draws

    # A function which returns the best formation according to the formation's average rating.
    def formationChooser(self):
        allFormationsAndRatings = []  # Involves all the formations and their avg ratings as a tuple.
        a = 0
        for form in Team.formation:  # Goes through every empty formation dictionary.
            teamForm = form.copy()  # Since formation is a class variable we take a copy of it to not change it.
            squad = self.players.copy()  # All players list. Any selected player will be dropped from the list.
            while "" in list(teamForm.values()):
                for pos in range(len(teamForm)):
                    available = {}  # The dictionary of the available players for the given position.
                    for ppl in squad:
                        if list(form.keys())[pos][:3] == "CAM" or list(form.keys())[pos] == "CDM":
                            if list(form.keys())[pos][:3] in list(ppl.rating.keys()):
                                available[ppl] = ppl.rating[list(teamForm.keys())[pos][:3]]
                        else:
                            if list(form.keys())[pos][0:2] in list(ppl.rating.keys()):
                                available[ppl] = ppl.rating[list(teamForm.keys())[pos][0:2]]

                    sortedAvailable = {}  # [position] : players rating in the given position
                    for i in sorted(list(available.values()), reverse=True):
                        for j in list(available.keys()):
                            if available[j] == i:
                                sortedAvailable[j] = i

                    # If there is no one available in a position the program fills the position with a dummy which has
                    # a low rating so the average rating of the formation will make the formation unlikely to be chosen.
                    # teamForm dictionary --> [position] : (player object, player's name)
                    if len(sortedAvailable) != 0:
                        a = list(form.keys())[pos]
                        person = list(sortedAvailable.keys())[0]
                        teamForm[a] = (person, person.name)
                        squad.remove(list(sortedAvailable.keys())[0])

                    else:
                        df = pd.read_excel(tslFiles[0], engine="openpyxl")
                        dummy = data.Player(df, 29)
                        global dummyCounter
                        dummyCounter += 1
                        a = list(form.keys())[pos]
                        teamForm[a] = (dummy, dummy.name)

            # Calculating the formations and their average ratings as a tuple.
            sumOfRatings = 0
            for i in range(11):
                playerTuple = teamForm[list(teamForm.keys())[i]]
                if list(teamForm.keys())[i][:3] == "CAM" or list(teamForm.keys())[i] == "CDM":
                    sumOfRatings += playerTuple[0].rating[list(teamForm.keys())[i][:3]]
                else:
                    sumOfRatings += playerTuple[0].rating[list(teamForm.keys())[i][:2]]
            avgRating = round((sumOfRatings / 11), 4)
            allFormationsAndRatings.append((teamForm, avgRating))
        # This part takes the highest rated formation from allFormations list and returns it as the bestFormation.
        ratingList = []
        bestFormation = {}  # Best formation's dictionary --> [position]: (player object, player name)
        for i in allFormationsAndRatings:
            ratingList.append(i[1])

        best = sorted(ratingList, reverse=True)[0]
        for j in allFormationsAndRatings:
            if best == j[1]:
                bestFormation = j[0]
                break

        # Converting the best formation dictionary to a simplest way by just entering the player's name to the value.
        lineup = {}  # --> [position]: player's name
        for i in range(11):
            pst = list(bestFormation.keys())[i]
            plyr = list(bestFormation.values())[i][1]
            lineup[pst] = plyr

        return (bestFormation, lineup, allFormationsAndRatings)

    '''
    Functions for deciding tactics.
    '''
    # A function to return the Player objects of given positions.
    def findingPlayer(self, formation, position):
        positions = ["GK", "CB", "RB", "LB", "CM", "CDM", "CAM", "RM", "RW", "LM", "LW", "ST"]
        if position == "CB":
            cb1 = formation["CB1"][0]
            cb2 = formation["CB2"][0]
            return (cb1, cb2)

        elif position == "wings":
            if "RW" in formation.keys():
                winger1 = formation["RW"][0]
            else:
                winger1 = formation["RM"][0]

            if "LW" in formation.keys():
                winger2 = formation["LW"][0]
            else:
                winger2 = formation["LM"][0]
            return (winger1, winger2)

        elif position == "backs":
            back1 = formation["RB"][0]
            back2 = formation["LB"][0]
            return (back1, back2)

        elif position == "midfielders":
            if "ST1" in formation.keys():
                midkey1 = list(formation.keys())[7]
                midkey2 = list(formation.keys())[8]
                mid1 = formation[midkey1][0]
                mid2 = formation[midkey2][0]
                return (mid1, mid2)

            else:
                mid1key = list(formation.keys())[7]
                mid2key = list(formation.keys())[8]
                mid3key = list(formation.keys())[9]
                mid1 = formation[mid1key][0]
                mid2 = formation[mid2key][0]
                mid3 = formation[mid3key][0]
                return (mid1, mid2, mid3)

        elif position == "forwards":
            if "ST1" in formation.keys():
                stkey1 = list(formation.keys())[9]
                stkey2 = list(formation.keys())[10]
                st1 = formation[stkey1][0]
                st2 = formation[stkey2][0]
                return (st1, st2)
            else:
                st = formation["ST"][0]
                return (st)

        elif position == ["GK"]:
            gk = formation["GK"][0]
            return (gk)

    # A function that decides if the backs are good enough to play offensive.
    # True is offensive, False is defensive.
    def attackingBacks(self, formation):
        (back1, back2) = Team.findingPlayer(self, formation, "backs")
        ratingAvg = (back1.rating["RB"] + back2.rating["LB"]) / 2

        # Checks the rating of the backs and returns true if the backs are qualified. May be separated.
        if ratingAvg > 61.7:
            return True
        else:
            return False

    def attackWidth(self, formation):
        (winger1, winger2) = Team.findingPlayer(self, formation, "wings")
        narrow = 0
        wide = 0
        for i in [winger1, winger2]:
            narrowP = (i.finishing + i.offTheBall + i.longShots) / 3
            wideP = (i.crossing + i.dribbling + i.firstTouch) / 3
            if i.flair > 12:
                wideP += i.flair * 0.07
            narrow += narrowP * 0.5
            wide += wideP * 0.5
        if self.attackTactic["Attacking Backs"] == True:
            (back1, back2) = Team.findingPlayer(self, formation, "backs")

        if wide > narrow + 2:
            return (2, narrow, wide)
        elif narrow + 2 > wide > narrow:
            return (1, narrow, wide)
        else:
            return (0, narrow, wide)

    # A function to return a list of players that are able to dribble.
    def dribbling(self, formation):
        dribblers = []
        for i in range(10):
            player = formation[list(formation.keys())[i + 1]][0]
            playerDribble = (player.firstTouch + player.dribbling + player.agility + player.pace + player.acceleration) / 5
            if player.flair > 12:
                playerDribble += player.flair * 0.05
            if playerDribble > 13:
                dribblers.append(player)
        return dribblers

    # The function that chooses whether to attack from wings or from middle by comparing the avg ratings of the wingers
    # and the midfielders in lineup. If there's no winger in team it automatically returns 0 since it's not the wisest
    # thing to do.
    # 0 --> middle / 1 --> even / 2 --> wings
    def attackFrom(self, formation):
        (winger1, winger2) = Team.findingPlayer(self, formation, "wings")
        if "ST1" in list(formation.keys()):
            (mid1, mid2) = Team.findingPlayer(self, formation, "midfielders")
            if "RM" in list(formation.keys()):
                wingerAvg = (winger1.rating["RM"] + winger2.rating["LM"]) / 2
                midAvg = (mid1.rating[list(formation.keys())[7]] + mid2.rating[list(formation.keys())[8]]) / 2
                if wingerAvg > midAvg + 0.5:
                    return 2
                elif midAvg - 0.5 < wingerAvg < midAvg + 0.5:
                    return 1
                else:
                    return 0

            elif "RW" in list(formation.keys()):
                wingerAvg = (winger1.rating["RW"] + winger2.rating["LW"]) / 2
                midAvg = (mid1.rating[list(formation.keys())[7][:2]] + mid2.rating[list(formation.keys())[8][:2]]) / 2
                if wingerAvg > midAvg + 0.5:
                    return 2
                elif midAvg - 0.5 < wingerAvg < midAvg + 0.5:
                    return 1
                else:
                    return 0

            else:
                return 0

        else:
            (mid1, mid2, mid3) = Team.findingPlayer(self, formation, "midfielders")
            if "RM" in list(formation.keys()):
                wingerAvg = (winger1.rating["RM"] + winger2.rating["LM"]) / 2
                if "CDM" in list(formation.keys()):
                    midAvg = ((mid1.rating[list(formation.keys())[7]] * 0.5) + (mid2.rating[list(formation.keys())[8]]\
                             + mid3.rating[list(formation.keys())[9]])) / 2.5
                    if wingerAvg > midAvg + 0.5:
                        return 2
                    elif midAvg - 0.5 < wingerAvg < midAvg + 0.5:
                        return 1
                    else:
                        return 0

                else:
                    midAvg = (mid1.rating[list(formation.keys())[7]] + mid2.rating[list(formation.keys())[8]]\
                             + mid3.rating[list(formation.keys())[9]]) / 3
                    if wingerAvg > midAvg + 0.5:
                        return 2
                    elif midAvg - 0.5 < wingerAvg < midAvg + 0.5:
                        return 1
                    else:
                        return 0

            else:
                wingerAvg = (winger1.rating["RW"] + winger2.rating["LW"]) / 2
                if "CDM" in list(formation.keys()):
                    if "CM1" in list(formation.keys()):
                        midAvg = ((mid1.rating[list(formation.keys())[7]] * 0.5) + (mid2.rating[list(formation.keys())[8][:2]]\
                                 + mid3.rating[list(formation.keys())[9][:2]])) / 2.5
                        if wingerAvg > midAvg + 0.5:
                            return 2
                        elif midAvg - 0.5 < wingerAvg < midAvg + 0.5:
                            return 1
                        else:
                            return 0
                    else:
                        midAvg = ((mid1.rating[list(formation.keys())[7]] * 0.5) + (mid2.rating[list(formation.keys())[8][:3]]\
                                  + mid3.rating[list(formation.keys())[9][:3]])) / 2.5
                        if wingerAvg > midAvg + 0.5:
                            return 2
                        elif midAvg - 0.5 < wingerAvg < midAvg + 0.5:
                            return 1
                        else:
                            return 0

                else:
                    midAvg = (mid1.rating[list(formation.keys())[7][:2]] + mid2.rating[list(formation.keys())[8][:2]]\
                              + mid3.rating[list(formation.keys())[9]]) / 3
                    if wingerAvg > midAvg + 0.5:
                        return 2
                    elif midAvg - 0.5 < wingerAvg < midAvg + 0.5:
                        return 1
                    else:
                        return 0

    # A function to decide crossing possibility by checking wingers and backs crossing abilities. Specialized player
    # crossing option may be added later.
    # True means crossing is on, False means crossing is off.
    def crossing(self, formation):
        (wing1, wing2) = Team.findingPlayer(self, formation, "wings")
        wing1Crossing = (wing1.crossing + wing1.technique + wing1.vision + wing1.decisions) / 4
        wing2Crossing = (wing2.crossing + wing2.technique + wing2.vision + wing2.decisions) / 4

        (back1, back2) = Team.findingPlayer(self, formation, "backs")
        back1Crossing = (back1.crossing + back1.technique + back1.vision + back1.decisions) / 4
        back2Crossing = (back2.crossing + back2.technique + back2.vision + back2.decisions) / 4
        if "ST1" in formation.keys():
            (st1, st2) = Team.findingPlayer(self, formation, "forwards")
            st1Heading = (st1.heading + st1.offTheBall + st1.finishing + st1.jumping) / 4
            st2Heading = (st2.heading + st2.offTheBall + st2.finishing + st1.jumping) / 4
            stHeight = sorted([int(st1.height[:3]), int(st1.height[:3])])[0]
            if self.attackTactic["Attacking Backs"] == True:
                crossP = ((wing1Crossing + wing2Crossing) * 0.21) + ((back1Crossing + back2Crossing) * 0.09)
                crossP += ((st1Heading + st2Heading) * 0.2)

            else:
                crossP = ((wing1Crossing + wing2Crossing) * 0.27) + ((back1Crossing + back2Crossing) * 0.03)
                crossP += ((st1Heading + st2Heading) * 0.2)
        else:
            (st1) = Team.findingPlayer(self, formation, "forwards")
            st1Heading = (st1.heading + st1.offTheBall + st1.finishing + st1.jumping) / 4
            stHeight = int(st1.height[:3])
            if self.attackTactic["Attacking Backs"] == True:
                crossP = ((wing1Crossing + wing2Crossing) * 0.21) + ((back1Crossing + back2Crossing) * 0.09)
                crossP += (st1Heading * 0.4)

            else:
                crossP = ((wing1Crossing + wing2Crossing) * 0.27) + ((back1Crossing + back2Crossing) * 0.03)
                crossP += (st1Heading * 0.4)

        crossP += (stHeight - 183) * 0.1
        if crossP > 13:
            return True
        else:
            return False

    # A function to return a list of players allowed to play creative according to their passing skills.
    def creativity(self, formation):
        creative = []
        for i in range(10):
            player = formation[list(formation.keys())[i + 1]][0]
            creativity = (player.passing + player.vision + player.technique + player.decisions) / 4
            if creativity > 14:
                creative.append(player)
        return creative

    # A function to decide the team's attacking tempo.
    # 2 --> high / 1 --> normal / 0 --> slow
    def tempo(self, formation):
        tempoSum = 0
        for i in range(10):
            player = formation[list(formation.keys())[i + 1]][0]
            playerTempo = (player.vision + (player.stamina * 3) + (player.passing * 2) + player.decisions +\
                          (player.teamWork * 4) + (player.workRate * 3) + player.technique + (player.firstTouch * 2)) / 17
            tempoSum += playerTempo

        if tempoSum / 10 > 12.90:
            return 2
        elif tempoSum / 10 > 12.45:
            return 1
        else:
            return 0

    # A function to decide defence width by comparing backs and centre backs. If the backs are better, defence is wider.
    # True is wide, False is narrow.
    def defenceWidth(self, formation):
        (back1, back2) = Team.findingPlayer(self, formation, "backs")
        (cb1, cb2) = Team.findingPlayer(self, formation, "CB")
        backRatings = (back1.rating["RB"] + back2.rating["LB"]) / 2
        if "CDM" in formation.keys():
            cdm = formation[list(formation.keys())[7]][0]
            defenceRating = ((cb1.rating["CB"] + cb2.rating["CB"]) * 0.4) + (cdm.rating["CDM"] * 0.2)
        else:
            defenceRating = (cb1.rating["CB"] + cb2.rating["CB"]) / 2

        if defenceRating > 64:
            return True
        else:
            if backRatings < 61:
                return False
            else:
                if defenceRating > 60:
                    return True
                else:
                    return False

    # A function to enable offside tactic if defence is capable enough. If defence line is 0, offside tactic is
    # automatically off.
    # True --> offside tactic on / False --> Offside tactic off
    def offsideTactic(self, formation):
        (back1, back2) = Team.findingPlayer(self, formation, "backs")
        (cb1, cb2) = Team.findingPlayer(self, formation, "CB")
        back1Offside = (back1.positioning + back1.acceleration + back1.teamWork + back1.anticipation + back1.concentration) / 5
        back2Offside = (back2.positioning + back2.acceleration + back2.teamWork + back2.anticipation + back2.concentration) / 5
        cb1Offside = (cb1.positioning + cb1.acceleration + cb1.teamWork + cb1.anticipation + cb1.concentration) / 5
        cb2Offside = (cb2.positioning + cb2.acceleration + cb2.teamWork + cb2.anticipation + cb2.concentration) / 5
        offside = ((back1Offside + back2Offside) * 0.125) + ((cb1Offside + cb2Offside) * 0.375)

        if self.defenceTactic["Defence Line"] == 0:
            return False

        return True if offside > 12.85 else False

    # A function to decide where the defence line will be.
    # 0 --> closer to goalkeeper / 1 --> default / 2 --> closer to midfield
    def defenceLine(self, formation):
        (back1, back2) = Team.findingPlayer(self, formation, "backs")
        (cb1, cb2) = Team.findingPlayer(self, formation, "CB")
        backAvg = (back1.rating["RB"] + back2.rating["LB"]) / 2
        cbAvg = (cb1.rating["CB"] + cb2.rating["CB"]) / 2
        teamRating = 0
        for i in range(6):
            # f_4_2 = {"GK": "", "RB": "", "LB": "", "CB1": "", "CB2": "",
            #          "RW": "", "LW": "", "CM1": "", "CM2": "", "ST1": "", "ST2": ""}
            playerPos = list(formation.keys())[i + 5]
            player = formation[playerPos][0]
            for char in range(len(playerPos) + 1):
                for pos in Team.positions:
                    if pos == playerPos[:char]:
                        position = pos
            teamRating += player.rating[position]
        teamAvg = teamRating / 6

        if self.attackTactic["Attacking Backs"] == True:
            defAvg = (cbAvg * 0.8) + (backAvg * 0.2)
        else:
            defAvg = (cbAvg * 0.65) + (backAvg * 0.35)

        defenceLine = (defAvg * 0.7) + (teamAvg * 0.3)

        if defenceLine > 62:
            return 2
        elif 60.5 < defenceLine < 62:
            return 1
        else:
            return 0

    # throwing / kicking
    def gkPlaytheBall(self, formation):
        gk = formation[list(formation.keys())[0]][0]
        kicking = (((gk.kicking + gk.vision + gk.decisions) / 3), "kicking")
        throwing = (((gk.throwing + gk.communication) / 2), "throwing")
        passing = (((gk.passing + gk.vision + gk.decisions + gk.communication) / 4), "passing")

        return sorted([kicking, throwing, passing], reverse=True)

    # 0 --> ersun / 1 --> defans / 2 --> dengeli / 3 --> atak / 4 --> ersun
    def mainTactic(self, formation):
        defences = ["RB", "LB", "CB", "CDM"]
        midfielders = ["CDM", "CM", "RM", "LM", "CAM"]
        forwards = ["RW", "LW", "ST", "CAM"]
        defenceRating = 0
        midfieldRating = 0
        forwardRating = 0

        for i in range(10):
            playerPos = list(formation.keys())[i + 1]
            player = formation[playerPos][0]
            for char in range(len(playerPos) + 1):
                for pos in Team.positions:
                    if pos == playerPos[:char]:
                        position = pos
            if position in defences:

                if "CDM" in formation.keys():
                    if self.attackTactic["Attacking Backs"] == True:
                        if position in ["RB", "LB"]:
                            defenceRating += player.rating[position] * 0.15
                        elif position == "CB":
                            defenceRating += player.rating[position] * 0.30
                        else:
                            defenceRating += player.rating[position] * 0.10

                    elif self.attackTactic["Attacking Backs"] == False:
                        if position in ["RB", "LB"]:
                            defenceRating += player.rating[position] * 0.20
                        elif position == "CB":
                            defenceRating += player.rating[position] * 0.25
                        else:
                            defenceRating += player.rating[position] * 0.10

                elif "CDM" not in formation.keys():
                    if self.attackTactic["Attacking Backs"] == True:
                        if position in ["RB", "LB"]:
                            defenceRating += player.rating[position] * 0.15
                        elif position == "CB":
                            defenceRating += player.rating[position] * 0.35

                    elif self.attackTactic["Attacking Backs"] == False:
                        if position in ["RB", "LB"]:
                            defenceRating += player.rating[position] * 0.20
                        elif position == "CB":
                            defenceRating += player.rating[position] * 0.30

            if position in midfielders:
                if "RM" not in formation.keys():
                    if "CAM" in [i[:3] for i in list(formation.keys())]:
                        if "CDM" in formation.keys():
                            if position == "CDM":
                                midfieldRating += player.rating[position] * 0.25
                            else:
                                midfieldRating += player.rating[position] * 0.375
                        else:
                            if position == "CAM":
                                midfieldRating += player.rating[position] * 0.25
                            else:
                                midfieldRating += player.rating[position] * 0.375

                    elif "CAM" not in [i[:3] for i in list(formation.keys())]:
                        if "CDM" in formation.keys():
                            if position == "CDM":
                                midfieldRating += player.rating[position] * 0.25
                            else:
                                midfieldRating += player.rating[position] * 0.375
                        else:
                            midfieldRating += player.rating[position] * 0.5

                elif "RM" in formation.keys():
                    if "CDM" in formation.keys():
                        if position == "CDM":
                            midfieldRating += player.rating[position] * 0.1
                        elif position == "CM":
                            midfieldRating += player.rating[position] * 0.25
                        else:
                            midfieldRating += player.rating[position] * 0.2

                    elif "CAM" in formation.keys():
                        if position == "CM":
                            midfieldRating += player.rating[position] * 0.3
                        elif position == "CAM":
                            midfieldRating += player.rating[position] * 0.20
                        else:
                            midfieldRating += player.rating[position] * 0.25

            if position in forwards:
                if "RW" in formation.keys():
                    if "CAM" in [i[:3] for i in list(formation.keys())]:
                        if "CDM" in formation.keys():
                            if position == "CAM":
                                forwardRating += player.rating[position] * 0.15
                            elif position == "ST":
                                forwardRating += player.rating[position] * 0.3
                            else:
                                forwardRating += player.rating[position] * 0.2

                        else:
                            if position == "CAM":
                                forwardRating += player.rating[position] * 0.15
                            elif position == "ST":
                                forwardRating += player.rating[position] * 0.35
                            else:
                                forwardRating += player.rating[position] * 0.25
                    else:
                        if "ST1" in formation.keys():
                            if position == "ST":
                                forwardRating += player.rating[position] * 0.3
                            else:
                                forwardRating += player.rating[position] * 0.2

                        else:
                            if position == "ST":
                                forwardRating += player.rating[position] * 0.4
                            else:
                                forwardRating += player.rating[position] * 0.3

                elif "RW" not in formation.keys():
                    if "CAM" in formation.keys():
                        if position == "ST":
                            forwardRating += player.rating[position] * 0.4
                        else:
                            forwardRating += player.rating[position] * 0.2
                    else:
                        forwardRating += player.rating[position]
        for i in [defenceRating, forwardRating, midfieldRating]:
            i *= 5
            round(i, 2)

        forward = (defenceRating * 0.05) + (midfieldRating * 0.30) + (forwardRating * 0.65)
        defence = (defenceRating * 0.65) + (midfieldRating * 0.30) + (forwardRating * 0.05)
        if self.defenceTactic["Defence Line"] == 2:
            if forward > 63:
                return 4
            elif 61.5 < forward < 63:
                return 3
            else:
                return 2

        elif self.defenceTactic["Defence Line"] == 0:
            if forward > 62:
                return 2
            elif 62 > forward > 60:
                return 1
            else:
                return 0

        else:
            if defence > 60.5:
                if forward - defence > 1:
                    return 4
                elif forward - defence > 0.5:
                    return 3
                else:
                    return 2

            else:
                if defence > 60:
                    return 2
                elif 59 < defence < 60:
                    return 1
                else:
                    return 0

    # Calculating the team's offense point by related tactics.
    def attackCounterUtil(self):
        mainTactic = self.main
        attackingBacks = self.attackTactic["Attacking Backs"]
        tempo = self.attackTactic["Tempo"]
        defenceLine = self.defenceTactic["Defence Line"]

        offensePoint = 0
        counterPoint = 0
        defencePoint = 0

        if mainTactic == 4:
            offensePoint += 50
            counterPoint += 35
            defencePoint += 24
        elif mainTactic == 3:
            offensePoint += 45
            counterPoint += 30
            defencePoint += 28
        elif mainTactic == 2:
            offensePoint += 41
            counterPoint += 24
            defencePoint += 32
        elif mainTactic == 1:
            offensePoint += 37
            counterPoint += 17
            defencePoint += 36
        else:
            offensePoint += 32
            counterPoint += 10
            defencePoint += 40

        if attackingBacks == True:
            offensePoint += 10
            counterPoint += 20
            defencePoint += 10
        else:
            offensePoint += 5
            counterPoint += 10
            defencePoint += 20

        if defenceLine == 2:
            offensePoint += 25
            counterPoint += 45
            defencePoint += 27
        elif defenceLine == 1:
            offensePoint += 20
            counterPoint += 30
            defencePoint += 33
        else:
            offensePoint += 15
            counterPoint += 15
            defencePoint += 40

        if tempo == 3:
            offensePoint += 15
        elif tempo == 2:
            offensePoint += 12
        else:
            offensePoint += 9

        return (offensePoint, counterPoint, defencePoint)


# Creating team objects.
tslTeams = []
for i in TurkishLeague:
    x = Team(i)
    tslTeams.append(x)

# Adding players to their club objects
for player in data.allPlayers:
    for i in range(len(TurkishLeague)):
        if player.club == TurkishLeague[i]:
            tslTeams[i].players.append(player)

# Defining the formations and lineups of all the teams.
for i in tslTeams:
    (formation, lineup, allformations) = Team.formationChooser(i)
    i.formation = formation
    i.lineup = lineup
    i.allFormations = allformations

# A loop to assign team's tactics.
for i in tslTeams:
    i.attackTactic["Attacking Backs"] = Team.attackingBacks(i, i.formation)
    i.attackTactic["Attack From"] = Team.attackFrom(i, i.formation)
    i.attackTactic["Attack Width"] = Team.attackWidth(i, i.formation)
    i.attackTactic["Creativity"] = Team.creativity(i, i.formation)
    i.attackTactic["Crossing"] = Team.crossing(i, i.formation)
    i.attackTactic["Dribbling"] = Team.dribbling(i, i.formation)
    i.attackTactic["Tempo"] = Team.tempo(i, i.formation)
    i.defenceTactic["Defence Line"] = Team.defenceLine(i, i.formation)
    i.defenceTactic["Defence Width"] = Team.defenceWidth(i, i.formation)
    i.defenceTactic["Offside Tactic"] = Team.offsideTactic(i, i.formation)
    i.defenceTactic["GK how to play in"] = Team.gkPlaytheBall(i, i.formation)
    i.main = Team.mainTactic(i, i.formation)
    print(i.name, i.lineup)
    i.defencePoint = Team.attackCounterUtil(i)[2]
    i.offensePoint = Team.attackCounterUtil(i)[0]
    i.counterPoint = Team.attackCounterUtil(i)[1]
