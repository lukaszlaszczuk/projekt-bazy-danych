# projekt-bazy-danych
Baza danych firmy spedycyjnej

Aby utworzyć oraz zapełnić danymi bazę danych należy:
1. Uruchomić skrypt `run_process.sh` za pomocą `bash run_process.sh`, który wykona:
  * instalację potrzebnych pakietów przy pomocy `pip install -r requirements.txt` ;
  * budowę schematu bazy danych przy pomocy pliku `generate_schema.py`
  * wygenerowanie danych do bazy przy pomocy `db_populate.py`
2. Analizę danych znajdujących się w bazie zawiera notebook `data-analysis-notebook.ipynb`.

**Uwaga** Wykresy znajdujące się w notebooku zostały wygenerowane przy pomocy biblioteki plotly i nie będą widoczne zaraz po otworzeniu pliku. Aby móc je zobaczyć należy wykonać kod znajdujący się w notebooku przy pomocy `Run All`. Wykresy te znajdują się w folderze `images`
