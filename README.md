# アイドルで理解するSelenium


## Blog

アイドルで理解するSelenium - リンクを見つけて移動するだけ

https://nao-y.hatenablog.com/entry/2020/05/13/235752

## Summary

CHEERZから任意のアイドルの画像をダウンロードするスクリプトです。

CHEERZのartist idを指定することで、`https://cheerz.cz/artist/{arist_id}/community` に投稿された画像をダウンロードできます。

`cheerz.cz/robots.txt`は以下のようになっており、許容範囲内のスクレイピングです。

```
User-agent: *
Disallow:
```

## Usage

```
$ git clone git@github.com:NaoY-2501/selenium_with_idol.git
$ cd selemium_with_idol
```

[`chromedriver-binary`](https://pypi.org/project/chromedriver-binary/)は手元のChromeのバージョンに合ったものをインストールしてください。

[chromedriver-binary Release history](https://pypi.org/project/chromedriver-binary/#history)


```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ pip install chromedriver-binary=={version}
(venv) $ python scraping.py
CHEERZ artist ID: 880
directory name (Optional. Default is artist id.): kanzaki fuka
Fetch page sources.
Accomplished. 44 sources has fetched.
Extract image URLs.
Accomplished. 865 URLs has extracted.
Save images.
100%|████████████████████|  865/865 [06:08<00:00,  2.35it/s]
Accomplished.
```

一度、実行した後に画像が追加されても同じディレクトリを指定すれば差分のみダウンロードされます。

```
(venv) $ python scraping.py
CHEERZ artist ID: 8466
directory name (Optional. Default is artist id.): yamagata hanna
Fetch page sources.
Accomplished. 7 sources has fetched.
Extract image URLs.
Accomplished. 135 URLs has extracted.
Save images.
Exist images: 133
New Images: 2
100%|████████████████████|  2/2 [00:00<00:00,  2.31it/s]
Accomplished.
```