#include <Arduino.h>

#include "wifi_control.cpp"
#include "io_control.cpp"
#include "ffs_control.cpp"
#include "sleep_func.cpp"

#define BANDRATE 115200
#define WEIGHT_THRESHOLD 20
RTC_DATA_ATTR int BOOT_COUNTER = 0;//起動回数

void autoCalibration();
void sleepMode();
void forceSleepMode();

void setup() {
    Serial.begin(BANDRATE);
    delay(500);
    Serial.println("--- SETUP Start ---");
    Serial.print("BOOT_COUNTER: ");
    Serial.println(BOOT_COUNTER);

    // 設定ファイルを読み取る
    loadConfigFile();

    // 各IOをセットアップする
    setupIO();
    //自動キャリブレーションをコメントアウト※測定できないときがあったため
    // if (BOOT_COUNTER == 0 || BOOT_COUNTER % autoCalibrationNum == 0){
    //     waitNotWeight(WEIGHT_THRESHOLD, 12000);
    //     autoCalibration();
    // }
    BOOT_COUNTER = BOOT_COUNTER + 1;
    getKg();
    delay(50);
    if (kg < WEIGHT_THRESHOLD) sleepMode();

    // WiFiに接続する
    int rssi = connectWiFi(saveData.ssid, saveData.password);
    if (rssi == 0){
        Serial.println("--- NOT CONNECT WiFI ---");
        delay(3000);
        sleepMode();
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
            if (isHttps){
                // LINEBotに通知を送る
                sendLineBot(
                    saveData.endpoint,
                    saveData.access_token,
                    kg
                );
            }
            forceSleepMode(); // 強制3分スリープ
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

void autoCalibration(){
    Serial.println("## Start Auto Calibration");
    zero_factor = scale.read_average();
    Serial.print("ZeroFacror: ");
    Serial.println(zero_factor);
    scale.set_offset(zero_factor);
    while(true){
        delay(100);
        kg = getKg();
        Serial.print("KG: ");
        Serial.println(kg);
        Serial.print("Calibration: ");
        Serial.println(calibration_factor);
        if (kg > 0.1){
            calibration_factor = calibration_factor - 10;
            scale.set_scale(calibration_factor);
        }
        else if (kg < -0.1) {
            calibration_factor = calibration_factor + 10;
            scale.set_scale(calibration_factor);
        }
        else {
            break;
        }
        delay(100);
    }
    Serial.println("## Complete Auto Calibration");
}

void sleepMode(){
    Serial.println("Start Deep Sleep");
    Serial.flush();
    deepSleep(86400 * 30);
};

void forceSleepMode(){
    Serial.println("3Minutes Force Deep Sleep");
    forceDeepSleep(60 * 3);
    Serial.flush();
}