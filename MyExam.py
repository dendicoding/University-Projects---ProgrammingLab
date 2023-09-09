class CSVFile:

    def __init__(self, name):
        self.name = name

    def get_data(self):
        pass


class CSVTimeSeriesFile(CSVFile):

    def get_data(self):  #!controlla e scarta già le righe vuote e non valide!

        #Nel caso in cui il nome del file non sia di tipo stringa, alzo una eccezione
        if isinstance(self.name, str) != True:
            raise ExamException('Filename: {} non è una stringa...'.format(
                self.name))

        # Provo ad aprirlo e leggere una riga per verificare la sua leggibilità
        self.can_read = True  #ipotizzo sia leggibile
        try:
            my_file = open(self.name, 'r')
            my_file.readline()  #leggo una riga
        except ExamException as e:  #nel caso in cui non funzionasse, eccezione
            self.can_read = False
            print('Errore in apertura del file: "{}"'.format(e))
            return None  #nel caso in cui non sia leggibile, non ritorno niente

        if self.can_read:
            # Inizializzo una lista vuota per salvare tutti i dati
            data = []

            # Apro il file
            my_file = open(self.name, 'r')

            # Leggo il file linea per linea
            for line in my_file:

                # Faccio lo split di ogni linea sulla virgola
                elements = line.split(',')

                # Posso anche pulire il carattere di newline
                # dall'ultimo elemento con la funzione strip():
                elements[-1] = elements[-1].strip()

                # p.s. in realta' strip() toglie anche gli spazi
                # bianchi all'inizio e alla fine di una stringa.

                # Se NON sto processando l'intestazione...
                if elements[0] != 'epoch':
                    # Aggiungo alla lista gli elementi di questa linea

                    data.append(elements)

                for lista in data:
                    try:
                        lista[0] = float(lista[0])
                        lista[1] = float(lista[1])
                    except ValueError:
                        data.remove(lista)

            # Chiudo il file
            my_file.close()

            #Returno ogni valore di data[]
            lista_annidata = []
            for value in data:
                lista_annidata.append(value)

            #creo una lista dove isolo i timestamps
            timestamps = []
            for list in lista_annidata:
                timestamps.append(list[0])

            #controllo se i timestamps sono effettivamente in ordine
            for ts in range(len(timestamps) - 1):
                if timestamps[ts + 1] < timestamps[ts]:
                    raise ExamException(
                        "I timestamps forniti non sono in ordine...")

            #controllo se vi sono timestamps duplicati
            set_di_ts = set(timestamps)
            if len(set_di_ts) < len(timestamps):
                raise ExamException("Ci sono dei timestamps duplicati...")

        return lista_annidata


class ExamException(Exception):
    pass


def compute_daily_max_difference(list_of_lists):
    giorno = []
    escursioni = []

    ##################################################################
    #  Funzione che aggiunge escursione giornaliera alla lista finale
    ##################################################################
    def add_esc(giorno):
        if len(giorno) == 1 or len(giorno) == 0:
            escursioni.append(
                None)  #l'escursione in caso di singola misurazione è None
        else:
            minimo = float(giorno[0])
            massimo = float(giorno[0])
            for temperatura in giorno:
                if temperatura < minimo: minimo = temperatura
                elif temperatura >= massimo: massimo = temperatura

            escursioni.append(round(massimo - minimo, 3))  #es. 1.85
            giorno.clear()

    #######################################
    # Separazione dei timestamps in giorni
    #######################################
    for i in range(len(list_of_lists)):

        if list_of_lists[i] == list_of_lists[-1]:
            if (int(list_of_lists[i][0]) -
                (int(list_of_lists[i][0]) % 86400)) == (
                    int(list_of_lists[i - 1][0]) -
                    (int(list_of_lists[i - 1][0]) % 86400)):
                giorno.append(float(list_of_lists[i][1]))
                add_esc(giorno)
            else:  #altrimenti se ultimo elemento non appartiene a ultimo giorno, vorra dire che vi sara un solo elemento in quel nuovo giorno
                escursioni.append(
                    None)  #l'escursione in caso di singola misurazione è None

        else:
            if (int(list_of_lists[i][0]) -
                (int(list_of_lists[i][0]) % 86400)) == (
                    int(list_of_lists[i + 1][0]) -
                    (int(list_of_lists[i + 1][0]) % 86400)):
                giorno.append(float(list_of_lists[i][1]))
            else:
                giorno.append(float(list_of_lists[i][1]))
                add_esc(giorno)

    return escursioni


####################
#     'Main'
####################
#time_series_file = CSVTimeSeriesFile(name = 'data.csv')
#time_series = time_series_file.get_data()

#lista_di_escursioni = compute_daily_max_difference(time_series)
#print(lista_di_escursioni)
