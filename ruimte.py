class Ruimte:
    # naam: de naam van de ruimte
    # ziekte: de parameters van de ziekte
    # beta [%]: besmettelijkheid van de ruimte
    def __init__(self, naam, ziekte, beta):
        self.naam = naam
        self.ziekte = ziekte
        self.beta = beta
        self.mondkapjes = False
        self.buren = {}
        self.besmettelijkheid = 0

    # haal alle besmettelijkheid uit de ruimte weg
    def reset(self):
        self.besmettelijkheid = 0

    # bezoek van mensen aan een ruimte beinvloed de hoeveelheid
    # besmettelijkheid van de ruimte
    def bezoek(self, mensen):
        if self.mondkapjes:
            self.besmettelijkheid += (1.0 - self.ziekte.epsilon_uit) * mensen.asym_ziek
        else:
            self.besmettelijkheid += mensen.asym_ziek
        self.besmettelijkheid *= self.beta

    # buren [ruimte -> afstand]: verbindingen met andere ruimtes
    def voeg_buren_toe(self, buren):
        self.buren.update(buren)

    def mondkapjes_plicht(self, ja_nee):
        self.mondkapjes = ja_nee

class Omgeving():
    def __init__(self, besmettelijkheid):
        self.naam = "omgeving"
        self.besmettelijkheid = besmettelijkheid
        self.mondkapjes = False

ONBEREIKBAAR = 1e10

def print_routes(routes):
    for r1 in routes.keys():
        for r2 in routes[r1].keys():
            naam1 = r1.naam
            naam2 = r2.naam
            afstand = routes[r1][r2][0]
            route = routes[r1][r2][1]
            if r1 != r2 and \
               not naam1.startswith("G") and \
               not naam2.startswith("G") and \
               afstand != ONBEREIKBAAR:
                print("%s->%s: %d via %s" % (naam1, naam2, afstand, ", ".join([r.naam for r in route])))

def bereken_routes(ruimtes, routes = None, iteratie = 0, debug = False):
    if debug:
        print("Iteratie %d:" % iteratie)
    if routes == None:
        routes = { r1: { r2: (ONBEREIKBAAR, []) for r2 in ruimtes} for r1 in ruimtes }
        for r in ruimtes:
            routes[r][r] = (0, [])
    veranderd = False
    for r1 in ruimtes:
        for r2 in ruimtes:
            for r3, d2_3 in r2.buren.items():
                if routes[r1][r2][0] + d2_3 < routes[r1][r3][0]:
                    veranderd = True
                    routes[r1][r3] = (routes[r1][r2][0] + d2_3, routes[r1][r2][1] + [r3])
    if debug:
        print_routes(routes)
        if veranderd:
            print("Veranderd - herhaal")
        else:
            print("Klaar")
            print("")
    if veranderd:
        routes = bereken_routes(ruimtes, routes, iteratie+1, debug)
    return routes
