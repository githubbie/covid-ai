# beta: besmettelijkheid [%]
#   kans dat een onbesmet iemand besmet wordt door een besmettelijke persoon als ze contact hebben
beta = 0.0001

# sigma: incubatie tijd [dagen]
#   aantal dagen voor een besmet persoon of ziek wordt, of niet ziek blijft
#
sigma = 0.2

# alpha: kans op ziekte [%]
#   percentage besmette personen dat ziek wordt na de incubatie tijd
alpha = 0.8

# gammasym_ziek: herstelkans [%]
#   percentage zieke mensen dat hersteld en daarna immuun wordt (en niet meer besmettelijk is)
gammasym_ziek = 0.1

# gamma_asym_ziek: immuniteitskans [%]
#   percentage asym_zieke mensen dat immuun wordt (en niet meer besmettelijk is)
gamma_asym_ziek = 0.1

# epsilon_in: effectiviteit maskers [%]
#   percentage demping dat masker biedt voor besmettelijkheid uit de omgeving
epsilon_in = 0.5

# epsilon_uit: effectiviteit makers [%]
#   percentage demping dat masker biedt voor het overdragen van besmettelijkheid naar de omgeving
epsilon_uit = 0.8

# mondkapjes_boete: effect op de blijheid van het dragen van een mondkapje
#   hoeveel blijheid het kost als iemand een mondkapje op moet
mondkapjes_boete = 0.01

# ziekte_boete: effect op de blijheid van ziek worden
#   hoeveel blijheid het kost als iemand ziek wordt
ziekte_boete = 100.0