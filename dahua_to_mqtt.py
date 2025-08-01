import os
import requests
import paho.mqtt.client as mqtt
import time
import logging

# --- Configuration via variables d'environnement ---
DAHUA_HOST = os.getenv("DAHUA_HOST")
DAHUA_USERNAME = os.getenv("DAHUA_USERNAME")
DAHUA_PASSWORD = os.getenv("DAHUA_PASSWORD")
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "DahuaVTO")

# --- Logger ---
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

# --- MQTT ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("✅ Connecté au broker MQTT")
    else:
        logging.error(f"❌ Erreur de connexion MQTT (code {rc})")

mqtt_client = mqtt.Client()
if MQTT_USERNAME and MQTT_PASSWORD:
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

# --- Dahua Event Stream ---
def connect_dahua():
    url = f"http://{DAHUA_HOST}/cgi-bin/eventManager.cgi?action=attach&codes=[All]"
    logging.info(f"Connexion au flux Dahua: {url}")
    with requests.get(url, auth=(DAHUA_USERNAME, DAHUA_PASSWORD), stream=True, timeout=10) as r:
        if r.status_code == 200:
            logging.info("✅ Connecté au flux d'événements Dahua. En attente...")
            for line in r.iter_lines():
                if line:
                    decoded = line.decode("utf-8", errors="ignore")
                    logging.info(f"[EVENT] {decoded}")
                    mqtt_client.publish(f"{MQTT_TOPIC_PREFIX}/events", decoded)
        else:
            logging.error(f"❌ Erreur Dahua: {r.status_code}")

# --- Boucle principale ---
while True:
    try:
        connect_dahua()
    except Exception as e:
        logging.error(f"Erreur: {e}. Reconnexion dans 10s...")
        time.sleep(10)
