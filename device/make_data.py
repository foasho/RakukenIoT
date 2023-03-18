import os
import sys

"""
設定ファイルの生成
"""
def make_config_conf(
    dir_path: str,
    endpoint:str,
    ssid:str,
    password:str,
    access_token:str,
    user_id:int
):
    if not os.path.exists(f"{dir_path}/data"):
        os.makedirs({dir_path}/data)
    with open(f"{dir_path}/data/config.conf") as f:
        f.write(f"endpoint={endpoint}\nssid={ssid}\npassword={password}\naccess_token={access_token}\nuser_id={user_id}")

if __name__ == "__main__":
    endpoint = input("接続するエンドポイントを入力してください[https://rakuken-iot.net]: ") or "https://rakuken-iot.net"
    ssid = input("あなたの2.4GHzのWiFi環境のSSIDを入力してください")
    password = input("あなたの2.4GHzのWiFi環境のパスワードを入力してください")
    access_token = input("アカウント作成後、認証トークンを取得し、入力してください[https://rakuken-iot.net/docs]")
    user_id = input("アカウント作成後、あなたのユーザーIDを入力してください[https://rakuken-iot.net/docs]")
    make_config_conf(dir_path=".")