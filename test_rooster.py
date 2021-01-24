from toeschouwer import *
from groep import *
from ruimte import *
from rooster import *

# School opbouwen
aantal_gangen = 3

L = [Ruimte("L%d" % n, 0) for n in range(aantal_gangen*2)]
G = [Ruimte("G%d" % n, 0) for n in range(aantal_gangen)]
VH = Ruimte("VH", 0)
DK = Ruimte("DK", 0)

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
D = [Groep("d%d" % n, 1, 0, 0, 0, 0) for n in range(aantal_klassen)]
K = [Groep("k%d" % n, 25, 0, 0, 5, 0) for n in range(aantal_klassen)]

printer = Printer()
tabel = TabelMaker()
toeschouwer = Keten(printer, tabel)
toeschouwer.volg(*(L+G+[VH, DK]))
toeschouwer.volg(*(K+D))

VH.mondkapjes=True

schooldag(K, D, L, G, VH, DK, routes, 1, toeschouwer)
for groep in K+D:
    groep.nacht()
schooldag(K, D, L, G, VH, DK, routes, 2, toeschouwer)

toeschouwer.afronden('model.csv')
