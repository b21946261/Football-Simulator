import tactics
import random


class Match:
    """
             The pitch has been separated into 12 piece. Check pitch.jpg
             Home team's goal is located in cell 1, away team's goal is located in cell 10.
             Formations and number of attacks are stored in local variables.
    """
    def __init__(self, home, away):


        self.pitchHome = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: []}
        self.pitchAway = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: []}
        self.homeFormation = home.formation
        self.awayFormation = away.formation
        self.homeAttacks = Match.attackNumber(self, home, away)[0]
        self.awayAttacks = Match.attackNumber(self, home, away)[1]
        self.totalAttacks = self.homeAttacks + self.awayAttacks
        self.ballPosition = 4

        """
        We need to track the position of every player in the lastPosition to prevent the teleportation of players.
        Ex: A player of the away team will not be able to instantly go from pitchAway[0] to pitchAway[11]
        
        """

        #
        for team in [home, away]:
            for player in team.lineup.keys:
                player.lastPosition = -1

    # Calculating the total amount of attacks by using the offense and defence points of home and away teams. The
    # dominant team usually attacks more.
    def attackNumber(self, home, away):
        """
        :param home:
        :param away:
        :return:
        """
        homeOffense = round(home.offensePoint + random.triangular(-10, 10))
        homeDefence = round(home.defencePoint + random.triangular(-10, 10))
        awayOffense = round(away.offensePoint + random.triangular(-10, 10))
        awayDefence = round(away.defencePoint + random.triangular(-10, 10))

        homeGuarantee = homeOffense * 0.2
        homeOverAway = homeOffense - awayDefence * 0.5
        homeTotal = homeGuarantee + homeOverAway
        awayGuarantee = awayOffense * 0.2
        awayOverHome = awayOffense - homeDefence * 0.5
        awayTotal = awayGuarantee + awayOverHome

        totalAttacks = (homeOffense * 0.70 + homeDefence * 0.30) + (awayOffense * 0.7 + awayDefence * 0.3)
        homeAttacks = totalAttacks * ((homeTotal + random.triangular(0, 5)) / (homeTotal + awayTotal))
        awayAttacks = totalAttacks - homeAttacks

        return (round(homeAttacks), round(awayAttacks))
