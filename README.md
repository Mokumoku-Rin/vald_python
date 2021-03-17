# vald python
valdをpythonから実行するサンプル

## 1. setup
必要なライブラリをインストール
```
    $ pip install -r requirements.txt
```
dockerを起動する
```
    $ mkdir -p vald_config/backup
    $ docker run -v $(pwd)/vald_config/:/etc/server -p 8081:8081 --rm -it vdaas/vald-agent-ngt
```

## 2. pythonからvaldにアクセス
```
    $ python main.py
```

## 3. 終了
```
    # Ctrl + c でdockerを終了
    # backupファイルを削除
    $ rm -r vald_config/backup/
```

## 4. reference
https://github.com/vdaas/vald-client-python
