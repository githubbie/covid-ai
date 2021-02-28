from covid import *
from model import *
from besluiten import *
from time import perf_counter
from q_learning4 import QLearning
import os.path

AANTAL_GANGEN = 10

model = LangeGangSchool(covid19, effecten, AANTAL_GANGEN, AANTAL_GANGEN*2-1)

def reset(model):
    model.reset_alles()
    model.beta(model.voorhal, 0.6)
    model.beta(model.docenten_kamer, 0.4)
    model.beta(model.lokalen, 0.2)
    model.beta(model.gangen, 0.8)
    model.groeps_verdeling(model.docenten, 1, 0, 0, 0, 0)
    model.groeps_verdeling(model.klassen, 29, 1, 0, 0, 0)
    model.besmettelijkheid(model.omgeving, 0)

reset(model)
model.start('model1.csv', 0)
model.simulatie(101, op_af([model.voorhal], 30, 50))
print(model.einde(''))

tic = perf_counter()
runs = 10
for n in range(runs):
    reset(model)
    model.start('', 0)
    model.simulatie(101, nergens_mondkapjes)
    model.einde('')
toc = perf_counter()
print("Executed {:d} model runs in {:8.2f} seconds, {:.2f} seconds/run, {:.0f} runs/hour.".format(runs, toc-tic, (toc-tic)/runs, 3600*runs/(toc-tic)))

def voortgang(ql, stap, logfile = None):
    iteraties, acties, blijheid = ql.gebruik()
    print("Beste oplossing bij {} - gevonden blijheid {:.2f} met {:d} acties:".format(stap, blijheid, len(acties)))
    if logfile:
        logfile.write("Beste oplossing bij {} - gevonden blijheid {:.2f} met {:d} acties\n".format(stap, blijheid, len(acties)))
        logfile.flush()
    for actie, dag in acties:
        print("  Op dag {:3d}, actie {:06b}".format(dag, actie))

# Boete voor besluit is even groot als 5% zieke kinderen
besluit_boete = -0.05*30*(AANTAL_GANGEN*2-1)*model.effecten.ziekte_boete
ql = QLearning(model, reset, besluit_boete, 1, 100, [0.1, 0.9, 0.1], 2)
log = open("sessie5.log", "a")
if os.path.exists('q_tabel_start.csv'):
    print("Laden q_table_start.csv:")
    ql.load_q_tabel('start')
    voortgang(ql, 'start', log)

for sessie in range(100):            # ~ 8,3 uur
    ql.train(400, '+training5.log')  # ~ 5 minuten per sessie
    voortgang(ql, sessie, log)
    ql.dump_q_tabel(sessie)

model.start('einde2.csv',1)
ql.gebruik()
model.einde('')

ql.dump_q_tabel('stop')