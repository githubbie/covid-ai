from ruimte import *
from groep import *
import csv

class Toeschouwer:
    def __init__(self):
        self.ruimtes = []
        self.groepen = []

    def volg(self, *items):
        for item in items:
            if isinstance(item, Ruimte):
                self.ruimtes.append(item)
            elif isinstance(item, Groep):
                self.groepen.append(item)

    def actie(self, beschrijving, lokaties):
        pass

    def afronden(self, *argumenten):
        pass

class Keten(Toeschouwer):
    def __init__(self, *toeschouwers):
        super().__init__()
        self.toeschouwers = toeschouwers

    def volg(self, *items):
        for toeschouwer in self.toeschouwers:
            toeschouwer.volg(*items)

    def actie(self, beschrijving, lokaties):
        for toeschouwer in self.toeschouwers:
            toeschouwer.actie(beschrijving, lokaties)

    def afronden(self, *argumenten):
        for toeschouwer in self.toeschouwers:
            toeschouwer.afronden(*argumenten)

    def voeg_toe(self, *toeschouwers):
        self.toeschouwers.extend(toeschouwers)


class Printer(Toeschouwer):
    def _lokatie_string(self, lokaties, groep):
        if groep in lokaties.keys():
            return lokaties[groep].naam 
        return "--"

    def _lokaties_string(self, lokaties, start):
        return ",".join([self._lokatie_string(lokaties, groep) 
                           for groep in self.groepen
                           if groep.naam.startswith(start)])

    def _bool_string(self, bool):
        return { True: "T", False: "F" }[bool]

    def _ruimte_string(self, ruimte):
        return "%s/%4.1f" % (self._bool_string(ruimte.mondkapjes), ruimte.besmettelijkheid)

    def _ruimtes_string(self):
        return ",".join([self._ruimte_string(ruimte) for ruimte in self.ruimtes])

    def _groep_string(self, groep):
        return "%4.1f/%4.1f/%4.1f/%4.1f/%4.1f/%4.1f" % \
            (groep.onbesmet, groep.besmet, groep.ziek, groep.asym_ziek, groep.immuun, groep.blijheid)

    def _groepen_string(self):
        return ",".join([self._groep_string(groep) for groep in self.groepen])

    def actie(self, beschrijving, lokaties):
        super().actie(beschrijving, lokaties)
        k_lokaties = self._lokaties_string(lokaties, "k")
        d_lokaties = self._lokaties_string(lokaties, "d")
        ruimtes = self._ruimtes_string()
        groepen = self._groepen_string()
        print("%s:\tk=(%s), d=(%s), R=(%s), G=(%s)" % \
            (beschrijving, k_lokaties, d_lokaties, ruimtes, groepen))

class TabelMaker(Printer):
    def __init__(self):
        super().__init__()
        self.tabel = []

    def _groep_kop(self, groep):
        return ([groep.naam] * 7, 
                ['lokatie', 'onbesmet', 'besmet', 'ziek', 'asym_ziek', 'immuun', 'blijheid'])

    def _ruimte_kop(self, ruimte):
        return ([ruimte.naam] * 3,
                ['mondkapjes', 'besmettelijkheid', 'besmettingen'])

    def _kop(self):
        kop1 = ['actie']
        kop2 = ['beschrijving']
        for groep in self.groepen:
            kop = self._groep_kop(groep)
            kop1.extend(kop[0])
            kop2.extend(kop[1])
        for ruimte in self.ruimtes:
            kop = self._ruimte_kop(ruimte)
            kop1.extend(kop[0])
            kop2.extend(kop[1])
        return (kop1, kop2)

    def actie(self, beschrijving, lokaties):
        regel = []
        regel.append(beschrijving)
        for groep in self.groepen:
            regel.extend([self._lokatie_string(lokaties, groep), 
                          groep.onbesmet, groep.besmet, groep.ziek,
                          groep.asym_ziek, groep.immuun, groep.blijheid])
        for ruimte in self.ruimtes:
            regel.extend([ruimte.mondkapjes, ruimte.besmettelijkheid])
            nieuwe_besmettingen = 0
            for groep, groep_ruimte in lokaties.items():
                if groep_ruimte == ruimte:
                    nieuwe_besmettingen += groep.nieuwe_besmettingen
            regel.append(nieuwe_besmettingen)
        self.tabel.append(regel)

    def afronden(self, file = None):
        if file == '':
            return
        elif file == None:
            file = '/dev/tty'
        with open(file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self._kop())
            writer.writerows(self.tabel)