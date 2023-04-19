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

* ### 参考
[PythonのLintとFormatter](https://www.sambaiz.net/article/125/)


## 単体テスト
* ### 準備
```sh
pip3 install pytest
pip3 install pytest-cov
```

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
* ### 参考
[pythonのカバレッジをpytest-covで調べる](https://qiita.com/mink0212/items/34b9def61d58ab781714)  
[【pytest】モックの使い方まとめ](https://zenn.dev/re24_1986/articles/0a7895b1429bfa)  
[【Python】GoogleAPIを利用したメソッドのテストでモックを使う](https://mizzsugar.hatenablog.com/entry/2019/06/05/205612)  

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
