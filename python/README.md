## ローカルPython開発環境構築
* ### Pythonインストール
```sh
# Pythonバージョン管理ツールをインストールする
brew install pyenv
# インストール可能なバージョンを確認する
pyenv install --list
# 表示された任意のバージョンをインストールする
pyenv install 3.6.10
# インストールしたバージョンをローカルデフォルトとする
pyenv local 3.6.10
# pyenvにPATHが通っていないとダメな場合がある。その際はshプロファイルに以下を記述する。
# export PYENV_ROOT="$HOME/.pyenv"
# export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"
```

* ### パッケージ管理ツール（pip）インストール
pythonをインストールすればついてくる。

* ### パッケージインストール
pip_packages.txtに記載しているものをインストールする。
```sh
pip3 install -r pip_packages.txt
```
追加でインストールする場合は以下を実行する。
```sh
pip3 install インストールするパッケージ名
pip3 freeze > pip_packages.txt
```

インストール済みのものをアップデートする場合は以下を実行する。
```sh
pip3 list -o
pip3 install -U インストールするパッケージ名==インストールしたいバージョン
pip3 freeze > pip_packages.txt
```

* ### 静的ツール用VScode設定
#### Formatter実行
```sh
find . -name "*.py" | xargs yapf --i --recursive .
```
#### Linter実行
```sh
find . -name "*.py" | xargs pylint
```
[（参考）PythonのLintとFormatter](https://www.sambaiz.net/article/125/)

## 単体テスト
* ### コマンドラインでカバレッジ確認
```sh
pytest -v --cov=src tests
* --covにはカバレッジ算出対象ソースのディレクトリ（テストディレクトリではない）を指定する
```

* ### テスト未実施コード行確認
```sh
pytest -v --cov=src --cov-report=term-missing
```

* ### 結果をHTML出力
```sh
pytest -v --cov=src --cov-report=html
* 実行パス直下にhtmlcovが作成され、その配下に出力される。
```

## 仮想環境作成
* ### 環境作成/パッケージインストール
> この配下にpip3 installでパッケージがインストールされるようになる。
> 環境無効化するとそれらは使用できなくなる。
```sh
$ python3 -m env py36env
$ pip3 install -r pip3_packages_36.txt
```

* ### 環境有効化
```sh
$ source py36env/bin/activate
```

* ### 環境無効化
```sh
$ deactive
```
