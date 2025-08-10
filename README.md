# AIウェブサイト要約アプリ

これは、GoogleのGemini APIを使ってウェブサイトの内容を要約するStreamlitアプリケーションです。  
要約したいサイトをcsvのリストにして、まとめて処理も行えます。

> 動作確認はpython3.11で行っています。


## 主な機能

- **URL指定で要約**: ウェブサイトのURLを1つ入力するだけで、そのページの内容をAIが自動で要約します。
- **CSVで一括要約**: 複数のURLをまとめたCSVファイルをアップロードすれば、一度にすべてのウェブサイトを要約できます。
- **プロンプトのカスタマイズ**: AIに要約を依頼する際の指示（プロンプト）を自由に追加・編集できます。
- **ダウンロード機能**: 要約結果をMarkdown形式やCSV形式でダウンロードして保存できます。

## 使い方

### 1. セットアップ（準備）

まず、このアプリケーションをあなたのPCで動かすための準備をします。

**a. ファイルのダウンロード**

Gitというツールを使って、プロジェクトのファイルをダウンロードします。
もしGitをインストールしていない場合は、[ここからダウンロード](https://git-scm.com/downloads)してください。

コマンドプロンプト（またはターミナル）を開いて、以下のコマンドを順番に実行してください。

```bash
# プロジェクトのファイルをPCにコピーします
git clone https://github.com/ryochinbo/website-summarizer.git

# コピーしたプロジェクトのフォルダに移動します
cd website-summarizer
```

**b. 環境構築**

次に、プロジェクトフォルダの中にある `setup.bat` というファイルを実行します。
これをダブルクリックするだけで、アプリケーションに必要なものが自動的に準備されます。

`setup.bat` の中では、以下のことが行われています。

- **仮想環境の作成**: このプロジェクト専用のPython環境を作ります。
- **ライブラリのインストール**: アプリケーションを動かすために必要なライブラリをインストールします。

### 2. アプリケーションの起動

セットアップが終わったら、いよいよアプリケーションを起動します。

プロジェクトフォルダの中にある `run.bat` をダブルクリックしてください。
自動的にブラウザが立ち上がり、アプリケーションの画面が表示されます。


### 3. 使用方法

**a. APIキーの設定**

このアプリを使うには、GoogleのGemini APIキーが必要です。

1.  [Google AI Studio](https://aistudio.google.com/app/apikey)にアクセスして、APIキーを取得します。
2.  取得したAPIキーを、アプリ画面の左側にある「Gemini APIキー」という入力欄に貼り付けます。

**b. 要約の実行**

- **1つのサイトを要約する場合**:
  1.  「モードを選択」で「URLを手入力」を選びます。
  2.  要約したいウェブサイトのURLを入力します。
  3.  「要約を実行」ボタンをクリックします。

- **複数のサイトをまとめて要約する場合**:
  1.  「モードを選択」で「CSVファイルをアップロード」を選びます。
  2.  `list` という名前の列に要約したいURLをまとめたCSVファイルを準備します。
  3.  CSVファイルをアップロードし、「一括要約を実行」ボタンをクリックします。

**システムプロンプトの追加**  
`システムプロンプト管理`の`新規プロンプト保存`をクリック  
追加したいシステムプロンプトをテキストファイル形式で作成し、ドラッグアンドドロップ。  　　
プロンプトのタイトルを記入し、`アップロード`ボタンをクリック


## ⚙️ アプリ (`main.py`)

このアプリケーションの主な動きは `main.py` というファイルに書かれています。


## 📜 ライセンス

このプロジェクトはMITライセンスのもとで公開されています。
自由にお使いいただけます。

```
MIT License

Copyright (c) 2025 ryochinbo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```