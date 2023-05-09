class PlayerInGame:

    def __init__(self, player, formation):
        self.stats = player
        self.position = PlayerInGame.playerPosition(self, formation, player)

        self.currentLocation = -1
        self.previousLocation = -1

        self.goals = 0
        self.assists = 0

        self.ballsLost = 0
        self.badFirstTouches = 0

        self.passesCompleted = 0
        self.passesFailed = 0

        self.shotsInTarget = 0
        self.shotsMissed = 0


    # A function to return the player's position.
    def playerPosition(self, formation, player):
        positions = ["GK", "CB", "RB", "LB", "CM", "CDM", "CAM", "RM", "RW", "LM", "LW", "ST"]
        for i in list(formation.keys()):
            if formation[i][0] == player:
                position = list(formation.keys())[i]

        for i in range(len(position) + 1):
            for j in positions:
                if position[:i] == j:
                    playerPos = j

        return playerPos


