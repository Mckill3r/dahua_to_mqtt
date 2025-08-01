# Dahua MQTT Bridge

Un conteneur Docker qui connecte un interphone vidéo **Dahua VTO** à un broker **MQTT**, idéal pour une intégration avec **Home Assistant** ou tout système domotique compatible MQTT.

## 🚀 Fonctionnalités
- Écoute en temps réel du flux `eventManager.cgi` des interphones Dahua.
- Publication des événements (appels, ouverture de porte, détection mouvement, etc.) sur des topics MQTT.
- Commande d'ouverture de porte via MQTT (`DahuaVTO/Command/Open`).
- Déploiement simple via **Docker Compose**.

## 🛠 Prérequis
- Un **interphone Dahua VTO** compatible API HTTP activée.
- Un broker **MQTT** fonctionnel (Mosquitto, EMQX, etc.).
- **Docker** et **Docker Compose** installés.

## 🔧 Installation
1. **Cloner le projet :**
   ```bash
   git clone https://github.com/<votre-compte>/dahua-mqtt.git
   cd dahua-mqtt
   ```
2. **Modifier les variables d'environnement dans `docker-compose.yml` :**  
   Avant de démarrer, éditez `docker-compose.yml` et adaptez les valeurs suivantes :
   ```yaml
   environment:
     - DAHUA_HOST=192.168.x.x      # IP du VTO Dahua
     - DAHUA_USERNAME=admin        # Identifiant Dahua
     - DAHUA_PASSWORD=motdepasse   # Mot de passe Dahua
     - MQTT_HOST=192.168.x.x       # IP du broker MQTT
     - MQTT_PORT=1883              # Port MQTT (par défaut 1883)
     - MQTT_USERNAME=mon_mqtt_user # (optionnel) Identifiant MQTT
     - MQTT_PASSWORD=mon_mqtt_pass # (optionnel) Mot de passe MQTT
     - MQTT_TOPIC_PREFIX=DahuaVTO  # Préfixe des topics MQTT
   ```
3. **Lancer le conteneur :**
   ```bash
   docker-compose up -d --build
   ```
4. **Vérifier les logs :**
   ```bash
   docker logs -f dahua_to_mqtt
   ```

## 📡 Utilisation MQTT
- **Événements :**  
  Chaque événement du VTO est publié sur un topic du type :
  ```
  DahuaVTO/AccessControl
  DahuaVTO/Invite
  DahuaVTO/VideoMotion
  ```
  avec un payload JSON détaillé.

- **Commande ouverture de porte :**  
  Pour déclencher l'ouverture de la porte :
  ```
  Topic : DahuaVTO/Command/Open
  Payload : (vide)
  ```

## 🏠 Intégration Home Assistant
Ajouter un `binary_sensor` ou une automatisation MQTT :
```yaml
automation:
  - alias: Notification appel VTO
    trigger:
      - platform: mqtt
        topic: "DahuaVTO/Invite"
    action:
      - service: notify.mobile_app
        data:
          message: "Appel entrant sur le VTO Dahua"
```

## 📜 Licence
Ce projet est sous licence **MIT** – libre utilisation et modification.

## 🏷 Tags
`mqtt`, `dahua`, `vto`, `home-assistant`, `docker`, `iot`, `smart-home`
