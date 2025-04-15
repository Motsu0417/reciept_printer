### ※以下の文章はChatGPTに書かせているので、若干違う可能性ありますがめんどくさくて編集してませんorz
 
# 領収書作成・印刷Webアプリ

このアプリケーションは、Webフォームから入力された情報をもとにPDF形式の領収書を自動生成し、Bluetoothプリンターを使って即時印刷するシステムです。

## 🛠️ 機能

- フォームから宛名・金額・但し書き・日付を入力して領収書PDFを生成
- PDFテンプレートに内容を重ね書きして発行（reciept.pdf をベースに作成）
- 作成済PDFを即時印刷（PDFtoPrinter.exe を使用）
- 印刷完了確認＆失敗時の自動ジョブキャンセル
- 同日内の通し番号付きPDF保存
- Flask + Waitress によるマルチスレッドWebサーバー構成

## 📂 ディレクトリ構成

- `application/`
  - `editPDF.py`：領収書PDFの生成ロジック
  - `printPDF.py`：印刷とジョブ監視ロジック
  - `printer_server.py`：Flaskサーバー本体
  - `RecieptPrinter.bat`：起動用バッチファイル（オプション）
  - `pdftoprinter/`
    - `PDFtoPrinter.exe`：印刷コマンド実行ツール（※別途DL）
  - `noto_sans.ttf`：使用フォント
  - `reciept.pdf`：領収書テンプレートPDF
  - `templates/`
    - `index.html`：入力フォームページ
    - `reprint.html`：再印刷ページ（予定）
- `reciept_files/`：発行済領収書PDFの保存先

## 🚀 実行方法

1. 必要なライブラリをインストール：

    ```bash
    pip install flask waitress pdfrw reportlab pywin32
    ```

2. PDFtoPrinter.exe を別途ダウンロードして配置：

    PDFtoPrinter.exe はこのリポジトリには含まれていません。以下のページから最新版をダウンロードし、`application/pdftoprinter/` に配置してください。

    - ダウンロード先：https://mendelson.org/pdftoprinter.html

    ※ 動作には Microsoft Visual C++ Redistributable（x86）最新版のインストールも必要です。  
    https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

3. Webサーバーを起動：

    ```bash
    python application/printer_server.py
    ```

    ※ コマンドライン操作が面倒な場合は、以下のバッチファイルを実行することでも起動できます：  
    `application/RecieptPrinter.bat`

4. ブラウザでアクセス：

    ```
    http://localhost:8080/
    ```

## 🖨️ 印刷について

- 使用プリンター：Aibecy PT-210 Bluetoothサーマルプリンター  
  （Amazonリンク：https://amzn.asia/d/eNvaNmG）

- このプリンターを使用するには専用ドライバが必要です。以下のページからダウンロードできます：

  - ドライバDL：https://oemdrivers.com/printer-goojprt-pt-210

  ※ ドライバのインストールと初期設定（特にポートと用紙サイズまわり）がちょっと面倒です。
    インストール後にプリンターのプロパティから、ポート・用紙・印刷品質などをしっかり調整してください。

- 印刷には `application/pdftoprinter/PDFtoPrinter.exe` を使用しています。
- 印刷中は `win32print` によってジョブを監視し、最大7秒まで完了を待ちます。
- タイムアウトや印刷失敗の場合は、ジョブを自動でキャンセルします。
- 印刷完了・失敗にかかわらず、発行されたPDFは削除されます。

## ⚙️ 注意事項

- `application/reciept.pdf` は任意のテンプレートPDFに差し替え可能（サイズ：145×54.8mm）
- このサイズは多くのプリンターで標準登録されていないため、Windowsのプリンタードライバに「用紙サイズを手動追加」する必要があります。  
  用紙サイズの追加方法の例：https://faq.nec-lavie.jp/qasearch/1007/app/servlet/relatedqa?QID=021048
- `printPDF.py` 内で使用するプリンター名・用紙サイズを設定してください。

## ✨ 今後の予定（TODO）

- `/reprint` ページからの再印刷対応
- 印刷履歴のログ化（CSV出力など）
- ジョブ別ログ記録とエラーレポート機能追加
