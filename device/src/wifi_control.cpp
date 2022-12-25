#include <WiFiClientSecure.h>
#include <WiFi.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>
#include "SSLClient.h"

#define HTTP_BODY_SIZE 300
static StaticJsonDocument<HTTP_BODY_SIZE> response;
static int apiPort = 80;
static bool isHttps = false;

static float kg;

/**
 * @brief WiFiに接続する
 * @param ssid 
 * @param password 
 * @return int RSSI(dBm値)
 */
static int connectWiFi(char *ssid, char *password){
    WiFi.begin(ssid, password);
    Serial.println("WiFi Start Begin");
    int count = 1;
    Serial.println("Connecting to WiFi..");
    while (WiFi.status() != WL_CONNECTED) {
        delay(300);
        Serial.print("..");
    }
    if (count >= 59){
        return 0;
    }
    int rssi = WiFi.RSSI();
    Serial.printf("## WiFi dBm [%d]", rssi);
    return rssi;
}


/**
 * @brief HTTP送信
 * 
 * @param endpoint 
 * @param request_json 
 * @param access_token
 * @param user_id
 * @param route 
 * @return String
 */
static String sendHttp(char* apihost, String route, String json, String access_token){
    String line = "";
    bool Success_h = false;
    int httpCode = 404;
    String portString = ":" + String(apiPort);

    // SSL接続確認
    if (isHttps){
        Serial.println("==== HTTPS ====");
        WiFiClientSecure client;
        client.setInsecure();
        if (!client.connect(apihost, apiPort)) {
            Serial.println("CONNECT-ERROR");
            return String("101");
        }
        Serial.println("--- HTTPS CONNECT SUCCESS ---");
        client.print("POST " + String(route) + " HTTP/1.1\r\n");
        client.print("Host: " + String(apihost) + portString + "r\n");
        client.print("Authorization: Bearer " + access_token + "\r\n");
        client.print("Content-Type: application/json; charset=thf-8\r\n");
        client.print("Connection: Keep-Alive\r\n");
        client.print("Content-Length: "+ String(json.length()) + "\r\n");
        client.print("\r\n");
        client.print(json + "\r\n");
                
        unsigned long timeout = millis();
        while (client.available() == 0) {
            if (millis() - timeout > 60000) {
                Serial.println(">>> Client Timeout !");
                client.stop();
                return String("102");
            }
        }
        
        
        while(client.available()) {
            String resp = client.readString();
            httpCode    = resp.substring(resp.indexOf(" ") + 1,
                                        resp.indexOf(" ", resp.indexOf(" ") + 1)).toInt();
            Success_h   = (httpCode == 200);
            line = resp.substring(resp.indexOf("{"),
                                        resp.indexOf("{", resp.indexOf("}") + 1));
            if (httpCode == 200){
                Success_h = true;
                break;
            }
        }
    }
    else {
        Serial.println("==== HTTP ====");
        WiFiClient client;
        if (!client.connect(apihost, apiPort)) {
            Serial.println("CONNECT-ERROR");
            return String("101");
        }

        Serial.println("--- HTTP CONNECT SUCCESS ---");
        client.print("POST " + String(route) + " HTTP/1.1\r\n");
        client.print("Host: " + String(apihost) + portString + "r\n");
        client.print("Authorization: Bearer " + access_token + "\r\n");
        client.print("Content-Type: application/json; charset=thf-8\r\n");
        client.print("Connection: Keep-Alive\r\n");
        client.print("Content-Length: "+ String(json.length()) + "\r\n");
        client.print("\r\n");
        client.print(json + "\r\n");
                
        unsigned long timeout = millis();
        while (client.available() == 0) {
            if (millis() - timeout > 60000) {
                Serial.println(">>> Client Timeout !");
                client.stop();
                return String("102");
            }
        }
        
        
        while(client.available()) {
            String resp = client.readString();
            httpCode    = resp.substring(resp.indexOf(" ") + 1,
                                        resp.indexOf(" ", resp.indexOf(" ") + 1)).toInt();
            Success_h   = (httpCode == 200);
            line = resp.substring(resp.indexOf("{"),
                                        resp.indexOf("{", resp.indexOf("}") + 1));
            if (httpCode == 200){
                Success_h = true;
                break;
            }
        }
    }
    if (!Success_h){
        return String("102");
    }
    return line;
}

/**
 * 文字を特定の文字で分割する
 * @param data      分割もとデータ
 * @param delimiter 分割判断文字
 * @param dst       分割後の格納先
*/
static int splitData(String data, char delimiter, String *dst){
    int index = 0;
    int arraySize = (sizeof(data)/sizeof((data)[0]));  
    int datalength = data.length();
    for (int i = 0; i < datalength; i++) {
        char tmp = data.charAt(i);
        if ( tmp == delimiter ) {
            index++;
            if ( index > (arraySize - 1)) return -1;
        }
        else dst[index] += tmp;
    }
    return (index + 1);
}

/**
 * 体重HTTPリクエストを送る
 * @param endpoint
 * @param access_token
 * @param user_id
 * @param route
*/
static StaticJsonDocument<HTTP_BODY_SIZE> sendWeight(char* endpoint, char* access_token, int user_id, float weight){
    String body = String("{\"data\":\"null\",\"success\":\"false\",\"messages\":\"\"}");
    StaticJsonDocument<HTTP_BODY_SIZE> resBody; 
    String json =  "{\"value\":"+ String(weight) +",\"user_id\":"+user_id+"}";

    char *route = "/api/weight-log";

    // "https://" もしくは "http://"　を取り除く
    char apihost[100];
    String readStr = String(endpoint);
    if (readStr.indexOf(String("https")) != -1){
        isHttps = true;
        readStr.replace("https://", "");
        readStr.trim();
        strcpy(apihost, String(readStr).c_str());
    }
    else {
        isHttps = false;
        // endpointにポートの記載があれば、”:”から切り取る
        if (readStr.indexOf(String(":")) != -1){
            String resTxts[2] = {"\0"};
            String spData = readStr;
            spData.replace("http://", "");
            splitData(spData, ':', resTxts);
            Serial.println("== [CHANGE PORT] ==");
            apiPort = atoi(resTxts[1].c_str());
            Serial.println(apiPort);
            strcpy(apihost, resTxts[0].c_str());
            Serial.println(apihost);
        }
        else {
            apiPort = 80;
            readStr.replace("http://", "");
            readStr.trim();
            strcpy(apihost, String(readStr).c_str());
        }
    }
    String result = sendHttp(apihost, String(route), json, String(access_token));
    Serial.println("### Complete Send Weight Data ###");
    if (result == String("101")){
        body = String("{\"data\":\"null\",\"success\":\"false\",\"messages\":\"101\"}");
        deserializeJson(resBody, body);
        return resBody;
    }
    else if (result == String("102")){
        body = String("{\"data\":\"null\",\"success\":\"false\",\"messages\":\"102\"}");
        deserializeJson(resBody, body);
        return resBody;
    }
    else {
        // 結果を返す
        deserializeJson(resBody, result);
        return resBody;
    }
    return resBody;
}

/**
 * 体重をLINEに送る
 * ※注意：HTTPS通信でないと利用できません
 * @param endpoint
 * @param access_token
 * @param weight
*/
static StaticJsonDocument<HTTP_BODY_SIZE> sendLineBot(char* endpoint, char* access_token, float weight){
    String body = String("{\"data\":\"null\",\"success\":\"false\",\"messages\":\"\"}");
    StaticJsonDocument<HTTP_BODY_SIZE> resBody; 
    String json =  "{\"weight\":"+ String(weight) + "}";

    char *route = "/api/line-weight";

    // "https://"を取り除く
    char apihost[100];
    String readStr = String(endpoint);
    readStr.replace("https://", "");
    readStr.trim();

    strcpy(apihost, String(readStr).c_str());
    String result = sendHttp(apihost, String(route), json, String(access_token));
    Serial.println("### Complete Send Line Weight Data ###");
    Serial.println("-----------------------------------------");
    Serial.println(result);
    Serial.println("-----------------------------------------");
    if (result == String("101")){
        body = String("{\"data\":\"null\",\"success\":\"false\",\"messages\":\"101\"}");
        deserializeJson(resBody, body);
        return resBody;
    }
    else if (result == String("102")){
        body = String("{\"data\":\"null\",\"success\":\"false\",\"messages\":\"102\"}");
        deserializeJson(resBody, body);
        return resBody;
    }
    else {
        // 結果を返す
        deserializeJson(resBody, result);
        return resBody;
    }
    return resBody;
}