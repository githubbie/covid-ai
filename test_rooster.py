from toeschouwer import *
from groep import *
from ruimte import *
from rooster import *
from covid import *


# School opbouwen
aantal_gangen = 3

L = [Ruimte("L%d" % n, covid19, 0.2) for n in range(aantal_gangen*2)]
G = [Ruimte("G%d" % n, covid19, 0.7) for n in range(aantal_gangen)]
VH = Ruimte("VH", covid19, 0.5)
DK = Ruimte("DK", covid19, 0.5)

for n in range(aantal_gangen):
    L[2*n].voeg_buren_toe({ G[n]: 1 })
    L[2*n+1].voeg_buren_toe({ G[n]: 1 })
    G[n].voeg_buren_toe({ L[2*n]: 1, L[2*n+1]: 1 })
    if n > 0:
        G[n].voeg_buren_toe({ G[n-1]: 1 })
    if n < aantal_gangen-1:
        G[n].voeg_buren_toe({ G[n+1]: 1 })

VH.voeg_buren_toe({ G[0]: 1 })
G[0].voeg_buren_toe({ VH: 1 })
DK.voeg_buren_toe({ G[aantal_gangen-1]: 1 })
G[aantal_gangen-1].voeg_buren_toe({ DK : 1 })

routes = bereken_routes(L+G+[VH,DK])
# print_routes(routes)

# Klassen & docenten opbouwen

aantal_klassen = 5
D = [Groep("d%d" % n, covid19, effecten, 1, 0, 0, 0, 0) for n in range(aantal_klassen)]
K = [Groep("k%d" % n, covid19, effecten, 29, 1, 0, 0, 0) for n in range(aantal_klassen)]

printer = Printer()
tabel = TabelMaker()
toeschouwer = Keten(tabel)
toeschouwer.volg(*(L+G+[VH, DK]))
toeschouwer.volg(*(K+D))

omgeving = Omgeving(0)

def combineer_groepen(naam, groepen):
    combinatie_groep = Groep(naam, groepen[0].ziekte, groepen[0].effecten, 0, 0, 0, 0, 0)
    for groep in groepen:
        combinatie_groep.som(groep)
    return combinatie_groep

class Log():
    def __init__(self, filenaam, modulo = 1):
        self.file = open(filenaam, 'w')
        self.namen = "dag blijheid onbesmet besmet ziek asym_ziek immuun plicht R".split()
        self.formats = "{:10d} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:10.2f} {:10d} {:10.2f}".split()
        self.modulo = modulo
        self.iteratie = 0
    
    def start(self):
        self.file.write(",".join(self.namen))
        self.file.write("\n")
        print("|"+"|".join(["{:^10s}".format(naam) for naam in self.namen])+"|")
        print("+"+"+".join(["-"*10 for _ in self.namen])+"+")

    def regel(self, *waardes):
        self.file.write(",".join(str(waarde) for waarde in waardes))
        self.file.write("\n")
        if self.iteratie % self.modulo == 0:
            print("|"+"|".join([format.format(waarde) for format, waarde in zip(self.formats, waardes)])+"|")
        self.iteratie += 1

    def einde(self):
        self.file.close()
        print("+"+"+".join(["-"*10 for _ in self.namen])+"+")
        print("|"+"|".join(["{:^10s}".format(naam) for naam in self.namen])+"|")

log = Log("model1.csv", 5)
log.start()
for dag in range(100):
    schooldag(K, D, L, G, VH, DK, routes, dag, toeschouwer)
    for groep in K+D:
        groep.verwerk_buiten_school(omgeving)
    totaal = combineer_groepen("totaal", K+D)
    plicht = sum([1 for r in [VH,DK] + L + G if r.mondkapjes])
    log.regel(dag, totaal.blijheid, totaal.onbesmet, totaal.besmet, totaal.ziek, totaal.asym_ziek, totaal.immuun, plicht, totaal.R())

    for groep in K+D:
        groep.nacht()
    for ruimte in [VH]: # [VH,DK]+L+G:
        if ruimte.mondkapjes:
            ruimte.mondkapjes_plicht(totaal.ziek > 5)
        else:
            ruimte.mondkapjes_plicht(totaal.ziek > 10)
log.einde()

toeschouwer.afronden('model.csv')
