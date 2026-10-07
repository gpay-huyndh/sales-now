**Hãy dịch yêu cầu này từ tiếng Nhật và trả lời.** 

# **【Webスクレイピングおよびデータ抽出課題】**

## **1\. 概要**

本テストは、実務におけるデータ収集能力、技術選定の思考プロセス、および生成AIを効果的に活用するスキルを評価するための実技試験です。開始時刻から9時間以内に指定した方法で提出してください。指定時刻時点でのcommit内容で評価します。時間内に完了していなくてもアプローチのプロセスを評価しますので指定時刻までに完成した範囲をcommitしてください。

## **2\. 課題A 会社HPからのデータ取得**

以下の上場企業10社のURLリストをインプット（入力データ）として使用し、リンクを辿る形で各企業の公式サイトのデータをスクレイピングし、生成AIを利用して指定のデータを抽出してください。サイトごとにデザインや構造が異なるため、高い汎用性を持たせてください。作成した環境の構築方法、実行方法は README.md に日本語で作成してください。

* **対象サイト：**

| 企業名 | URL |
| ----- | ----- |
| ニッスイ | [https\://www\.nissui.co.jp/](https://www.nissui.co.jp/) |
| Ｕｍｉｏｓ | [https\://www\.umios.com/](https://www.umios.com/) |
| ユキグニファクトリー | [https\://www\.yukiguni-factory.co.jp/](https://www.yukiguni-factory.co.jp/) |
| サカタのタネ | [https\://www\.sakataseed.co.jp/](https://www.sakataseed.co.jp/) |
| ホクト | [https\://www\.hokto-kinoko.co.jp/](https://www.hokto-kinoko.co.jp/) |
| ショーボンドホールディングス | [https\://www\.sho-bondhd.jp/](https://www.sho-bondhd.jp/) |
| ミライト・ワン | [https\://www\.mirait-one.com/](https://www.mirait-one.com/) |
| タマホーム | [https\://www\.tamahome.jp/](https://www.tamahome.jp/) |
| 極洋 | [https\://www\.kyokuyo.co.jp/](https://www.kyokuyo.co.jp/) |
| 日本アクア | [https\://www\.n-aqua.jp/](https://www.n-aqua.jp/) |

* **抽出対象データ：**本社住所、代表氏名、資本金、設立年月


## **3\. 課題B Bot対策サイトへの挑戦【加点項目・任意】**

（課題Aが完全に終わった方のみ）一般的なスクレイピング手法ではブロックされるサイトからのデータ取得に挑戦してください。

* **対象ページ：[https\://vn.indeed.com/jobs?q=remote](https://vn.indeed.com/jobs?q=remote)**  
* **報告内容 (**report.md **に記載):**  
  * どのようなBot対策が行われているか  
  * それに対してどのようなアプローチを試み、結果どうなったか

## **4\. 技術選定とアプローチの比較検討**

データを取得するにあたり、複数の手段（各種ライブラリ、フレームワーク、ノーコードツール、生成AIのAPI活用など）を比較検討してください。  
　例：Python＋Playwright＋LangChain、TypeScript＋Firecrawl＋Vercel AI SDK、Dify、n8n  
比較の際は、以下の3つの軸を中心とした評価と、そこからの選定理由を report.md に作成してください。

* **コスト (Cost):** 開発にかかる時間、インフラ費用、ツール利用料など  
* **スピード (Speed):** 開発スピードおよびデータ取得の実行速度  
* **品質・網羅性 (Quality / Completeness):** データの正確性と取りこぼしの少なさ

## 

## **5\. 生成AIの使用について**

本課題では、ChatGPT、Claude、GitHub Copilotなどの**生成AIを自由に使用して構いません。**  
ただし、以下の条件を遵守してください。  
⚠️ **必須条件:** ChatGPTやClaudeなどのチャット型AIを使用した場合は、そのプロンプトと回答の履歴（または共有リンク）を提出してください。

## 

## **6\. 提出方法**

成果物はすべて**GitHub**経由で提出してください。

1. **リポジトリの作成:** プライベートリポジトリを作成してください。  
2. **アクセス権の付与:** 弊社が指定する以下3名のGitHub IDをコラボレーターとして招待してください。  
   * atsunori0406  
   * salesnow-tomohiro  
3. **ディレクトリ構造（推奨）:** リポジトリ内は以下のように整理してください。  
   `├── prompts/      # 生成AIに使用したプロンプトの履歴（txt形式）`  
   `├── result/       # 取得したデータ（CSVまたはJSON形式）`  
   `├── src/          # 実際に作成したソースコード一式`  
   `├── README.md     # 環境構築方法、実行方法の手順書`  
   `└── report.md     # 技術選定の比較表、Bの考察結果`

## 

## **7\. 評価基準**

* **理解力:** 課題の本質を正しく理解できているか。  
* **設計力:** コスト・スピード・品質を考慮した適切な技術選定ができているか。  
* **AI活用力:** 生成AIを効率的に使いこなし、適切なフローを構築できているか。  
* **ドキュメンテーション：**第三者が見てわかりやすいドキュメントがかけているか。
