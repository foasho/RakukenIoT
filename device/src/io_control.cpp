#include "HX711.h"
#include "io_pins.h"

//HX711接続ピンの設定
static HX711 scale;
static float bias = 1.0;

// これが倍率にかかる(Scale): Default-> 
static RTC_DATA_ATTR float calibration_factor = -13850;
// これが基準点になる(offset): Default-> 79931
static RTC_DATA_ATTR long zero_factor = 79931;
// オートキャリブレーションをかける回数
#define autoCalibrationNum 30

//センサのノイズ除去(ローパスフィルタ)
static volatile float LoadCellVal, LoadCellVal_RC;  // ロードセルの値、フィルタ後の値
#define samplingSpeedN 3                            // ハイスピードサンプリング回数
#define samplingN 10                                // 通常記録時のサンプリング回数
#define a 0.8                                       // 0<a<1の範囲　大きいほどローパスフィルタの効果大だが反応が鈍くなる
static int i;

static void setupLoadCell(){
    //ロードセルHX711の設定
    scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);// ロードセルのピンの設定
    scale.set_scale(calibration_factor);             // この値はSparkFun_HX 711_Calibrationスケッチを使用して取得されます
    scale.set_offset(zero_factor);                   // 以前の既知の0_factorを使用してスケールを0アウトします
}

static void setupIO(){
    pinMode(STATUS_LED, OUTPUT);
    pinMode(BUZZER, OUTPUT);
    pinMode(SENSOR, INPUT);
    setupLoadCell();
}

static float getKg(){
    LoadCellVal_RC = scale.get_units();
    for (i = 1; i < samplingN; i++) {                                        // n回分繰り返し
        LoadCellVal = scale.get_units();                               // ロードセルの値をHX711から取得
        LoadCellVal_RC = a * LoadCellVal_RC + (float)LoadCellVal * (1 - a);//フィルタ(n回分を差分方程式でノイズを除去する)
    }
    float _kg = LoadCellVal_RC *  -1 * bias;
    return _kg;
}

static float getSpeedKg(){
    LoadCellVal_RC = scale.get_units();
    for (i = 1; i < samplingSpeedN; i++) {                                        // n回分繰り返し
        LoadCellVal = scale.get_units();                               // ロードセルの値をHX711から取得
        LoadCellVal_RC = a * LoadCellVal_RC + (float)LoadCellVal * (1 - a);//フィルタ(n回分を差分方程式でノイズを除去する)
    }
    float _kg = LoadCellVal_RC *  -1 * bias;
    return _kg;
}

static bool waitNotWeight(int threshold, int mSec){
    Serial.println("WAIT NOT WEIGHT");
    uint32_t ms = millis();
    bool suc = true;
    while(true){
        ms = millis();
        delay(100);
        if (ms > mSec) {
            suc = false;
            break;
        };
        float _kg = getKg();
        if (_kg < threshold) break;
    }
    return suc;
}

static void orderBuzzer(int ms){
    digitalWrite(BUZZER, HIGH);
    delay(ms);
    digitalWrite(BUZZER, LOW);
}

static void onLED(){
    digitalWrite(STATUS_LED, HIGH);
}

static void offLED(){
    digitalWrite(STATUS_LED, LOW);
}

static bool isHumanSensor(){
    return digitalRead(SENSOR);
}

static bool getHumanSensor(){
    return analogRead(SENSOR);
}