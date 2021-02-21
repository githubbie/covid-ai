from ruimte import Ruimte

def op_af(ruimtes, op_waarde, af_waarde):
    def besluit(model):
        for ruimte in ruimtes:
            if ruimte.mondkapjes:
                ruimte.mondkapjes_plicht(model.totaal().ziek >= af_waarde)
            else:
                ruimte.mondkapjes_plicht(model.totaal().ziek >= op_waarde)
    
    return besluit

def op_af2(ruimtes, op_waarde, af_waarde):
    def besluit(model, _toestand = []):
        if len(_toestand) == 0:
            _toestand = [0]
        toestand = _toestand[0]
        ziek = model.totaal().ziek
        if toestand == 0:
            for ruimte in ruimtes:
                ruimte.mondkapjes_plicht(ziek >= op_waarde)
            if ziek >= op_waarde:
                toestand = 1
        if toestand == 1:
            for ruimte in ruimtes:
                ruimte.mondkapjes_plicht(ziek >= op_waarde)
            if ziek >= af_waarde:
                toestand = 2
        if toestand == 2:
            for ruimte in ruimtes:
                ruimte.mondkapjes_plicht(ziek >= af_waarde)
        _toestand[0] = toestand
    
    return besluit

def nergens_mondkapjes(model):
    for ruimte in model.ruimtes:
        ruimte.mondkapjes_plicht(False)

def overal_mondkapjes(model):
    for ruimte in model.ruimtes:
        ruimte.mondkapjes_plicht(True)
