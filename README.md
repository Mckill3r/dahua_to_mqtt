# Dahua MQTT Bridge

Un conteneur Docker qui connecte les interphones Dahua VTO et publie leurs événements sur MQTT, idéal pour une intégration avec Home Assistant.

## 🚀 Fonctionnalités
- Connexion directe au flux `eventManager.cgi` de Dahua.
- Publication des événements sur MQTT.
- Commande d'ouverture de porte via MQTT (`DahuaVTO/Command/Open`).

## 🛠 Prérequis
- Docker et Docker Compose
- Broker MQTT (ex: Mosquitto)
- Un interphone Dahua compatible HTTP API activée

## 🔧 Installation
```bash
git clone https://github.com/Mckill3r/dahua_to_mqtt
cd dahua-mqtt
docker-compose up -d --build
```

## ⚙ Variables d'environnement
- `DAHUA_HOST`: IP du VTO Dahua
- `DAHUA_USERNAME` / `DAHUA_PASSWORD`: identifiants Dahua
- `MQTT_HOST` / `MQTT_PORT`: broker MQTT
- `MQTT_USERNAME` / `MQTT_PASSWORD`: identifiants MQTT
- `MQTT_TOPIC_PREFIX`: préfixe pour les topics (par défaut: DahuaVTO)

## 🏠 Intégration Home Assistant
Créer un `binary_sensor` MQTT basé sur les événements, ou utiliser des automatisations pour notifications.

## 📜 Licence
Projet sous licence MIT. Contributions bienvenues !
