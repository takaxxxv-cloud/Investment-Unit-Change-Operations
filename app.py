import streamlit as st

# ページのタイトル設定
st.set_page_config(page_title="口数変更オペレーション判定", page_icon="🏢", layout="centered")

# ==========================================
# ✨ 高級感を演出するカスタムCSSスキン
# ==========================================
st.markdown("""
    <style>
    /* 全体の背景とベースフォントの設定 */
    .stApp {
        background-color: #0d131f; /* 深いサファイアネイビー */
        color: #f1f5f9;
    }
    
    /* タイトル（H1）のデザイン */
    h1 {
        font-family: 'Times New Roman', 'Noto Serif JP', serif;
        color: #dfc59f !important; /* シャンパンゴールド */
        font-weight: 400;
        letter-spacing: 0.05em;
        border-bottom: 1px solid rgba(223, 197, 159, 0.3);
        padding-bottom: 15px;
        margin-bottom: 30px !important;
    }
    
    /* サブタイトル（H3・質問文）のデザイン */
    h3 {
        font-family: 'Helvetica Neue', 'Noto Sans JP', sans-serif;
        color: #ffffff !important;
        font-weight: 500;
        letter-spacing: 0.03em;
        line-height: 1.6;
    }
    
    /* 説明文（通常のテキスト） */
    .stMarkdown p {
        color: #94a3b8; /* 静かなプラチナグレー */
        font-size: 15px;
    }
    
    /* 2択ボタン（st.button）のラグジュアリー化 */
    div.stButton > button {
        background-color: #172237 !important; /* ボタン背景（重厚なネイビー） */
        color: #dfc59f !important; /* 文字色（ゴールド） */
        border: 1px solid #dfc59f !important; /* ゴールドの繊細な枠線 */
        border-radius: 4px !important; /* 角丸を少しシャープに */
        padding: 16px 24px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* ボタンにマウスを乗せたとき（ホバー効果） */
    div.stButton > button:hover {
        background-color: #dfc59f !important; /* 背景がゴールドに反転 */
        color: #0d131f !important; /* 文字がネイビーに反転 */
        box-shadow: 0 6px 20px rgba(223, 197, 159, 0.3);
        transform: translateY(-2px);
    }
    
    /* 通常の結果ボックス（st.info）のカスタム */
    div[data-testid="stNotificationV2"] {
        background-color: #1a2436 !important;
        border-left: 4px solid #dfc59f !important; /* 左側にゴールドのアクセント */
        color: #ffffff !important;
        border-radius: 4px;
    }
    
    /* 吉田さん相談などの警告（st.warning）のカスタム */
    div[data-testid="stNotificationV2"]:has(.st-ae) {
        background-color: #2c1a1a !important;
        border-left: 4px solid #ef4444 !important; /* イレギュラーは警告の赤 */
    }
    
    /* 区切り線 */
    hr {
        border-color: rgba(223, 197, 159, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)


# 【データ定義】
TREE_DATA = {
    # --- スタート ---
    "start": {
        "type": "question",
        "text": "【ステップ1】対象ファンドの「募集方式」を選択してください",
        "choices": [
            {"text": "1. 先着方式", "next": "mode_first_come"},
            {"text": "2. 抽選方式", "next": "mode_lottery"}
        ]
    },

    # --- 1. 先着方式 ---
    "mode_first_come": {
        "type": "question",
        "text": "【先着】「応募状況（応募率）」を選択してください",
        "choices": [
            {"text": "A. 応募率 100% 以内", "next": "fc_under_100"},
            {"text": "B. 応募率 100% 超え", "next": "fc_over_100"}
        ]
    },
    "fc_under_100": {
        "type": "result",
        "status": "info",
        "text": "🏛️ 【確定オペレーション】\n\nキャンセル後、再応募の手続きを進めてください。"
    },
    "fc_over_100": {
        "type": "question",
        "text": "【先着：100%超え】変更内容の「方向性」を選択してください",
        "choices": [
            {"text": "a. 口数増加", "next": "fc_over_inc"},
            {"text": "b. 口数減少", "next": "fc_over_dec"}
        ]
    },
    "fc_over_inc": {
        "type": "result",
        "status": "warning",
        "text": """👑 **【要確認エスカレーション】**

預り口譲渡（増額分）の処理対象です。

吉田に増額分の口数を伝えて、譲渡の案内をしてもいいか最終判断を仰いでください。"""
    },
    "fc_over_dec": {
        "type": "question",
        "text": "【先着：100%超え：減少】投資家の「同意」はありますか？",
        "choices": [
            {"text": "① 同意あり", "next": "fc_over_dec_agreed"},
            {"text": "② 同意なし", "next": "fc_over_dec_no_agree"}
        ]
    },
    "fc_over_dec_agreed": {
        "type": "result",
        "status": "info",
        # 👇 【先着・同意あり減少】のテキストをアップデート
        "text": "🏛️ 【確定オペレーション】\n\n【Ⅰ】キャンセルを実行し、希望口数を預り口譲渡へ回します。\n\n減らす口数を吉田に報告し、その分の割当を依頼してください。"
    },
    "fc_over_dec_no_agree": {
        "type": "question",
        "text": "【先着：100%超え：減少：同意なし】「応募口数」の規模を選択してください",
        "choices": [
            {"text": "α. 応募口数 999口以下", "next": "fc_over_dec_999"},
            {"text": "β. 応募口数 1000口以上", "next": "fc_over_dec_1000"}
        ]
    },
    "fc_over_dec_999": {
        "type": "result",
        "status": "info",
        "text": "🏛️ 【確定オペレーション】\n\n【Ⅱ】出資確定期限切れを待ち、再抽選対象にして希望口数を割り当てます。"
    },
    "fc_over_dec_1000": {
        "type": "result",
        "status": "warning",
        "text": """👑 **【要確認エスカレーション】**

本案件は大口（1000口以上）かつ同意なしの例外処理となります。
吉田に相談の上、【Ⅰ】または【Ⅱ】の最終判断を仰いでください。

* **【Ⅰ】キャンセル、希望口数を預り口譲渡**
* **【Ⅱ】出資確定期限切れを待ち、再抽選対象にして希望口数を割当**"""
    },

    # --- 2. 抽選方式 ---
    "mode_lottery": {
        "type": "question",
        "text": "【抽選】募集の「フェーズ」を選択してください",
        "choices": [
            {"text": "A. 募集中 [締切前]", "next": "lot_during_campaign"},
            {"text": "B. 募集終了後 [抽選前・当選発表後]", "next": "lot_after_campaign"}
        ]
    },
    "lot_during_campaign": {
        "type": "result",
        "status": "info",
        "text": "🏛️ 【確定オペレーション】\n\n投資家マイページより、投資家側で直接口数変更を行ってもらうよう案内してください。"
    },
    "lot_after_campaign": {
        "type": "question",
        "text": "【抽選：募集終了後】変更内容の「方向性」を選択してください",
        "choices": [
            {"text": "a. 口数増加", "next": "lot_aft_inc"},
            {"text": "b. 口数減少", "next": "lot_aft_dec"}
        ]
    },
    "lot_aft_inc": {
        "type": "result",
        "status": "info",
        "text": "🏛️ 【確定オペレーション】\n\n原則受付不可となります。"
    },
    "lot_aft_dec": {
        "type": "question",
        "text": "【抽選：募集終了後：減少】投資家の「同意」はありますか？",
        "choices": [
            {"text": "① 同意あり", "next": "lot_aft_dec_agreed"},
            {"text": "② 同意なし", "next": "lot_aft_dec_no_agree"}
        ]
    },
    "lot_aft_dec_agreed": {
        "type": "result",
        "status": "info",
        # 👇 【抽選・同意あり減少】のテキストをアップデート
        "text": "🏛️ 【確定オペレーション】\n\n【I】キャンセルを実行し、希望口数を預り口譲渡へ回します。\n\n減らす口数を吉田に報告し、その分の割当を依頼してください。"
    },
    "lot_aft_dec_no_agree": {
        "type": "question",
        "text": "【抽選：募集終了後：減少：同意なし】「応募口数」の規模を選択してください",
        "choices": [
            {"text": "α. 応募口数 999口以下", "next": "lot_aft_dec_999"},
            {"text": "β. 応募口数 1000口以上", "next": "lot_aft_dec_1000"}
        ]
    },
    "lot_aft_dec_999": {
        "type": "result",
        "status": "info",
        "text": "🏛️ 【確定オペレーション】\n\n【Ⅱ】出資確定期限切れを待ち、再抽選対象にして希望口数を割り当てます。"
    },
    "lot_aft_dec_1000": {
        "type": "result",
        "status": "warning",
        "text": """👑 **【要確認エスカレーション】**

本案件は大口（1000口以上）かつ同意なしの例外処理となります。
吉田に相談の上、【Ⅰ】または【Ⅱ】の最終判断を仰いでください。

* **【Ⅰ】キャンセル、希望口数を預り口譲渡**
* **【Ⅱ】出資確定期限切れを待ち、再抽選対象にして希望口数を割当**"""
    }
}

# アプリの状態管理（今どこにいるか）を初期化
if "current_node" not in st.session_state:
    st.session_state.current_node = "start"

# メインUIの描画
st.title("🏢 Asset Operation Flow Manager")
st.write("不動産クラウドファンディング投資口数変更における、最適化された業務手順の自動判定システム")
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
            if st.button(choice["text"], use_container_width=True):
                st.session_state.current_node = choice["next"]
                st.rerun()

elif node["type"] == "result":
    # 結果の表示（ステータスに応じて見た目を変える）
    if node["status"] == "warning":
        st.warning(node["text"])
    else:
        st.info(node["text"])
    
    st.write("")
    
    # やり直しボタン
    if st.button("メインメニューへ戻る", use_container_width=True):
        st.session_state.current_node = "start"
        st.rerun()
