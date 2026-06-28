import paho.mqtt.client as mqtt
import json

BROKER = "broker.hivemq.com"
PORT = 1883

# ===== CONNECT =====
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to HiveMQ!")

    client.subscribe("esp32/sensor")
    client.subscribe("ai/person")   # 🔥 YOLO
    print("Subscribed to topics")
   
# ===== MESSAGE =====
def on_message(client, userdata, msg):

    topic = msg.topic
    payload = msg.payload.decode()

    # ---------------- ESP32 sensor ----------------
    if topic == "esp32/sensor":
        try:
            data = json.loads(payload)

            print("\n---------------------------")
            print("📡 ESP32 DATA")
            print("Temperature:", data.get("temp", "N/A"))
            print("Humidity:", data.get("hum", "N/A"))
            print("Gas:", data.get("gas", "N/A"))
            print("Distance:", data.get("dist", "N/A"))
            print("Status:", data.get("status", "N/A"))

        except:
            print("⚠️ Invalid sensor JSON:", payload)


# ===== MQTT CLIENT =====
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

client.loop_forever()