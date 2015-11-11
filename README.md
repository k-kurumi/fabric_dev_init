# fabric_dev_init

ubuntuの初期設定用fabfile

# Usage

1. vmの起動

```
vagrant up
```

2. ssh_configの作成

```
vagrant ssh-config --host vagrant > ssh_config
```

3. 実行

```
# SSH_CONFIG_PATH指定なしのときは~/.ssh/configが参照される
export SSH_CONFIG_PATH=ssh_config

# dotfilesほか主要ライブラリのインストール
fab -H vagrant tool.init

# ruby
fab -H vagrant ruby.list
fab -H vagrant ruby.install:2.2.2

# python
fab -H vagrant python.list
fab -H vagrant python.install:2.7.10

# golang
fab -H vagrant golang.list
fab -H vagrant golang.install:go1.4.2

# node.js
fab -H vagrant node.list
fab -H vagrant node.install:v0.12.4
```
