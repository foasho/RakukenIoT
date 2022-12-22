# RAKUKEN-API
- API: FastAPI
- DB: mysql

## 説明
CREATE USER 'rk'@'localhost' IDENTIFIED BY '設定したパスワード';
GRANT ALL ON *.* TO rk@localhost;
FLUSH PRIVILEGES;

## マイグレーション
### マイグレーションファイル作成
```commandline
alembic revision --autogenerate -m "Sample"
```

### マイグレーションファイル反映
```commandline
alembic upgrade head
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
sudo mysql_secure_installation
パスワードを入力し、あとはひらすらy
sudo mysql -u root -p
CREATE USER 'rk'@'localhost' IDENTIFIED BY '設定したパスワード';
GRANT ALL ON *.* TO rk@localhost;
FLUSH PRIVILEGES;
mysql -u rk -p
'設定したパスワード'
create database rkdb;
exit;

alembic upgrade head
```

```commandline
sudo nano /etc/systemd/system/rkapi.service
---------------
[Unit]
Description=Gunicorn Daemon for FastAPI RakukenIoT Application
After=network.target

[Service]
User=demo
Group=www-data
WorkingDirectory=/home/ubuntu/RakukenIoT/api
ExecStart=/home/ubuntu/rk/bin/gunicorn main:app --config gunicorn_conf.py

[Install]
WantedBy=multi-user.target
---------------

sudo systemctl daemon-reload
sudo systemctl enable rkapi
sudo systemctl start rkapi
sudo systemctl status rkapi
```

```commandline
sudo apt install nginx
sudo nano /etc/nginx/conf.d/default.conf
```