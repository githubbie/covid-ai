from covid import *
from model import *
from besluiten import *
from time import perf_counter
from q_learning import QLearning

model = LangeGangSchool(covid19, effecten, 10, 10*2-1)

def reset(model):
    model.reset_alles()
    model.beta(model.lokalen, 0.0)
    model.beta(model.gangen, 0.0)
    model.beta(model.docenten_kamer, 0.0)
    model.beta(model.voorhal, 1.0)
    model.groeps_verdeling(model.docenten, 1, 0, 0, 0, 0)
    model.groeps_verdeling(model.klassen, 29, 1, 0, 0, 0)
    model.besmettelijkheid(model.omgeving, 0)

for op in range(0, 150, 1000):
    beste_blijheid = -1e9
    beste_af = 0
    for af in range(0, 150, 1000):
        reset(model)
        model.start('model1.csv', 0)
        model.simulatie(101, op_af2([model.voorhal], op, af))
        tz, tb = model.einde('')
        if tb > beste_blijheid:
            beste_blijheid = tb
            beste_tz = tz
            beste_af = af
    print("op={:3d}, beste_af={:3d}, aantal zieken={:8.2f}, beste_blijheid={:8.2f}".format(op, beste_af, beste_tz, beste_blijheid))

reset(model)
model.start('model1.csv', 0)
model.simulatie(101, op_af2([model.voorhal], 30, 50))
print(model.einde(''))

tic = perf_counter()
runs = 1
for n in range(runs):
    reset(model)
    model.start('', 0)
    model.simulatie(101, nergens_mondkapjes)
    model.einde('')
toc = perf_counter()
print("Executed {:d} model runs in {:8.2f} seconds, {:.2f} seconds/run.".format(runs, toc-tic, (toc-tic)/runs))

ql = QLearning(model, reset, 10, [0.1, 0.6, 0.1])
ql.train(200000, 'training.log', None, 10000)
