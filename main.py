import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
import google.generativeai as genai
from io import StringIO

# --- 定数 ---
PROMPTS_FILE = "system_prompts.csv"

# --- 関数 ---

def load_prompts():
    """システムプロンプトをCSVファイルから読み込む"""
    if os.path.exists(PROMPTS_FILE):
        return pd.read_csv(PROMPTS_FILE)
    else:
        # ファイルが存在しない場合は、デフォルトのプロンプトを持つDataFrameを返す
        default_prompts = {
            "title": ["デフォルトの要約プロンプト"],
            "prompt": ["以下のウェブサイトのコンテンツを簡潔に要約してください。重要なポイントを箇条書きで示してください。\n\n---\n{content}"]
        }
        df = pd.DataFrame(default_prompts)
        df.to_csv(PROMPTS_FILE, index=False)
        return df

def save_prompt(title, prompt, prompts_df):
    """新しいプロンプトをDataFrameに追加し、CSVに保存する"""
    new_prompt = pd.DataFrame([{"title": title, "prompt": prompt}])
    prompts_df = pd.concat([prompts_df, new_prompt], ignore_index=True)
    prompts_df.to_csv(PROMPTS_FILE, index=False)
    return prompts_df

def get_website_text(url):
    """URLからウェブサイトのテキストコンテンツを取得する"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        soup = BeautifulSoup(response.content, 'html.parser')
        # 主要なテキストコンテンツを抽出（bodyタグ全体など、適宜調整）
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(separator='\n', strip=True)
    except requests.exceptions.RequestException as e:
        st.error(f"URLの取得に失敗しました: {e}")
        return None

def summarize_with_gemini(api_key, system_prompt, text_content):
    """Gemini APIを使用してテキストを要約する"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash') # モデル名は適宜変更してください
        prompt = system_prompt.format(content=text_content)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini APIの呼び出し中にエラーが発生しました: {e}")
        return None

def generate_title_with_gemini(api_key, summary_text):
    """Gemini APIを使用して要約からタイトルを生成する"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')  # モデル名は適宜変更
        prompt = f"以下の要約に最適な短いタイトルを生成してください。一つだけファイル名になるものを考え、それのみを出力してください:\n\n{summary_text}"
        response = model.generate_content(prompt)
        return response.text.strip().replace('"', '')  # タイトルを整形
    except Exception as e:
        st.error(f"Gemini APIでのタイトル生成中にエラーが発生しました: {e}")
        return "無題"

# --- Streamlit UI ---

st.set_page_config(page_title="Website Summarizer", layout="wide")
st.title("AI Website Summarizer")

# --- サイドバー ---
with st.sidebar:
    st.header("設定")

    # APIキー入力
    api_key = st.text_input("Gemini APIキー", type="password", key="api_key_input")

    st.divider()

    # システムプロンプト管理
    st.subheader("システムプロンプト管理")
    prompts_df = load_prompts()

    with st.expander("新規プロンプト保存"):
        uploaded_prompt_file = st.file_uploader("プロンプトファイル (.txt)", type="txt")
        new_prompt_title = st.text_input("このプロンプトのタイトル")
        if st.button("アップロードしたプロンプトを保存"):
            if uploaded_prompt_file is not None and new_prompt_title:
                prompt_content = StringIO(uploaded_prompt_file.getvalue().decode("utf-8")).read()
                prompts_df = save_prompt(new_prompt_title, prompt_content, prompts_df)
                st.success("プロンプトを保存しました！")
                st.rerun() # プロンプト選択肢を更新するために再実行
            else:
                st.warning("ファイルとタイトルの両方を入力してください。")

    # モード選択
    st.divider()
    mode = st.selectbox("モードを選択", ["URLを手入力", "CSVファイルをアップロード"])


# --- メインコンテンツ ---

# プロンプト選択
st.subheader("1. システムプロンプトを選択・編集")
prompt_titles = prompts_df["title"].tolist()
selected_title = st.selectbox("使用するプロンプトを選択", prompt_titles)
selected_prompt_text = prompts_df[prompts_df["title"] == selected_title]["prompt"].iloc[0]

# 選択したプロンプトを編集可能にする
edited_prompt = st.text_area(
    "プロンプトをプレビュー・編集",
    value=selected_prompt_text,
    height=200
)

st.subheader("2. 要約するコンテンツを入力")

# --- モード別UI ---
if mode == "URLを手入力":
    url_input = st.text_input("要約したいウェブサイトのURLを入力")
    if st.button("要約を実行", key="run_url"):
        if not api_key:
            st.warning("Gemini APIキーを入力してください。")
        elif not url_input:
            st.warning("URLを入力してください。")
        else:
            with st.spinner("ウェブサイトのコンテンツを取得中..."):
                content = get_website_text(url_input)

            if content:
                with st.spinner("Geminiが要約を生成中..."):
                    summary = summarize_with_gemini(api_key, edited_prompt, content)

                st.subheader("要約結果")
                if summary:
                    with st.spinner("Geminiがタイトルを生成中..."):
                        title = generate_title_with_gemini(api_key, summary)
                    st.subheader("要約結果")
                    st.markdown(f"# {title}\n\n{summary}")

                    st.download_button(
                        label="マークダウンとしてダウンロード",
                        data=f"# {title}\n\n{summary}",
                        file_name=f"{title}.md",
                        mime="text/markdown",
                    )
                else:
                    st.error("要約の生成に失敗しました。")

elif mode == "CSVファイルをアップロード":
    uploaded_csv_file = st.file_uploader("URLリストを含むCSVファイルをアップロード", type="csv")

    if uploaded_csv_file is not None:
        try:
            df_urls = pd.read_csv(uploaded_csv_file)
            if 'list' not in df_urls.columns:
                st.error("CSVファイルには 'list' という名前のカラムが必要です。")
            else:
                st.write("アップロードされたCSVのプレビュー:")
                st.dataframe(df_urls)

                if st.button("一括要約を実行", key="run_csv"):
                    if not api_key:
                        st.warning("Gemini APIキーを入力してください。")
                    else:
                        results = []
                        progress_bar = st.progress(0)
                        total_urls = len(df_urls)

                        for i, row in df_urls.iterrows():
                            url = row['list']
                            st.write(f"{i+1}/{total_urls}: {url} を処理中...")
                            content = get_website_text(url)
                            if content:
                                summary = summarize_with_gemini(api_key, edited_prompt, content)
                                results.append(summary or "要約失敗")
                            else:
                                results.append("コンテンツ取得失敗")
                            progress_bar.progress((i + 1) / total_urls)

                        df_urls['summary'] = results
                        st.subheader("処理結果")
                        st.dataframe(df_urls)

                        csv_output = df_urls.to_csv(index=False).encode('cp932')
                        st.download_button(
                            label="結果をCSVとしてダウンロード",
                            data=csv_output,
                            file_name="summary_results.csv",
                            mime="text/csv",
                        )
        except Exception as e:
            st.error(f"CSVファイルの処理中にエラーが発生しました: {e}")