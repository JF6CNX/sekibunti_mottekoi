NMR積分データ自動集計ツール
このスクリプトは、NMR解析結果（integrals.txt）を自動収集し、サンプルごと・時間ごとに整理したExcelファイルを生成します。

フォルダ内を再帰的に探索
サンプルごとにシートを分割
time × peak number のマトリクス化
ppm範囲も同時に記録

🧰 必要環境
Python 3.8以上推奨
以下のライブラリ
pip install openpyxl

標準ライブラリ：
os
re
collections

📁 入力データ構造
対象フォルダ：
C:/Users/haruk/chem/nmr（ここは個人で変更する必要があります）

各データは以下の構造を想定：
sample_xxx_1h/
    └── root/
        └── sub/
            └── integrals.txt
📄 integrals.txt のフォーマット

各行は以下の形式：

番号  ppm_start  ppm_end  積分値

例：
1 7.10 7.25 123.45
2 3.45 3.60 67.89
🧠 サンプル名のルール

フォルダ名から自動抽出：
sample_1h
sample_re_1h
_1h, _2h, 1d など → 時間情報
_re → 再測定データとしてそのまま保持

⚙️ 処理内容
1. データ収集
integrals.txt を全探索
サンプル名ごとに分類
peak番号ごとに整理
2. Excel出力形式

各サンプルごとにシート作成：
1行目
time | 1 | 2 | 3 | ...
2行目
ppm  | 7.10–7.25 | 3.45–3.60 | ...
3行目以降
1h   | 123.4 | 56.7 | ...
2h   | ...
💾 出力先
C:/Users/haruk/OneDrive - （個人でパスを変更する必要があります）

▶ 実行方法
python script_name.py

実行後：

Excelファイルを閉じるよう指示される
Enterで処理開始
上書き保存される

⚠️ 注意点
■ Excelが開いていると保存できない
→ PermissionError が出るため、閉じてからEnter

■ フォルダ構造依存
以下の構造に依存：
os.path.dirname(os.path.dirname(os.path.dirname(root)))

構造が変わるとサンプル名抽出が壊れる可能性あり

■ time判定ルール
\d+[dh（個人が設定している時間の単位をここに記載してください）]
例：

1h
12h
1d

📌 特徴
自動データ統合
サンプル別シート生成
ppm範囲保持
re測定データ対応
Excel形式で即解析可能
