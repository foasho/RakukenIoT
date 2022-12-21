#include <Arduino.h>

#include "wifi_control.cpp"
#include "io_control.cpp"
#include "ffs_control.cpp"
#include "sleep_func.cpp"

#define BANDRATE 115200
#define WEIGHT_THRESHOLD 20

void setup() {
    Serial.begin(BANDRATE);
    delay(1000); // 安定化のためのDelay
    Serial.println("--- SETUP Start ---");

    // 設定ファイルを読み取る
    loadConfigFile();

    // 各IOをセットアップする
    setupIO();

    // WiFiに接続する
    int rssi = connectWiFi(saveData.ssid, saveData.password);
    if (rssi == 0){
        Serial.println("--- NOT CONNECT WiFI ---");
        delay(3000);
        ESP.restart();
    }

    
}

void loop() {
    delay(300);
    onLED();
    kg = getKg();
    Serial.println("--- WiFi ---");
    Serial.println(WiFi.status());// 3:
    Serial.println("------------");

    if (kg > WEIGHT_THRESHOLD){
        Serial.println("Start Sending");
        delay(1500);

        digitalWrite(BUZZER, HIGH);
        // 最新値の体重を取得
        kg = getKg();
        response = sendWeight(
            saveData.endpoint, 
            saveData.access_token,
            saveData.user_id,
            kg
        );
        String suc = response["success"];
        response.clear();
        delay(1000);
        offLED();
        if (suc == String("true")){
            orderBuzzer(250);
            Serial.println("SUCCESS SEND API");
            forceDeepSleep(60 * 3); // 強制3分スリープ
        }
        else {
            orderBuzzer(1500); //失敗時は長くブザーを鳴らす
        }
        deepSleep(86400*30);
    }
    else {
        Serial.println("NOT FOUND WEIGHT");
        deepSleep(86400*30);
    }
}
