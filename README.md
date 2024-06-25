# AutoPoster

Voici un script conçu pour automatiser la publication de commentaires sous le fameux post de NasDas et Hachemi.

## Prérequis

- Python 3.x
- Selenium
- ChromeDriver

## Installation

1. Clonez le dépôt

```bash
git clone https://github.com/votreUsername/AutoPoster.git
```

2. Installez les dépendances

```bash
pip install -r requirements.txt
```

3. Téléchargez le ChromeDriver correspondant à votre version de Chrome [ici](https://sites.google.com/a/chromium.org/chromedriver/downloads)

4. Décompressez le fichier téléchargé et déplacez le fichier `chromedriver` dans le dossier `AutoPoster`

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