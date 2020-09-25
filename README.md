# webhook_server_templates

webhook(http post)でデータを受け取りその情報を通信したり、htmlで表示したりするアプリ。
ある程度の骨組みを作り（または最後まで作成）、webhookなどで受信して閲覧したりすることをある程度簡単に実装することができるようにすることが目的。

---

## 開発のモチベーション

sigfoxでマイコンでデータを送信してbackendからデータを受信するときにある程度自分なりの様々な閲覧方法に対応できるように変更していきたいと考えたため、このレポジトリを作成することにした。

このレポジトリではsigfox backendからhttp postでデータを受け取り、それをFlaskでデータを受信、sqlに登録する。それをhtmlで閲覧したり、http postをされたら任意のデータを返してそれをまた別のサービスに変換するような形をできるように作成することにした。

またsigfox backendだけでなく、マイコンなどでhttpなどで送信するデータをまた蓄積することもできると考えられるため、ある程度柔軟に対応できるようになればいいかなと望んで作成を行っていく。
（マイコンならMQTTなどのほうがいいのは作成者も理解してます…ただ気楽さなどを考慮したらhttpでやってもいいかなと。）

---

## システム概要

システムの概要は以下の通り

``` system
[様々なhttp postするサービス] -> ngrok -> Flask -> html
                                               |-> sql
                                               |-> http request -> マイコンなどのアプリ作成予定
```

ngrokはherokuやSaasなどでデプロイすることによってクラウドサービスに変換することができる。
ただでもあくまでもデモの作成目的なのでngrokで十分と考えている。

Flaskで作成するのはある程度のキャパを受容できるサーバーのほうが開発の柔軟性が担保できるという考え方があるため採用しました。
もう一つは送られてきたデータをscikit-learnで推論することが簡単にできるようにpythonで実装することで環境の用意を最小限に抑えることができることも目的のひとつである。

---

## 各種ページの遷移図

作成中…
(もしかしたら忘れるかも…)

---

## 実行方法

1.Flaskサーバーを起動する

Flaskサーバーの起動は

```command prompt
python main.py
```

でFlaskサーバーが立ち上がる。

2.ngrokを起動する

ngrokを起動する。Flaskはデバッグモードでの起動にしてあるので

``` command prompt
ngrok http 5000
```

でngrokを起動しURLを確認、URLを踏む。

---

### 参考文献

1. ngrok

- [ngrok - secure introspectable tunnels to localhost](https://ngrok.com/)

2. Flask

- [Welcome to Flask — Flask Documentation (1.1.x)](https://flask.palletsprojects.com/en/1.1.x/)
- [Flaskの簡単な使い方 - Qiita](https://qiita.com/zaburo/items/5091041a5afb2a7dffc8)

3. bootstrap

- [Bootstrap · The most popular HTML, CSS, and JS library in the world.](https://getbootstrap.com/)
- [Bootstrapの基本的な使い方 - Qiita](https://qiita.com/nooonchi/items/224a456df1485d7acd61)
- [はじめよう！Bootstrap - Qiita](https://qiita.com/kitfactory/items/3822a211fceac7c0eb6d)

4. command prompt

- [curl コマンド 使い方メモ - Qiita](https://qiita.com/yasuhiroki/items/a569d3371a66e365316f)
- [curlコマンドでapiを叩く - Qiita](https://qiita.com/buntafujikawa/items/758425773b2239feb9a7)
- [cURLでHTTPステータスコードだけを取得する - Qiita](https://qiita.com/mazgi/items/585348b6cdff3e320726)
- [curl入門 - GET編 - Qiita](https://qiita.com/mame_daifuku/items/98028213060be293416e)
