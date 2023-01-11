# RAKUKEN-API
- Python: 3.7.5
- フレームワーク: FastAPI
- データベース : MySQL

## 実行方法
```commandline
pip install -r requiments.txt
python main.py
もしくは
python run.py
```

## 説明
CREATE USER 'rk'@'localhost' IDENTIFIED BY '設定したパスワード';
GRANT ALL ON *.* TO rk@localhost;
FLUSH PRIVILEGES;

## .env(設定ファイル)の作成
```commandline
DB_NAME=rk※データベース名
DB_PWD=データベースのパスワード
DB_USER=データベースのユーザー
DB_HOST=localhost※データベースのホスト
SECRET_KEY=任意文字※暗号化につかうのでできるだけ長いもの
DEBUG=<true か　false>
LINE_ACCESS_TOKEN=LINEのMessagingAPIのアクセストークン
LINE_CHANNEL_SECRET=LINEのチャンネルのシークレットトークン
```

## マイグレーション
### マイグレーションファイル反映
```commandline
alembic upgrade head
```
### 自分でDBを拡張する場合：マイグレーションファイル作成
```commandline
alembic revision --autogenerate -m "SampleName"
```

## インストール(Ubuntu18.04想定)
```commandline
sudo apt install python3.7 python3.7-dev python3.7-venv python3-venv
python3.7 -m venv rk
source /home/ubuntu/rk/bin/activate
```

```commandline
sudo apt install -y mysql-server mysql-client default-libmysqlclient-dev
sudo apt install -y build-essential libssl-dev python3-setuptools g++
```

```commandline
python -m pip install -U pip
pip install -r requirements.txt
```

データベースの作成
```commandline
パスワードを入力し、あとはひらすらy
sudo mysql -u root
CREATE USER 'rk'@'localhost' IDENTIFIED BY '設定したパスワード';
GRANT ALL ON *.* TO rk@localhost;
FLUSH PRIVILEGES;
quit;
mysql -u rk -p
'設定したパスワード'
create database rkdb;
exit;

<.envファイルの作成>
alembic upgrade head
```
# SSL証明書を使わず、HTTPとしてサービス化する場合
```commandline
sudo nano /etc/systemd/system/rkapi.service
---------------
[Unit]
Description=API Server
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/RakukenProjects
Environment="PATH=/home/ubuntu/rk/bin"
ExecStart=/home/ubuntu/rk/bin/gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
---------------

sudo systemctl daemon-reload
sudo systemctl enable rkapi
sudo systemctl start rkapi
sudo systemctl status rkapi
```

# SSL証明書を使って、HTTPSとしてサービス化する場合
```commandline

```
```commandline
sudo nano /etc/systemd/system/rkapi.service
---------------
[Unit]
Description=Gunicorn Daemon for FastAPI RakukenIoT Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/RakukenIoT/api
Environment="PATH=/home/ubuntu/rk/bin"
ExecStart=/home/ubuntu/rk/bin/gunicorn main:app --config gunicorn_conf.py

[Install]
WantedBy=multi-user.target
---------------

sudo systemctl daemon-reload
sudo systemctl enable rkapi
sudo systemctl start rkapi
sudo systemctl status rkapi
```

## Nginxでサーバー化
```commandline
sudo apt install nginx　-y

#既存設定ファイルを移動
sudo mv /etc/nginx/sites-enabled/default ./default_backup

sudo nano /etc/nginx/sites-available/rakuken-iot.net
----
server {
    client_max_body_size 64M;
    listen 80;
    server_name api.slingacademy.com;
    location / {
    proxy_pass http://127.0.0.1:8000;
        proxy_read_timeout     60;
        proxy_connect_timeout  60;
        proxy_redirect         off;

        # Allow the use of websockets
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
----

sudo ln -s /etc/nginx/sites-available/rakuken-iot.net /etc/nginx/sites-enabled/
```

## LetsEncriptでSSL化
```commandline
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain -d www.your_domain

>> メールアドレス入力
>> A:同意
>> Y:同意

https://your_domain

自動更新化
```

## デバッグ
```commandline
sudo 
```