from random import uniform, randrange
from time import perf_counter

# returns de index van het maximum in de lijst
def argmax(l):
    f = lambda i: l[i]
    return max(range(len(l)), key=f)

class QLearning():
    def __init__(self, model, model_reset, besluit_boete, model_simulatie_stappen, max_dag_nummer, Qs):
        self.model = model
        self.model_reset = model_reset
        self.dag_nummer = 0
        self._q_tabel = {}
        self.Q_alpha = Qs[0]
        self.Q_gamma = Qs[1]
        self.Q_epsilon = Qs[2]
        self.besluit_boete = besluit_boete
        self.model_simulatie_stappen = model_simulatie_stappen
        self.max_dag_nummer = max_dag_nummer
        self.done = False
        self.aantal_acties = self._aantal_acties()

    def codeer_toestand(self):
        N=5
        return tuple([self.dag_nummer, 
                      N*round(self.model.totaal.ziek/N), 
                      N*round((self.model.totale_zieken - self.model.totaal.ziek)/N),
                      self.model.voorhal.mondkapjes,
                      self.model.docenten_kamer.mondkapjes,
                      self.model.lokalen[0].mondkapjes,
                      self.model.gangen[0].mondkapjes])
        return tuple([self.dag_nummer, 
                      round(self.model.totaal.ziek), 
                      round(self.model.totale_zieken - self.model.totaal.ziek),
                      self.model.voorhal.mondkapjes,
                      self.model.docenten_kamer.mondkapjes,
                      self.model.lokalen[0].mondkapjes] + \
                      [gang.mondkapjes for gang in self.model.gangen])

    def _aantal_acties(self):
        # 0 = simulatie_dag
        # 1 = verander voorhal mondkapjesplicht
        # 2 = verander docenten_kamer mondkapjesplicht
        # 3 = verander lokalen mondkapjesplicht
        # 4..4+N = verander gang N mondkapjesplicht
        return 4 + 1 # len(self.model.gangen)

    def doe_actie(self, actie_nummer):
        if actie_nummer == 0:
            begin_blijheid = self.model.totaal.blijheid
            for _ in range(self.model_simulatie_stappen):
                self.dag_nummer += 1
                self.model.simulatie_stap(self.dag_nummer)
                if self.dag_nummer == self.max_dag_nummer:
                    self.done = True
            return self.model.totaal.blijheid - begin_blijheid

        if actie_nummer == 1:
            self.model.voorhal.mondkapjes_plicht(not(self.model.voorhal.mondkapjes))
        elif actie_nummer == 2:
            self.model.docenten_kamer.mondkapjes_plicht(not(self.model.docenten_kamer.mondkapjes))
        elif actie_nummer == 3:
            for lokaal in self.model.lokalen:
                lokaal.mondkapjes_plicht(not(lokaal.mondkapjes))
        else:
            for gang in self.model.gangen:
                gang.mondkapjes_plicht(not(gang.mondkapjes))
            #self.model.gangen[actie_nummer-4].mondkapjes_plicht(not(self.model.gangen[actie_nummer-4].mondkapjes))
        return self.besluit_boete

    def lees_Q_tabel(self, toestand):
        if not(toestand in self._q_tabel):
            self._q_tabel[toestand] = [uniform(0,1) for _ in range(self.aantal_acties)]
        return self._q_tabel[toestand]
    
    def werk_Q_tabel_bij(self, toestand, actie, volgende_toestand, beloning):
        volgende_max = max(self.lees_Q_tabel(volgende_toestand))
        nieuwe_waarde = (1-self.Q_alpha)*self.lees_Q_tabel(toestand)[actie] + self.Q_alpha*(beloning + self.Q_gamma * volgende_max)
        self._q_tabel[toestand][actie] = nieuwe_waarde

    def episode(self):
        self.model_reset(self.model)
        self.dag_nummer = 0
        self.done = False
        iteratie = 0
        while not self.done:
            begin_toestand = self.codeer_toestand()
            if uniform(0,1) < self.Q_epsilon:
                actie = randrange(self.aantal_acties)
            else:
                actie = argmax(self.lees_Q_tabel(begin_toestand))

            beloning = self.doe_actie(actie)
            volgende_toestand = self.codeer_toestand()
            self.werk_Q_tabel_bij(begin_toestand, actie, volgende_toestand, beloning)
            iteratie += 1
        return iteratie

    def train(self, iteraties, logfile = '', Qs = None, dump_iteraties = 0):
        if Qs:
            self.Q_alpha = Qs[0]
            self.Q_gamma = Qs[1]
            self.Q_epsilon = Qs[2]
        if logfile.startswith('+'):
            file = open(logfile[1:], 'a')
        elif logfile == '':
            file = None
        else:
            file = open(logfile, 'w')
        status_string = "Epoch {:d} eindigt na {:d} iteraties in blijheid {:.2f} met {:d} Q-tabel toestanden, na {:.2f} seconde."
        for i in range(iteraties):
            tic = perf_counter()
            iteraties = self.episode()
            duur = perf_counter() - tic
            status = status_string.format(i, iteraties, self.model.totaal.blijheid, len(self._q_tabel), duur)
            print(status)
            if file:
                file.write(status)
                file.write("\n")
                file.flush()
            if dump_iteraties > 0 and i % dump_iteraties == 0:
                self.dump_q_tabel(i)

        if file:
            file.close()

    def dump_q_tabel(self, nummer):
        with open("q_tabel_{:d}.csv".format(nummer), "w") as file:
            for toestand in sorted(self._q_tabel.keys()):
                t = str(toestand)[1:-1]
                v = str(self._q_tabel[toestand])[1:-1]
                file.write(t)
                file.write(",")
                file.write(v)
                file.write("\n")