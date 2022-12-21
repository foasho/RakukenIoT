#include "SPIFFS.h"

/* --- 状態変数/定数 --- */
#define MODE_SETUP 0 // BLE設定モード
#define MODE_WORK 1  // 通常稼働モード
/* -------------------- */

/**
 * RTCメモリに保持し続けるデータ
*/
static RTC_DATA_ATTR char vEndpoint[100];         // APIエンドポイント
static RTC_DATA_ATTR char vWifiSSID[100];         // WiFi(SSID)
static RTC_DATA_ATTR char vWifiPWD[100];          // WiFi(PWD)
static RTC_DATA_ATTR char vAccessToken[200];      // APIアクセストークン
static RTC_DATA_ATTR int vUserId;                 // ユーザーID

/**
 * 設定ファイルの変数データセット
*/
struct DATA_SET {
    char endpoint[100];
    char ssid[100];
    char password[100];
    char access_token[200];
    int user_id;
};
static DATA_SET saveData;


/**
 * @brief データ反映
 */
static void loadData() {
    strcpy(saveData.endpoint, String(vEndpoint).c_str());
    strcpy(saveData.ssid, String(vWifiSSID).c_str());
    strcpy(saveData.password, String(vWifiPWD).c_str());
    strcpy(saveData.access_token, String(vAccessToken).c_str());
    saveData.user_id = vUserId;
}
/**
 * @brief データの保存
 */
static void putData() {
    strcpy(saveData.endpoint, String(vEndpoint).c_str());
    strcpy(saveData.ssid, String(vWifiSSID).c_str());
    strcpy(saveData.password, String(vWifiPWD).c_str());
    strcpy(saveData.access_token, String(vAccessToken).c_str());
    saveData.user_id = vUserId;
}


/**
 * @brief 内部設定WiFiファイルの書き込み
 */
static void writeWiFiConfig(String ssidData, String pwdData){
    SPIFFS.begin();
    try{
        // 既にファイルがある場合は古いものを削除する
        SPIFFS.remove("/config.conf");
    }
    catch(...){}
    File fw = SPIFFS.open("/config.conf", "w");
    String writeStr = "\nendpoint=" + String(saveData.endpoint)
        + "\nssid=" + ssidData
        + "\npassword=" + pwdData 
        + "\naccessToken=" + String(saveData.access_token) 
        + "\nuserId=" + String(saveData.user_id);
    fw.println( writeStr );
    fw.close();
    SPIFFS.end();
}

/**
 * @brief 内部設定ファイルの書き込み
 */
static void writeConfig(
    String epData,
    String ssidData,
    String pwdData,
    String tokenData,
    String userIdData
){
    SPIFFS.begin();
    try{
        // 既にファイルがある場合は古いものを削除する
        SPIFFS.remove("/config.conf");
    }
    catch(...){}
    File fw = SPIFFS.open("/config.conf", "w");
    String writeStr = "\nendpoint=" + epData
        + "\nssid=" + ssidData
        + "\npassword=" + pwdData 
        + "\naccessToken=" + tokenData 
        + "\nuserId=" + userIdData;
    fw.println( writeStr );
    fw.close();
    SPIFFS.end();
}

/**
 * @brief 内部設定ファイルの読み込み
 */
static void loadConfigFile(){
    SPIFFS.begin(); // SPIFFS config.confファイルの読み込み
    Serial.println("## Load Config");
    File fr = SPIFFS.open("/config.conf", "r");
    while(fr.available()){
        String readStr = fr.readStringUntil('\n'); // 改行まで１行読み出し
        Serial.println(readStr);
        if (readStr.substring(0, String("endpoint=").length()) == "endpoint="){
            readStr.replace("endpoint=", "");
            readStr.trim();
            strcpy(vEndpoint, String(readStr).c_str());
        }
        if (readStr.substring(0, String("ssid=").length()) == "ssid="){
            readStr.replace("ssid=", "");
            readStr.trim();
            strcpy(vWifiSSID, String(readStr).c_str());
        }
        else if (readStr.substring(0, String("password=").length()) == "password=") {
            readStr.replace("password=", "");
            readStr.trim();
            strcpy(vWifiPWD, String(readStr).c_str());
        }
        else if (readStr.substring(0, String("userId=").length()) == "userId="){
            readStr.replace("userId=", "");
            readStr.trim();
            vUserId = atoi(String(readStr).c_str());
        }
        else if (readStr.substring(0, String("accessToken=").length()) == "accessToken=") {
            readStr.replace("accessToken=", "");
            readStr.trim();
            strcpy(vAccessToken, String(readStr).c_str());
        }
    }
    fr.close();
    loadData();
    SPIFFS.end();
}