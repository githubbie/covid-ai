import covid

class Groep:
    # onbesmet: aantal mensen dat geen virus draagt, maar wel nog vatbaar is
    # besmet: aantal mensen dat het virus draagt, maar nog niet ziek of besmettelijk is
    # ziek: aantal mensen dat ziek is en besmettelijk
    # asym_ziek: aantal mensen dat niet ziek is, maar wel besmettelijk
    # immuun: aantal mensen dat geen virus draagt en ook niet meer vatbaar is
    def __init__(self, naam, onbesmet, besmet, ziek, asym_ziek, immuun):
        self.naam = naam
        
        # huidige toestand
        self.onbesmet = onbesmet
        self.besmet = besmet
        self.ziek = ziek
        self.asym_ziek = asym_ziek
        self.immuun = immuun
        self.blijheid = 0

        # meest recente veranderingen
        self.nieuwe_besmettingen = 0
        self.nieuwe_zieken = 0
        self.nieuwe_asym_zieken = 0
        self.herstelde_zieken = 0
        self.herstelde_asym_zieken = 0

    # Tijdens de nacht worden mensen ziek of weer beter
    def nacht(self):
        self.nieuwe_zieken = self.besmet * covid.sigma * covid.alpha
        self.nieuwe_asym_zieken = self.besmet * covid.sigma * (1.0 - covid.alpha)
        self.herstelde_zieken = self.ziek * covid.gammasym_ziek
        self.herstelde_asym_zieken = self.asym_ziek * covid.gamma_asym_ziek

        self.besmet += - self.nieuwe_zieken - self.nieuwe_asym_zieken
        self.ziek += self.nieuwe_zieken - self.herstelde_zieken
        self.asym_ziek += self.nieuwe_asym_zieken - self.herstelde_asym_zieken
        self.immuun += self.herstelde_zieken + self.herstelde_asym_zieken
        self.blijheid -= covid.ziekte_boete * self.nieuwe_zieken

        self.nieuwe_besmettingen = 0

    # Buiten schooltijd kun je ziek worden van je omgeving
    def verwerk_buiten_school(self, omgeving):
        self.bezoek(omgeving, 120)

    # Bezoek een ruimte voor een bepaalde tijd (in minuten)
    def bezoek(self, ruimte, tijd):
        besmettelijkheid = covid.beta * ruimte.besmettelijkheid * (tijd / 24*60)

        if ruimte.mondkapjes:
            besmettelijkheid *= (1.0 - covid.epsilon_in)
            self.blijheid -= covid.mondkapjes_boete * (tijd / 24*60)

        self.nieuwe_besmettingen = min(self.onbesmet, self.onbesmet * besmettelijkheid)
        self.onbesmet -= self.nieuwe_besmettingen
        self.besmet += self.nieuwe_besmettingen