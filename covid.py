class Ziekte():
    def __init__(self, alpha, beta, gamma_sym_ziek, gamma_asym_ziek, sigma, epsilon_in, epsilon_uit):
        # beta: besmettelijkheid [%]
        #   kans dat een onbesmet iemand besmet wordt door een besmettelijke persoon als ze contact hebben
        self.beta = beta

        # sigma: incubatie tijd [%]
        #   kans dat een besmet persoon ziek wordt, of nog besmet blijft
        #   omgekeerd evenredig met het aantal dagen voor een besmet persoon of ziek wordt
        #
        self.sigma = sigma

        # alpha: kans op ziekte [%]
        #   percentage besmette personen dat ziek wordt na de incubatie tijd
        self.alpha = alpha

        # gammasym_ziek: herstelkans [%]
        #   percentage zieke mensen dat hersteld en daarna immuun wordt (en niet meer besmettelijk is)
        self.gamma_sym_ziek = gamma_sym_ziek

        # gamma_asym_ziek: immuniteitskans [%]
        #   percentage asym_zieke mensen dat immuun wordt (en niet meer besmettelijk is)
        self.gamma_asym_ziek = gamma_asym_ziek

        # epsilon_in: effectiviteit maskers [%]
        #   percentage demping dat masker biedt voor besmettelijkheid uit de omgeving
        self.epsilon_in = epsilon_in

        # epsilon_uit: effectiviteit makers [%]
        #   percentage demping dat masker biedt voor het overdragen van besmettelijkheid naar de omgeving
        self.epsilon_uit = epsilon_uit

class Welbevinden():
    def __init__(self, mondkapjes_tijd_boete, mondkapjes_keer_boete, ziekte_boete):
        # mondkapjes_boete: effect op de blijheid van het dragen van een mondkapje [/min]
        #   hoeveel blijheid het kost als iemand een mondkapje op moet
        self.mondkapjes_tijd_boete = mondkapjes_tijd_boete

        # mondkapjes_opzet_boete: effect op de blijheid van het opzetten van een mondkapje [/#]
        self.mondkapjes_keer_boete = mondkapjes_keer_boete

        # ziekte_boete: effect op de blijheid van ziek worden [/#]
        #   hoeveel blijheid het kost als iemand ziek wordt
        self.ziekte_boete = ziekte_boete

covid19 = Ziekte(0.8, 0.0001, 0.1, 0.1, 0.2, 0.5, 0.8)
effecten = Welbevinden(0.1/(24*60), 0.01, 10.0)