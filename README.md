# Pràctica 1 - Tipologia i Cicle de Vida de les Dades  
**Assignatura:** M2.951  
**Semestre:** 0000-1    
**Data:** 29-10-2024  

## Autors
- Antoni Vives Cabaleiro - tvivescabaleiro@uoc.edu  
- Julen Antonio Echevarria - jantonioe@uoc.edu  

## Lloc web elegit
[https://www.linkedin.com](https://www.linkedin.com)

## Enllaç DOI Zenodo

https://zenodo.org/records/14035759


## Descripció del repositori
Aquest repositori conté un scraper per extreure informació de feines a LinkedIn. S'utilitzen les credencials personals per a iniciar sessió i extreure informació d'ofertes laborals segons el títol especificat com a paràmetre.

- **`PR_1/source/main.py`**: Executa el scraper a partir dels paràmetres introduïts (`Títol del treball` i `Número de cerques`).
- **`PR_1/source/linkedin_scraper.py`**: Conté la lògica del scraper, incloent-hi el login, la cerca de feines, i l'extracció d'informació.
- **`PR_1/source/credentials.py`**: Conté les credencials (nom d'usuari i contrasenya) per a LinkedIn.
- **`PR_1/source/requirements.txt`**: Llista de paquets Python utilitzats (Python 3.10).
- **`PR_1/dataset/linkedin_jobs.csv`**: Fitxer CSV on es guarden les dades recollides pel scraper.

## Instruccions
Per utilitzar el codi generat, segueix els passos següents:

1. Clona el repositori i instal·la els paquets necessaris:
   ```bash
   git clone <repositori>
   cd <repositori>
   pip install -r requirements.txt
   ```
2. Executa el scraper des de la línia de comandes:
   ```bash
   python main.py 'Títol del treball' 'Número de cerques'
   ```
Exemple:

```bash
    python main.py 'Data Scientist' 50
   ```
