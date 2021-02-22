from covid import *
from model import *
from besluiten import *
from time import perf_counter
from q_learning import QLearning

AANTAL_GANGEN = 10

model = LangeGangSchool(covid19, effecten, AANTAL_GANGEN, AANTAL_GANGEN*2-1)

def reset(model):
    model.reset_alles()
    model.beta(model.lokalen, 0.0)
    model.beta(model.gangen, 0.0)
    model.beta(model.docenten_kamer, 0.0)
    model.beta(model.voorhal, 1.0)
    model.groeps_verdeling(model.docenten, 1, 0, 0, 0, 0)
    model.groeps_verdeling(model.klassen, 29, 1, 0, 0, 0)
    model.besmettelijkheid(model.omgeving, 0)

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

# Boete voor besluit is even groot als 5% zieke kinderen

besluit_boete = -0.05*30*(AANTAL_GANGEN*2-1)*model.effecten.ziekte_boete
print(besluit_boete)
ql = QLearning(model, reset, besluit_boete, 5, 100, [0.1, 0.6, 0.1])
ql.train(3600, 'training.log', None, 1000)