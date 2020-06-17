import random
import numpy as np
import datetime
import logging
import pandas as pd
from faker import Faker
from sklearn.preprocessing import scale

from util.MySQLConnector import MySQLConnector

logging.getLogger().setLevel(logging.INFO)
random.seed(30)
faker = Faker('pl_PL')
Faker.seed(30)
np.random.seed(30)


def faker_generator(kind, n):
    array = []
    for i in range(1, n + 1):
        eval('array.append(faker.{}())'.format(kind))
    return array


def create_employees(year_start_vec):
    lista_id_pracownikow = []
    ilosc_pracownikow = list(int(np.random.randint(76, 90, 1)) + 4 * i for i in range(len(od_daty)))
    for i in range(len(year_start_vec)):
        if i == 0:
            lista_id_pracownikow.append(list(range(1, ilosc_pracownikow[i] + 1)))
        else:
            if ilosc_pracownikow[i] > ilosc_pracownikow[i - 1]:
                lista_pomocnicza = list(lista_id_pracownikow[i - 1])

                lista_pomocnicza.extend(list(range(lista_pomocnicza[-1] + 1,
                                                   lista_pomocnicza[-1] + 1 + ilosc_pracownikow[i] - ilosc_pracownikow[
                                                       i - 1])))
                lista_id_pracownikow.append(lista_pomocnicza)
            elif ilosc_pracownikow[i] < ilosc_pracownikow[i - 1]:
                wylosowany_index = int(random.choice(lista_id_pracownikow[i - 1]))
                lista_pomocnicza = list(lista_id_pracownikow[i - 1])
                del lista_pomocnicza[
                    wylosowany_index:(wylosowany_index + ilosc_pracownikow[i - 1] - ilosc_pracownikow[i] + 1)]
                lista_id_pracownikow.append(lista_pomocnicza)
            else:
                lista_id_pracownikow.append(lista_id_pracownikow[i - 1])
    return lista_id_pracownikow


def create_salaries(year_start_vec, year_end_vec, pensja_podstawa, podwyzka_val, lista_id_pracownikow):
    pensja = []
    podwyzka = 0
    # lista_do_losowania_pensji = np.random.lognormal(pensja_podstawa - 1000 + podwyzka, pensja_podstawa + 1400 + podwyzka, 100)
    for i in range(len(year_start_vec)):
        if od_daty[i].year % 2 == 0 and i > 0:
            podwyzka += podwyzka_val
        # pensja.extend(random.choices(lista_do_losowania_pensji, k=len(lista_id_pracownikow[i])))
        pensja.extend(np.random.lognormal(mean=np.log(pensja_podstawa + podwyzka_val), sigma=0.25,
                                          size=len(lista_id_pracownikow[i])))

    pensje = []
    for i in range(len(lista_id_pracownikow)):
        for j in lista_id_pracownikow[i]:
            pensje.append((j, float(pensja[j]), year_start_vec[i], year_end_vec[i]))
    return pensje


def generate_stock_data(stock_days):
    ceny_akcji = []
    for i in range(len(stock_days)):
        if i < 1:
            ceny_akcji.append(np.random.normal(10, 0.5, 1))
        else:
            if ceny_akcji[i - 1] < 3:
                ceny_akcji.append(np.random.normal(ceny_akcji[i - 1] + 1, 0.5, 1))
            else:
                ceny_akcji.append(np.random.normal(ceny_akcji[i - 1], 0.5, 1))

    ilosc_emisji = [15000000 / 10] * len(ceny_akcji)
    akcje = []
    for i in range(len(ceny_akcji)):
        akcje.append((days_stock[i], float(ceny_akcji[i]), ilosc_emisji[i]))
    return akcje


def load_petrol_data():
    df_petrol = pd.read_csv('data/ceny_paliwa.csv')
    df_petrol['Data'] = pd.to_datetime(df_petrol['Data'])
    return df_petrol


def generate_petrol_data(df_petrol):
    ceny_paliwa = []
    for row in df_petrol.iterrows():
        ceny_paliwa.append((row[1]['Wartosc'], row[1]['Data'].to_pydatetime()))
    return ceny_paliwa


def generate_liabilities(stock_days):
    kwoty = len(stock_days) * [150000]
    dlugi = []
    for i in range(len(kwoty)):
        dlugi.append((stock_days[i], kwoty[i]))
    return dlugi


def generate_client_data(client_number):
    id_klientow = list(range(1, client_number))
    imiona = faker_generator('first_name', len(id_klientow))
    nazwiska = faker_generator('last_name', len(id_klientow))
    emaile = faker_generator('email', len(id_klientow))
    numery = faker_generator('phone_number', len(id_klientow))
    miasta = faker_generator('city', len(id_klientow))
    klienci = []
    for i in range(len(id_klientow)):
        klienci.append((id_klientow[i], imiona[i], nazwiska[i], emaile[i], numery[i], miasta[i]))
    return klienci


def generate_car_data(car_number, typ_samochodu, id_samochodow):
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
    for i in range(car_number):
        flota.append((
            id_samochodow[i], float(wagi_samochodow[i]), przebiegi[i], float(spalania[i]), float(max_zaladunki[i]),
            typ_samochodu[i]))
    return flota


def generate_fees(stock_days):
    dni_ubezpieczen = random.choices(range(1, 29), k=len(flota))
    miesiace_ubezpieczen = random.choices(range(1, 13), k=len(flota))
    oplaty = []
    counter = 0
    for i in range(len(stock_days)):
        for j in range(len(dni_ubezpieczen)):
            if dni_ubezpieczen[j] == stock_days[i].day and miesiace_ubezpieczen[j] == stock_days[i].month:
                oplaty.append(
                    (counter, 'ubezpieczenie', float(random.choice(list(np.arange(3000, 4000, 100)))), stock_days[i]))
                counter += 1
    return oplaty


def generate_jobs(df_petrol):
    scaled_petrol = -0.03 * scale(np.array(df_petrol['Wartosc']).reshape(-1, 1), axis=0).reshape(1, -1)[0]
    il_zlecen = [int(np.random.lognormal(np.log(15), 0.5)) for _ in range(len(days_stock))]
    # logging.info(f'Całkowita liczba zleceń: {sum(il_zlecen)}')
    id_zlecenia = list(range(1, sum(il_zlecen) + 1))

    dystanse = []
    for i in il_zlecen:
        dystanse.append(random.choices(range(150, 2900), k=i))
    wolni_kierowcy = pd.DataFrame(lista_id_pracownikow[0], columns=['id_kierowcy'])
    zajeci_kierowcy = pd.DataFrame(columns=['id_kierowcy', 'data_zakonczenia'])
    wolne_samochody = pd.DataFrame(zip(id_samochodow, typ_samochodu), columns=['id_samochodu', 'typ_samochodu'])
    zajete_samochody = pd.DataFrame(columns=['id_samochodu', 'typ_samochodu', 'data_zakonczenia'])
    niezrealizowane_zamowienia = pd.DataFrame(columns=['typ_samochodu', 'data_przyjecia'])

    counter = 0
    id_pracownika = []
    id_samochodu = []
    dystans = []
    daty_zlecen = []
    daty_realizacji = []
    kwoty = []

    for i in range(len(days_stock)):
        week = i // 7
        petrol_coef = scaled_petrol[week]
        potrzebne_sam_ciezarowe = 0
        potrzebne_sam_dostawcze = 0

        if days_stock[i].year != days_stock[i - 1].year:
            logging.info(f'Rozpoczęcie symulacji dla roku {days_stock[i].year}')
            counter += 1
            if counter != 1:
                logging.info(f'Stara liczba pracowników: {len(lista_id_pracownikow[counter - 2])}')
                logging.info(
                    f'Lista id zwolnionych pracowników {list(set(lista_id_pracownikow[counter - 2]).difference(set(lista_id_pracownikow[counter - 1])))}')
            if counter != 10:
                logging.info(f'Nowa liczba pracowników: {len(lista_id_pracownikow[counter - 1])}')

            zaktualizowani_pracownicy = set(lista_id_pracownikow[counter - 1])
            starzy_zajeci = set(zajeci_kierowcy['id_kierowcy'])
            id_nowi_zajeci = zaktualizowani_pracownicy.intersection(starzy_zajeci)

            id_nowi_wolni = zaktualizowani_pracownicy.difference(starzy_zajeci)

            wolni_kierowcy = pd.DataFrame(id_nowi_wolni, columns=['id_kierowcy'])
            # logging.info(f'Zaktualizowani wolni pracownicy: {wolni_kierowcy}')
            zajeci_kierowcy = zajeci_kierowcy[zajeci_kierowcy['id_kierowcy'].isin(list(id_nowi_zajeci))]
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
        # logging.info(f'Wolne samochody: {wolne_samochody}')
        # logging.info(f'Zajęte samochody: {zajete_samochody}')

        powrot_do_wolnych_kierowca = zajeci_kierowcy[zajeci_kierowcy['data_zakonczenia'] == days_stock[i]].iloc[:,
                                     :-1].reset_index(drop=True)
        zajeci_kierowcy = zajeci_kierowcy[zajeci_kierowcy['data_zakonczenia'] != days_stock[i]].reset_index(
            drop=True)
        wolni_kierowcy = pd.concat([wolni_kierowcy, powrot_do_wolnych_kierowca]).reset_index(drop=True)
        # logging.info(f'Wolni kierowcy: {wolni_kierowcy}')
        # logging.info(f'Zajęci kierowcy: {zajeci_kierowcy}')

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
            # logging.info(f'Niezrealizowane zamówienia dzień {days_stock[i]}:\n {niezrealizowane_zamowienia}')

            zalegle_daty = list(list(zalegle_daty_zlecen_dostawcze) + list(zalegle_daty_zlecen_ciezarowki))
            # logging.info(f'Zaległe Daty przyjęcia: {zalegle_daty}')

            k_ciezarowe = potrzebne_sam_ciezarowe + licz_usuwanych_ciezarowek \
                if potrzebne_sam_ciezarowe + licz_usuwanych_ciezarowek < liczba_wolnych_ciezarowek \
                else liczba_wolnych_ciezarowek
            k_dostawcze = potrzebne_sam_dostawcze + licz_usuwanych_dostawczych \
                if potrzebne_sam_dostawcze + licz_usuwanych_dostawczych < liczba_wolnych_dostawczych \
                else liczba_wolnych_dostawczych
            ilosc_zlecen_normalna = (k_ciezarowe + k_dostawcze) - len(zalegle_daty)
            daty_przyjecia = zalegle_daty + ilosc_zlecen_normalna * [days_stock[i]]
            dystanse[i] = dystanse[i][:k_ciezarowe + k_dostawcze]
        else:
            k_ciezarowe = potrzebne_sam_ciezarowe \
                if potrzebne_sam_ciezarowe < liczba_wolnych_ciezarowek \
                else liczba_wolnych_ciezarowek
            k_dostawcze = potrzebne_sam_dostawcze \
                if potrzebne_sam_dostawcze < liczba_wolnych_dostawczych \
                else liczba_wolnych_dostawczych

            daty_przyjecia = (k_ciezarowe + k_dostawcze) * [days_stock[i]]
            dystanse[i] = dystanse[i][:k_ciezarowe + k_dostawcze]

        wyrzucane_samochody_1 = list(random.sample(
            list(wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod ciezarowy']['id_samochodu']),
            k=k_ciezarowe))
        wyrzucane_samochody_2 = list(random.sample(
            list(wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod dostawczy']['id_samochodu']),
            k=k_dostawcze))

        wybierany_df = wolne_samochody[
            wolne_samochody['id_samochodu'].isin(wyrzucane_samochody_1 + wyrzucane_samochody_2)].reset_index(drop=True)
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod ciezarowy', 'data_zakonczenia'] = \
            np.repeat(days_stock[i] + datetime.timedelta(days=5), len(wyrzucane_samochody_1))

        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod dostawczy', 'data_zakonczenia'] = \
            np.repeat(days_stock[i] + datetime.timedelta(days=2), len(wyrzucane_samochody_2))

        wybrane_id_samochodow = list(wolne_samochody[wolne_samochody['id_samochodu'].isin(
            wyrzucane_samochody_1 + wyrzucane_samochody_2)]['id_samochodu'])

        # logging.info(f'DataFrame samochodów używanych w zleceniach dzień {days_stock[i]}:\n {wybierany_df}')
        wolne_samochody = wolne_samochody[~wolne_samochody['id_samochodu'].isin(wybrane_id_samochodow)].reset_index(
            drop=True)
        # logging.info(f'Wolne samochody po aktualizacji dzień {days_stock[i]}:\n {wolne_samochody}')
        zajete_samochody = pd.concat([zajete_samochody, wybierany_df]).reset_index(drop=True)
        # logging.info(f'Zajęte samochody po aktualizacji dzień {days_stock[i]}:\n {zajete_samochody}')

        # wybieranie kierowców
        potrzebni_kierowcy = k_ciezarowe + k_dostawcze
        wyrzucani_kierowcy = list(random.sample(list(wolni_kierowcy['id_kierowcy']),  # kierowcy wybrani do przejazdów
                                                k=potrzebni_kierowcy))
        wybierany_df_kierowcy = wolni_kierowcy[wolni_kierowcy['id_kierowcy'].isin(wyrzucani_kierowcy)].reset_index(
            drop=True)
        # logging.info(wybierany_df_kierowcy[:k_ciezarowe].shape[0])

        if not wybierany_df_kierowcy.empty:
            wybierany_df_kierowcy.loc[:k_ciezarowe, 'data_zakonczenia'] = \
                pd.Series(np.repeat(days_stock[i] + datetime.timedelta(days=5), k_ciezarowe))

            wybierany_df_kierowcy.loc[k_ciezarowe:, 'data_zakonczenia'] = \
                np.repeat(days_stock[i] + datetime.timedelta(days=2), k_dostawcze)
        wolni_kierowcy = wolni_kierowcy[~wolni_kierowcy['id_kierowcy'].isin(wyrzucani_kierowcy)].reset_index(drop=True)
        # logging.info(f'Wolni kierowcy po aktualizacji dzień {days_stock[i]}:\n {wolni_kierowcy}')
        zajeci_kierowcy = pd.concat([zajeci_kierowcy, wybierany_df_kierowcy]).reset_index(drop=True)
        # logging.info(f'Zajęci kierowcy po aktualizacji dzień {days_stock[i]}:\n {zajeci_kierowcy}')

        assert len(list(wybierany_df_kierowcy['id_kierowcy'])) == len(wybrane_id_samochodow)

        potrzebne_sam_ciezarowe = potrzebne_sam_ciezarowe - k_ciezarowe if potrzebne_sam_ciezarowe - k_ciezarowe > 0 else 0
        potrzebne_sam_dostawcze = potrzebne_sam_dostawcze - k_dostawcze if potrzebne_sam_dostawcze - k_dostawcze > 0 else 0

        # logging.info(
        # f'Ilość niezrealizowanych zleceń w dniu {days_stock[i]}: {potrzebne_sam_dostawcze + potrzebne_sam_ciezarowe}')
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
            # logging.info(f"Niezrealizowane zamówienia: {niezrealizowane_zamowienia}")
            assert niezrealizowane_zamowienia.shape[0] > 0

        if k_dostawcze + k_ciezarowe > len(dystanse[i]):
            roznica = (k_dostawcze + k_ciezarowe) - len(dystanse[i])
            dystanse[i].extend(list(np.random.randint(700, 900, roznica)))
        assert k_dostawcze + k_ciezarowe == len(wybrane_id_samochodow)
        assert k_dostawcze + k_ciezarowe == len(list(wybierany_df_kierowcy['id_kierowcy']))
        assert k_dostawcze + k_ciezarowe == len(dystanse[i])
        assert k_dostawcze + k_ciezarowe == len(daty_przyjecia)

        id_pracownika.extend(list(wybierany_df_kierowcy['id_kierowcy']))
        id_samochodu.extend(list(wybrane_id_samochodow))
        dystans.extend(list(dystanse[i]))
        kwoty.extend([round((0.75 + petrol_coef) * j, 2) if j > 800 else round((1 + petrol_coef) * j, 2) for j in dystanse[i]])
        daty_zlecen.extend(list(daty_przyjecia))
        daty_realizacji.extend([days_stock[i]] * (k_dostawcze + k_ciezarowe))

    id_zlecenia = id_zlecenia[:len(dystans)]
    # logging.info(f"dlugosc id_zlecenia: {len(id_zlecenia)}, dlugosc pracownika {len(id_pracownika)}")
    assert len(id_zlecenia) == len(dystans)
    assert len(id_zlecenia) == len(id_pracownika)

    id_klienta = random.choices(id_klientow, k=len(id_zlecenia))
    zlecenia = []

    for i in range(len(id_zlecenia)):
        zlecenia.append(
            (id_zlecenia[i], int(id_pracownika[i]), int(id_samochodu[i]), int(id_klienta[i]), float(dystans[i]),
             daty_zlecen[i], daty_realizacji[i], float(kwoty[i])))

    return zlecenia


def generate_pracownicy(lista_id_pracownikow):
    imiona_prac = faker_generator('first_name', lista_id_pracownikow[-1][-1] + 1)
    nazwiska_prac = faker_generator('last_name', lista_id_pracownikow[-1][-1] + 1)
    pracownicy = []
    for i in range(lista_id_pracownikow[-1][-1]):
        pracownicy.append((id_pracownikow[i], imiona_prac[i], nazwiska_prac[i]))
    return pracownicy


def populate_database():
    db_connection = MySQLConnector.connect("localhost", "root", database="spedycja")
    cursor = MySQLConnector.get_cursor(db_connection)
    for table_name in szablon_bazy.keys():
        mySql_insert_query = 'INSERT INTO {}'.format(table_name) + ' (' + \
                             ', '.join([i for i in szablon_bazy[table_name]]) + \
                             ') VALUES(%s' + ', %s' * (len(szablon_bazy[table_name]) - 1) + ');'
        logging.info(f"{mySql_insert_query}, {table_name}")
        MySQLConnector.executemany(cursor, mySql_insert_query, eval(table_name))
        MySQLConnector.commit(db_connection)

    MySQLConnector.close_connection(db_connection)
    logging.info("Wypełnianie bazy danych zakończone sukcesem!")


if __name__ == "__main__":

    sdate_stock = datetime.date(2010, 1, 1)
    edate_stock = datetime.date(2020, 4, 1)
    delta = edate_stock - sdate_stock
    days_stock = []
    for i in range(delta.days + 1):
        day = sdate_stock + datetime.timedelta(days=i)
        days_stock.append(day)

    od_daty = [datetime.date(i, 1, 1) for i in range(2010, 2020)]
    od_daty.append(datetime.date(2020, 1, 1))
    do_daty = [datetime.date(i, 12, 31) for i in range(2010, 2020)]
    do_daty.append(edate_stock)

    id_samochodow = list(range(1, 76))
    id_klientow = list(range(1, 1350))
    typ_samochodu = random.choices(80 * ['samochod ciezarowy'] + 20 * ['samochod dostawczy'], k=75)

    szablon_bazy = {'akcje': ('data', 'cena', 'emitowana_ilosc'),
                    'ceny_paliwa': ('cena', 'data'),
                    'dlugi': ('data', 'kwota'),
                    'flota': (
                        'id_samochodu', 'waga_samochodu', 'przebieg', 'spalanie', 'max_zaladunek', 'typ_samochodu'),
                    'klienci': ('id_klienta', 'Imie', 'Nazwisko', 'e_mail', 'telefon', 'miejscowosc'),
                    'pracownicy': ('id_pracownika', 'Imie', 'Nazwisko'),
                    'oplaty': ('id_oplaty', 'rodzaj_oplaty', 'kwota_transakcji', 'data'),
                    'pensje': ('id_pracownika', 'pensja', 'od_daty', 'do_daty'),
                    'zlecenia': (
                        'id_zlecenia', 'id_pracownika', 'id_samochodu', 'id_klienta', 'dystans', 'data_przyjecia',
                        'data_realizacji', 'kwota')}

    petrol_data = load_petrol_data()
    lista_id_pracownikow = create_employees(od_daty)
    id_pracownikow = list(range(1, lista_id_pracownikow[-1][-1] + 1))
    pensje = create_salaries(od_daty, do_daty, 4800, 100, lista_id_pracownikow)
    akcje = generate_stock_data(days_stock)
    ceny_paliwa = generate_petrol_data(petrol_data)
    dlugi = generate_liabilities(days_stock)
    klienci = generate_client_data(1350)
    flota = generate_car_data(75, typ_samochodu, id_samochodow)
    oplaty = generate_fees(days_stock)
    zlecenia = generate_jobs(petrol_data)
    pracownicy = generate_pracownicy(lista_id_pracownikow)
    populate_database()
