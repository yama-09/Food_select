import streamlit as st
import pandas as pd
import chardet

# ページ設定
st.set_page_config(page_title="食品登録 デモ", page_icon="🍴", layout="wide")

# CSSスタイルでカードのデザインを定義
st.markdown("""
    <style>
        .card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            font-weight: bold;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# タイトル
st.markdown("<h1 style='text-align: center;'>食品登録 デモ</h1>", unsafe_allow_html=True)

# ファイルのアップロード
st.markdown("### ExcelまたはCSVファイルをアップロードしてください")
uploaded_file = st.file_uploader("対応ファイル: .xlsx, .xls, .csv", type=["xlsx", "xls", "csv"])

# セッションステートを初期化
if "selected_data" not in st.session_state:
    st.session_state.selected_data = None

if uploaded_file:
    try:
        # ファイルの種類によって読み込み処理を変更
        if uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith(".csv"):
            # エンコーディングを自動検出
            raw_data = uploaded_file.getvalue()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

            # 検出されたエンコーディングでCSVを読み込む
            df = pd.read_csv(uploaded_file, encoding=encoding)
        else:
            st.error("対応していないファイル形式です。ExcelまたはCSVファイルをアップロードしてください。")
        
        # カラムの選択セクション
        st.markdown("### カラムを選択してください")
        column_list = df.columns.tolist()
        selected_column = st.selectbox("カラム名", column_list)
        
        # 登録ボタン
        if st.button("登録"):
            st.session_state.selected_data = df[selected_column].dropna().unique()
        
        # 選択されたデータの表示
        if st.session_state.selected_data is not None:
            st.markdown(f"## 選択されたカラム: **{selected_column}**")
            st.markdown("### 重複を除いた値:")

            # カード形式でデータを表示
            for value in st.session_state.selected_data:
                st.markdown(f"<div class='card'>{value}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
