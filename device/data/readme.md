# 設定ファイル"config.conf"

ハードウェアが読み取る設定ファイル
本番運用では、アプリからBluetoothで設定値を送るが、
試作やテストではそのまま設定ファイルを書き込む

dataフォルダ直下にconfig.confを作成し、内容を書き込む
```
- data
  |- config.conf
　|- readme.md
```

入力例(詳細は以下”パラメータ説明”を参照)
```
endpoint=https://example.com
ssid=XXXXXXX-X-XXXX
password=yyyyyyyyyy
access_token=zzzzzzzzzzzzz....
user_id=1
```

## パラメータ説明

|パラメータ名|説明|入力例|備考|
|---|---|---|---|
|endpoint|APIのエンドポイント|https://example.com||
|ssid|WiFiのSSID|XXXXXXX-X-XXXX|ルーターを確認|
|password|WiFiのパスワード|yyyyyyyyyy|ルーターを確認|
|accessToken|認証トークン|zzzzzzzzzzzzz....|管理画面のリファレンスから直接作成|
|userId|ユーザーID|1||
