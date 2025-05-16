# README

Test access to [API-SNCF](https://numerique.sncf.com/startup/api/) using python.

## Check static typing with mypy

`pipenv run mypy get_data.py`

## Database

Le schéma de la base SQLite alimentée par `get_data.py` est donné dans `db_schema.sql`. 

Le nom du fichier de la base SQLite doit être renseigné dans le fichier `.env`.


## Token API SNCF

Le token de l'API SNCF doit être renseigné dans le fichier `.env`.

## Utilisation

```bash
$ pipenv run python3 get_data.py <command> -m maxpages [-e] dummyvalue
```

`<command>` peut être :

- `get-stop-points`,
- `get-stop-areas`,
- `get-networks`,
- `get-lines`

`maxpages` : nb max de pages à récupérer. (0 = toutes les pages)

`-e` : si présent, renseigner la base SQLite sinon faire uniquement un essai à vide.

(dummyvalue peut être n'importe quelle valeur - il s'agit d'une provision de paramètre).
 