DROP DATABASE IF EXISTS spedycja;
CREATE DATABASE IF NOT EXISTS spedycja;
USE spedycja;

SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';

DROP TABLE IF EXISTS pracownicy,
                     flota,
                     klienci,
                     zlecenia, 
                     pensje,
					 ceny_paliwa, 
					 oplaty;


CREATE TABLE pracownicy (
    id_pracownika      INT             NOT NULL,
    Imie               VARCHAR(30)     NOT NULL,
    Nazwisko           VARCHAR(50)     NOT NULL,
    PRIMARY KEY (id_pracownika)
);

CREATE TABLE flota (
    id_samochodu     INT            NOT NULL,
    waga_samochodu   DOUBLE         NOT NULL,
    przebieg         DOUBLE         NOT NULL,
    spalanie         DOUBLE         NOT NULL,
    max_zaladunek    DOUBLE         NOT NULL,
    typ_samochodu    VARCHAR(30)    NOT NULL,
    PRIMARY KEY (id_samochodu)
);


CREATE TABLE klienci (
   id_klienta       INT             NOT NULL,
   Imie             VARCHAR(30)     NOT NULL,
   Nazwisko         VARCHAR(50)     NOT NULL,
   e_mail           VARCHAR(80)     NOT NULL,
   telefon          VARCHAR(16)     NOT NULL,
   miejscowosc      VARCHAR(50)     NOT NULL,
   PRIMARY KEY (id_klienta)
); 

CREATE TABLE zlecenia (
    id_zlecenia      INT             NOT NULL,
    id_pracownika    INT             NOT NULL,
    id_samochodu     INT             NOT NULL,
    id_klienta       INT             NOT NULL,
    dystans          DOUBLE          NOT NULL,
    data_przyjecia   DATETIME        NOT NULL,
    data_realizacji  DATETIME        NOT NULL,
    kwota            DOUBLE          NOT NULL,
    FOREIGN KEY (id_pracownika)  REFERENCES   pracownicy   (id_pracownika)  ON DELETE CASCADE,
    FOREIGN KEY (id_samochodu)   REFERENCES   flota   (id_samochodu)   ON DELETE CASCADE,
    FOREIGN KEY (id_klienta)     REFERENCES   klienci   (id_klienta)     ON DELETE CASCADE,
    PRIMARY KEY (id_zlecenia)
);

CREATE TABLE pensje (
    id_pracownika    INT           NOT NULL,
    pensja           VARCHAR(50)   NOT NULL,
    od_daty          DATE          NOT NULL,
    do_daty          DATE          NOT NULL,
    FOREIGN KEY (id_pracownika)  REFERENCES   pracownicy   (id_pracownika)  ON DELETE CASCADE
);

CREATE TABLE ceny_paliwa (
    cena      DOUBLE     NOT NULL,
    data      DATE       NOT NULL,
    PRIMARY KEY (data)
); 

CREATE TABLE oplaty (
    rodzaj_oplaty      VARCHAR(30)     NOT NULL,
    kwota_transakcji   DOUBLE          NOT NULL,
    data               DATE            NOT NULL,
    PRIMARY KEY (data)
);

CREATE TABLE akcje (
    data               DATE            NOT NULL,
    cena               DOUBLE          NOT NULL,
    emitowana_ilosc    INT             NOT NULL,
    PRIMARY KEY (data)
); 

CREATE TABLE dlugi (
    data               DATE            NOT NULL,
    kwota              DOUBLE          NOT NULL,
    PRIMARY KEY (data)
); 
