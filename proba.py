import mysql.connector
import random
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from faker import Faker

def faker_generator(kind, n):
    array = []
    for i in range(1,n+1):
        eval('array.append(faker.{}())'.format(kind))
    return array    
    
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="haslo",
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

sdate_stock = datetime.date(2010,1,1)
edate_stock = datetime.date(2020,4,1)
delta = edate_stock - sdate_stock
days_stock = [] 
for i in range(delta.days + 1):
    day = sdate_stock + datetime.timedelta(days=i)
    days_stock.append(day)

szablon_bazy = {'akcje':('data', 'cena', 'emitowana_ilosc'), \
                'ceny_paliwa':('cena', 'data'), \
                'dlugi':('data', 'kwota'), \
                'flota':('id_samochodu', 'waga_samochodu','przebieg', 'spalanie', 'max_zaladunek', 'typ_samochodu'), \
                'klienci':('id_klienta', 'Imie', 'Nazwisko', 'e_mail', 'telefon', 'miejscowosc'), \
                'pracownicy':('id_pracownika', 'Imie', 'Nazwisko'), \
                'oplaty':('rodzaj_oplaty', 'kwota_transakcji', 'data'), \
                'pensje':('id_pracownika', 'pensja', 'od_daty', 'do_daty'), \
                'zlecenia':('id_zlecenia', 'id_pracownika', 'id_samochodu', 'id_klienta', 'dystans', 'data_przyjecia', 'data_realizacji', 'kwota')}

#############################
#    pensje
#############################

#pensje_prac = [4000]*len(id_pracownikow)
od_daty = [datetime.date(i,1,1) for i in range(2010,2020)]
od_daty.append(datetime.date(2020,1,1))
do_daty = [datetime.date(i,12,31) for i in range(2010,2020)]
do_daty.append(edate_stock)
ilosc_pracownikow = np.random.poisson(82, len(od_daty))
print(ilosc_pracownikow,'ilosc_prac')
lista_id_pracownikow = []
for i in range(len(od_daty)):
    if i==0:
        lista_id_pracownikow.append(list(range(1, ilosc_pracownikow[i]+1)))
    else:
        if ilosc_pracownikow[i] > ilosc_pracownikow[i - 1]:
            lista_pomocnicza = list(lista_id_pracownikow[i-1])
            
            lista_pomocnicza.extend(list(range(lista_pomocnicza[-1]+1, lista_pomocnicza[-1]+1+ilosc_pracownikow[i]-ilosc_pracownikow[i-1])))
            #print(lista_pomocnicza.extend(list(range(lista_id_pracownikow[i-1][-1]+1, lista_id_pracownikow[i-1][-1]+1+ilosc_pracownikow[i]-ilosc_pracownikow[i-1]))))
            lista_id_pracownikow.append(lista_pomocnicza)
        elif ilosc_pracownikow[i] < ilosc_pracownikow[i - 1]:
            wylosowany_index = int(random.choice(lista_id_pracownikow[i-1]))
            lista_pomocnicza = list(lista_id_pracownikow[i-1])
            del lista_pomocnicza[wylosowany_index:(wylosowany_index+ilosc_pracownikow[i - 1]-ilosc_pracownikow[i]+1)]
            lista_id_pracownikow.append(lista_pomocnicza)
        else:
            lista_id_pracownikow.append(lista_id_pracownikow[i-1])
lista_id_pracownikow
pensje = []
for i in range(len(lista_id_pracownikow)):
    for j in lista_id_pracownikow[i]:
        pensje.append((j,4000 ,od_daty[i], do_daty[i]))
id_pracownikow = list(range(1,lista_id_pracownikow[-1][-1]+1))
#######################3
### akcje i paliwa
#######################
ceny_akcji = []
ceny_pal = []
for i in range(len(days_stock)):
    if i<1:
        ceny_akcji.append(np.random.normal(10, 0.5, 1))
    else:
        if ceny_akcji[i-1]<3:
            ceny_akcji.append(np.random.normal(ceny_akcji[i-1]+1, 0.5,1))
        else:
            ceny_akcji.append(np.random.normal(ceny_akcji[i-1], 0.5,1))
ceny_pal = (np.random.normal(4.3,0.3,len(ceny_akcji)))
ceny_pal =np.convolve(ceny_pal, np.ones((40,))/40)[(40-1):]  #sredia kroczaca
ilosc_emisji = [15000000/10]*len(ceny_akcji)

##plt.figure()
##plt.plot(days_stock, ceny_akcji)

akcje = []
for i in range(len(ceny_akcji)):
    akcje.append((days_stock[i], float(ceny_akcji[i]), ilosc_emisji[i]))

    
ceny_paliwa= []
for i in range(len(ceny_paliwa[:-40])):
    ceny_paliwa.append(((float((ceny_paliwa[:-40])[i]), (days_stock[:-40])[i])))



#plt.figure()
#plt.plot(days_stock[:-40], ceny_paliwa[:-40])

################################3
#    dlugi
###############################

kwoty = len(days_stock)*[150000]
dlugi = []
for i in range(len(kwoty)):
    dlugi.append((days_stock[i], kwoty[i]))


###############################
##    klienci
#############
    
id_samochodow = list(range(1,76))

id_klientow = list(range(1,1350))
id_zlecen = list(range(1,3000))


imiona = faker_generator('first_name',len(id_klientow))
nazwiska = faker_generator('last_name',len(id_klientow))
emaile = faker_generator('email',len(id_klientow))
numery = faker_generator('phone_number',len(id_klientow))
miasta = faker_generator('city',len(id_klientow))
klienci = []
for i in range(len(id_klientow)):
    klienci.append((id_klientow[i], imiona[i], nazwiska[i], emaile[i], numery[i], miasta[i]))

#########################
##### flota
##########################
typ_samochodu = random.choices(85*['samochod ciezarowy'] + 15*['samochod dostawczy'],k=75)
wagi_samochodow = []
przebiegi = []
max_zaladunki = []
spalania = []
for samochod in typ_samochodu:
    if samochod == 'samochod ciezarowy':
        wagi_samochodow.append(random.choice(list(np.arange(12000,15001,100))))
        max_zaladunki.append(40000 - wagi_samochodow[-1])
        spalania.append(wagi_samochodow[-1]*3/1000-7)
    else:
        wagi_samochodow.append(random.choice(list(np.arange(2000,2600,100))))
        max_zaladunki.append(3500 - wagi_samochodow[-1])
        spalania.append(wagi_samochodow[-1]*1/120-26/3)
    przebiegi.append(random.choice(list(range(30,1000000))))    


flota = []
for i in range(75):
    flota.append((id_samochodow[i], float(wagi_samochodow[i]), przebiegi[i], float(spalania[i]), float(max_zaladunki[i]), typ_samochodu[i]))
#################
#    oplaty
###################
rodzaj_oplaty = ['oplata']*len(days_stock)
kwota_transkacji = [600]*len(days_stock)
oplaty = []
for i in range(len(days_stock)):
    oplaty.append((rodzaj_oplaty[i], kwota_transkacji[i], days_stock[i]))

#########################
#  zlecenia
######################

###########   PROBA WYGENEROWANIA SENSOWNYCH DANYCH

il_zlecen = list(random.choices(list(np.arange(12,32,1)), k = len(days_stock)))

#id_zlecenia = list(range(sum(il_zlecen)))
dystanse = []
for i in il_zlecen:
    dystanse.append(random.choices(range(150,2900), k = i))
wolni_kierowcy = pd.DataFrame(lista_id_pracownikow[0],columns = ['id_kierowcy'])
zajeci_kierowcy = pd.DataFrame()
wolne_samochody = pd.DataFrame(zip(id_samochodow, typ_samochodu),columns = ['id_samochodu', 'typ_samochodu'])
zajete_samochody = pd.DataFrame(columns = ['id_samochodu', 'typ_samochodu', 'data_zakonczenia'])
niezrealizowane_zamowienia = pd.DataFrame(columns = ['id_zlecenia','data_przyjecia','id_samochodu', 'typ_samochodu'])

print(wolne_samochody)
potrzebne_sam_ciezarowe = 0
potrzebne_sam_dostawcze = 0
counter = 0 
id_pracujacych = lista_id_pracownikow[counter]
id_zlecenia = []
id_pracownika = []
id_samochodu = []
dystans = []
daty_zlecen = []
kwoty = []
for i in range(len(days_stock)):
    if i ==0:
        for j in range(il_zlecen[i]):
            if dystanse[i][j]>800:
                potrzebne_sam_ciezarowe += 1
            else:
                potrzebne_sam_dostawcze += 1
        wyrzucane_samochody_1 = list(random.choices(list(wolne_samochody[wolne_samochody['typ_samochodu']=='samochod ciezarowy']['id_samochodu']), k = potrzebne_sam_ciezarowe))
        wyrzucane_samochody_2 = list(random.choices(list(wolne_samochody[wolne_samochody['typ_samochodu']=='samochod dostawczy']['id_samochodu']), k = potrzebne_sam_dostawcze))
        wybierany_df = wolne_samochody[wolne_samochody['id_samochodu'].isin(wyrzucane_samochody_1+wyrzucane_samochody_2)]
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod ciezarowy', 'data_zakonczenia'] = days_stock[i]+datetime.timedelta(days=5)
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod dostawczy', 'data_zakonczenia'] = days_stock[i]+datetime.timedelta(days=2)
        #print(wybierany_df)
        wybrane_id_samochodow = list(wolne_samochody[wolne_samochody['id_samochodu'].isin(wyrzucane_samochody_1+wyrzucane_samochody_2)].index.values)
        #zajete_samochody = pd.concat(zajete_samochody, wybierany_df)
        wolne_samochody = wolne_samochody.drop(index = wybrane_id_samochodow, inplace = False)
        #print(wolne_samochody)
        zajete_samochody = pd.concat([zajete_samochody, wybierany_df])
        #print(zajete_samochody)
        potrzebne_sam_ciezarowe = 0
        potrzebne_sam_dostawcze = 0
        
        id_zlecenia.extend(list(range(1, il_zlecen[i])))
        id_pracownika.extend((il_zlecen[i]+1)*[10])
        print(len(id_zlecenia), len(id_pracownika))
        id_samochodu.extend(wybrane_id_samochodow)
        dystans.extend(dystanse[i])
        kwoty.extend([0.75*j if j>800 else j for j in dystanse[i]])
        daty_zlecen.extend([days_stock[i]]*(il_zlecen[i]))
        
 #       print(len(lista_id_pracownikow))
    else:
        
        id_pracujacych = lista_id_pracownikow[counter]
        
        if days_stock[i].year != days_stock[i-1].year:
            counter +=1
        for j in range(il_zlecen[i]):
            if dystanse[i][j]>800:
                potrzebne_sam_ciezarowe += 1
            else:
                potrzebne_sam_dostawcze += 1

                
        powrot_do_wolnych = zajete_samochody[zajete_samochody['data_zakonczenia'] == days_stock[i]]
        powrot_do_wolnych = zajete_samochody[zajete_samochody['data_zakonczenia'] == days_stock[i]].drop('data_zakonczenia', axis = 1)
        
        wolne_samochody = pd.concat([wolne_samochody, powrot_do_wolnych])
        liczba_wolnych_ciezarowek = wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod ciezarowy'].shape[0]
        liczba_wolnych_dostawczych = wolne_samochody[wolne_samochody['typ_samochodu'] == 'samochod dostawczy'].shape[0]

        
        
        if niezrealizowane_zamowienia.shape[0] > 0:
            
            l_ciezarowek = niezrealizowane_zamowienia[niezrealizowane_zamowienia['typ_samochodu'] == 'samochod ciezarowy'].shape[0]
            l_dostawczych = niezrealizowane_zamowienia[niezrealizowane_zamowienia['typ_samochodu'] == 'samochod dostawczy'].shape[0]
        
            
            licz_usuwanych_ciezarowek = liczba_wolnych_ciezarowek if liczba_wolnych_ciezarowek < l_ciezarowek else l_ciezarowek
            licz_usuwanych_dostawczych = liczba_wolnych_dostawczych if liczba_wolnych_dostawczych < l_dostawczych else l_dostawczych
            
            niezrealizowane_zamowienia[niezrealizowane_zamowienia['typ_samochodu'] == 'samochod ciezarowy'].iloc[:licz_usuwanych_ciezarowek]# = 
                        
        

        
        
        
        
        k_ciezarowe = potrzebne_sam_ciezarowe if liczba_wolnych_ciezarowek>potrzebne_sam_ciezarowe else liczba_wolnych_ciezarowek
        k_dostawcze = potrzebne_sam_dostawcze if liczba_wolnych_dostawczych>potrzebne_sam_dostawcze else liczba_wolnych_dostawczych
        
        wyrzucane_samochody_1 = list(random.choices(list(wolne_samochody[wolne_samochody['typ_samochodu']=='samochod ciezarowy']['id_samochodu']),\
                                                    k = k_ciezarowe))
        wyrzucane_samochody_2 = list(random.choices(list(wolne_samochody[wolne_samochody['typ_samochodu']=='samochod dostawczy']['id_samochodu']),\
                                                    k = k_dostawcze))
        
        
        potrzebne_sam_ciezarowe = potrzebne_sam_ciezarowe - k_ciezarowe
        potrzebne_sam_dostawcze = potrzebne_sam_dostawcze - k_dostawcze
        
        
        
        
        if potrzebne_sam_ciezarowe + potrzebne_sam_dostawcze > 0:
            niezrealizowane_zamowienia_pom = pd.DataFrame({'id_zlecenia':list(range(id_zlecenia[-1]+1 + k_ciezarowe_k_dostawcze, id_zlecenia[-1] + il_zlecen[i] )),
                                                           'data_przyjecia':(potrzebne_sam_ciezarowe+potrzebne_sam_dostawcze) * [days_stock[i]],
                                                           'id_samochodu':(potrzebne_sam_ciezarowe+potrzebne_sam_dostawcze) *[None],
                                                           'typ_samochodu':potrzebne_sam_ciezarowe*['samochod ciezarowy'] + potrzebne_sam_dostawcze*['samochod dostawczy']})
            niezrealizowane_zamowienia = pd.concat([niezrealizowane_zamowienia, niezrealizowane_zamowienia_pom])
        
            
        
        wybierany_df = wolne_samochody[wolne_samochody['id_samochodu'].isin(wyrzucane_samochody_1+wyrzucane_samochody_2)]
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod ciezarowy', 'data_zakonczenia'] = days_stock[i]+datetime.timedelta(days=5)
        wybierany_df.loc[wybierany_df['typ_samochodu'] == 'samochod dostawczy', 'data_zakonczenia'] = days_stock[i]+datetime.timedelta(days=2)

        wybrane_id_samochodow = list(wolne_samochody[wolne_samochody['id_samochodu'].isin(wyrzucane_samochody_1+wyrzucane_samochody_2)].index.values)
        
        wolne_samochody = wolne_samochody.drop(index = wybrane_id_samochodow, inplace = False)
        zajete_samochody = pd.concat([zajete_samochody, wybierany_df])


        
        #   print(id_zlecenia)
        
        id_zlecenia.extend(list(range(id_zlecenia[-1]+1, id_zlecenia[-1] + il_zlecen[i])))
        id_pracownika.extend((il_zlecen[i]+1)*[20])
        id_samochodu.extend(wybrane_id_samochodow)
        dystans.extend(dystanse[i])
        kwoty.extend([0.75*j if j>800 else j for j in dystanse[i]])
        daty_zlecen.extend([days_stock[i]]*(il_zlecen[i]))
        #print(len(id_zlecenia), len(id_pracownika))
        
        
daty_realizacji = daty_zlecen
id_klienta = random.choices(id_klientow, k = len(id_zlecenia))
zlecenia = []
id_samochodu = ([20]*(len(id_zlecenia)))
print(len(id_zlecenia), len(id_pracownika), len(id_samochodu), len(id_klienta), len(dystans), len(daty_zlecen), len(kwoty))
for i in range(len(id_zlecenia)):
    # print(id_zlecenia[i])
     #print(id_pracownika[i])
    zlecenia.append((id_zlecenia[i],int(id_pracownika[i]),int(id_samochodu[i]),int(id_klienta[i]), dystans[i],daty_zlecen[i], daty_realizacji[i], kwoty[i]))
    

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
#pracownicy
#############################
imiona_prac = random.choices(imiona, k = lista_id_pracownikow[-1][-1]+1)
nazwiska_prac = random.choices(nazwiska, k = lista_id_pracownikow[-1][-1]+1)

pracownicy = []
for i in range(lista_id_pracownikow[-1][-1]):
    pracownicy.append((id_pracownikow[i], imiona_prac[i], nazwiska_prac[i]))


###############################
#   wypelnianie bazy
#########################

for table_name in szablon_bazy.keys():
    mySql_insert_query = 'INSERT INTO {}'.format(table_name) + ' (' +\
                         ', '.join([i for i in szablon_bazy[table_name]])+\
                           ') VALUES(%s '+',%s'*(len(szablon_bazy[table_name])-1) + ');'
    print(mySql_insert_query, table_name)
    mycursor.executemany(mySql_insert_query, eval(table_name))
    mydb.commit()



mydb.close()
plt.show()
