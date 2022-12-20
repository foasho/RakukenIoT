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
source rk/bin/activate
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
rk01.rkrkSDH01
create database rkdb;
exit;

alembic upgrade head
```

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