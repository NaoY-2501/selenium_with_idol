# アイドルで理解するSelenium


## Blog

TBA.

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
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ python scraping.py
CHEERZ artist ID: 880
directory name (Optional. Default is artist id.): kanzaki fuka
Fetch page sources.
Accomplished. 44 sources has fetched.
Extract image URLs.
Accomplished. 865 URLs has extracted.
Save images.
100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 865/865 [06:08<00:00,  2.35it/s]
Accomplished.
```

一度、実行した後に画像が追加されても同じディレクトリを指定すれば差分のみダウンロードされます。