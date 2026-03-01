import os
import anthropic

# 環境変数から取得
api_key = os.environ["ANTHROPIC_API_KEY"]
issue_title = os.environ.get("ISSUE_TITLE", "")
issue_body = os.environ.get("ISSUE_BODY", "") or ""
instruction = f"{issue_title}\n{issue_body}".strip()

# 現在のindex.htmlを読み込む
with open("index.html", "r", encoding="utf-8") as f:
    current_html = f.read()

# Claude APIを呼び出す
client = anthropic.Anthropic(api_key=api_key)

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8096,
    messages=[
        {
            "role": "user",
            "content": f"""あなたは家計管理アプリのメンテナンス担当です。
以下のindex.htmlファイルに対して、指示に従って変更を加えてください。

【指示】
{instruction}

【重要なルール】
- 変更後の完全なHTMLファイルのみを出力してください
- コードブロック（```）は使わないでください
- 説明文も不要です
- HTMLの<!DOCTYPE html>から始めて</html>で終わる完全なファイルを出力してください
- 既存のデータ（取引データのSEED、借金データ等）は必ず保持してください
- localStorageのシードバージョンキーを一つ上げてください（例: v5→v6）

【現在のindex.html】
{current_html}
"""
        }
    ]
)

# 結果を保存
updated_html = message.content[0].text.strip()

# 念のため<!DOCTYPE html>から始まるか確認
if not updated_html.startswith("<!DOCTYPE") and not updated_html.startswith("<html"):
    # HTMLの開始位置を探す
    start = updated_html.find("<!DOCTYPE")
    if start == -1:
        start = updated_html.find("<html")
    if start != -1:
        updated_html = updated_html[start:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(updated_html)

print(f"✅ 変更完了: {instruction[:50]}")
