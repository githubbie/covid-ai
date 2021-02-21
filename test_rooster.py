from covid import *
from model import *
from besluiten import *

model = LangeGangSchool(covid19, effecten, 3, 5)
model.beta(model.lokalen, 0.0)
model.beta(model.gangen, 0.0)
model.beta([model.voorhal], 1)
model.groeps_verdeling(model.docenten, 1, 0, 0, 0, 0)
model.groeps_verdeling(model.klassen, 29, 1, 0, 0, 0)
model.besmettelijkheid(model.omgeving, 0)

for op in range(10):
    beste_blijheid = -1e9
    beste_af = 0
    for af in range(op+1):
        model.start('model1.csv', 0)
        model.simulatie(101, op_af(model.gangen, op, af))
        tz, tb = model.einde('')
        if tb > beste_blijheid:
            beste_blijheid = tb
            beste_tz = tz
            beste_af = af
    print("op={:3d}, beste_af={:3d}, aantal zieken={:8.2f}, beste_blijheid={:8.2f}".format(op, beste_af, beste_tz, beste_blijheid))