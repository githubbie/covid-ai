class Groep:
    # naam: de naam van de groep
    # ziekte: de parameters van de ziekte
    # effecten: de effecten van de maatregelen op de blijheid van de groep
    # onbesmet: aantal mensen dat geen virus draagt, maar wel nog vatbaar is
    # besmet: aantal mensen dat het virus draagt, maar nog niet ziek of besmettelijk is
    # ziek: aantal mensen dat ziek is en besmettelijk
    # asym_ziek: aantal mensen dat niet ziek is, maar wel besmettelijk
    # immuun: aantal mensen dat geen virus draagt en ook niet meer vatbaar is
    def __init__(self, naam, ziekte, effecten, onbesmet, besmet, ziek, asym_ziek, immuun):
        self.naam = naam
        self.ziekte = ziekte
        self.effecten = effecten
        
        # huidige toestand
        self.onbesmet = onbesmet
        self.besmet = besmet
        self.ziek = ziek
        self.asym_ziek = asym_ziek
        self.immuun = immuun
        self.blijheid = 0
        self.mondkapje = False

        # meest recente veranderingen
        self.nieuwe_besmettingen = 0
        self.nieuwe_zieken = 0
        self.nieuwe_asym_zieken = 0
        self.herstelde_zieken = 0
        self.herstelde_asym_zieken = 0
    
    def reset_alles(self):
        # huidige toestand
        self.onbesmet = 0
        self.besmet = 0
        self.ziek = 0
        self.asym_ziek = 0
        self.immuun = 0
        self.blijheid = 0
        self.mondkapje = False

        # meest recente veranderingen
        self.nieuwe_besmettingen = 0
        self.nieuwe_zieken = 0
        self.nieuwe_asym_zieken = 0
        self.herstelde_zieken = 0
        self.herstelde_asym_zieken = 0

    # Tijdens de nacht worden mensen ziek of weer beter
    def nacht(self):
        self.nieuwe_zieken = self.besmet * self.ziekte.sigma * self.ziekte.alpha
        self.nieuwe_asym_zieken = self.besmet * self.ziekte.sigma * (1.0 - self.ziekte.alpha)
        self.herstelde_zieken = self.ziek * self.ziekte.gamma_sym_ziek
        self.herstelde_asym_zieken = self.asym_ziek * self.ziekte.gamma_asym_ziek

        self.besmet += - self.nieuwe_zieken - self.nieuwe_asym_zieken
        self.ziek += self.nieuwe_zieken - self.herstelde_zieken
        self.asym_ziek += self.nieuwe_asym_zieken - self.herstelde_asym_zieken
        self.immuun += self.herstelde_zieken + self.herstelde_asym_zieken
        self.blijheid -= self.effecten.ziekte_boete * self.nieuwe_zieken

        self.nieuwe_besmettingen = 0
        self.mondkapje = False

    # Buiten schooltijd kun je ziek worden van je omgeving
    def verwerk_buiten_school(self, omgeving):
        self.mondkapje = False
        self.bezoek(omgeving, 120)

    # Bezoek een ruimte voor een bepaalde tijd (in minuten)
    def bezoek(self, ruimte, tijd):
        besmettelijkheid = self.ziekte.beta * ruimte.besmettelijkheid * (tijd / 24*60)

        if ruimte.mondkapjes:
            if not self.mondkapje:
                self.blijheid -= self.effecten.mondkapjes_keer_boete
                self.mondkapje = True
            besmettelijkheid *= (1.0 - self.ziekte.epsilon_in)
            self.blijheid -= self.effecten.mondkapjes_tijd_boete * (tijd / 24*60)
        else:
            self.mondkapje = False

        nieuwe_besmettingen = min(self.onbesmet, self.onbesmet * besmettelijkheid)
        self.onbesmet -= nieuwe_besmettingen
        self.besmet += nieuwe_besmettingen
        self.nieuwe_besmettingen += nieuwe_besmettingen
        if besmettelijkheid > 0 and self.naam == 'k0':
            return
            print(self.naam, ruimte.naam, besmettelijkheid, self.onbesmet, self.nieuwe_besmettingen, self.besmet)

    def som(self, andere_groep):
        self.onbesmet += andere_groep.onbesmet
        self.besmet += andere_groep.besmet
        self.ziek += andere_groep.ziek
        self.asym_ziek += andere_groep.asym_ziek
        self.immuun += andere_groep.immuun
        self.blijheid += andere_groep.blijheid

        # meest recente veranderingen
        self.nieuwe_besmettingen += andere_groep.nieuwe_besmettingen
        self.nieuwe_zieken += andere_groep.nieuwe_zieken
        self.nieuwe_asym_zieken += andere_groep.nieuwe_asym_zieken
        self.herstelde_zieken += andere_groep.herstelde_zieken
        self.herstelde_asym_zieken += andere_groep.herstelde_asym_zieken

    def R(self):
        if (self.ziek + self.asym_ziek > 0.5):
            return self.nieuwe_besmettingen / (self.ziek + self.asym_ziek) / self.ziekte.sigma
        else:
            return float('nan')