import pandas as pd

dummyCounter = 0
'''
The list of all the teams in Turkish League and the list of excel files that stores the data about their players.
'''
TurkishLeague = ["Alanyaspor", "Ankaragücü", "Antalyaspor", "Beşiktaş", "Çaykur Rizespor", "Denizlispor",
                 "Fenerbahçe", "Galatasaray SK", "Gazişehir Gaziantep", "Gençlerbirliği", "Göztepe SK",
                 "İstanbul Başakşehir", "Kasımpaşa", "Kayserispor", "Konyaspor",
                 "Sivasspor", "Trabzonspor", "Yeni Malatyaspor"]
tslFiles = [f"Spor Toto Super League/{i}.xlsx" for i in TurkishLeague]


'''
Player class that keeps the information about player's abilities, ratings and statistics.
'''


class Player:
    def __init__(self, excel, index):
        self.name = excel.iloc[index][0].split("-")[0]
        self.position = excel.iloc[index][1].split(" - ")
        self.nation = excel.iloc[index][2]
        self.club = excel.iloc[index][3]
        self.age = excel.iloc[index][4]
        self.finishing = excel.iloc[index][5]
        self.dribbling = excel.iloc[index][6]
        self.firstTouch = excel.iloc[index][7]
        self.heading = excel.iloc[index][8]
        self.corners = excel.iloc[index][9]
        self.marking = excel.iloc[index][10]
        self.crossing = excel.iloc[index][11]
        self.passing = excel.iloc[index][12]
        self.penalty = excel.iloc[index][13]
        self.freeKick = excel.iloc[index][14]
        self.technique = excel.iloc[index][15]
        self.tackling = excel.iloc[index][16]
        self.longShots = excel.iloc[index][17]
        self.longThrows = excel.iloc[index][18]
        self.aggression = excel.iloc[index][19]
        self.bravery = excel.iloc[index][20]
        self.workRate = excel.iloc[index][21]
        self.decisions = excel.iloc[index][22]
        self.determination = excel.iloc[index][23]
        self.concentration = excel.iloc[index][24]
        self.leadership = excel.iloc[index][25]
        self.anticipation = excel.iloc[index][26]
        self.flair = excel.iloc[index][27]
        self.positioning = excel.iloc[index][28]
        self.composure = excel.iloc[index][29]
        self.teamWork = excel.iloc[index][30]
        self.offTheBall = excel.iloc[index][31]
        self.vision = excel.iloc[index][32]
        self.agility = excel.iloc[index][33]
        self.stamina = excel.iloc[index][34]
        self.balance = excel.iloc[index][35]
        self.strength = excel.iloc[index][36]
        self.pace = excel.iloc[index][37]
        self.acceleration = excel.iloc[index][38]
        self.fitness = excel.iloc[index][39]
        self.jumping = excel.iloc[index][40]
        self.height = excel.iloc[index][41]
        self.skills = [self.finishing, self.dribbling, self.firstTouch, self.heading, self.marking, self.crossing,
                       self.passing, self.technique, self.tackling, self.longShots, self.vision]
        self.mentals = [self.aggression, self.bravery, self.workRate, self.decisions, self.determination,
                        self.anticipation, self.positioning, self.composure, self.teamWork, self.offTheBall]
        self.physical = [self.agility, self.balance, self.strength, self.pace,
                         self.acceleration, self.jumping, self.stamina]
        self.rating = Player.positionRating(self, self.position)
        self.goalScored = 0
        self.assists = 0
        self.matchesPlayed = 0


        """
        Attributes that are needed in match. 
        
        lastPosition --> The last position the player has been registered.
        
        Everything else is statistical.
        """





    # Calculates the players rating with the given position of the player and returns a dictionary which the keys are
    # the positions and the values are the ratings. The method of calculating is multiplying every single ability of the
    # player  with an amount that has been chosen accordingly to its importance. Since the mental abilities are less
    # important than abilities that are directly about the ball, they have lower impact to player's rating.
    def positionRating(self, positions):
        recipe = pd.read_excel("ratingRecipe.xlsx", engine="openpyxl")
        ratings = {}
        for position in positions:
            if "RB" in position or "LB" in position:
                sumOfSkills = 0
                sumOfMentals = 0
                sumOfPhysical = 0
                for i in range(len(self.skills)):
                    x = self.skills[i] * recipe.iloc[i][1]
                    sumOfSkills += x
                skillRating = (sumOfSkills / recipe.iloc[11][1]) * 5
                for i in range(len(self.mentals)):
                    x = self.mentals[i] * recipe.iloc[i + 19][1]
                    sumOfMentals += x
                mentalRating = (sumOfMentals / recipe.iloc[29][1]) * 5
                for i in range(len(self.physical)):
                    x = self.physical[i] * recipe.iloc[i + 30][1]
                    sumOfPhysical += x
                physicalRating = (sumOfPhysical / recipe.iloc[37][1]) * 5
                rating = (skillRating * 0.43) + (mentalRating * 0.27) + (physicalRating * 0.30)
                if position == "RB":
                    ratings["RB"] = round(rating, 2)
                else:
                    ratings["LB"] = round(rating, 2)

            elif "CB" in position:
                sumOfSkills = 0
                sumOfMentals = 0
                sumOfPhysical = 0
                for i in range(len(self.skills)):
                    x = self.skills[i] * recipe.iloc[i][2]
                    sumOfSkills += x
                skillRating = (sumOfSkills / recipe.iloc[11][2]) * 5
                for i in range(len(self.mentals)):
                    x = self.mentals[i] * recipe.iloc[i + 19][2]
                    sumOfMentals += x
                mentalRating = (sumOfMentals / recipe.iloc[29][2]) * 5
                for i in range(len(self.physical)):
                    x = self.physical[i] * recipe.iloc[i + 30][2]
                    sumOfPhysical += x
                physicalRating = (sumOfPhysical / recipe.iloc[37][2]) * 5
                rating = (skillRating * 0.35) + (mentalRating * 0.30) + (physicalRating * 0.35)
                rating += (int(self.height[:3]) - 190) * 0.10
                ratings["CB"] = round(rating, 2)

            elif "CDM" in position:
                sumOfSkills = 0
                sumOfMentals = 0
                sumOfPhysical = 0
                for i in range(len(self.skills)):
                    x = self.skills[i] * recipe.iloc[i][3]
                    sumOfSkills += x
                skillRating = (sumOfSkills / recipe.iloc[11][3]) * 5
                for i in range(len(self.mentals)):
                    x = self.mentals[i] * recipe.iloc[i + 19][3]
                    sumOfMentals += x
                mentalRating = (sumOfMentals / recipe.iloc[29][3]) * 5
                for i in range(len(self.physical)):
                    x = self.physical[i] * recipe.iloc[i + 30][3]
                    sumOfPhysical += x
                physicalRating = (sumOfPhysical / recipe.iloc[37][3]) * 5
                rating = (skillRating * 0.40) + (mentalRating * 0.26) + (physicalRating * 0.34)
                ratings["CDM"] = round(rating, 2)

            elif "CM" in position:
                sumOfSkills = 0
                sumOfMentals = 0
                sumOfPhysical = 0
                for i in range(len(self.skills)):
                    x = self.skills[i] * recipe.iloc[i][4]
                    sumOfSkills += x
                skillRating = (sumOfSkills / recipe.iloc[11][4]) * 5
                for i in range(len(self.mentals)):
                    x = self.mentals[i] * recipe.iloc[i + 19][4]
                    sumOfMentals += x
                mentalRating = (sumOfMentals / recipe.iloc[29][4]) * 5
                for i in range(len(self.physical)):
                    x = self.physical[i] * recipe.iloc[i + 30][4]
                    sumOfPhysical += x
                physicalRating = (sumOfPhysical / recipe.iloc[37][4]) * 5
                rating = (skillRating * 0.45) + (mentalRating * 0.27) + (physicalRating * 0.28)
                ratings["CM"] = round(rating, 2)

            elif "RM" in position or "LM" in position:
                sumOfSkills = 0
                sumOfMentals = 0
                sumOfPhysical = 0
                for i in range(len(self.skills)):
                    x = self.skills[i] * recipe.iloc[i][5]
                    sumOfSkills += x
                skillRating = (sumOfSkills / recipe.iloc[11][5]) * 5
                for i in range(len(self.mentals)):
                    x = self.mentals[i] * recipe.iloc[i + 19][5]
                    sumOfMentals += x
                mentalRating = (sumOfMentals / recipe.iloc[29][5]) * 5
                for i in range(len(self.physical)):
                    x = self.physical[i] * recipe.iloc[i + 30][5]
                    sumOfPhysical += x
                physicalRating = (sumOfPhysical / recipe.iloc[37][5]) * 5
                rating = (skillRating * 0.43) + (mentalRating * 0.23) + (physicalRating * 0.34)

                if position == "RM":
                    ratings["RM"] = round(rating, 2)
                else:
                    ratings["LM"] = round(rating, 2)

            elif "CAM" in position:
                sumOfSkills = 0
                sumOfMentals = 0
                sumOfPhysical = 0
                for i in range(len(self.skills)):
                    x = self.skills[i] * recipe.iloc[i][6]
                    sumOfSkills += x
                skillRating = (sumOfSkills / recipe.iloc[11][6]) * 5
                for i in range(len(self.mentals)):
                    x = self.mentals[i] * recipe.iloc[i + 19][6]
                    sumOfMentals += x
                mentalRating = (sumOfMentals / recipe.iloc[29][6]) * 5
                for i in range(len(self.physical)):
                    x = self.physical[i] * recipe.iloc[i + 30][6]
                    sumOfPhysical += x
                physicalRating = (sumOfPhysical / recipe.iloc[37][6]) * 5
                rating = (skillRating * 0.48) + (mentalRating * 0.29) + (physicalRating * 0.23)
                ratings["CAM"] = round(rating, 2)

            elif "RW" in position or "LW" in position:
                sumOfSkills = 0
                sumOfMentals = 0
                sumOfPhysical = 0
                for i in range(len(self.skills)):
                    x = self.skills[i] * recipe.iloc[i][7]
                    sumOfSkills += x
                skillRating = (sumOfSkills / recipe.iloc[11][7]) * 5
                for i in range(len(self.mentals)):
                    x = self.mentals[i] * recipe.iloc[i + 19][7]
                    sumOfMentals += x
                mentalRating = (sumOfMentals / recipe.iloc[29][7]) * 5
                for i in range(len(self.physical)):
                    x = self.physical[i] * recipe.iloc[i + 30][7]
                    sumOfPhysical += x
                physicalRating = (sumOfPhysical / recipe.iloc[37][7]) * 5
                rating = (skillRating * 0.40) + (mentalRating * 0.20) + (physicalRating * 0.40)

                if position == "RW":
                    ratings["RW"] = round(rating, 2)
                else:
                    ratings["LW"] = round(rating, 2)

            else:
                sumOfSkills = 0
                sumOfMentals = 0
                sumOfPhysical = 0
                for i in range(len(self.skills)):
                    x = self.skills[i] * recipe.iloc[i][8]
                    sumOfSkills += x
                skillRating = (sumOfSkills / recipe.iloc[11][8]) * 5
                for i in range(len(self.mentals)):
                    x = self.mentals[i] * recipe.iloc[i + 19][8]
                    sumOfMentals += x
                mentalRating = (sumOfMentals / recipe.iloc[29][8]) * 5
                for i in range(len(self.physical)):
                    x = self.physical[i] * recipe.iloc[i + 30][8]
                    sumOfPhysical += x
                physicalRating = (sumOfPhysical / recipe.iloc[37][8]) * 5
                rating = (skillRating * 0.50) + (mentalRating * 0.25) + (physicalRating * 0.25)
                ratings["ST"] = round(rating, 2)

        sortedRatings = {}
        for i in sorted(list(ratings.values()), reverse=True):
            for j in list(ratings.keys()):
                if ratings[j] == i:
                    sortedRatings[j] = i
        return sortedRatings

'''
GoalKeeper class since the given abilities for an in field player and GK is different. Also the stats that'll be stored
will be different.
'''
class GoalKeepers:
    def __init__(self, excel, index):
        self.name = excel.iloc[index][0].split("-")[0]
        self.position = list(excel.iloc[index][1])
        self.nation = excel.iloc[index][2]
        self.club = excel.iloc[index][3]
        self.age = excel.iloc[index][4]
        self.rushingOut = excel.iloc[index][5]
        self.oneOnOnes = excel.iloc[index][6]
        self.commandOfArea = excel.iloc[index][7]
        self.kicking = excel.iloc[index][8]
        self.eccentricity = excel.iloc[index][9]
        self.handling = excel.iloc[index][10]
        self.throwing = excel.iloc[index][11]
        self.aerialReach = excel.iloc[index][12]
        self.communication = excel.iloc[index][13]
        self.firstTouch = excel.iloc[index][14]
        self.passing = excel.iloc[index][15]
        self.reflexes = excel.iloc[index][16]
        self.punchingTendency = excel.iloc[index][17]
        self.aggression = excel.iloc[index][18]
        self.bravery = excel.iloc[index][19]
        self.workRate = excel.iloc[index][20]
        self.decisions = excel.iloc[index][21]
        self.determination = excel.iloc[index][22]
        self.concentration = excel.iloc[index][23]
        self.leadership = excel.iloc[index][24]
        self.anticipation = excel.iloc[index][25]
        self.flair = excel.iloc[index][26]
        self.positioning = excel.iloc[index][27]
        self.composure = excel.iloc[index][28]
        self.teamWork = excel.iloc[index][29]
        self.offTheBall = excel.iloc[index][30]
        self.vision = excel.iloc[index][31]
        self.agility = excel.iloc[index][32]
        self.stamina = excel.iloc[index][33]
        self.balance = excel.iloc[index][34]
        self.strength = excel.iloc[index][35]
        self.pace = excel.iloc[index][36]
        self.acceleration = excel.iloc[index][37]
        self.fitness = excel.iloc[index][38]
        self.jumping = excel.iloc[index][39]
        self.height = excel.iloc[index][40]
        self.skills = [self.rushingOut, self.oneOnOnes, self.commandOfArea, self.kicking, self.eccentricity,
                       self.handling, self.throwing, self.aerialReach, self.communication, self.firstTouch,
                       self.passing, self.reflexes, self.punchingTendency, self.vision, self.agility, self.balance,
                       self.strength, self.jumping]
        self.mental = [self.aggression, self.bravery, self.decisions, self.determination, self.anticipation,
                       self.positioning, self.composure, self.teamWork]
        self.rating = GoalKeepers.gkRating(self)
        self.goalConceded = 0
        self.assists = 0

    # Basically the same way to calculate a player's rating.
    def gkRating(self):
        recipe = pd.read_excel("gkRating.xlsx", engine="openpyxl")
        sumOfSkills = 0
        sumOfMentals = 0
        ratings = {}
        for i in range(len(self.skills)):
            x = self.skills[i] * recipe.iloc[i][1]
            sumOfSkills += x
            skillRating = (sumOfSkills / recipe.iloc[18][1]) * 5
        for i in range(len(self.mental)):
            x = self.mental[i] * recipe.iloc[i + 19][1]
            sumOfMentals += x
            mentalRating = (sumOfMentals / recipe.iloc[27][1]) * 5
        rating = (skillRating * 0.65) + (mentalRating * 0.35)
        rating += (int(self.height[0:3]) - 185) * 0.06
        ratings["GK"] = round(rating, 2)
        return ratings


# Adding all the players from their excel files to a list that involves every player in whole project. Easily accessible
# by using the index of the player.
allPlayers = []
for team in tslFiles:
    df = pd.read_excel(team, engine="openpyxl")
    for i in range(len(df)):
        player = Player(df, i)
        allPlayers.append(player)

# Adding the gk's to the allPlayers list.
gk = pd.read_excel("Spor Toto Super League/GK1.xlsx", engine="openpyxl")
for i in range(len(gk)):
    player = GoalKeepers(gk, i)
    allPlayers.append(player)
