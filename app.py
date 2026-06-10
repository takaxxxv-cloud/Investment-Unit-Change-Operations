import streamlit as st

# ページのタイトル設定
st.set_page_config(page_title="口数変更オペレーション判定", page_icon="🏢", layout="centered")

# 【最新データ定義】修正いただいたテキストファイルを100%反映
TREE_DATA = {
    # --- スタート ---
    "start": {
        "type": "question",
        "text": "【ステップ1】対象ファンドの「募集方式」を選択してください [cite: 1]",
        "choices": [
            {"text": "1. 先着方式", "next": "mode_first_come"},
            {"text": "2. 抽選方式", "next": "mode_lottery"}
        ]
    },

    # --- 1. 先着方式 ---
    "mode_first_come": {
        "type": "question",
        "text": "【先着】「応募状況（応募率）」を選択してください [cite: 1]",
        "choices": [
            {"text": "A. 応募率 100% 以内 [枠あり]", "next": "fc_under_100"},
            {"text": "B. 応募率 100% 超え [満額・キャンセル待ち]", "next": "fc_over_100"}
        ]
    },
    "fc_under_100": {
        "type": "result",
        "status": "info",
        "text": "💡 【オペレーション】\n\nキャンセル後、再応募 [cite: 1]"
    },
    "fc_over_100": {
        "type": "question",
        "text": "【先着：100%超え】変更内容の「方向性」を選択してください [cite: 2, 3, 4]",
        "choices": [
            {"text": "a. 口数増加", "next": "fc_over_inc"},
            {"text": "b. 口数減少", "next": "fc_over_dec"}
        ]
    },
    "fc_over_inc": {
        "type": "result",
        "status": "info",
        "text": "💡 【オペレーション】\n\n預り口譲渡（増額分） [cite: 3]"
    },
    "fc_over_dec": {
        "type": "question",
        "text": "【先着：100%超え：減少】投資家の「同意」はありますか？ [cite: 4]",
        "choices": [
            {"text": "① 同意あり", "next": "fc_over_dec_agreed"},
            {"text": "② 同意なし", "next": "fc_over_dec_no_agree"}
        ]
    },
    "fc_over_dec_agreed": {
        "type": "result",
        "status": "info",
        "text": "💡 【オペレーション】\n\n【Ⅰ】キャンセル。希望口数を預り口譲渡。 [cite: 4]"
    },
    "fc_over_dec_no_agree": {
        "type": "question",
        "text": "【先着：100%超え：減少：同意なし】「応募口数」はどちらですか？ [cite: 4, 5]",
        "choices": [
            {"text": "α. 応募口数 999口以下", "next": "fc_over_dec_999"},
            {"text": "β. 応募口数 1000口以上", "next": "fc_over_dec_1000"}
        ]
    },
    "fc_over_dec_999": {
        "type": "result",
        "status": "info",
        "text": "💡 【オペレーション】\n\n【Ⅱ】出資確定期限切れを待ち、再抽選対象にして希望口数を割当 [cite: 6]"
    },
    "fc_over_dec_1000": {
        "type": "result",
        "status": "warning",
        "text": "🚨 【要確認オペレーション】\n\n吉田に相談。【Ⅰ】or【Ⅱ】の判断をしてもらう [cite: 7]"
    },

    # --- 2. 抽選方式 ---
    "mode_lottery": {
        "type": "question",
        "text": "【抽選】募集の「フェーズ」を選択してください [cite: 7]",
        "choices": [
            {"text": "A. 募集中 [締切前]", "next": "lot_during_campaign"},
            {"text": "B. 募集終了後 [抽選前・当選発表後]", "next": "lot_after_campaign"}
        ]
    },
    "lot_during_campaign": {
        "type": "result",
        "status": "info",
        "text": "💡 【オペレーション】\n\n投資家側で口数変更してもらう。 [cite: 8]"
    },
    "lot_after_campaign": {
        "type": "question",
        "text": "【抽選：募集終了後】変更内容の「方向性」を選択してください [cite: 8, 9, 10]",
        "choices": [
            {"text": "a. 口数増加", "next": "lot_aft_inc"},
            {"text": "b. 口数減少", "next": "lot_aft_dec"}
        ]
    },
    "lot_aft_inc": {
        "type": "result",
        "status": "info",
        "text": "💡 【オペレーション】\n\n原則不可。 [cite: 9]"
    },
    "lot_aft_dec": {
        "type": "question",
        "text": "【抽選：募集終了後：減少】投資家の「同意」はありますか？ [cite: 10]",
        "choices": [
            {"text": "① 同意あり", "next": "lot_aft_dec_agreed"},
            {"text": "② 同意なし", "next": "lot_aft_dec_no_agree"}
        ]
    },
    "lot_aft_dec_agreed": {
        "type": "result",
        "status": "info",
        "text": "💡 【オペレーション】\n\n【I】キャンセル。希望口数を預り口譲渡。 [cite: 10]"
    },
    "lot_aft_dec_no_agree": {
        "type": "question",
        "text": "【抽選：募集終了後：減少：同意なし】「応募口数」はどちらですか？ [cite: 10, 11]",
        "choices": [
            {"text": "α. 応募口数 999口以下", "next": "lot_aft_dec_999"},
            {"text": "β. 応募口数 1000口以上", "next": "lot_aft_dec_1000"}
        ]
    },
    "lot_aft_dec_999": {
        "type": "result",
        "status": "info",
        "text": "💡 【オペレーション】\n\n【Ⅱ】出資確定期限切れを待ち、再抽選対象にして希望口数を割当 [cite: 12]"
    },
    "lot_aft_dec_1000": {
        "type": "result",
        "status": "warning",
        "text": "🚨 【要確認オペレーション】\n\n吉田に相談。【Ⅰ】or【Ⅱ】の判断をしてもらう [cite: 13]"
    }
}

# アプリの状態管理（今どこにいるか）を初期化
if "current_node" not in st.session_state:
    st.session_state.current_node = "start"

# メインUIの描画
st.title("🏢 不動産クラファン 口数変更オペレーション判定")
st.write("該当する項目を順に選択してください。最終的な業務手順が表示されます。")
st.write("---")

# 現在のノードデータを取得
current_id = st.session_state.current_node
node = TREE_DATA[current_id]

if node["type"] == "question":
    # 質問の表示
    st.subheader(node["text"])
    st.write("")
    
    # 選択肢の数に応じてボタンを横並びで自動生成
    cols = st.columns(len(node["choices"]))
    for idx, choice in enumerate(node["choices"]):
        with cols[idx]:
            if st.button(choice["text"], use_container_width=True, type="primary"):
                st.session_state.current_node = choice["next"]
                st.rerun()

elif node["type"] == "result":
    # 結果の表示（ステータスに応じて見た目を変える）
    if node["status"] == "warning":
        st.warning(node["text"])
    else:
        st.info(node["text"])
        st.success("判定が完了しました。")
    
    st.write("")
    
    # やり直しボタン
    if st.button("トップに戻る（他の案件を判定する）", use_container_width=True):
        st.session_state.current_node = "start"
        st.rerun()