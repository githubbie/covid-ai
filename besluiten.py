from ruimte import Ruimte

def op_af(ruimtes, op_waarde, af_waarde):
    def besluit(model):
        for ruimte in ruimtes:
            if ruimte.mondkapjes:
                ruimte.mondkapjes_plicht(model.totaal().ziek > af_waarde)
            else:
                ruimte.mondkapjes_plicht(model.totaal().ziek > op_waarde)
    
    return besluit