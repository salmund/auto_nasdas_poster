# AutoPoster

Voici un script conçu pour automatiser la publication de commentaires sous le fameux post de NasDas et Hachemi.

## Prérequis

- Python 3.x
- Selenium
- ChromeDriver

## Installation

1. Clonez le dépôt

```bash
git clone https://github.com/salmund/auto_nasdas_poster
```

2. Installez les dépendances

```bash
pip install -r requirements.txt
```

## Utilisation

1. Ouvrez le fichier `id.json` et modifiez-le avec vos identifiants Instagram

```json
{
    "identifiant": "votreUsername",
    "password": "votreMotDePasse"
}
```

2. Lancez le script

```bash
python autoposter.py
```
