import streamlit as st
import pandas as pd

# ページ設定
st.set_page_config(page_title="Excelカラム選択デモ", page_icon="📊", layout="wide")

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
st.markdown("<h1 style='text-align: center;'>Excel 食材選択デモ</h1>", unsafe_allow_html=True)

# Excelファイルのアップロード
st.markdown("### Excelファイルをアップロードしてください")
uploaded_file = st.file_uploader("Excelファイルを選択", type=["xlsx", "xls"])

# セッションステートを初期化
if "selected_data" not in st.session_state:
    st.session_state.selected_data = None

if uploaded_file:
    try:
        # ExcelファイルをDataFrameとして読み込む
        df = pd.read_excel(uploaded_file)
        
        # カラムの選択セクション
        st.markdown("### Excel内の情報を選択してください")
        column_list = df.columns.tolist()
        selected_column = st.selectbox("カラム名", column_list)
        
        # 登録ボタン
        if st.button("登録"):
            st.session_state.selected_data = df[selected_column].dropna().unique()
        
        # 選択されたデータの表示
        if st.session_state.selected_data is not None:
            st.markdown(f"### 選択された情報: **{selected_column}**")

            # カード形式でデータを表示
            for value in st.session_state.selected_data:
                st.markdown(f"<div class='card'>{value}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
