### 概要
実行時引数に指定したGoogleWorkspace（GWS）組織のグループと、そこに所属するユーザーの一覧をCSVファイル「groups_list_{組織の顧客ID}.csv」に出力する。
組織にグループがなければCSVファイルは作成されない。

### 背景
GWSのグループとそこに所属するユーザーの一覧はGWS管理コンソールから一括取得できないため、それを可能とするツールがあると便利。

### 環境準備
- ローカル環境
  - pythonをインストール
    - バージョンは3.9以降が望ましい
  - pip3をインストール
    - バージョンは21.2以降が望ましい
  - ソースコードを取得
  - 必要なライブラリをインストール
  ```sh
  # ソースコードが存在する場所で実行する
  pip3 install -r requirements.txt
  ```
- GoogleCloudプロジェクト環境
  - プロジェクトを作成
    - 対象のGWS組織配下に作成する
  - [Admin SDK API](https://console.cloud.google.com/apis/api/admin.googleapis.com/)を有効化
  - [OAuth同意画面](https://console.cloud.google.com/apis/credentials/consent?hl=ja)を作成
    - ここでスコープを「組織内」にすると同一GWS組織内のアカウントでの実行のみを許可する
  - [OAuthクライアントシークレット](https://console.cloud.google.com/apis/credentials?hl=ja)を作成しJSONをダウンロード
    - アプリケーションの種類は「デスクトップアプリ」を選択する
    - ソースコードが存在するパスに移動し、名前をcredentials.jsonに変更する

### 実行
```sh
# ソースコードが存在する場所で実行する
# 実行するとブラウザでOAuth同意画面が開くので、画面の指示に従ってアクセスを許可する
python3 main.py {組織の顧客ID}
```

### メモ
 - Group APIで取得できる情報にはグループのオーナー情報が含まれない模様。
 - 実行に関して、ローカルの実行ユーザーが上記で作成したGoogleCloudプロジェクトに何らかのIAMロールを持つ必要はないし、対象のGWSコンソールへのアクセス権を持つ必要もない。シークレットJSONの持ち主かどうかで認証し、上記コマンド実行後のOAuth同意画面にて認可している。

### 参考
- [Directory API: デベロッパー ガイド](https://developers.google.com/admin-sdk/directory/v1/guides/guides?hl=ja)
- [Admin SDK API リファレンス](https://developers.google.com/admin-sdk/reference-overview?hl=ja)