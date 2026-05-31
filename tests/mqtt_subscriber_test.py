"""
Test de réception MQTT pour le Membre 1.
Utilisation : python tests/mqtt_subscriber_test.py

Important : ce test nécessite une connexion au broker MQTT configuré.
Si votre environnement n'a pas accès à Internet, utilisez un broker Mosquitto local.
"""

import json
from pathlib import Path

import paho.mqtt.client as mqtt

CONFIG_PATH = Path(__file__).resolve().parents[1] / "simulator" / "config.json"


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def on_connect(client, userdata, flags, reason_code, properties=None):
    config = userdata
    print(f"Connecté au broker. Code : {reason_code}")
    client.subscribe(config["mqtt_topic"])
    print(f"Abonnement au topic : {config['mqtt_topic']}")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print("Message reçu :")
    print(payload)
    try:
        data = json.loads(payload)
        required_fields = ["device_id", "timestamp", "temperature", "smoke", "gas", "humidity", "location", "scenario"]
        missing = [field for field in required_fields if field not in data]
        if missing:
            print(f"Champs manquants : {missing}")
        else:
            print("Format JSON valide pour le Membre 2.")
    except json.JSONDecodeError:
        print("Payload non JSON.")
    print("-" * 70)


def main():
    config = load_config()
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=config)
    except Exception:
        client = mqtt.Client(userdata=config)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config["broker_host"], int(config["broker_port"]), 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
