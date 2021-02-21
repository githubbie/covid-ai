class Model():
    def __init__(self):
        self.ruimtes = []
        self.groepen = []
        self.ziekte = None

    def start(self):
        self.routes = routes = bereken_routes(self.ruimtes)

class LangeGangSchool(Model):
    def __init__(self, ziekte, effecten, aantal_gangen, aantal_klassen):
        self.lokalen = [Ruimte("L%d" % n, ziekte, 0.1) for n in range(aantal_gangen*2)]
        self.gangen = [Ruimte("G%d" % n, ziekte, 1.0) for n in range(aantal_gangen)]
        self.leerling_kantine = Ruimte("VH", ziekte, 0.5)
        self.docent_kantine = Ruimte("DK", ziekte, 0.1)

        for n in range(aantal_gangen):
            self.lokalen[2*n].voeg_buren_toe({ self.gangen[n]: 1 })
            self.lokalen[2*n+1].voeg_buren_toe({ self.gangen[n]: 1 })
            self.gangen[n].voeg_buren_toe({ self.lokalen[2*n]: 1, self.lokalen[2*n+1]: 1 })
            if n > 0:
                self.gangen[n].voeg_buren_toe({ self.gangen[n-1]: 1 })
            if n < aantal_gangen-1:
                self.gangen[n].voeg_buren_toe({ self.gangen[n+1]: 1 })

        self.leerling_kantine.voeg_buren_toe({ self.gangen[0]: 1 })
        self.gangen[0].voeg_buren_toe({ self.leerling_kantine: 1 })
        self.docent_kantine.voeg_buren_toe({ self.gangen[aantal_gangen-1]: 1 })
        self.gangen[aantal_gangen-1].voeg_buren_toe({ self.docent_kantine : 1 })
        self.ruimtes = [self.leerling_kantine, self.docent_kantine] + self.lokalen + self.gangen

        self.docenten = [Groep("d%d" % n, ziekte, effecten, 1, 0, 0, 0, 0) for n in range(aantal_klassen)]
        self.klassen = [Groep("k%d" % n, ziekte, effecten, 30, 0, 0, 0, 0) for n in range(aantal_klassen)]


