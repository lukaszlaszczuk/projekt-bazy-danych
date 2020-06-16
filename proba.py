import mysql.connector
import random
import numpy as np
import datetime
import logging
import matplotlib.pyplot as plt
import pandas as pd
from faker import Faker

logging.getLogger().setLevel(logging.INFO)


def faker_generator(kind, n):
    array = []
    for i in range(1, n + 1):
        eval('array.append(faker.{}())'.format(kind))
    return array


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database='spedycja'
)

mycursor = mydb.cursor()
#######################
#     DANE FLOTA      #
#######################

random.seed(30)
faker = Faker('pl_PL')
Faker.seed(30)
np.random.seed(30)

sdate_stock = datetime.date(2010, 1, 1)
edate_stock = datetime.date(2011, 4, 1)
delta = edate_stock - sdate_stock
days_stock = []
for i in range(delta.days + 1):
    day = sdate_stock + datetime.timedelta(days=i)
    days_stock.append(day)

szablon_bazy = {'akcje': ('data', 'cena', 'emitowana_ilosc'),
                'ceny_paliwa': ('cena', 'data'),
                'dlugi': ('data', 'kwota'),
                'flota': ('id_samochodu', 'waga_samochodu', 'przebieg', 'spalanie', 'max_zaladunek', 'typ_samochodu'),
                'klienci': ('id_klienta', 'Imie', 'Nazwisko', 'e_mail', 'telefon', 'miejscowosc'),
                'pracownicy': ('id_pracownika', 'Imie', 'Nazwisko'),
                'oplaty': ('rodzaj_oplaty', 'kwota_transakcji', 'data'),
                'pensje': ('id_pracownika', 'pensja', 'od_daty', 'do_daty'),
                'zlecenia': ('id_zlecenia', 'id_pracownika', 'id_samochodu', 'id_klienta', 'dystans', 'data_przyjecia',
                             'data_realizacji', 'kwota')}

#############################
#    pensje
#############################

# pensje_prac = [4000]*len(id_pracownikow)
od_daty = [datetime.date(i, 1, 1) for i in range(2010, 2020)]
od_daty.append(datetime.date(2020, 1, 1))
do_daty = [datetime.date(i, 12, 31) for i in range(2010, 2020)]
do_daty.append(edate_stock)
ilosc_pracownikow = list(int(np.random.randint(70, 90, 1)) + 4 * i for i in range(len(od_daty)))
print(ilosc_pracownikow, 'ilosc_prac')
lista_id_pracownikow = []
for i in range(len(od_daty)):
    if i == 0:
        lista_id_pracownikow.append(list(range(1, ilosc_pracownikow[i] + 1)))
    else:
        if ilosc_pracownikow[i] > ilosc_pracownikow[i - 1]:
            lista_pomocnicza = list(lista_id_pracownikow[i - 1])

            lista_pomocnicza.extend(list(range(lista_pomocnicza[-1] + 1,
                                               lista_pomocnicza[-1] + 1 + ilosc_pracownikow[i] - ilosc_pracownikow[
                                                   i - 1])))
            # print(lista_pomocnicza.extend(list(range(lista_id_pracownikow[i-1][-1]+1, lista_id_pracownikow[i-1][-1]+1+ilosc_pracownikow[i]-ilosc_pracownikow[i-1]))))
            lista_id_pracownikow.append(lista_pomocnicza)
        elif ilosc_pracownikow[i] < ilosc_pracownikow[i - 1]:
            wylosowany_index = int(random.choice(lista_id_pracownikow[i - 1]))
            lista_pomocnicza = list(lista_id_pracownikow[i - 1])
            del lista_pomocnicza[
                wylosowany_index:(wylosowany_index + ilosc_pracownikow[i - 1] - ilosc_pracownikow[i] + 1)]
            lista_id_pracownikow.append(lista_pomocnicza)
        else:
            lista_id_pracownikow.append(lista_id_pracownikow[i - 1])

pensje = []
for i in range(len(lista_id_pracownikow)):
    for j in lista_id_pracownikow[i]:
        pensje.append((j, 4000, od_daty[i], do_daty[i]))
id_pracownikow = list(range(1, lista_id_pracownikow[-1][-1] + 1))
#######################3
### akcje i paliwa
#######################
ceny_akcji = []
ceny_pal = []
for i in range(len(days_stock)):
    if i < 1:
        ceny_akcji.append(np.random.normal(10, 0.5, 1))
    else:
        if ceny_akcji[i - 1] < 3:
            ceny_akcji.append(np.random.normal(ceny_akcji[i - 1] + 1, 0.5, 1))
        else:
            ceny_akcji.append(np.random.normal(ceny_akcji[i - 1], 0.5, 1))
ceny_pal = (np.random.normal(4.3, 0.3, len(ceny_akcji)))
ceny_pal = np.convolve(ceny_pal, np.ones((40,)) / 40)[(40 - 1):]  # sredia kroczaca
ilosc_emisji = [15000000 / 10] * len(ceny_akcji)

##plt.figure()
##plt.plot(days_stock, ceny_akcji)

akcje = []
for i in range(len(ceny_akcji)):
    akcje.append((days_stock[i], float(ceny_akcji[i]), ilosc_emisji[i]))

ceny_paliwa = []
for i in range(len(ceny_paliwa[:-40])):
    ceny_paliwa.append(((float((ceny_paliwa[:-40])[i]), (days_stock[:-40])[i])))

# plt.figure()
# plt.plot(days_stock[:-40], ceny_paliwa[:-40])

################################3
#    dlugi
###############################

kwoty = len(days_stock) * [150000]
dlugi = []
for i in range(len(kwoty)):
    dlugi.append((days_stock[i], kwoty[i]))

###############################
##    klienci
#############

id_samochodow = list(range(1, 76))

id_klientow = list(range(1, 1350))
id_zlecen = list(range(1, 3000))

imiona = faker_generator('first_name', len(id_klientow))
nazwiska = faker_generator('last_name', len(id_klientow))
emaile = faker_generator('email', len(id_klientow))
numery = faker_generator('phone_number', len(id_klientow))
miasta = faker_generator('city', len(id_klientow))
klienci = []
for i in range(len(id_klientow)):
    klienci.append((id_klientow[i], imiona[i], nazwiska[i], emaile[i], numery[i], miasta[i]))

print(f'Nazwy miast w tabeli klienci: {miasta}')

#########################
##### flota
##########################
typ_samochodu = random.choices(85 * ['samochod ciezarowy'] + 15 * ['samochod dostawczy'], k=75)
wagi_samochodow = []
przebiegi = []
max_zaladunki = []
spalania = []
for samochod in typ_samochodu:
    if samochod == 'samochod ciezarowy':
        wagi_samochodow.append(random.choice(list(np.arange(12000, 15001, 100))))
        max_zaladunki.append(40000 - wagi_samochodow[-1])
        spalania.append(wagi_samochodow[-1] * 3 / 1000 - 7)
    else:
        wagi_samochodow.append(random.choice(list(np.arange(2000, 2600, 100))))
        max_zaladunki.append(3500 - wagi_samochodow[-1])
        spalania.append(wagi_samochodow[-1] * 1 / 120 - 26 / 3)
    przebiegi.append(random.choice(list(range(30, 1000000))))

flota = []
for i in range(75):
    flota.append((
        id_samochodow[i], float(wagi_samochodow[i]), przebiegi[i], float(spalania[i]), float(max_zaladunki[i]),
        typ_samochodu[i]))
#################
#    oplaty
###################
rodzaj_oplaty = ['oplata'] * len(days_stock)
kwota_transkacji = [600] * len(days_stock)
oplaty = []
for i in range(len(days_stock)):
    oplaty.append((rodzaj_oplaty[i], kwota_transkacji[i], days_stock[i]))

#########################
#  zlecenia
######################

###########   PROBA WYGENEROWANIA SENSOWNYCH DANYCH

il_zlecen = list(np.random.randint(15, 40, len(days_stock)))
logging.info(f'Całkowita liczba zleceń: {sum(il_zlecen)}')
id_zlecenia = list(range(1, sum(il_zlecen) + 1))

dystanse = []
for i in il_zlecen:
    dystanse.append(random.choices(range(150, 2900), k=i))
wolni_kierowcy = pd.DataFrame(lista_id_pracownikow[0], columns=['id_kierowcy'])
zajeci_kierowcy = pd.DataFrame(columns=['id_kierowcy', 'data_zakonczenia'])
wolne_samochody = pd.DataFrame(zip(id_samochodow, typ_samochodu), columns=['id_samochodu', 'typ_samochodu'])
zajete_samochody = pd.DataFrame(columns=['id_samochodu', 'typ_samochodu', 'data_zakonczenia'])
niezrealizowane_zamowienia = pd.DataFrame(columns=['typ_samochodu', 'data_przyjecia'])

# print(wolne_samochody)
potrzebne_sam_ciezarowe = 0
potrzebne_sam_dostawcze = 0
counter = 0
id_pracujacych = lista_id_pracownikow[counter]

id_pracownika = []
id_samochodu = []
dystans = []
daty_zlecen = []
daty_realizacji = []
kwoty = []
for i in range(len(days_stock)):
    if i == 0:
        for j in range(il_zlecen[i]):
            if dystanse[i][j] > 800:
                potrzebne_sam_ciezarowe += 1
            else:
                potrzebne_sam_dostawcze += 1
        wyrzucane_samochody_1 = list(random.sample(  # ciężarówki wybrane do przejazdów
            list(wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod ciezarowy']['id_samochodu']),
            k=potrzebne_sam_ciezarowe))
        wyrzucane_samochody_2 = list(random.sample(  # dostawcze wybrane do przejazdów
            list(wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod dostawczy']['id_samochodu']),
            k=potrzebne_sam_dostawcze))
        wybierany_df = wolne_samochody[
            wolne_samochody['id_samochodu'].isin(wyrzucane_samochody_1 + wyrzucane_samochody_2)].reset_index(drop=True)
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod ciezarowy', 'data_zakonczenia'] = days_stock[
                                                                                                          i] + datetime.timedelta(
            days=5)
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod dostawczy', 'data_zakonczenia'] = days_stock[
                                                                                                          i] + datetime.timedelta(
            days=2)
        wybrane_id_samochodow = list(wolne_samochody[wolne_samochody['id_samochodu'].isin(
            wyrzucane_samochody_1 + wyrzucane_samochody_2)]['id_samochodu'])
        logging.info(f'Samochody używane w zleceniach:\n {wybrane_id_samochodow}')
        logging.info(f'DataFrame samochodów używanych w zleceniach:\n {wybierany_df}')
        wolne_samochody = wolne_samochody[~wolne_samochody['id_samochodu'].isin(wybrane_id_samochodow)].reset_index(
            drop=True)
        logging.info(f'Wolne samochody po aktualizacji:\n {wolne_samochody}')
        # wolne_samochody = wolne_samochody.drop(index=wybrane_id_samochodow, inplace=False)
        zajete_samochody = pd.concat([zajete_samochody, wybierany_df]).reset_index(drop=True)
        logging.info(f'Zajęte samochody po aktualizacji:\n {zajete_samochody}')

        # wybieranie kierowców
        potrzebni_kierowcy = potrzebne_sam_ciezarowe + potrzebne_sam_dostawcze
        wyrzucani_kierowcy = list(random.sample(list(wolni_kierowcy['id_kierowcy']),  # kierowcy wybrani do przejazdów
                                                k=potrzebni_kierowcy))
        print(f'Wyrzucani kierowcy: {wyrzucani_kierowcy}')
        wybierany_df_kierowcy = wolni_kierowcy[wolni_kierowcy['id_kierowcy'].isin(wyrzucani_kierowcy)].reset_index(
            drop=True)
        logging.info(f'Wybierany_df_kierowcy: \n {wybierany_df_kierowcy}')
        print(f'Ciężarówki: {potrzebne_sam_ciezarowe}, dostawcze: {potrzebne_sam_dostawcze}')

        wybierany_df_kierowcy.loc[:potrzebne_sam_ciezarowe, 'data_zakonczenia'] = days_stock[
                                                                                      i] + datetime.timedelta(
            days=5)
        print(wybierany_df_kierowcy)
        wybierany_df_kierowcy.loc[potrzebne_sam_ciezarowe:, 'data_zakonczenia'] = days_stock[
                                                                                      i] + datetime.timedelta(
            days=2)
        wolni_kierowcy = wolni_kierowcy[~wolni_kierowcy['id_kierowcy'].isin(wyrzucani_kierowcy)].reset_index(drop=True)
        logging.info(f'Wolni kierowcy po aktualizacji:\n {wolni_kierowcy}')
        zajeci_kierowcy = pd.concat([zajeci_kierowcy, wybierany_df_kierowcy]).reset_index(drop=True)
        logging.info(f'Zajęci kierowcy po aktualizacji:\n {zajeci_kierowcy}')

        potrzebne_sam_ciezarowe = 0
        potrzebne_sam_dostawcze = 0

        assert len(list(wybierany_df_kierowcy['id_kierowcy'])) == len(wybrane_id_samochodow)

        id_pracownika.extend(list(wybierany_df_kierowcy['id_kierowcy']))
        logging.info(f'Id pracowników wybranych do zlecenia w pierwszym dniu: {id_pracownika}')
        id_samochodu.extend(wybrane_id_samochodow)
        logging.info(f'Id samochodów wybranych do zlecenia w pierwszym dniu: {id_samochodu}')
        dystans.extend(dystanse[i])
        kwoty.extend([0.75 * j if j > 800 else j for j in dystanse[i]])
        daty_zlecen.extend([days_stock[i]] * potrzebni_kierowcy)
        daty_realizacji.extend([days_stock[i]] * potrzebni_kierowcy)

    else:  # pozostałe dni symulacji
        # wolni_kierowcy ['id_kierowcy']
        # zajeci_kierowcy ['id_kierowcy', 'data_zakonczenia']
        # wolne_samochody ['id_samochodu', 'typ_samochodu']
        # zajete_samochody ['id_samochodu', 'typ_samochodu', 'data_zakonczenia']
        id_pracujacych = lista_id_pracownikow[counter]
        k_ciezarowe = 0
        k_dostawcze = 0
        potrzebne_sam_ciezarowe = 0
        potrzebne_sam_dostawcze = 0

        if days_stock[i].year != days_stock[i - 1].year:
            counter += 1
            # nowi_pracujacy = pd.DataFrame(lista_id_pracownikow[counter], columns=['id_kierowcy'])
            # starzy_zajeci_kierowcy = zajeci_kierowcy
            # wolni_kierowcy = nowi_pracujacy
            # zajeci_kierowcy = list(nowi_pracujacy.difference(starzy_zajeci_kierowcy))

        for j in range(il_zlecen[i]):
            if dystanse[i][j] > 800:
                potrzebne_sam_ciezarowe += 1
            else:
                potrzebne_sam_dostawcze += 1

        powrot_do_wolnych_samochod = zajete_samochody[zajete_samochody['data_zakonczenia'] == days_stock[i]].iloc[:,
                                     :-1].reset_index(drop=True)
        zajete_samochody = zajete_samochody[zajete_samochody['data_zakonczenia'] != days_stock[i]].reset_index(
            drop=True)
        wolne_samochody = pd.concat([wolne_samochody, powrot_do_wolnych_samochod]).reset_index(drop=True)
        logging.info(f'Wolne samochody: {wolne_samochody}')
        logging.info(f'Zajęte samochody: {zajete_samochody}')

        powrot_do_wolnych_kierowca = zajeci_kierowcy[zajeci_kierowcy['data_zakonczenia'] == days_stock[i]].iloc[:,
                                     :-1].reset_index(drop=True)
        zajeci_kierowcy = zajeci_kierowcy[zajeci_kierowcy['data_zakonczenia'] != days_stock[i]].reset_index(
            drop=True)
        wolni_kierowcy = pd.concat([wolni_kierowcy, powrot_do_wolnych_kierowca]).reset_index(drop=True)
        logging.info(f'Wolni kierowcy: {wolni_kierowcy}')
        logging.info(f'Zajęci kierowcy: {zajeci_kierowcy}')

        liczba_wolnych_ciezarowek = wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod ciezarowy'].shape[0]
        liczba_wolnych_dostawczych = wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod dostawczy'].shape[0]

        if niezrealizowane_zamowienia.shape[0] > 0:
            niezrealizowane_ciezarowki = \
                niezrealizowane_zamowienia[niezrealizowane_zamowienia['typ_samochodu'] == 'samochod ciezarowy'].shape[0]
            niezrealizowane_dostawcze = \
                niezrealizowane_zamowienia[niezrealizowane_zamowienia['typ_samochodu'] == 'samochod dostawczy'].shape[0]

            # zaległe zamówienia
            licz_usuwanych_ciezarowek = niezrealizowane_ciezarowki \
                if niezrealizowane_ciezarowki < liczba_wolnych_ciezarowek else liczba_wolnych_ciezarowek
            licz_usuwanych_dostawczych = niezrealizowane_dostawcze \
                if niezrealizowane_dostawcze < liczba_wolnych_dostawczych else liczba_wolnych_dostawczych

            zalegle_realizacje_ciezarowki = niezrealizowane_zamowienia[
                                                niezrealizowane_zamowienia[
                                                    'typ_samochodu'] == 'samochod ciezarowy'].iloc[
                                            :licz_usuwanych_ciezarowek, :]
            zalegle_daty_zlecen_ciezarowki = zalegle_realizacje_ciezarowki['data_przyjecia']
            niezrealizowane_ciezarowki = niezrealizowane_zamowienia[
                                             niezrealizowane_zamowienia['typ_samochodu'] == 'samochod ciezarowy'].iloc[
                                         licz_usuwanych_ciezarowek:, :]

            zalegle_realizacje_dostawcze = niezrealizowane_zamowienia[
                                               niezrealizowane_zamowienia[
                                                   'typ_samochodu'] == 'samochod dostawczy'].iloc[
                                           :licz_usuwanych_dostawczych, :]
            zalegle_daty_zlecen_dostawcze = zalegle_realizacje_dostawcze['data_przyjecia']
            niezrealizowane_dostawcze = niezrealizowane_zamowienia[
                                            niezrealizowane_zamowienia['typ_samochodu'] == 'samochod dostawczy'].iloc[
                                        licz_usuwanych_dostawczych:, :]

            niezrealizowane_zamowienia = pd.concat([niezrealizowane_ciezarowki, niezrealizowane_dostawcze]).reset_index(
                drop=True)
            logging.info(f'Niezrealizowane zamówienia dzień {days_stock[i]}:\n {niezrealizowane_zamowienia}')

            zalegle_daty = list(list(zalegle_daty_zlecen_dostawcze) + list(zalegle_daty_zlecen_ciezarowki))
            logging.info(f'Zaległe Daty przyjęcia: {zalegle_daty}')

            k_ciezarowe = potrzebne_sam_ciezarowe + licz_usuwanych_ciezarowek \
                if potrzebne_sam_ciezarowe + licz_usuwanych_ciezarowek < liczba_wolnych_ciezarowek \
                else liczba_wolnych_ciezarowek
            k_dostawcze = potrzebne_sam_dostawcze + licz_usuwanych_dostawczych \
                if potrzebne_sam_dostawcze + licz_usuwanych_dostawczych < liczba_wolnych_dostawczych \
                else liczba_wolnych_dostawczych
            ilosc_zlecen_normalna = (k_ciezarowe+k_dostawcze) - len(zalegle_daty)
            daty_przyjecia = zalegle_daty + ilosc_zlecen_normalna*[days_stock[i]]
            dystanse[i] = dystanse[i][:k_ciezarowe + k_dostawcze]
        else:
            k_ciezarowe = potrzebne_sam_ciezarowe \
                if potrzebne_sam_ciezarowe < liczba_wolnych_ciezarowek \
                else liczba_wolnych_ciezarowek
            k_dostawcze = potrzebne_sam_dostawcze \
                if potrzebne_sam_dostawcze < liczba_wolnych_dostawczych \
                else liczba_wolnych_dostawczych

            daty_przyjecia = (k_ciezarowe+k_dostawcze) * [days_stock[i]]
            dystanse[i] = dystanse[i][:k_ciezarowe + k_dostawcze]
        logging.info(f'Daty przyjęcia: {daty_przyjecia}')


        wyrzucane_samochody_1 = list(random.sample(
            list(wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod ciezarowy']['id_samochodu']),
            k=k_ciezarowe))
        wyrzucane_samochody_2 = list(random.sample(
            list(wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod dostawczy']['id_samochodu']),
            k=k_dostawcze))

        wybierany_df = wolne_samochody[
            wolne_samochody['id_samochodu'].isin(wyrzucane_samochody_1 + wyrzucane_samochody_2)].reset_index(drop=True)
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod ciezarowy', 'data_zakonczenia'] = days_stock[
                                                                                                          i] + datetime.timedelta(
            days=5)
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod dostawczy', 'data_zakonczenia'] = days_stock[
                                                                                                          i] + datetime.timedelta(
            days=2)
        wybrane_id_samochodow = list(wolne_samochody[wolne_samochody['id_samochodu'].isin(
            wyrzucane_samochody_1 + wyrzucane_samochody_2)]['id_samochodu'])
        print(
            f"WYbrane id samochodu {wolne_samochody[wolne_samochody['id_samochodu'].isin(wyrzucane_samochody_1 + wyrzucane_samochody_2)]}")
        logging.info(f'Samochody używane w zleceniach dzień {days_stock[i]}:\n {wybrane_id_samochodow}')
        logging.info(f'DataFrame samochodów używanych w zleceniach dzień {days_stock[i]}:\n {wybierany_df}')
        wolne_samochody = wolne_samochody[~wolne_samochody['id_samochodu'].isin(wybrane_id_samochodow)].reset_index(
            drop=True)
        logging.info(f'Wolne samochody po aktualizacji dzień {days_stock[i]}:\n {wolne_samochody}')
        zajete_samochody = pd.concat([zajete_samochody, wybierany_df]).reset_index(drop=True)
        logging.info(f'Zajęte samochody po aktualizacji dzień {days_stock[i]}:\n {zajete_samochody}')

        # wybieranie kierowców
        potrzebni_kierowcy = k_ciezarowe + k_dostawcze
        wyrzucani_kierowcy = list(random.sample(list(wolni_kierowcy['id_kierowcy']),  # kierowcy wybrani do przejazdów
                                                k=potrzebni_kierowcy))
        wybierany_df_kierowcy = wolni_kierowcy[wolni_kierowcy['id_kierowcy'].isin(wyrzucani_kierowcy)].reset_index(
            drop=True)
        wybierany_df_kierowcy.loc[:k_ciezarowe, 'data_zakonczenia'] = days_stock[
                                                                          i] + datetime.timedelta(
            days=5)
        wybierany_df_kierowcy.loc[k_ciezarowe:, 'data_zakonczenia'] = days_stock[
                                                                          i] + datetime.timedelta(
            days=2)
        wolni_kierowcy = wolni_kierowcy[~wolni_kierowcy['id_kierowcy'].isin(wyrzucani_kierowcy)].reset_index(drop=True)
        logging.info(f'Wolni kierowcy po aktualizacji dzień {days_stock[i]}:\n {wolni_kierowcy}')
        zajeci_kierowcy = pd.concat([zajeci_kierowcy, wybierany_df_kierowcy]).reset_index(drop=True)
        logging.info(f'Zajęci kierowcy po aktualizacji dzień {days_stock[i]}:\n {zajeci_kierowcy}')

        assert len(list(wybierany_df_kierowcy['id_kierowcy'])) == len(wybrane_id_samochodow)

        potrzebne_sam_ciezarowe = potrzebne_sam_ciezarowe - k_ciezarowe if potrzebne_sam_ciezarowe - k_ciezarowe > 0 else 0
        potrzebne_sam_dostawcze = potrzebne_sam_dostawcze - k_dostawcze if potrzebne_sam_dostawcze - k_dostawcze > 0 else 0

        logging.info(
            f'Ilość niezrealizowanych zleceń w dniu {days_stock[i]}: {potrzebne_sam_dostawcze + potrzebne_sam_ciezarowe}')
        if potrzebne_sam_ciezarowe > 0 or potrzebne_sam_dostawcze > 0:
            niezrealizowane_zamowienia_pom = pd.DataFrame({
                'data_przyjecia': (
                                          potrzebne_sam_ciezarowe + potrzebne_sam_dostawcze) * [
                                      days_stock[i]],
                'typ_samochodu': potrzebne_sam_ciezarowe * [
                    'samochod ciezarowy'] + potrzebne_sam_dostawcze * [
                                     'samochod dostawczy']})
            niezrealizowane_zamowienia = pd.concat(
                [niezrealizowane_zamowienia, niezrealizowane_zamowienia_pom]).reset_index(drop=True)
            logging.info(f"Niezrealizowane zamówienia: {niezrealizowane_zamowienia}")
            assert niezrealizowane_zamowienia.shape[0] > 0

        # wolne_samochody = wolne_samochody.drop(index=wybrane_id_samochodow, inplace=False)
        # zajete_samochody = pd.concat([zajete_samochody, wybierany_df])
        if k_dostawcze + k_ciezarowe > len(dystanse[i]):
            roznica = (k_dostawcze + k_ciezarowe) - len(dystanse[i])
            print(list(np.random.randint(700, 900, roznica)))
            dystanse[i].extend(list(np.random.randint(700, 900, roznica)))
        print(f" Liczba zleceń: {k_dostawcze + k_ciezarowe}, ilość dystansów: {len(dystanse[i])}")
        assert k_dostawcze + k_ciezarowe == len(wybrane_id_samochodow)
        assert k_dostawcze + k_ciezarowe == len(list(wybierany_df_kierowcy['id_kierowcy']))
        assert k_dostawcze + k_ciezarowe == len(dystanse[i])
        assert k_dostawcze + k_ciezarowe == len(daty_przyjecia)
        # id_zlecenia.extend(list(range(id_zlecenia[-1] + 1, id_zlecenia[-1] + il_zlecen[i])))
        id_pracownika.extend(list(wybierany_df_kierowcy['id_kierowcy']))
        id_samochodu.extend(list(wybrane_id_samochodow))
        dystans.extend(list(dystanse[i]))
        kwoty.extend([0.75 * j if j > 800 else j for j in dystanse[i]])
        daty_zlecen.extend(list(daty_przyjecia))
        daty_realizacji.extend([days_stock[i]] * (k_dostawcze + k_ciezarowe))
        # print(len(id_zlecenia), len(id_pracownika))

id_zlecenia = id_zlecenia[:len(dystans)]
logging.info(f"dlugosc id_zlecenia: {len(id_zlecenia)}, dlugosc pracownika {len(id_pracownika)}")
assert len(id_zlecenia) == len(dystans)
assert len(id_zlecenia) == len(id_pracownika)

id_klienta = random.choices(id_klientow, k=len(id_zlecenia))
zlecenia = []
# id_samochodu = ([20] * (len(id_zlecenia)))
print(type(id_zlecenia), type(id_pracownika), type(id_samochodu), type(id_klienta), type(dystans), type(daty_zlecen),
      type(kwoty))

for i in range(len(id_zlecenia)):
    zlecenia.append((id_zlecenia[i], int(id_pracownika[i]), int(id_samochodu[i]), int(id_klienta[i]), float(dystans[i]),
                     daty_zlecen[i], daty_realizacji[i], float(kwoty[i])))

# print(zlecenia)

########################### WCZESNIEJSZE GENEROWANIE

##id_prac = random.choices(id_pracownikow[:75], k = len(id_zlecen))
##id_sam = id_prac
##id_klien = random.choices(id_klientow, k = len(id_zlecen))
##dystans = [1000]*len(id_zlecen)
##daty_zlecen = [sdate_stock]* len(id_zlecen)
##daty_realizacji = [edate_stock]*len(id_zlecen)
##kwoty = [1200] * len(id_zlecen)
##zlecenia = []

##for i in range(len(daty_zlecen)):
##    zlecenia.append((id_zlecen[i],int(id_prac[i]),int(id_sam[i]),int(id_klien[i]), dystans[i],daty_zlecen[i], daty_realizacji[i], kwoty[i]))
##


#############################
# pracownicy
#############################
imiona_prac = random.choices(imiona, k=lista_id_pracownikow[-1][-1] + 1)
nazwiska_prac = random.choices(nazwiska, k=lista_id_pracownikow[-1][-1] + 1)

pracownicy = []
for i in range(lista_id_pracownikow[-1][-1]):
    pracownicy.append((id_pracownikow[i], imiona_prac[i], nazwiska_prac[i]))

###############################
#   wypelnianie bazy
#########################

for table_name in szablon_bazy.keys():
    mySql_insert_query = 'INSERT INTO {}'.format(table_name) + ' (' + \
                         ', '.join([i for i in szablon_bazy[table_name]]) + \
                         ') VALUES(%s' + ', %s' * (len(szablon_bazy[table_name]) - 1) + ');'
    print(mySql_insert_query, table_name)
    mycursor.executemany(mySql_insert_query, eval(table_name))
    mydb.commit()

mydb.close()
logging.info("Wypełnianie bazy danych zakończone sukcesem!")
# plt.show()
