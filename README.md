# weather-notification

## 開発環境

### python をインストール

```shell
brew install pyenv
pyenv install 3.12.0
pyenv local 3.12.0
```

### 仮装環境構築

```shell
python -m venv venv
source venv/bin/activate
```

### ライブラリをインストール

```shell
pip install -r requirements.txt
```

### local の設定ファイルを作成する

```shell
chmod +x ./tools/setup.sh
./tools/setup.sh
```

- api_key: openWhetherAPI のキーを設定
- slack_web_hook_url: 通知の先の Slack

## lamda にライブラリをアップロードする

ライブラリを利用する場合、lamda にアップロードする必要がある。

```shell
pip install -t python [ライブラリ名]
zip -r9 [ファイル名].zip python
```

作成したファイルを lamda にアップロードする
