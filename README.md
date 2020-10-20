# UFW

![ansible ci](https://github.com/link-u/ansible-roles-v2_ufw/workflows/ansible%20ci/badge.svg)

## 目次

<!-- TOC depthFrom:2 -->

- [目次](#目次)
- [概要](#概要)
- [動作確認バージョン](#動作確認バージョン)
- [使い方 (ansible)](#使い方-ansible)
    - [Role variables](#role-variables)
    - [Example playbook](#example-playbook)
- [後方互換性について](#後方互換性について)
    - [削除された変数の一覧](#削除された変数の一覧)
- [Licence](#licence)

<!-- /TOC -->

<br>

## 概要

ufw をインストール・設定する ansible role

<br>

## 動作確認バージョン

- Ubuntu 18.04 (bionic)
- ansible >= 2.8
- Jinja2 2.10.3

<br>

## 使い方 (ansible)

### Role variables

```yaml
### インストール設定 ###############################################################################
## インストールフラグ
#  * False にすると install.yml をスキップできる.
#  * install.yml 以外を流し込みたいときに使う.
#  * install.yml の中には apt 関係のモジュールが書き込まれている.
ufw_install_flag: True

## ufw を一時的にリセットするフラグ
#  * True にすると「一時的に」ファイアーウォールの設定を全てリセットする (つまりノーガード状態).
#  * group_vars に書く必要は特に無い.
#  * デフォルト値は False
#  * 使い所としては, ファイアーウォールの設定を見直したいときに使う.
#  * 使う場合は, ansible-playbook コマンドのオプション引数である -e (--extra-vars) を付け足して意識的に使うことを心がける.
#    * 参考: https://tekunabe.hatenablog.jp/entry/2018/12/14/ansible_extra_vars_file
ufw_reset_flag: False

## /etc/default/ufw に対する設定 (基本的に変更する必要はない)
#  ※ 注意事項
#    pythonの文字列リテラルで指定する場合は'"string"'の形で指定する(""を入れる)
#    yes / no の指定は'yes'の形で指定する(""を入れない)
#    ファイルパスはもともとの表記に合わせて""を入れていない
ufw_default:
  IPV6: 'yes'
  DEFAULT_INPUT_POLICY: '"DROP"'
  DEFAULT_OUTPUT_POLICY: '"ACCEPT"'
  DEFAULT_FORWARD_POLICY: '"DROP"'
  DEFAULT_APPLICATION_POLICY: '"SKIP"'
  MANAGE_BUILTINS: 'no'
  IPT_SYSCTL: '/etc/ufw/sysctl.conf'
  IPT_MODULES: '"nf_conntrack_ftp nf_nat_ftp nf_conntrack_netbios_ns"'


### 追加設定 #######################################################################################
## 全ポートの開放を許可する IP アドレスリスト
#  * group_vars に書く必要あり.
#  * 設定例を下記に示す.
ufw_white_ip_list: []
## 設定例
# ufw_white_ip_list:
#   - "198.51.100.1"      # 特定のアドレスを指定
#   - "192.0.2.0/24"      # ネットワークアドレスを指定
#   - "127.0.0.1"

## 特定のポートを開放する ufw の設定リスト
ufw_port_settings: []
## 設定例
# 例1. 基本的な書き方
# ufw_port_settings:
#   - to_port: "80"           # ポート番号 (必須).         ufw モジュールの to_port と同じ形式
#     rule: "allow"           # ルール (省略時は "allow"). ufw モジュールの rules と同じ形式
#     proto: "tcp"            # トランスポート層のプロトコル (省略時は "any"). ufw モジュールの proto と同じ形式
#     from_ip_list:           # IP アドレスの一覧 (必須). リストで定義する.
#       - "any"
#
# 例2. 80/tcp と 443/tcp を同時に開放.
# ufw_port_settings:
#   - to_port: "80,443"       # 複数ポート指定可能. 書き方は ufw コマンドでの設定時と同じ.
#     rule: "allow"
#     proto: "tcp"
#     from_ip_list:
#       - "any"
#
# 例3. 特定の IP アドレスに対して 22/tcp を開放
#   - to_port: "22"           # 22番 (ssh) を指定
#     rule: "allow"
#     proto: "tcp"            # TCP プロトコルを指定
#     from_ip_list:
#       - "198.51.100.1"      # 特定のアドレスを指定
#       - "192.0.2.0/24"      # ネットワークアドレスを指定
#
# 例4. 省略例
#   - to_port: "22"           # 22番 (ssh) を指定
#     proto: "tcp"            # TCP プロトコルを指定
#     from_ip_list:
#       - "198.51.100.1"      # 特定のアドレスを指定
#       - "192.0.2.0/24"      # ネットワークアドレスを指定
```

<br>

### Example playbook

```yaml
- hosts:
    - servers
  become: True
  roles:
    - { role: ufw, tags: ["ufw"] }
```

<br>

## 後方互換性について

### 削除された変数の一覧

次の変数は group_vars からは削除してもらって大丈夫です.

* `ufw_state` と `ufw_policy`
  * 万が一本番環境で `ufw_state: disable` や `ufw_policy: allow` が設定されたまま気づかなかった場合危険なため削除しました.
  * ローカル環境において ufw の設定を解除したい場合は, `ufw_state: disable` や `ufw_policy: allow` を設定する代わりに ufw role を使用しないようにしてください.

* `ufw_allow_ssh_from_anyware`
  * `ufw_port_settings` を用いて同じ設定が可能なため削除しました.
* `ufw_allow_ssh_from_ip_list`
  * `ufw_port_settings` を用いて同じ設定が可能なため削除しました.
* `ufw_package`
  * タスク中に直書きでパッケージを指定するように変更したためこの変数は削除しました.

<br>

## Licence
MIT
