# projekt-bazy-danych
Baza danych firmy spedycyjnej

Aby utworzyć oraz zapełnić danymi bazę danych należy:
1. Wykonać skrypt `run_process.sh`, który wykona:
  * instalację potrzebnych pakietów przy pomocy `pip install -r requirements.txt` ;
  * budowę schematu bazy danych przy pomocy pliku `generate_schema.py`
  * wygenerowanie danych do bazy przy pomocy `db_populate.py`
2. Analizę danych znajdujących się w bazie zawiera notebook `data-analysis-notebook.ipynb`.
