import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="大会結果 & 戦績・対戦勝率ダッシュボード",
    page_icon="🏆",
    layout="wide"
)

# ------------------------------------------------------------------------------
# 初期データの設定
# ------------------------------------------------------------------------------
if "players" not in st.session_state:
    st.session_state.players = [
        "yuka.", "ミック", "らいせ", "くみえもん", "タルト", "らむね", "れい", "四季" ,"しらす" ,"もふもふ" ,"がらす" ,"リュウ" ,"つくし" ,"すぷわむる" ,"N/A" ,"れんか"
    ]

if "matches" not in st.session_state:
    st.session_state.matches = [
        # 勝者サイド 1回戦
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "勝者サイド", "stage": "1回戦", "winner": "yuka.", "loser": "ミック", "score": "2-0", "mvp": "yuka.", "match_code": "#W1-1"},
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "勝者サイド", "stage": "1回戦", "winner": "くみえもん", "loser": "らいせ", "score": "2-1", "mvp": "くみえもん", "match_code": "#W1-2"},
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "勝者サイド", "stage": "1回戦", "winner": "タルト", "loser": "らむね", "score": "2-0", "mvp": "タルト", "match_code": "#W1-3"},
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "勝者サイド", "stage": "1回戦", "winner": "れい", "loser": "四季", "score": "2-0", "mvp": "れい", "match_code": "#W1-4"},
        
        # 勝者サイド 準決勝
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "勝者サイド", "stage": "準決勝", "winner": "yuka.", "loser": "くみえもん", "score": "2-0", "mvp": "yuka.", "match_code": "#W2-1"},
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "勝者サイド", "stage": "準決勝", "winner": "タルト", "loser": "れい", "score": "2-0", "mvp": "タルト", "match_code": "#W2-2"},
        
        # 勝者サイド 決勝
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "勝者サイド", "stage": "決勝", "winner": "タルト", "loser": "yuka.", "score": "3-2", "mvp": "タルト", "match_code": "#W3-1"},

        # グランドファイナル
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "勝者サイド", "stage": "グランドファイナル", "winner": "タルト", "loser": "らいせ", "score": "3-2", "mvp": "タルト", "match_code": "#W4-1"},

        # 敗者サイド 1回戦
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "敗者サイド", "stage": "1回戦", "winner": "らいせ", "loser": "ミック", "score": "2-0", "mvp": "らいせ", "match_code": "#L1-1"},
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "敗者サイド", "stage": "1回戦", "winner": "四季", "loser": "らむね", "score": "2-0", "mvp": "四季", "match_code": "#L1-2"},
        
        # 敗者サイド 2回戦
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "敗者サイド", "stage": "2回戦", "winner": "らいせ", "loser": "れい", "score": "2-1", "mvp": "らいせ", "match_code": "#L2-1"},
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "敗者サイド", "stage": "2回戦", "winner": "くみえもん", "loser": "四季", "score": "2-1", "mvp": "くみえもん", "match_code": "#L2-2"},
        
        # 敗者サイド 準決勝
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "敗者サイド", "stage": "準決勝", "winner": "らいせ", "loser": "くみえもん", "score": "3-0", "mvp": "らいせ", "match_code": "#L3-1"},
        
        # 敗者サイド 決勝
        {"tournament": "第1回 ゼロセカ マスター部門", "bracket": "敗者サイド", "stage": "決勝", "winner": "らいせ", "loser": "yuka.", "score": "3-0", "mvp": "らいせ", "match_code": "#L4-1"},

        # 第2回大会
        #勝者サイド 1回戦
        {"tournament": "過去のプロセカ大会第1回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "yuka.", "loser": "しらす", "score": "2-0", "mvp": "yuka.", "match_code": "#W1-1"},
        {"tournament": "過去のプロセカ大会第1回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "もふもふ", "loser": "がらす", "score": "2-0", "mvp": "もふもふ", "match_code": "#W1-2"},
        {"tournament": "過去のプロセカ大会第1回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "タルト", "loser": "リュウ", "score": "2-0", "mvp": "タルト", "match_code": "#W1-3"},
        {"tournament": "過去のプロセカ大会第1回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "すぷわむる", "loser": "つくし", "score": "1-2", "mvp": "すぷわむる", "match_code": "#W1-4"},

        # 勝者サイド 準決勝
        {"tournament": "過去のプロセカ大会第1回", "bracket": "勝者サイド", "stage": "準決勝", "winner": "yuka.", "loser": "もふもふ", "score": "2-0", "mvp": "yuka.", "match_code": "#W2-1"},
        {"tournament": "過去のプロセカ大会第1回", "bracket": "勝者サイド", "stage": "準決勝", "winner": "すぷわむる", "loser": "タルト", "score": "2-1", "mvp": "すぷわむる", "match_code": "#W2-2"},
                
        # 勝者サイド 決勝
        {"tournament": "過去のプロセカ大会第1回", "bracket": "勝者サイド", "stage": "決勝", "winner": "yuka.", "loser": "すぷわむる", "score": "3-0", "mvp": "yuka.", "match_code": "#W3-1"},

        # グランドファイナル
        {"tournament": "過去のプロセカ大会第1回", "bracket": "勝者サイド", "stage": "グランドファイナル", "winner": "yuka.", "loser": "すぷわむる", "score": "3-1", "mvp": "yuka.", "match_code": "#W4-1"},

        # 敗者サイド 1回戦
        {"tournament": "過去のプロセカ大会第1回", "bracket": "敗者サイド", "stage": "1回戦", "winner": "しらす", "loser": "がらす", "score": "2-1", "mvp": "しらす", "match_code": "#L1-1"},
        {"tournament": "過去のプロセカ大会第1回", "bracket": "敗者サイド", "stage": "1回戦", "winner": "つくし", "loser": "リュウ", "score": "0-2", "mvp": "つくし", "match_code": "#L1-2"},
                
        # 敗者サイド 2回戦
        {"tournament": "過去のプロセカ大会第1回", "bracket": "敗者サイド", "stage": "2回戦", "winner": "タルト", "loser": "しらす", "score": "0-2", "mvp": "タルト", "match_code": "#L2-1"},
        {"tournament": "過去のプロセカ大会第1回", "bracket": "敗者サイド", "stage": "2回戦", "winner": "つくし", "loser": "もふもふ", "score": "0-2", "mvp": "つくし", "match_code": "#L2-2"},
                
        # 敗者サイド 準決勝
        {"tournament": "過去のプロセカ大会第1回", "bracket": "敗者サイド", "stage": "準決勝", "winner": "タルト", "loser": "つくし", "score": "3-1", "mvp": "らいせ", "match_code": "#L3-1"},
                
        # 敗者サイド 決勝
        {"tournament": "過去のプロセカ大会第1回", "bracket": "敗者サイド", "stage": "決勝", "winner": "すぷわむる", "loser": "タルト", "score": "0-3", "mvp": "すぷわむる", "match_code": "#L4-1"},

        # 「過去のプロセカ大会第2回」の試合データ一覧
        # --- 🟠 勝者サイド ---
        # 1回戦
        {"tournament": "過去のプロセカ大会第2回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "yuka.", "loser": "がらす", "score": "0-0", "mvp": "yuka.", "match_code": "#W1-1"},
        {"tournament": "過去のプロセカ大会第2回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "リュウ", "loser": "つくし", "score": "0-DQ", "mvp": "リュウ", "match_code": "#W1-2"},
        {"tournament": "過去のプロセカ大会第2回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "タルト", "loser": "四季", "score": "2-0", "mvp": "タルト", "match_code": "#W1-3"},
        {"tournament": "過去のプロセカ大会第2回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "らいせ", "loser": "しらす", "score": "2-0", "mvp": "らいせ", "match_code": "#W1-4"},
        
        # 準決勝
        {"tournament": "過去のプロセカ大会第2回", "bracket": "勝者サイド", "stage": "準決勝", "winner": "yuka.", "loser": "リュウ", "score": "2-0", "mvp": "yuka.", "match_code": "#W2-1"},
        {"tournament": "過去のプロセカ大会第2回", "bracket": "勝者サイド", "stage": "準決勝", "winner": "タルト", "loser": "らいせ", "score": "2-0", "mvp": "タルト", "match_code": "#W2-2"},
        
        # 勝者サイド決勝
        {"tournament": "過去のプロセカ大会第2回", "bracket": "勝者サイド", "stage": "決勝", "winner": "yuka.", "loser": "タルト", "score": "3-1", "mvp": "yuka.", "match_code": "#W3-1"},

        # --- 🔵 敗者サイド ---
        # 1回戦
        {"tournament": "過去のプロセカ大会第2回", "bracket": "敗者サイド", "stage": "1回戦", "winner": "がらす", "loser": "N/A", "score": "0-DQ", "mvp": "がらす", "match_code": "#L1-1"},
        {"tournament": "過去のプロセカ大会第2回", "bracket": "敗者サイド", "stage": "1回戦", "winner": "しらす", "loser": "四季", "score": "2-0", "mvp": "しらす", "match_code": "#L1-2"},
        
        # 2回戦
        {"tournament": "過去のプロセカ大会第2回", "bracket": "敗者サイド", "stage": "2回戦", "winner": "らいせ", "loser": "がらす", "score": "2-0", "mvp": "らいせ", "match_code": "#L2-1"},
        {"tournament": "過去のプロセカ大会第2回", "bracket": "敗者サイド", "stage": "2回戦", "winner": "リュウ", "loser": "しらす", "score": "2-0", "mvp": "リュウ", "match_code": "#L2-2"},
        
        # 準決勝
        {"tournament": "過去のプロセカ大会第2回", "bracket": "敗者サイド", "stage": "準決勝", "winner": "らいせ", "loser": "リュウ", "score": "3-1", "mvp": "らいせ", "match_code": "#L3-1"},
        
        # 決勝
        {"tournament": "過去のプロセカ大会第2回", "bracket": "敗者サイド", "stage": "決勝", "winner": "タルト", "loser": "らいせ", "score": "3-2", "mvp": "タルト", "match_code": "#L4-1"},

        # --- 🏆 グランドファイナル ---
        {"tournament": "過去のプロセカ大会第2回", "bracket": "勝者サイド", "stage": "グランドファイナル", "winner": "yuka.", "loser": "タルト", "score": "3-2", "mvp": "yuka.", "match_code": "#W4-1"},
    
        # --- 🟠 勝者サイド ---
    # 1回戦
    {"tournament": "過去のプロセカ大会第3回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "yuka.", "loser": "N/A", "score": "- - -", "mvp": "yuka.", "match_code": "#W1-1"},
    {"tournament": "過去のプロセカ大会第3回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "らむね", "loser": "四季", "score": "2-0", "mvp": "らむね", "match_code": "#W1-2"},
    {"tournament": "過去のプロセカ大会第3回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "れんか", "loser": "しらす", "score": "2-1", "mvp": "蓮歌", "match_code": "#W1-3"},
    {"tournament": "過去のプロセカ大会第3回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "がらす", "loser": "タルト", "score": "2-0", "mvp": "がらす", "match_code": "#W1-4"},
    
    # 準決勝
    {"tournament": "過去のプロセカ大会第3回", "bracket": "勝者サイド", "stage": "準決勝", "winner": "らむね", "loser": "yuka.", "score": "2-0", "mvp": "らむね", "match_code": "#W2-1"},
    {"tournament": "過去のプロセカ大会第3回", "bracket": "勝者サイド", "stage": "準決勝", "winner": "がらす", "loser": "れんか", "score": "2-0", "mvp": "がらす", "match_code": "#W2-2"},
    
    # 勝者サイド決勝
    {"tournament": "過去のプロセカ大会第3回", "bracket": "勝者サイド", "stage": "決勝", "winner": "らむね", "loser": "がらす", "score": "3-1", "mvp": "らむね", "match_code": "#W3-1"},

    # --- 🔵 敗者サイド ---
    # 1回戦
    {"tournament": "過去のプロセカ大会第3回", "bracket": "敗者サイド", "stage": "1回戦", "winner": "四季", "loser": "-", "score": "- - -", "mvp": "四季", "match_code": "#L1-1"},
    {"tournament": "過去のプロセカ大会第3回", "bracket": "敗者サイド", "stage": "1回戦", "winner": "しらす", "loser": "タルト", "score": "2-1", "mvp": "しらす", "match_code": "#L1-2"},
    
    # 2回戦
    {"tournament": "過去のプロセカ大会第3回", "bracket": "敗者サイド", "stage": "2回戦", "winner": "れんか", "loser": "四季", "score": "2-0", "mvp": "れんか", "match_code": "#L2-1"},
    {"tournament": "過去のプロセカ大会第3回", "bracket": "敗者サイド", "stage": "2回戦", "winner": "yuka.", "loser": "しらす", "score": "0-DQ", "mvp": "yuka.", "match_code": "#L2-2"},
    
    # 準決勝
    {"tournament": "過去のプロセカ大会第3回", "bracket": "敗者サイド", "stage": "準決勝", "winner": "yuka.", "loser": "れんか", "score": "3-0", "mvp": "yuka.", "match_code": "#L3-1"},
    
    # 決勝
    {"tournament": "過去のプロセカ大会第3回", "bracket": "敗者サイド", "stage": "決勝", "winner": "yuka.", "loser": "がらす", "score": "3-0", "mvp": "yuka.", "match_code": "#L4-1"},

    # --- 🏆 グランドファイナル ---
    {"tournament": "過去のプロセカ大会第3回", "bracket": "勝者サイド", "stage": "グランドファイナル", "winner": "らむね", "loser": "yuka.", "score": "3-1", "mvp": "らむね", "match_code": "#W4-1"},

    # --- 🟠 勝者サイド ---
    # 1回戦
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "yuka.", "loser": "らむね", "score": "2-0", "mvp": "yuka.", "match_code": "#W1-1"},
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "タルト", "loser": "つくし", "score": "2-1", "mvp": "タルト", "match_code": "#W1-2"},
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "すぶわむる", "loser": "しらす", "score": "2-0", "mvp": "すぶわむる", "match_code": "#W1-3"},
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "1回戦", "winner": "もふもふ", "loser": "がらす", "score": "2-0", "mvp": "もふもふ", "match_code": "#W1-4"},
    
    # 準決勝
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "準決勝", "winner": "yuka.", "loser": "たると", "score": "2-1", "mvp": "yuka.", "match_code": "#W2-1"},
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "準決勝", "winner": "もふもふ", "loser": "すぶわむる", "score": "2-1", "mvp": "もふもふ", "match_code": "#W2-2"},
    
    # 勝者サイド決勝
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "決勝", "winner": "yuka.", "loser": "もふもふ", "score": "3-0", "mvp": "yuka.", "match_code": "#W3-1"},

    # --- 🔵 敗者サイド ---
    # 1回戦
    {"tournament": "過去のプロセカ大会第4回", "bracket": "敗者サイド", "stage": "1回戦", "winner": "つくし", "loser": "らむね", "score": "2-0", "mvp": "つくし", "match_code": "#L1-1"},
    {"tournament": "過去のプロセカ大会第4回", "bracket": "敗者サイド", "stage": "1回戦", "winner": "がらす", "loser": "しらす", "score": "2-1", "mvp": "がらす", "match_code": "#L1-2"},
    
    # 2回戦
    {"tournament": "過去のプロセカ大会第4回", "bracket": "敗者サイド", "stage": "2回戦", "winner": "つくし", "loser": "すぶわむる", "score": "2-0", "mvp": "つくし", "match_code": "#L2-1"},
    {"tournament": "過去のプロセカ大会第4回", "bracket": "敗者サイド", "stage": "2回戦", "winner": "タルト", "loser": "がらす", "score": "2-0", "mvp": "タルト", "match_code": "#L2-2"},
    
    # 準決勝
    {"tournament": "過去のプロセカ大会第4回", "bracket": "敗者サイド", "stage": "準決勝", "winner": "タルト", "loser": "つくし", "score": "3-2", "mvp": "タルト", "match_code": "#L3-1"},
    
    # 決勝
    {"tournament": "過去のプロセカ大会第4回", "bracket": "敗者サイド", "stage": "決勝", "winner": "タルト", "loser": "もふもふ", "score": "1-DQ", "mvp": "タルト", "match_code": "#L4-1"},

    # --- 🏆 グランドファイナル ---
    # 1戦目（敗者側のタルトが勝利してリセット発生）
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "グランドファイナル", "winner": "たると", "loser": "yuka.", "score": "3-2", "mvp": "たると", "match_code": "#W4-1"},
    # 2戦目（リセットマッチ：yuka.が勝利して最終優勝）
    {"tournament": "過去のプロセカ大会第4回", "bracket": "勝者サイド", "stage": "グランドファイナルリセット", "winner": "yuka.", "loser": "たると", "score": "3-1", "mvp": "yuka.", "match_code": "#W5-1"},




    ]

# ------------------------------------------------------------------------------
# サイドバー：データ管理
# ------------------------------------------------------------------------------
st.sidebar.header("⚙️ データ登録")

with st.sidebar.expander("➕ 選手を追加", expanded=False):
    new_player_name = st.text_input("選手名")
    if st.button("選手を登録"):
        if new_player_name.strip():
            if new_player_name not in st.session_state.players:
                st.session_state.players.append(new_player_name.strip())
                st.success(f"選手「{new_player_name}」を追加しました！")
                st.rerun()
            else:
                st.warning("すでに登録されている選手名です。")
        else:
            st.error("選手名を入力してください。")

with st.sidebar.expander("📝 試合結果を追加", expanded=False):
    t_name = st.text_input("大会名", value="第1回 ゼロセカ マスター部門")
    bracket_type = st.radio("サイド", ["勝者サイド", "敗者サイド"])
    t_stage = st.selectbox("ラウンド", ["1回戦", "2回戦", "準決勝", "決勝", "グランドファイナル"])
    m_code = st.text_input("試合コード (例: #W1-1)", value="#W1-1")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        winner = st.selectbox("勝者", st.session_state.players, index=0)
    with col_p2:
        loser_options = [p for p in st.session_state.players if p != winner]
        loser = st.selectbox("敗者", loser_options, index=0 if loser_options else None)
        
    score = st.text_input("スコア (例: 2-0)", value="2-0")
    mvp = st.selectbox("MVP選手", [winner, loser] if loser else [winner])

    if st.button("試合結果を保存"):
        if winner and loser:
            st.session_state.matches.append({
                "tournament": t_name,
                "bracket": bracket_type,
                "stage": t_stage,
                "match_code": m_code,
                "winner": winner,
                "loser": loser,
                "score": score,
                "mvp": mvp
            })
            st.success("試合結果を登録しました！")
            st.rerun()

# ------------------------------------------------------------------------------
# メイン画面ヘッダー
# ------------------------------------------------------------------------------
st.title("🏆 大会結果 & 戦績・対戦勝率ダッシュボード")

tab1, tab2, tab3 = st.tabs(["🌳 トーナメント表", "👤 選手別戦績", "⚔️ 対戦相手別勝率 (通年)"])
df_matches = pd.DataFrame(st.session_state.matches)

# HTMLカード描画関数
def render_match_card(row_data):
    if row_data is None or row_data.empty:
        return "<div style='height: 85px;'></div>"
    
    m = row_data.iloc[0]
    score_parts = m['score'].split('-') if '-' in m['score'] else ['0', '0']
    
    return f"""
    <div style="background: white; border: 1px solid #dcdcdc; border-radius: 6px; padding: 6px 10px; margin-bottom: 12px; font-family: sans-serif; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <div style="font-size: 10px; color: #888; font-weight: bold; margin-bottom: 3px;">{m.get('match_code', '')}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 3px; font-weight: bold; font-size: 14px; color: #2c3e50;">
            <span>{m['winner']}</span>
            <span style="color: #27ae60;">{score_parts[0]}</span>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 3px; font-size: 14px; color: #7f8c8d;">
            <span>{m['loser']}</span>
            <span>{score_parts[1] if len(score_parts) > 1 else '0'}</span>
        </div>
    </div>
    """

# ------------------------------------------------------------------------------
# タブ 1: トーナメント表（ダブルイリミネーション形式対応）
# ------------------------------------------------------------------------------
with tab1:
    tournaments = df_matches["tournament"].unique()
    selected_t = st.selectbox("大会を選択してください", tournaments)
    
    t_data = df_matches[df_matches["tournament"] == selected_t]
    
    st.markdown(f"<h2 style='text-align: center; margin-bottom: 30px;'>{selected_t}</h2>", unsafe_allow_html=True)
    
    # --- 勝者サイド (Winners Bracket) ---
    st.markdown("### 🟠 勝者サイド (Winners Bracket)")
    col_w1, col_w2, col_w3, col_w4 = st.columns(4)
    
    w_data = t_data[t_data.get("bracket", "勝者サイド") == "勝者サイド"]
    
    with col_w1:
        st.markdown("<span style='background:#ff5722; color:white; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>1回戦</span>", unsafe_allow_html=True)
        st.write("")
        for code in ["#W1-1", "#W1-2", "#W1-3", "#W1-4"]:
            m_row = w_data[w_data["match_code"] == code]
            st.markdown(render_match_card(m_row), unsafe_allow_html=True)

    with col_w2:
        st.markdown("<span style='background:#555; color:white; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>準決勝</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
        for code in ["#W2-1", "#W2-2"]:
            m_row = w_data[w_data["match_code"] == code]
            st.markdown(render_match_card(m_row), unsafe_allow_html=True)
            st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    with col_w3:
        st.markdown("<span style='background:#555; color:white; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>決勝</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        m_row = w_data[w_data["match_code"] == "#W3-1"]
        st.markdown(render_match_card(m_row), unsafe_allow_html=True)

    with col_w4:
        st.markdown("<span style='background:#333; color:white; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>グランドファイナル</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        m_row = w_data[w_data["match_code"] == "#W4-1"]
        st.markdown(render_match_card(m_row), unsafe_allow_html=True)

    st.markdown("---")
    
    # --- 敗者サイド (Losers Bracket) ---
    st.markdown("### 🔵 敗者サイド (Losers Bracket)")
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    
    l_data = t_data[t_data.get("bracket", "") == "敗者サイド"]
    
    with col_l1:
        st.markdown("<span style='background:#ff5722; color:white; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>1回戦</span>", unsafe_allow_html=True)
        st.write("")
        for code in ["#L1-1", "#L1-2"]:
            m_row = l_data[l_data["match_code"] == code]
            st.markdown(render_match_card(m_row), unsafe_allow_html=True)
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    with col_l2:
        st.markdown("<span style='background:#555; color:white; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>2回戦</span>", unsafe_allow_html=True)
        st.write("")
        for code in ["#L2-1", "#L2-2"]:
            m_row = l_data[l_data["match_code"] == code]
            st.markdown(render_match_card(m_row), unsafe_allow_html=True)
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    with col_l3:
        st.markdown("<span style='background:#555; color:white; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>準決勝</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        m_row = l_data[l_data["match_code"] == "#L3-1"]
        st.markdown(render_match_card(m_row), unsafe_allow_html=True)

    with col_l4:
        st.markdown("<span style='background:#555; color:white; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>決勝</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        m_row = l_data[l_data["match_code"] == "#L4-1"]
        st.markdown(render_match_card(m_row), unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# タブ 2: 選手別戦績
# ------------------------------------------------------------------------------
with tab2:
    st.header("選手別 個人成績")
    selected_player = st.selectbox("選手を選択", st.session_state.players, key="p_stats")
    
    p_wins = df_matches[df_matches["winner"] == selected_player]
    p_losses = df_matches[df_matches["loser"] == selected_player]
    
    total_wins = len(p_wins)
    total_losses = len(p_losses)
    total_games = total_wins + total_losses
    win_rate = (total_wins / total_games * 100) if total_games > 0 else 0.0
    
    titles_won = len(df_matches[(df_matches["winner"] == selected_player) & (df_matches["stage"] == "グランドファイナル")])
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("通算試合数", f"{total_games} 試合")
    m_col2.metric("通算勝利", f"{total_wins} 勝")
    m_col3.metric("通算敗北", f"{total_losses} 敗")
    m_col4.metric("通算勝率", f"{win_rate:.1f} %")
    
    if titles_won > 0:
        st.balloons()
        st.success(f"🏆 大会優勝回数: {titles_won} 回")

    st.subheader(f"📜 {selected_player} の対戦履歴")
    p_history = df_matches[(df_matches["winner"] == selected_player) | (df_matches["loser"] == selected_player)]
    
    if not p_history.empty:
        formatted_history = []
        for _, row in p_history.iterrows():
            is_win = row["winner"] == selected_player
            opponent = row["loser"] if is_win else row["winner"]
            result = "勝 ⭕" if is_win else "負 ❌"
            formatted_history.append({
                "大会名": row["tournament"],
                "サイド/ラウンド": f"{row.get('bracket','')}/ {row['stage']}",
                "コード": row.get('match_code',''),
                "結果": result,
                "対戦相手": opponent,
                "スコア": row["score"],
                "MVP": row["mvp"]
            })
        st.dataframe(pd.DataFrame(formatted_history), use_container_width=True)
    else:
        st.write("試合データがありません。")

# ------------------------------------------------------------------------------
# タブ 3: 対戦相手別勝率 (通年)
# ------------------------------------------------------------------------------
with tab3:
    st.header("対戦相手別 勝率分析 (通年)")
    player_a = st.selectbox("基準となる選手を選択", st.session_state.players, key="h2h_player")
    
    opponents = [p for p in st.session_state.players if p != player_a]
    h2h_data = []
    
    for opp in opponents:
        wins = len(df_matches[(df_matches["winner"] == player_a) & (df_matches["loser"] == opp)])
        losses = len(df_matches[(df_matches["winner"] == opp) & (df_matches["loser"] == player_a)])
        total = wins + losses
        rate = (wins / total * 100) if total > 0 else 0.0
        
        if total > 0:
            h2h_data.append({
                "対戦相手": opp,
                "勝利数": wins,
                "敗北数": losses,
                "総試合数": total,
                "勝率(%)": round(rate, 1)
            })
            
    df_h2h = pd.DataFrame(h2h_data)
    
    if not df_h2h.empty:
        col_chart, col_table = st.columns([3, 2])
        
        with col_chart:
            fig = px.bar(
                df_h2h, 
                x="対戦相手", 
                y="勝率(%)", 
                text="勝率(%)",
                title=f"{player_a} の対戦相手別勝率",
                color="勝率(%)",
                color_continuous_scale="Reds",
                range_y=[0, 100]
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
        with col_table:
            st.subheader("📊 詳細データ")
            st.dataframe(df_h2h, use_container_width=True)
    else:
        st.info("対戦データがまだありません。")

    st.markdown("---")
    st.subheader("⚔️ 特定の2人の直接対戦 (1v1 H2H)")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        p1 = st.selectbox("選手1", st.session_state.players, index=0, key="vs1")
    with col_v2:
        p2_options = [p for p in st.session_state.players if p != p1]
        p2 = st.selectbox("選手2", p2_options, index=0 if p2_options else None, key="vs2")
        
    if p1 and p2:
        p1_wins = len(df_matches[(df_matches["winner"] == p1) & (df_matches["loser"] == p2)])
        p2_wins = len(df_matches[(df_matches["winner"] == p2) & (df_matches["loser"] == p1)])
        
        st.markdown(f"### **{p1}** `{p1_wins} 勝`  vs  `{p2_wins} 勝` **{p2}**")