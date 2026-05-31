"""
Projet IoT & IA - Détection intelligente d'incendie
Membre 1 : Simulation des capteurs et publication MQTT

Version corrigée :
- Si le broker MQTT public est inaccessible, le script ne s'arrête plus.
- Il passe automatiquement en mode hors ligne et continue à générer les messages JSON.
- Si paho-mqtt n'est pas installé, le mode hors ligne fonctionne quand même.

Cette partie représente la couche objets / edge du projet.
Elle fournit au Membre 2 un topic MQTT et un format JSON stable pour Node-RED.
"""

import argparse
import json
import random
import socket
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None


CONFIG_PATH = Path(__file__).with_name("config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "broker_host": "localhost",
    "broker_port": 1883,
    "mqtt_topic": "iot/fire/sensor/data",
    "device_id": "fire_sensor_01",
    "location": "Salle_1",
    "publish_interval_seconds": 3,
    "offline_if_mqtt_unreachable": True,
    "scenario_weights": {
        "normal": 0.65,
        "suspect": 0.25,
        "danger": 0.10
    }
}


def load_config() -> Dict[str, Any]:
    """Load simulator configuration from config.json and merge it with defaults."""
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG.copy()

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        user_config = json.load(file)

    config = DEFAULT_CONFIG.copy()
    config.update(user_config)

    if "scenario_weights" in user_config:
        merged_weights = DEFAULT_CONFIG["scenario_weights"].copy()
        merged_weights.update(user_config["scenario_weights"])
        config["scenario_weights"] = merged_weights

    return config


def generate_normal_data() -> Dict[str, Any]:
    return {
        "temperature": round(random.uniform(20, 35), 2),
        "smoke": random.randint(20, 200),
        "gas": random.randint(50, 250),
        "humidity": random.randint(45, 65)
    }


def generate_suspect_data() -> Dict[str, Any]:
    return {
        "temperature": round(random.uniform(40, 60), 2),
        "smoke": random.randint(250, 600),
        "gas": random.randint(300, 550),
        "humidity": random.randint(30, 45)
    }


def generate_danger_data() -> Dict[str, Any]:
    return {
        "temperature": round(random.uniform(65, 90), 2),
        "smoke": random.randint(650, 1000),
        "gas": random.randint(600, 900),
        "humidity": random.randint(15, 30)
    }


def choose_scenario(config: Dict[str, Any]) -> str:
    weights = config.get("scenario_weights", DEFAULT_CONFIG["scenario_weights"])
    scenarios = ["normal", "suspect", "danger"]
    probabilities = [
        float(weights.get("normal", 0.65)),
        float(weights.get("suspect", 0.25)),
        float(weights.get("danger", 0.10))
    ]
    return random.choices(scenarios, weights=probabilities, k=1)[0]


def generate_sensor_message(config: Dict[str, Any]) -> Dict[str, Any]:
    scenario = choose_scenario(config)

    if scenario == "normal":
        values = generate_normal_data()
    elif scenario == "suspect":
        values = generate_suspect_data()
    else:
        values = generate_danger_data()

    return {
        "device_id": config["device_id"],
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "temperature": values["temperature"],
        "smoke": values["smoke"],
        "gas": values["gas"],
        "humidity": values["humidity"],
        "location": config["location"],
        "scenario": scenario
    }


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connexion MQTT réussie.")
    else:
        print(f"Connexion MQTT échouée. Code : {reason_code}")


def create_mqtt_client():
    if mqtt is None:
        raise RuntimeError("Le package paho-mqtt n'est pas installé.")

    # Compatible with paho-mqtt 2.x and safe for current versions.
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    except Exception:
        client = mqtt.Client()

    client.on_connect = on_connect
    return client


def connect_mqtt(config: Dict[str, Any]) -> Optional[Any]:
    """Try to connect to MQTT. Return client if OK, otherwise return None."""
    if mqtt is None:
        print("paho-mqtt n'est pas installé : passage en mode hors ligne.")
        return None

    broker_host = config["broker_host"]
    broker_port = int(config["broker_port"])

    try:
        client = create_mqtt_client()
        print(f"Connexion au broker MQTT : {broker_host}:{broker_port}")
        client.connect(broker_host, broker_port)
        client.loop_start()
        return client
    except (OSError, socket.gaierror, TimeoutError, RuntimeError) as exc:
        if config.get("offline_if_mqtt_unreachable", True):
            print(f"MQTT inaccessible ({exc}) : passage en mode hors ligne.")
            return None
        raise


def publish_or_print(client: Optional[Any], topic: str, payload: str) -> None:
    """Publish payload if MQTT is available, otherwise print only."""
    if client is None:
        print("Message généré (mode hors ligne) :")
        print(payload)
        return

    result = client.publish(topic, payload)
    result.wait_for_publish()
    print("Message publié :")
    print(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulateur de capteurs incendie - Membre 1")
    parser.add_argument("--offline", action="store_true", help="Forcer le mode hors ligne sans connexion MQTT")
    parser.add_argument("--once", action="store_true", help="Générer un seul message puis arrêter")
    parser.add_argument("--interval", type=int, default=None, help="Intervalle entre deux messages en secondes")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()

    if args.interval is not None:
        config["publish_interval_seconds"] = args.interval

    broker_host = config["broker_host"]
    broker_port = int(config["broker_port"])
    mqtt_topic = config["mqtt_topic"]
    publish_interval = int(config["publish_interval_seconds"])

    print("Démarrage du simulateur IoT - Membre 1")
    print(f"Broker MQTT : {broker_host}:{broker_port}")
    print(f"Topic MQTT  : {mqtt_topic}")
    print(f"Intervalle  : {publish_interval} secondes")
    print("-" * 70)

    client = None if args.offline else connect_mqtt(config)

    if args.offline:
        print("Mode hors ligne forcé : aucune connexion MQTT ne sera utilisée.")

    try:
        while True:
            message = generate_sensor_message(config)
            payload = json.dumps(message, ensure_ascii=False)
            publish_or_print(client, mqtt_topic, payload)
            print("-" * 70)

            if args.once:
                break

            time.sleep(publish_interval)

    except KeyboardInterrupt:
        print("Arrêt manuel du simulateur.")
    finally:
        if client is not None:
            client.loop_stop()
            client.disconnect()
            print("Connexion MQTT fermée.")
        else:
            print("Simulateur arrêté en mode hors ligne.")


if __name__ == "__main__":
    main()
