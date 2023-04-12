### 概要
実行時引数に指定したGoogleWorkspace（GWS）組織のグループと、そこに所属するユーザーの一覧をCSVファイルに出力する。

### 背景
GWSのグループとそこに所属するユーザーの一覧はGWS管理コンソールから一括取得できないため、それを可能とするツールがあると便利。

### 環境準備
- GoogleCloudプロジェクト環境
  - プロジェクトを作成
    - 対象のGWS組織配下に作成する
  - Admin SDK APIを有効化
  - OAUTH同意画面を作成
    - ここでスコープを「組織内」にすると同一GWS組織内のアカウントでの実行のみを許可する
  - OAuthクライアントシークレットJSONをダウンロード
    - ソースコードが存在するパスに移動しておく
  - 実行ユーザーがGoogle CloudプロジェクトにIAMロールを持つ必要はない
- pythonをインストール
  - バージョンは3.9以降
- pip3をインストール
  - バージョンは21.2以降
- 必要なライブラリをインストール
```sh
pip3 install -r requirements.txt
```

### 実行
- 対象GWS組織に適切な権限を持つロールのユーザーで実行
```sh
python3 main.py {組織の顧客ID}
```

### メモ
Group APIで取得できる情報にはグループのオーナー情報が含まれない模様。

### 参考
- [Directory API: デベロッパー ガイド](https://developers.google.com/admin-sdk/directory/v1/guides/guides?hl=ja)
- [Admin SDK API リファレンス](https://developers.google.com/admin-sdk/reference-overview?hl=ja)