import random
TurkishLeague = ["Alanyaspor", "Ankaragücü", "Antalyaspor", "Beşiktaş", "Çaykur Rizespor", "Denizlispor", "Fenerbahçe", "Galatasaray", "Gazişehir Gaziantep",
            "Gençlerbirliği", "Göztepe SK", "İstanbul Başakşehir", "Kasımpaşa", "Kayserispor", "Konyaspor", "Sivasspor", "Trabzonspor", "Yeni Malatyaspor"]


class Fixture:
    def __init__(self, league):
        self.league = league
        self.fixture = Fixture.createFixture(self.league)

    def createFixture(league):
        random.shuffle(league)
        first_ele = league[0]
        del league[0]
        fixture = []


        for i in range(17):
            first = 1
            last = len(league) - 1
            week = []
            week.append(f"{first_ele} - {league[0]}")
            while last > first:
                week.append(f"{league[first]} - {league[last]}")
                first += 1
                last += -1
            lastEle = league.pop()
            league.insert(0, lastEle)
            fixture.append(week)

        for i in range(17):
            week = []
            for j in fixture[i]:
                splitted = j.split("-")
                home = splitted[1]
                away = splitted[0]
                week.append(f"{home} - {away}")
            fixture.append(week)

        return fixture



