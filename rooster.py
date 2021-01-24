from toeschouwer import *
import random

# ken elke groep uit groepen een willekeurig lokaal uit lokalen
# toe, in de lokaties (deze wordt gewijzigd!). Elke lokaal krijgt
# maar 1 groep
def willekeurig(lokaties, groepen, lokalen):
    geselecteerde_lokalen = random.sample(lokalen, len(groepen))
    lokaties.update(dict(zip(groepen, geselecteerde_lokalen)))
    return lokaties

# ken elke groep uit groepen hetzelfde lokaal toe in de lokaties
# (deze wordt gewijzigd).
def verzamel(lokaties, groepen, lokaal):
    lokaties.update({ groep: lokaal for groep in groepen })
    return lokaties

# verwerk de aanwezigheid volgens de toekenning in lokaties
def bezoek(lokaties, tijd):
    # alle ruimtes krijgen bezoek van de groepen, om de
    # besmettelijkheid vast te stellen
    #for groep, ruimte in lokaties.items():
    #    ruimte.bezoek(groep)
    # alle groepen bezoeken hun ruimtes, om de besmettingen
    # vast te stellen
    for groep, ruimte in lokaties.items():
        groep.bezoek(ruimte, tijd)

# reset alle gegeven ruimtes
def reset(*ruimtes):
    for ruimte in ruimtes:
        ruimte.reset()

# verplaats alle groepen uit de huidige lokaties, naar de gegeven
# doelen, gebruik makend van de routes en met stap_tijd per stap.
# Na afloop zijn alle ruimtes in de lokaties gewijzigd in de doelen
def verplaats(lokaties, doelen, routes, stap_tijd, toeschouwer):
    # alle groepen verplaatsen zich van hun huidige lokaties naar de
    # doelen, met gegeven staptijd verblijf in elke volgende stap in de route
    groepen = lokaties.keys()
    veranderd = True
    stap = 1
    while veranderd:
        veranderd = False
        for groep in groepen:
            huidig = lokaties[groep]
            doel = doelen[groep]
            if huidig != doel:
                lokaties[groep] = routes[huidig][doel][1][0]
                lokaties[groep].bezoek(groep)
                veranderd = True
        if veranderd:
            bezoek(lokaties, stap_tijd)
            toeschouwer.actie(" +- stap %d" % stap, lokaties)
            stap+=1

def begin(lokaties):
    for groep, ruimte in lokaties.items():
        ruimte.bezoek(groep)

def les(lokaties, docenten_rooster, klassen, lokalen, routes, stap_tijd, les_tijd, toeschouwer):
    doelen = willekeurig(docenten_rooster.copy(), klassen, list(docenten_rooster.values()))
    verplaats(lokaties, doelen, routes, stap_tijd, toeschouwer)
    bezoek(lokaties, les_tijd)

def pauze(lokaties, pauze_lokaties, routes, stap_tijd, pauze_tijd, toeschouwer):
    verplaats(lokaties, pauze_lokaties, routes, stap_tijd, toeschouwer)
    bezoek(lokaties, pauze_tijd)

def schooldag(klassen, docenten, lokalen, gangen, voorhal, docenten_kamer, routes, 
              dag, toeschouwer = Toeschouwer()):
    # alle klassen beginnen in voorhal, alle docenten in docenten_kamer
    pauze_lokaties = {}
    verzamel(pauze_lokaties, klassen, voorhal)
    verzamel(pauze_lokaties, docenten, docenten_kamer)
    # alle docenten hebben vast lokalen per dag
    docenten_rooster = {}
    willekeurig(docenten_rooster, docenten, lokalen)

    # start de dag
    reset(*lokalen, *gangen, voorhal, docenten_kamer)
    toeschouwer.actie("+ start dag %d" % dag, {})
    begin(pauze_lokaties)
    bezoek(pauze_lokaties, 5.0)
    toeschouwer.actie("+- begin %d" % dag, pauze_lokaties)
    lokaties = pauze_lokaties.copy()

    # 1e blok van 2 lessen
    for n in [1, 2]:
        reset(*lokalen, *gangen, voorhal, docenten_kamer)
        les(lokaties, docenten_rooster, klassen, lokalen, routes, 0.5, 50, toeschouwer)
        toeschouwer.actie("+- les %d.%d" % (dag, n), lokaties)

    # kleine pauze
    reset(*lokalen, *gangen, voorhal, docenten_kamer)
    pauze(lokaties, pauze_lokaties, routes, 0.5, 20, toeschouwer)
    toeschouwer.actie("+- kl pauze %d" % dag, lokaties)

    # 2e blok van 3 lessen
    for n in [3, 4, 5]:
        reset(*lokalen, *gangen, voorhal, docenten_kamer)
        les(lokaties, docenten_rooster, klassen, lokalen, routes, 0.5, 50, toeschouwer)
        toeschouwer.actie("+- les %d.%d" % (dag, n), lokaties)

    # grote pauze
    reset(*lokalen, *gangen, voorhal, docenten_kamer)
    pauze(lokaties, pauze_lokaties, routes, 0.5, 30, toeschouwer)
    toeschouwer.actie("+- gr pauze %d" % dag, lokaties)

    # 3e blok van 2 lessen
    for n in [6, 7]:
        reset(*lokalen, *gangen, voorhal, docenten_kamer)
        les(lokaties, docenten_rooster, klassen, lokalen, routes, 0.5, 50, toeschouwer)
        toeschouwer.actie("+- les %d.%d" % (dag, n), lokaties)

    reset(*lokalen, *gangen, voorhal, docenten_kamer)
    pauze(lokaties, pauze_lokaties, routes, 0.5, 1, toeschouwer)
    toeschouwer.actie("+- einde %d" % dag, lokaties)

    # einde van de dag
    reset(*lokalen, *gangen, voorhal, docenten_kamer)
    toeschouwer.actie("+ einde dag %d" % dag, {})