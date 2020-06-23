#!/usr/bin/env python
# coding: utf-8


import mysql.connector
import os
import re
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.optimize import fsolve
from scipy.stats import norm
from sklearn.preprocessing import scale
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from util.MySQLConnector import MySQLConnector


connection = MySQLConnector.connect('localhost', 'root', database='spedycja')
cursor = MySQLConnector.get_cursor(connection)


start_date = datetime(2010, 1, 1)
end_date = datetime(2020, 4, 1)



def get_liczba_oczekujacych_zlecen(start_date, end_date):
    n_oczekujace = pd.DataFrame(columns=['Data', 'Ilość oczekujących'])
    oczekujace_help = pd.DataFrame(columns=['Data przyjęcia', 'Data realizacji'])
    oczekujace = daty[daty['Data przyjęcia'] != daty['Data realizacji']].reset_index(drop=True)
    date_range = pd.date_range(start_date, end_date)
    for date in date_range:
        oczekujace_help = oczekujace_help[oczekujace_help['Data realizacji']!=date]
        niezrealizowane_date = oczekujace[oczekujace['Data przyjęcia']==date]
        oczekujace_help = pd.concat([oczekujace_help, niezrealizowane_date]).reset_index(drop=True)
        n_oczekujace = pd.concat([n_oczekujace, pd.DataFrame({'Data': [date], 'Ilość oczekujących': [oczekujace_help.shape[0]]})]).reset_index(drop=True)
    return n_oczekujace
    


def save_html(fig: go.Figure, file_name: str):
    if not os.path.exists("images"):
        os.mkdir("images")

    file_path = os.path.join("images", file_name)
    plotly.io.write_html(fig, file=file_path)


cursor.execute('SELECT data_przyjecia, data_realizacji from zlecenia')
result = cursor.fetchall()


daty = pd.DataFrame(result, columns=['Data przyjęcia', 'Data realizacji'])

n_oczekujace = get_liczba_oczekujacych_zlecen(start_date, end_date)


fig = go.Figure()
fig.add_trace(go.Scatter(x=n_oczekujace['Data'],
                         y=n_oczekujace['Ilość oczekujących'],
                        mode="markers"))
fig.update_layout(title={
    'text': f'Liczba oczekujących zleceń w czasie',
'y': 0.9,
'x':0.5},
width=1200,
height=600,
titlefont=dict(size=25),
                 font=dict(size=16),
xaxis_title='',
                 yaxis_title='Dzienna liczba oczekujących zleceń')
fig.show()


save_html(fig, 'oczekujace_zlecenia_scatter.html')


dates = [i[0] for i in n_oczekujace.resample('W-Mon', on='Data')['Data']]
avg_oczekujacych_week = np.array([i[1].mean() for i in n_oczekujace.resample('W-Mon', on='Data')['Ilość oczekujących']])


fig = go.Figure()
fig.add_trace(go.Scatter(x=dates,
                         y=avg_oczekujacych_week))
fig.update_layout(title={
    'text': f'Agregacja tygodniowa liczby oczekujących zleceń',
'y': 0.9,
'x':0.5},
width=1200,
height=600,
titlefont=dict(size=25),
                 font=dict(size=16),
xaxis_title='',
                 yaxis_title='Liczba oczekujących zleceń')
fig.show()


save_html(fig, 'oczekujace_zlecenia__tygodniowo_line.html')


cursor.execute('SELECT od_daty from pensje')
result = cursor.fetchall()
daty = pd.DataFrame(result, columns=['Data rozpoczęcia kontraktu'])


date = [i[0] for i in daty.groupby('Data rozpoczęcia kontraktu')]
ilosc_pracownikow = [i[1].shape[0] for i in daty.groupby('Data rozpoczęcia kontraktu')]


fig = px.bar(x=date,
                         y=ilosc_pracownikow)

fig.add_trace(go.Scatter(x=date,
                         y=ilosc_pracownikow,
                        name='Liczba pracowników'))
fig.update_layout(title={
    'text': f'Liczba pracowników w danym roku',
'y': 0.95,
'x':0.5},
width=1200,
height=600,
titlefont=dict(size=25),
                 font=dict(size=16),
xaxis_title='',
                 yaxis_title='Liczba pracowników')
fig.show()


save_html(fig, 'pracownicy_ilosc_rocznie.html')


cursor.execute('SELECT dystans, data_realizacji from zlecenia')
result = cursor.fetchall()
df = pd.DataFrame(result, columns=['Dystans', 'Data rozpoczęcia realizacji'])


df['Data zakończenia realizacji'] = df.apply(lambda x: x[1]+timedelta(days=2) if x[0]<800 else x[1]+timedelta(days=5), axis=1)
df


date_range = pd.date_range(start_date, end_date)
liczba_zajetych = [df[(df['Data rozpoczęcia realizacji'] <= date) & (df['Data zakończenia realizacji'] > date)].shape[0] for date in date_range]


fig = go.Figure()
fig.add_trace(go.Scatter(x=date_range,
                         y=liczba_zajetych))
fig.update_layout(title={
    'text': f'Liczba kursujących kierowców w czasie',
'y': 0.9,
'x':0.5},
width=1200,
height=600,
titlefont=dict(size=25),
                 font=dict(size=16),
xaxis_title='',
                 yaxis_title='Liczba kierowców')
fig.show()


save_html(fig, 'kursujacy_kierowcy_liczba_dziennie.html')


trading_days_year = 252
r = 0.005/trading_days_year
years = 10 


cursor.execute('select * from akcje;')
result = cursor.fetchall()
akcje = pd.DataFrame(result, columns=['data', 'cena', 'ilosc_akcji'])


akcje_log_return = np.log(akcje['cena']).diff().dropna().reset_index(drop=True)
std_akcje_log_return = np.std(akcje_log_return)


cursor.execute('select * from dlugi;')
result = cursor.fetchall()
dlugi = pd.DataFrame(result, columns=['data', 'wartosc'])


fig = px.line(x=akcje['data'], y=akcje['cena'])
fig.update_layout(autosize=True,
                  title={
    'text': f'Cena akcji',
'y': 0.95,
'x':0.5},
width=1200,
height=600,
titlefont=dict(size=25),
                 font=dict(size=16),
xaxis_title='',
                 yaxis_title='Cena')


save_html(fig, 'cena_akcji.html')


fig = px.line(x=akcje['data'][1:], y=akcje_log_return)
fig.update_layout(autosize=True,
                  title={
    'text': f'Dzienne logarytmiczne stopy zwrotu',
'y': 0.95,
'x':0.5},
width=1200,
height=600,
titlefont=dict(size=25),
                 font=dict(size=16),
xaxis_title='',
                 yaxis_title='Log stopy zwrotu')


save_html(fig, 'log_stopy_zwrotu.html')


fig = go.Figure()
fig.add_trace(go.Scatter(x=akcje['data'],
                        y=akcje['cena']*akcje['ilosc_akcji'],
                       mode='lines',
                        name='Aktywa'))
fig.add_trace(go.Scatter(x=akcje['data'],
                        y=dlugi['wartosc'],
                       mode='lines',
                        name='Długi'))

fig.update_layout(autosize=True,
                  title={
    'text': f'Wartość akcji vs wartość długów',
'y': 0.95,
'x':0.5},
width=1200,
height=600,
titlefont=dict(size=25),
                 font=dict(size=16),
xaxis_title='',
                 yaxis_title='Wartość (zł)')


save_html(fig, 'wartosc_akcji_vs_dlugu.html')



def d1(V_t, L, r, sigma_v, horizon):
    return (np.log(V_t/L) + (r+0.5*sigma_v**2)*horizon) / (sigma_v*np.sqrt(horizon))

def d2(V_t, L, r, sigma_v, horizon):
    return (np.log(V_t/L) + (r-0.5*sigma_v**2)*horizon) / (sigma_v*np.sqrt(horizon))

def equations(params, add_args):
    V_t, sigma_v = params
    L, r, horizon, E_t, sigma_e = add_args
    d1_v = d1(V_t, L, r, sigma_v, horizon)
    d2_v = d2(V_t, L, r, sigma_v, horizon)
    return (V_t*norm.cdf(d1_v) -        L*np.exp(-r*horizon)*norm.cdf(d2_v) -        E_t,
      E_t*sigma_e - norm.cdf(d1_v)*sigma_v*V_t)


result = []
for i in range(trading_days_year, years*trading_days_year-2):
    aktywa = akcje['cena'][i]*akcje['ilosc_akcji'][i]
    dlugi_wartosc = dlugi['wartosc'][i]
    std_rocz_log_stopy = np.std(akcje_log_return[i-trading_days_year:i])
    V_t, sigma_v = fsolve(equations,
                                    (aktywa, std_rocz_log_stopy),
                                    args=[dlugi_wartosc, r, trading_days_year,
                                          aktywa, std_rocz_log_stopy])
    d2_ret = d2(V_t, dlugi_wartosc, r, sigma_v, trading_days_year)
    result.append(1 - norm.cdf(d2_ret))
result = pd.Series(np.array(result))


fig = px.line(x=akcje['data'][312:], y=result)
fig.update_layout(autosize=True,
            width=900,
            height=600,
            title={
                'text': "Prawdopodobieństwo bankructwa w czasie",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 25}},
            xaxis_title={'text': "Czas",
                         'font': {'size':20}},
            yaxis_title={'text': "$DP~(10^{-6})$",
                         'font': {'size':20}},
                 font=dict(size=16))


save_html(fig, 'prawdopodobienstwo_bankructwa.html')


cursor.execute('''
select id_k, data_przyjecia, data_realizacji, Imie, Nazwisko from(
(SELECT id_klienta as id_z, data_przyjecia, data_realizacji from zlecenia) as t1
inner join
(SELECT id_klienta as id_k, Imie, Nazwisko from klienci) as t2 on t1.id_z = t2.id_k)
WHERE data_przyjecia != data_realizacji;
''')

result = cursor.fetchall()
df = pd.DataFrame(result, columns=["id_klienta", "data_przyjecia", "data_realizacji", "Imie", "Nazwisko"])



df['Imie i nazwisko'] = df['Imie'] + ' ' + df['Nazwisko']
df['Czas_oczekiwania'] = df['data_realizacji'] - df['data_przyjecia']
df = df.drop(['Imie', 'Nazwisko', 'data_przyjecia', 'data_realizacji'], axis=1)



df_map = df.drop_duplicates('id_klienta').iloc[:, :-1].reset_index(drop=True)



czas_oczekiwania = df.groupby('id_klienta')['Czas_oczekiwania'].sum()


top_czas_oczekiwania = czas_oczekiwania.sort_values(ascending=False).reset_index().head(20)


najdluzej_czekajacy = pd.merge(top_czas_oczekiwania, df_map, on='id_klienta').iloc[:, 1:]
najdluzej_czekajacy.iloc[:, ::-1]

cursor.execute(
    '''
    select q1.id_pracownika, sredni_zysk, Imie, Nazwisko from 
    (select id_pracownika,avg(kwota) as sredni_zysk from zlecenia group by id_pracownika order by avg(kwota) desc limit 10) as q1
    inner join
    (select * from pracownicy) as q2 on q1.id_pracownika=q2.id_pracownika;
    ''')
result = cursor.fetchall()
df = pd.DataFrame(result, columns=['id', 'sredni zysk', 'Imie', 'Nazwisko'])


df


cursor.execute(
    '''
    select q1.id_pracownika, pensja, Imie, Nazwisko from 
    (select distinct id_pracownika, pensja from spedycja.pensje) as q1
    inner join
    (select * from pracownicy) as q2 on q1.id_pracownika=q2.id_pracownika
    order by pensja desc;
    ''')

result = cursor.fetchall()
najlepiej_zarabiajacy = pd.DataFrame(result, columns=['id', 'Pensja', 'Imie', 'Nazwisko'])



podsumowanie = pd.merge(najlepiej_zarabiajacy[najlepiej_zarabiajacy['id'].isin(df['id'])], df, on='id')
podsumowanie['miejsce_w_pensjach'] = najlepiej_zarabiajacy[najlepiej_zarabiajacy['id'].isin(df['id'])].index.values



podsumowanie[['miejsce_w_pensjach', 'sredni zysk',
              'Pensja', 'Imie_x', 'Nazwisko_x']].sort_values('sredni zysk', ascending=False).reset_index(drop=True)


cursor.execute(
    '''
    select q1.id_pracownika, sredni_zysk, pensja, Imie, Nazwisko from 
    (select id_pracownika,avg(kwota) as sredni_zysk from zlecenia group by id_pracownika order by avg(kwota) desc) as q1
    inner join
    (select * from pracownicy) as q2 on q1.id_pracownika=q2.id_pracownika
    inner join
    (select distinct id_pracownika, pensja from spedycja.pensje) as q3 on q1.id_pracownika=q3.id_pracownika;
    ''')
result = cursor.fetchall()
df_wszyscy = pd.DataFrame(result, columns=['id', 'sredni zysk', 'pensja', 'Imie', 'Nazwisko'])


podsumowanie_inni = pd.merge(df_wszyscy[~df_wszyscy['id'].isin(df['id'])], df, on='id', how='left')


fig = go.Figure()
fig.add_trace(go.Scatter(x=podsumowanie['sredni zysk'], y=podsumowanie['Pensja'],
                         mode="markers", marker_color='red', name="Najlepsi pracownicy"))
fig.add_trace(go.Scatter(x=podsumowanie_inni['sredni zysk_x'], y=podsumowanie_inni['pensja'],
                         mode="markers", marker_color='blue', name="Inni pracownicy"))
fig.update_layout(autosize=True,
            width=900,
            height=600,
            title={
                'text': "Pensja vs generowany średni zysk",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 25}},
            xaxis_title={'text': "Średni zysk",
                         'font': {'size':20}},
            yaxis_title={'text': "Pensja",
                         'font': {'size':20}},
                 font=dict(size=16),
                                   yaxis=dict(range=[1000, 7500]),
                 xaxis=dict(range=[1000, 1300]))



save_html(fig, 'pensja_vs_generowany_zysk.html')


cursor.execute(
    '''
    select id_samochodu,sum(suma_przebiegow) from (select przebieg as suma_przebiegow, id_samochodu as id_samochodu from flota
    union
    select sum(dystans), id_samochodu from zlecenia group by id_samochodu) as eksploatacja group by id_samochodu order by sum(suma_przebiegow) desc limit 0,10;
    ''')

result = cursor.fetchall()
najbardziej_eksploatowane = pd.DataFrame(result, columns=['id', 'całkowity przebieg'])


najbardziej_eksploatowane  # lista najbardziej eksploatowanych samochodów


cursor.execute(
    '''
    SELECT YEAR(zlecenia_ze_spalaniem.data_realizacji) as rok, SUM(dystans/100*cena*spalanie) as 'calkowita koszty paliwa'
    FROM (SELECT zlecenia.id_samochodu as id_samochodu,
           dystans, data_realizacji, spalanie FROM zlecenia
    INNER JOIN
    (SELECT spalanie, id_samochodu FROM flota) flota
    ON zlecenia.id_samochodu = flota.id_samochodu) zlecenia_ze_spalaniem
    INNER JOIN ceny_paliwa ON ceny_paliwa.data=DATE(zlecenia_ze_spalaniem.data_realizacji)
    group by rok;
    ''')
result = cursor.fetchall()
df = pd.DataFrame(result, columns=['Rok', 'Koszt'])


cursor.execute(
    '''
    select * from ceny_paliwa;
    ''')
result = cursor.fetchall()
paliwo = pd.DataFrame(result, columns=['cena', 'Data'])


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=paliwo['Data'][:-51:52], y=df['Koszt'][:-1], name='Koszty na paliwo'))
fig.add_trace(go.Scatter(x=paliwo['Data'][:-51], y=paliwo['cena'], name="Cena paliwa"), secondary_y=True)
fig.update_layout(autosize=True,
            width=1200,
            height=600,
            title={
                'text': "Całkowity koszt paliwa vs ceny paliwa",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 25}},
            xaxis_title={'text': "Czas",
                         'font': {'size':20}},
            yaxis_title={'text': "Kwota wydana na paliwo",
                         'font': {'size':20}},
                 font=dict(size=16))
fig.update_yaxes(title_text="Cena paliwa", secondary_y=True)
#                  yaxis=dict(range=[0, 1.8*1e6]))


save_html(fig, 'koszt_na_paliwo_vs_cena.html')



cursor.execute(
    '''
    SELECT klienci.id_klienta as Id_klienta,
           Imie, Nazwisko, e_mail, telefon, miejscowosc,
           Zarobek_na_kliencie
    FROM klienci
    INNER JOIN
    (SELECT id_klienta, sum(kwota) as Zarobek_na_kliencie
    FROM zlecenia
    GROUP BY id_klienta) smallest_and_greatest
    ON smallest_and_greatest.id_klienta = klienci.id_klienta
    ORDER BY Zarobek_na_kliencie desc
    LIMIT 10;
    ''')
result = cursor.fetchall()
najlepsi_klienci = pd.DataFrame(result, columns=['Id', "Imię", "Nazwisko", "mail",
                                                 "telefon", "Miejscowość", "Zysk"])


najlepsi_klienci



fig = px.bar(x=najlepsi_klienci['Nazwisko'],
                         y=najlepsi_klienci['Zysk'])


fig.update_layout(title={
    'text': f'Najbardziej zyskowni klienci',
'y': 0.95,
'x':0.5},
width=900,
height=600,
titlefont=dict(size=25),
                 font=dict(size=16),
xaxis_title='',
                 yaxis_title='Liczba pracowników')
fig.show()



save_html(fig, 'zyskowni_klienci.html')
s

MySQLConnector.close_connection(connection)

