#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ========== WiFi ==========
const char* ssid = "Thunderbird2.4G";
const char* password = "jayden666";

// ========== MQTT ==========
const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);

// ========== DHT ==========
#define DHTPIN 23
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// ========== MQ-2 ==========
#define MQ2_PIN 34

// ========== HC-SR04 ==========
#define TRIG_PIN 5
#define ECHO_PIN 18

// ========== OLED ==========
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ---------- WiFi ----------
void setup_wifi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

// ---------- MQTT reconnect ----------
void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP32Client123")) {
      Serial.println("MQTT Connected");
    } else {
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  dht.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Wire.begin(21, 22);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED FAIL");
    while (false);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);

  setup_wifi();
  client.setServer(mqtt_server, 1883);

  Serial.println("System Ready");
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // ===== Sensors =====
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int gas = analogRead(MQ2_PIN);

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  float distance = duration * 0.034 / 2;

  // ===== JSON =====
  String payload =
    String("{\"temp\":") + temp +
    ",\"hum\":" + hum +
    ",\"gas\":" + gas +
    ",\"dist\":" + distance + "}";

  client.publish("esp32/sensor", payload.c_str());

  Serial.println(payload);

  // ===== OLED DISPLAY =====
  display.clearDisplay();

  display.setCursor(0, 0);
  display.print("Temp: "); display.print(temp); display.println(" C");

  display.setCursor(0, 16);
  display.print("Hum : "); display.print(hum); display.println(" %");

  display.setCursor(0, 32);
  display.print("Gas : "); display.print(gas);

  display.setCursor(0, 48);
  display.print("Dist: "); display.print(distance); display.println(" cm");

  display.display();

  delay(2000);
}