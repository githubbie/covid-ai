from ruimte import *
from groep import *
from rooster import *
from toeschouwer import *

class Log():
    def __init__(self, filenaam = '', modulo = 1):
        if filenaam == '':
            self.file = None
        else:
            self.file = open(filenaam, 'w')
        self.namen = "dag blijheid onbesmet besmet ziek asym_ziek immuun mk_plicht R".split()
        self.formats = "{:11d} {:11.2f} {:11.2f} {:11.2f} {:11.2f} {:11.2f} {:11.2f} {:11d} {:11.2f}".split()
        self.modulo = modulo
        self.iteratie = 0
    
    def start(self):
        if self.file:
            self.file.write(",".join(self.namen))
            self.file.write("\n")
        if self.modulo > 0:
            print("|"+"|".join(["{:^11s}".format(naam) for naam in self.namen])+"|")
            print("+"+"+".join(["-"*11 for _ in self.namen])+"+")

    def regel(self, *waardes):
        if self.file:
            self.file.write(",".join(str(waarde) for waarde in waardes))
            self.file.write("\n")
        if self.modulo > 0 and self.iteratie % self.modulo == 0:
            print("|"+"|".join([format.format(waarde) for format, waarde in zip(self.formats, waardes)])+"|")
        self.iteratie += 1

    def einde(self):
        if self.file:
            self.file.close()
        if self.modulo > 0:
            print("+"+"+".join(["-"*11 for _ in self.namen])+"+")
            print("|"+"|".join(["{:^11s}".format(naam) for naam in self.namen])+"|")

class Model():
    def __init__(self, ziekte, effecten):
        self.ruimtes = []
        self.groepen = []
        self.omgeving = Omgeving(0.0)
        self.ziekte = ziekte
        self.effecten = effecten

    def beta(self, waar, beta):
        if isinstance(waar, Ruimte):
            waar = [waar]
        for ruimte in waar:
            ruimte.beta = beta

    def besmettelijkheid(self, waar, besmettelijkheid):
        if isinstance(waar, Omgeving):
            waar = [waar]
        for ruimte in waar:
            ruimte.besmettelijkheid = besmettelijkheid

    def groeps_verdeling(self, wie, onbesmet, besmet, ziek, asym_ziek, immuun):
        if isinstance(wie, Groep):
            wie = [wie]
        for groep in wie:
            groep.onbesmet = onbesmet
            groep.besmet = besmet
            groep.ziek = ziek
            groep.asym_ziek = asym_ziek
            groep.immuun = immuun

    def start(self, filenaam, modulo = 1):
        self.routes = bereken_routes(self.ruimtes)
        printer = Printer()
        tabel = TabelMaker()
        #self.toeschouwer = Keten(tabel)
        #self.toeschouwer.volg(*(self.ruimtes))
        #self.toeschouwer.volg(*(self.groepen))
        self.toeschouwer = Toeschouwer()
        self.log = Log(filenaam, modulo)
        self.log.start()

    def simulatie_stap(self, nummer):
        self.dag(nummer)
        mk_plicht = sum([1 for r in self.ruimtes if r.mondkapjes])
        self.log.regel(nummer, 
                       self.totaal.blijheid, 
                       self.totaal.onbesmet, 
                       self.totaal.besmet, 
                       self.totaal.ziek, 
                       self.totaal.asym_ziek, 
                       self.totaal.immuun, 
                       mk_plicht, 
                       self.totaal.R())
        self.nacht(nummer)

    def simulatie(self, aantal_dagen, neem_mondkapjes_besluit):
        for nummer in range(aantal_dagen):
            self.simulatie_stap(nummer)
            neem_mondkapjes_besluit(self)

    def einde(self, filenaam):
        self.log.einde()
        self.toeschouwer.afronden(filenaam)

    def _totaal(self):
        combinatie_groep = Groep("totaal:", self.ziekte, self.effecten, 0, 0, 0, 0, 0)
        for groep in self.groepen:
           combinatie_groep.som(groep)
        return combinatie_groep

    def reset_alles(self):
        for ruimte in self.ruimtes:
            ruimte.reset_alles()
        for groep in self.groepen:
            groep.reset_alles()
        self.totaal = self._totaal()

class LangeGangSchool(Model):
    def __init__(self, ziekte, effecten, aantal_gangen, aantal_klassen):
        super().__init__(ziekte, effecten)
        self.lokalen = [Ruimte("L%d" % n, ziekte, 0.0) for n in range(aantal_gangen*2)]
        self.gangen = [Ruimte("G%d" % n, ziekte, 0.0) for n in range(aantal_gangen)]
        self.voorhal = Ruimte("VH", ziekte, 0.0)
        self.docenten_kamer = Ruimte("DK", ziekte, 0.0)

        for n in range(aantal_gangen):
            self.lokalen[2*n].voeg_buren_toe({ self.gangen[n]: 1 })
            self.lokalen[2*n+1].voeg_buren_toe({ self.gangen[n]: 1 })
            self.gangen[n].voeg_buren_toe({ self.lokalen[2*n]: 1, self.lokalen[2*n+1]: 1 })
            if n > 0:
                self.gangen[n].voeg_buren_toe({ self.gangen[n-1]: 1 })
            if n < aantal_gangen-1:
                self.gangen[n].voeg_buren_toe({ self.gangen[n+1]: 1 })

        self.voorhal.voeg_buren_toe({ self.gangen[0]: 1 })
        self.gangen[0].voeg_buren_toe({ self.voorhal: 1 })
        self.docenten_kamer.voeg_buren_toe({ self.gangen[aantal_gangen-1]: 1 })
        self.gangen[aantal_gangen-1].voeg_buren_toe({ self.docenten_kamer : 1 })
        self.ruimtes = [self.voorhal, self.docenten_kamer] + self.lokalen + self.gangen

        self.docenten = [Groep("d%d" % n, ziekte, effecten, 1, 0, 0, 0, 0) for n in range(aantal_klassen)]
        self.klassen = [Groep("k%d" % n, ziekte, effecten, 30, 0, 0, 0, 0) for n in range(aantal_klassen)]
        self.groepen = self.docenten + self.klassen

        self.totale_zieken = 0.0

    def reset_alles(self):
        super().reset_alles()
        self.totale_zieken = 0.0
        
    def dag(self, nummer):
        schooldag(self.klassen, self.docenten, self.lokalen, self.gangen, self.voorhal, self.docenten_kamer, self.routes, nummer, self.toeschouwer)
        for groep in self.groepen:
            groep.verwerk_buiten_school(self.omgeving)
        self.totaal = self._totaal()

    def nacht(self, nummer):
        for groep in self.groepen:
            groep.nacht()
        self.totaal = self._totaal()
        self.totale_zieken += self.totaal.nieuwe_zieken

    def einde(self, filenaam):
        super().einde(filenaam)
        return self.totale_zieken, self.totaal.blijheid
