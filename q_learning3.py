from random import uniform, randrange
from time import perf_counter

# returns de index van het maximum in de lijst
def argmax(l):
    f = lambda i: l[i]
    return max(range(len(l)), key=f)

class QLearning():
    def __init__(self, model, model_reset, besluit_boete, model_simulatie_stappen, max_dag_nummer, Qs, N):
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
        self.N = N
        self.done = False
        self.aantal_acties = self._aantal_acties()

    def codeer_toestand(self):
        return tuple([self.N*round(self.model.totaal.ziek/self.N), 
                      self.N*round((self.model.totale_zieken - self.model.totaal.ziek)/self.N)])

    def _aantal_acties(self):
        return 2**4 # len(self.model.gangen)

    def zet_mondkapjes(self, *waardes):
        for ruimtes, waarde in zip([self.model.voorhal, self.model.docenten_kamer, self.model.lokalen, self.model.gangen], waardes):
            if isinstance(ruimtes, list):
                for ruimte in ruimtes:
                    ruimte.mondkapjes_plicht(waarde)
            else:
                ruimtes.mondkapjes_plicht(waarde)

    def doe_actie(self, actie_nummer):
        self.zet_mondkapjes(actie_nummer & 1 == 1,
                            actie_nummer & 2 == 2,
                            actie_nummer & 4 == 4,
                            actie_nummer & 8 == 8)

        begin_blijheid = self.model.totaal.blijheid
        for _ in range(self.model_simulatie_stappen):
            self.dag_nummer += 1
            self.model.simulatie_stap(self.dag_nummer)
            if self.dag_nummer == self.max_dag_nummer:
                self.done = True
        return self.model.totaal.blijheid - begin_blijheid

    def lees_Q_tabel(self, toestand):
        if not(toestand in self._q_tabel):
            self._q_tabel[toestand] = [0] + [-10]*(self.aantal_acties-1)
        return self._q_tabel[toestand]
    
    def werk_Q_tabel_bij(self, toestand, actie, volgende_toestand, beloning):
        volgende_max = max(self.lees_Q_tabel(volgende_toestand))
        nieuwe_waarde = (1-self.Q_alpha)*self.lees_Q_tabel(toestand)[actie] + self.Q_alpha*(beloning + self.Q_gamma * volgende_max)
        self._q_tabel[toestand][actie] = nieuwe_waarde

    def train_episode(self):
        self.model_reset(self.model)
        self.dag_nummer = 0
        self.done = False
        iteratie = 0
        actie_log = []
        toestand = self.codeer_toestand()
        while not self.done:
            if uniform(0,1) < self.Q_epsilon:
                actie = randrange(self.aantal_acties)
            else:
                actie = argmax(self.lees_Q_tabel(toestand))
            actie_log.append((self.dag_nummer, "{:06b}".format(actie)))

            beloning = self.doe_actie(actie)
            begin_toestand, toestand = toestand, self.codeer_toestand()
            self.werk_Q_tabel_bij(begin_toestand, actie, toestand, beloning)
            iteratie += 1
        return iteratie, actie_log

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
            iteraties, actie_log = self.train_episode()
            if self.model.totaal.blijheid > -600:
                print("{} {:.2f}".format(actie_log, self.model.totaal.blijheid))
            duur = perf_counter() - tic
            status = status_string.format(i, iteraties, self.model.totaal.blijheid, len(self._q_tabel), duur)
            #print(status)
            if file:
                file.write(status)
                file.write("\n")
                file.flush()
            if dump_iteraties > 0 and i % dump_iteraties == 0:
                self.dump_q_tabel(i)

        if file:
            file.close()

    def dump_q_tabel(self, nummer):
        with open("q_tabel_{}.csv".format(nummer), "w") as file:
            for toestand in sorted(self._q_tabel.keys()):
                t = str(toestand)[1:-1]
                v = str(self._q_tabel[toestand])[1:-1]
                file.write(t)
                file.write(",")
                file.write(v)
                file.write("\n")

    def load_q_tabel(self, nummer):
        with open("q_tabel_{}.csv".format(nummer), "r") as file:
            self._q_tabel = {}
            for regel in file.readlines():
                data = []
                for item in regel.split(','):
                    item = item.strip()
                    if item == "False":
                        data.append(False)
                    elif item == "True":
                        data.append(True)
                    elif '.' in item:
                        data.append(float(item))
                    else:
                        data.append(int(item))
                toestand = tuple(data[:-self.aantal_acties])
                waardes = data[-self.aantal_acties:]
                self._q_tabel[toestand] = waardes

    def gebruik(self):
        self.model_reset(self.model)
        self.dag_nummer = 0
        self.done = False
        acties = []
        iteratie = 0
        while not self.done:
            toestand = self.codeer_toestand()
            actie = argmax(self.lees_Q_tabel(toestand))
            acties.append((actie, self.dag_nummer))

            beloning = self.doe_actie(actie)
            iteratie += 1
        return iteratie, acties, self.model.totaal.blijheid