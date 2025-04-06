#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// Configurações WiFi
const char* ssid = "NOME_WIFI"; // Substitua pelo nome da sua rede WiFi
const char* password = "PASS_WIFI"; // Substitua pela senha da sua rede WiFi
const char* serverName = "http://example.com/api"; // Substitua pela URL da sua API

// Instância do BME280
Adafruit_BME280 bme;

// Constantes para ajuste de pressão
const float ALTITUDE_M = 45.0;          // Sua altitude em metros
const float SEA_LEVEL_PRESSURE_HPA = 1013.25; // Pressão padrão ao nível do mar (hPa)

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // SDA=21, SCL=22 (ESP32)

  // Conectar ao WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi");

  // Inicializar BME280 no endereço 0x76
  if (!bme.begin(0x76, &Wire)) {
    Serial.println("Erro: BME280 não encontrado! Verifique conexões.");
    while (1);
  }
  Serial.println("BME280 iniciado!");
}

void loop() {
  // Ler dados do BME280
  float temperature = bme.readTemperature();
  float raw_pressure = bme.readPressure() / 100.0F; // Pressão bruta em hPa
  float humidity = bme.readHumidity();

  // Ajustar pressão para o nível do mar (fórmula barométrica)
  float adjusted_pressure = raw_pressure / pow(1 - (0.0065 * ALTITUDE_M) / (temperature + 0.0065 * ALTITUDE_M + 273.15), 5.255);

  // Limitar para 1 casa decimal
  char temperatureStr[8]; 
  char rawPressureStr[8]; 
  char adjustedPressureStr[8]; 
  char humidityStr[8];

  dtostrf(temperature, 4, 1, temperatureStr);
  dtostrf(raw_pressure, 6, 1, rawPressureStr);
  dtostrf(adjusted_pressure, 6, 1, adjustedPressureStr);
  dtostrf(humidity, 6, 1, humidityStr);

  // Exibir no Serial Monitor
  Serial.print("Temperatura: "); Serial.println(temperatureStr);
  Serial.print("Pressão bruta: "); Serial.println(rawPressureStr);
  Serial.print("Pressão ajustada: "); Serial.println(adjustedPressureStr);
  Serial.print("Umidade: "); Serial.println(humidityStr);

  // Enviar para a API
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Criar JSON com os dados formatados com 1 casa decimal
    String jsonPayload = "{\"temperature\":" + String(temperatureStr) + 
                         ",\"pressure\":" + String(adjustedPressureStr) + 
                         ",\"humidity\":" + String(humidityStr) + "}";

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.print("Dados enviados! Resposta: ");
      Serial.println(http.getString());
    } else {
      Serial.print("Erro na requisição: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi desconectado!");
  }

  delay(300000); // Esperar 5 minutos
}