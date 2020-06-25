# projekt-bazy-danych
###Baza danych firmy spedycyjnej

W celu wygenerowania bazy, najpierw należy upewnić się, czy zainstalowane są wszystkie potrzebne biblioteki języka Python. Lista niezbędnych bibliotek (wraz z ich wersjami) znajduje się w pliku requirements.txt. Możemy je zainstalować w łatwy sposób przy użyciu systemu pip, za pomocą komendy:


    pip install -r requirements.txt


Jeżeli wszystkie potrzebne biblioteki są zainstalowane, to możemy wygenerować raport wynikowy.
W raporcie znajduje się kod tworzący schemat bazy oraz wykonujący skryptowe wypełnianie tabel bazy danych.
Program potrzebuje kilku informacji, które musimy podać, edytując plik `projekt-bazy-danych/project/database-info/database_credentials.xlsx`.
Informacje te to:

* nazwa hostu;
* nazwa użytkownika;
* hasło do bazy danych (w przypadku braku zostawiamy puste).

Po uzupełnieniu odpowiednich informacji możemy wygenerować raport wynikowy
używając następującego polecenia w folderze `projekt-bazy-danych/project/raport`:
 
    stitch raport.md -o raport_wynikowy.pdf
    
Polecenie to wygeneruje końcowy raport z analizą. W środku raportu znajduje się kod, który:

* zbuduje schemat bazy danych przy pomocy skryptu `generate_schema.py`;
* wygeneruje dane do bazy przy pomocy `db_populate.py`;
* przeprowadzi analizę danych do 3. części projektu.


