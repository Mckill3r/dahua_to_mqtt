import os
import requests
from requests.auth import HTTPDigestAuth
import paho.mqtt.client as mqtt
import json
import warnings

# --- SUPPRIMER LES WARNINGS ---
warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- CONFIGURATION VIA VARIABLES D'ENVIRONNEMENT ---
VTO_IP = os.getenv("DAHUA_HOST", "")
VTO_USER = os.getenv("DAHUA_USERNAME", "admin")
VTO_PASS = os.getenv("DAHUA_PASSWORD", "password")

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USERNAME", "")
MQTT_PASS = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "DahuaVTO")

# --- MAPPING DES ÉVÉNEMENTS ---
EVENT_LABELS = {
    "CallNoAnswered": "Appel non répondu",
    "Invite": "Appel entrant",
    "CallHangUp": "Fin d'appel",
    "CallAnswer": "Appel répondu",
    "AccessControl": "Ouverture de porte",
    "VideoMotion": "Détection de mouvement",
    "AlarmLocal": "Alarme locale",
    "FingerPrintCheck": "Vérification empreinte",
    "SIPRegisterResult": "Enregistrement SIP",
    "RtspSessionDisconnect": "Déconnexion RTSP",
    "TimeChange": "Changement de l'heure",
    "NTPAdjustTime": "Heure ajustée par NTP",
}

# --- INITIALISATION MQTT ---
mqtt_client = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)
if MQTT_USER and MQTT_PASS:
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

# --- CALLBACK POUR COMMANDES MQTT ---
def on_mqtt_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MQTT] Commande reçue : {topic} -> {payload}")
    if topic == f"{MQTT_TOPIC_PREFIX}/Command/Open":
        open_door()

mqtt_client.subscribe(f"{MQTT_TOPIC_PREFIX}/Command/Open")
mqtt_client.on_message = on_mqtt_message

# --- FONCTION POUR OUVRIR LA PORTE ---
def open_door():
    print("[ACTION] Ouverture de la porte demandée via MQTT...")
    url_open = f"http://{VTO_IP}/cgi-bin/accessControl.cgi?action=openDoor&channel=1&UserID=101&Type=Remote"
    resp = requests.get(url_open, auth=HTTPDigestAuth(VTO_USER, VTO_PASS))
    if resp.status_code == 200:
        print("[ACTION] Porte ouverte avec succès.")
    else:
        print(f"[ERREUR] Impossible d'ouvrir la porte. Code: {resp.status_code}")

# --- FONCTION DE PUBLICATION MQTT ---
def publish_event(event_type, data):
    topic = f"{MQTT_TOPIC_PREFIX}/{event_type}"
    mqtt_client.publish(topic, json.dumps(data))
    print(f"[MQTT] Publié sur {topic}: {data}")

# --- LIRE LE FLUX D'ÉVÉNEMENTS DAHUA ---
def listen_events():
    url = f"http://{VTO_IP}/cgi-bin/eventManager.cgi?action=attach&codes=%5BAll%5D"
    print(f"[INFO] Connexion au flux d'événements Dahua ({url})...")

    with requests.get(url, auth=HTTPDigestAuth(VTO_USER, VTO_PASS), stream=True) as resp:
        if resp.status_code == 200:
            print("[INFO] Connecté au flux d'événements. En attente...")
            for line in resp.iter_lines():
                if line:
                    decoded = line.decode(errors="ignore")
                    if decoded.startswith("Code="):
                        print(f"[EVENT] Brut : {decoded}")

                        # Extraire Code et Action
                        parts = decoded.split(";", 2)
                        code = parts[0].split("=")[1]
                        action = parts[1].split("=")[1] if len(parts) > 1 else "N/A"
                        label = EVENT_LABELS.get(code, code)

                        # Construire payload enrichi
                        event_payload = {
                            "event": code,
                            "label": label,
                            "action": action,
                            "raw": decoded
                        }

                        # Publier sur topic spécifique
                        publish_event(code, event_payload)
        else:
            print(f"[ERREUR] Impossible de se connecter au flux : {resp.status_code}")

if __name__ == "__main__":
    listen_events()
