import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import logging
import os
import socket

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Comments:
    def __init__(self, file_path):
        self.file_path = file_path
        self.comments = self.load_comments()

    def load_comments(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            comments = file.readlines()

        comments = list(set(comments))  # Supprime les doublons
        return [self.filter_bmp_chars(comment.strip()) for comment in comments if comment.strip()]

    def get_random_comment(self):
        return random.choice(self.comments)

    def filter_bmp_chars(self, text):
        # Garder uniquement les caractères dans le BMP
        return ''.join(c for c in text if c <= '\uFFFF')

def comment_on_post(driver, post_url, comment):
    try:
        driver.get(post_url)
        time.sleep(3)  # Attendre que la page charge complètement
        comment_box = driver.find_element(By.XPATH, '//textarea[@aria-label="Ajouter un commentaire..."]')
        comment_box.click()
        comment_box = driver.find_element(By.XPATH, '//textarea[@aria-label="Ajouter un commentaire..."]')
        comment_box.send_keys(comment)
        comment_box.send_keys(Keys.RETURN)
        time.sleep(2)  # Attendre que le commentaire soit posté
        logging.info(f"Commentaire posté: {comment}")
    except Exception as e:
        logging.error(f"Erreur lors du commentaire: {str(e)}")

def send_notification(message):
    try:
        # Configurer ici l'adresse IP de votre téléphone ou un service de notification
        host = "192.168.1.51"  # exemple d'IP locale
        port = 37241  # Port arbitraire pour l'exemple

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(message.encode(), (host, port))
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi de la notification: {str(e)}")

def main():
    start_time = time.time()
    
    # Options pour le navigateur
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialiser le driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Connexion à Instagram
    driver.get("https://www.instagram.com/accounts/login/")

    while True:
        try:
            driver.find_element(By.XPATH, '//button[text()="Autoriser tous les cookies"]').click()
            break
        except:
            time.sleep(1)
    logging.info("Bouton 'Autoriser tous les cookies' cliqué")

    # Entrer les informations de connexion
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    # Importer les identifiants depuis un fichier json
    with open('id.json', 'r') as file:
        credentials = json.load(file)

    identifiant = credentials['identifiant']
    password = credentials['password']
    username_input.send_keys(identifiant)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)  # Attendre la connexion

    # URL du post Instagram à commenter
    post_url = "https://www.instagram.com/p/C8kkWOBNV0g/"

    # Variables de contrôle pour respecter les limites d'Instagram
    max_comments_per_hour = 30
    max_comments_per_day = 200
    comments_posted_today = 0

    while comments_posted_today < max_comments_per_day:
        for _ in range(max_comments_per_hour):
            if comments_posted_today >= max_comments_per_day:
                break
            # Charger les commentaires dynamiquement
            comments = Comments('comments.txt')
            comment = comments.get_random_comment()
            comment_on_post(driver, post_url, comment)
            comments_posted_today += 1
            send_notification(f"Commentaire posté: {comment}")
            time.sleep(120)  # Pause de 2 minutes entre chaque commentaire pour éviter le spam

        # Pause de 1 heure après avoir posté 30 commentaires
        time.sleep(3600)

    driver.quit()
    end_time = time.time()
    elapsed_time = end_time - start_time
    send_notification(f"Script arrêté. Durée de fonctionnement: {elapsed_time / 60:.2f} minutes")

if __name__ == "__main__":
    main()
