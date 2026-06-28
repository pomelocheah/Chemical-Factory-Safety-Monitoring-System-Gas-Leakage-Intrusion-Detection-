#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ========== WiFi ==========
const char* ssid = "HONOR X9d";
const char* password = "Wong0326@";

// ========== MQTT ==========
const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);

// ========== YOLO ==========
bool yoloPerson = false;
bool yoloActive = false;

// ========== DHT ==========
#define DHTPIN 23
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// ========== MQ-2 ==========
#define MQ2_PIN 34
const int GAS_THRESHOLD = 2500;

// ========== HC-SR04 ==========
#define TRIG_PIN 5
#define ECHO_PIN 18

// ========== Buzzer ==========
#define BUZZER_PIN 25   // LOW active

// ========== LED ==========
#define RED_LED 26
#define YELLOW_LED 27
#define GREEN_LED 14

// ========== OLED ==========
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ================= WIFI =================
void setup_wifi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

// ================= MQTT CALLBACK =================
void callback(char* topic, byte* payload, unsigned int length) {
  String msg = "";

  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  if (String(topic) == "ai/person") {
    yoloPerson = (msg == "1");
    Serial.print("YOLO Person: ");
    Serial.println(yoloPerson);
  }
  if (String(topic) == "ai/yolo/status")
{
    if (msg == "on")
        yoloActive = true;
    else
        yoloActive = false;

    Serial.print("YOLO Status: ");
    Serial.println(yoloActive ? "ON" : "OFF");
}
}


// ================= MQTT RECONNECT =================
void reconnect() {
  while (!client.connected()) {
    Serial.println("Connecting MQTT...");

    if (client.connect("ESP32Client123")) {
      Serial.println("MQTT Connected");

      client.subscribe("ai/person");
    } else {
      Serial.print("Failed, rc=");
      Serial.println(client.state());
      delay(2000);
    }
  }
  client.subscribe("ai/person");
client.subscribe("ai/yolo/status");
}

// ================= SETUP =================
void setup() {
  Serial.begin(115200);

  dht.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  digitalWrite(BUZZER_PIN, HIGH); // OFF (LOW active)

  Wire.begin(21, 22);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED FAIL");
    while (true);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);

  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  reconnect();
}

// ================= LOOP =================
void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  // ===== Sensors =====
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  int gas = analogRead(MQ2_PIN);
  bool gasDetected = (gas > GAS_THRESHOLD);

  // HC-SR04
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  float distance = duration * 0.034 / 2;

  bool distanceDetected = (distance > 0 && distance < 30);

  // ===== HUMAN LOGIC (YOLO + distance) =====
  bool humanDetected = yoloPerson && distanceDetected;

  // ===== STATUS =====
  String status;

  if (gasDetected && humanDetected)
    status = "danger";
  else if (gasDetected || humanDetected)
    status = "warning";
  else
    status = "safe";

  // ===== MQTT JSON =====
  String payload =
    String("{\"temp\":") + temp +
    ",\"hum\":" + hum +
    ",\"gas\":" + gas +
    ",\"dist\":" + distance +
    ",\"status\":\"" + status + "\"}";

  client.publish("esp32/sensor", payload.c_str());

  Serial.println(payload);

  // ===== LED + BUZZER =====
  if (status == "danger") {
    digitalWrite(RED_LED, HIGH);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  }
  else if (status == "warning") {
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  }
  else {
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
  }#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ========== WiFi ==========
const char* ssid = "HONOR X9d";
const char* password = "Wong0326@";

// ========== MQTT ==========
const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);

// ========== YOLO ==========
bool yoloPerson = false;
bool yoloActive = false;

// ========== DHT ==========
#define DHTPIN 23
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// ========== MQ-2 ==========
#define MQ2_PIN 34
const int GAS_THRESHOLD = 2500;

// ========== HC-SR04 ==========
#define TRIG_PIN 5
#define ECHO_PIN 18

// ========== Buzzer ==========
#define BUZZER_PIN 25   // LOW active

// ========== LED ==========
#define RED_LED 26
#define YELLOW_LED 27
#define GREEN_LED 14

// ========== OLED ==========
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ================= WIFI =================
void setup_wifi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

// ================= MQTT CALLBACK =================
void callback(char* topic, byte* payload, unsigned int length) {
  String msg = "";

  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  if (String(topic) == "ai/person") {
    yoloPerson = (msg == "1");
    Serial.print("YOLO Person: ");
    Serial.println(yoloPerson);
  }
  if (String(topic) == "ai/yolo/status")
{
    if (msg == "on")
        yoloActive = true;
    else
        yoloActive = false;

    Serial.print("YOLO Status: ");
    Serial.println(yoloActive ? "ON" : "OFF");
}
}


// ================= MQTT RECONNECT =================
void reconnect() {
  while (!client.connected()) {
    Serial.println("Connecting MQTT...");

    if (client.connect("ESP32Client123")) {
      Serial.println("MQTT Connected");

      client.subscribe("ai/person");
    } else {
      Serial.print("Failed, rc=");
      Serial.println(client.state());
      delay(2000);
    }
  }
  client.subscribe("ai/person");
client.subscribe("ai/yolo/status");
}

// ================= SETUP =================
void setup() {
  Serial.begin(115200);

  dht.begin();

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  digitalWrite(BUZZER_PIN, HIGH); // OFF (LOW active)

  Wire.begin(21, 22);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED FAIL");
    while (true);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);

  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  reconnect();
}

// ================= LOOP =================
void loop() {
  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  // ===== Sensors =====
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  int gas = analogRead(MQ2_PIN);
  bool gasDetected = (gas > GAS_THRESHOLD);

  // HC-SR04
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  float distance = duration * 0.034 / 2;

  bool distanceDetected = (distance > 0 && distance < 30);

  // ===== HUMAN LOGIC (YOLO + distance) =====
  bool humanDetected = yoloPerson && distanceDetected;

  // ===== STATUS =====
  String status;

  if (gasDetected && humanDetected)
    status = "danger";
  else if (gasDetected || humanDetected)
    status = "warning";
  else
    status = "safe";

  // ===== MQTT JSON =====
  String payload =
    String("{\"temp\":") + temp +
    ",\"hum\":" + hum +
    ",\"gas\":" + gas +
    ",\"dist\":" + distance +
    ",\"status\":\"" + status + "\"}";

  client.publish("esp32/sensor", payload.c_str());

  Serial.println(payload);

  // ===== LED + BUZZER =====
  if (status == "danger") {
    digitalWrite(RED_LED, HIGH);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  }
  else if (status == "warning") {
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  }
  else {
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
  }

  // ===== OLED =====
  display.clearDisplay();

  display.setCursor(0, 0);
  display.print("Temp: "); display.print(temp);

  display.setCursor(0, 16);
  display.print("Hum : "); display.print(hum);

  display.setCursor(0, 32);
  display.print("Gas : "); display.print(gas);

  display.setCursor(0, 48);
  display.print("Dist: "); display.print(distance);

  display.setCursor(0, 56);
  display.print("Status: ");
  display.print(status);

  display.display();

  delay(2000);
}

  // ===== OLED =====
  display.clearDisplay();

  display.setCursor(0, 0);
  display.print("Temp: "); display.print(temp);

  display.setCursor(0, 16);
  display.print("Hum : "); display.print(hum);

  display.setCursor(0, 32);
  display.print("Gas : "); display.print(gas);

  display.setCursor(0, 48);
  display.print("Dist: "); display.print(distance);

  display.setCursor(0, 56);
  display.print("Status: ");
  display.print(status);

  display.display();

  delay(2000);
}
