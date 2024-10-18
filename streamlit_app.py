import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm


import random

# APIキー設定
# Or use os.getenv('GEMINI_API_KEY') to fetch an environment variable.
# import os
GEMINI_API_KEY = st.secrets["IdeaApp"]["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)


# 単語の準備
# 一般的に誰でも知っている日本語名詞リスト
nouns = [
    "空", "風", "雨", "太陽", "星", "月", "山", "川", "海", "湖", "石", "花", "木", "草", "雲",
    "道", "橋", "家", "部屋", "窓", "扉", "椅子", "机", "ベッド", "鏡", "本", "新聞", "雑誌",
    "時計", "テレビ", "ラジオ", "電話", "パソコン", "カメラ", "音楽", "映画", "車", "電車",
    "飛行機", "船", "自転車", "バス", "料理", "ご飯", "パン", "肉", "魚", "野菜", "果物",
    "水", "ジュース", "コーヒー", "お茶", "ビール", "ワイン", "皿", "フォーク", "ナイフ", "スプーン",
    "箸", "鍋", "歯ブラシ", "タオル", "石鹸", "シャンプー", "靴", "服", "帽子", "バッグ", "財布",
    "鍵", "ペン", "鉛筆", "消しゴム", "ノート", "教科書", "辞書", "地図", "家族", "友達", "子供",
    "大人", "先生", "学生", "仕事", "会社", "会議", "休み", "スポーツ", "サッカー", "野球",
    "バスケットボール", "テニス", "ゴルフ", "水泳", "運動", "旅行", "公園", "庭", "遊園地",
    "ゲーム", "本屋", "映画館", "劇場", "美術館", "博物館", "動物園", "水族館", "図書館",
    "病院", "薬", "医者", "看護師", "風邪", "病気", "健康", "手紙", "郵便", "銀行", "お金",
    "買い物", "店", "スーパー", "レストラン", "ホテル", "部屋", "予約", "空港", "駅", "電車",
    "切符", "旅行", "道案内", "地図", "信号", "交差点", "高速道路", "橋", "トンネル", "砂漠",
    "島", "半島", "火山", "森", "ジャングル", "草原", "丘", "崖", "洞窟", "滝", "川", "湖",
    "海", "大洋", "港", "船", "波", "潮", "船旅", "釣り", "ダイビング", "登山", "キャンプ",
    "天気", "季節", "春", "夏", "秋", "冬", "雪", "雨", "風", "嵐", "台風", "雲", "雷", "虹",
    "星", "月", "宇宙", "太陽系", "惑星", "銀河", "宇宙飛行士", "人工衛星", "ロケット",
    "生命", "生物", "植物", "動物", "魚", "鳥", "哺乳類", "爬虫類", "昆虫", "花", "木",
    "森", "草", "植物園", "動物園", "水族館", "ペット", "犬", "猫", "鳥", "魚", "馬", "牛",
    "豚", "鶏", "農場", "農業", "作物", "野菜", "果物", "米", "小麦", "トラクター", "収穫",
    "市場", "売買", "商品", "取引", "お金", "銀行", "投資", "借金", "ローン", "貯金", "給料"
]

# タイトルを設定する
st.set_page_config(
    page_title="ゼロイチAI",
    page_icon="🐤"
)

st.title("ゼロイチアイデア採点AI")
st.markdown("""
##### 概要
２つのランダムな単語から新しいビジネスを考える「複合連結型発想法」を実践できるサイトです。
全く新しいアイデアを自由な発想で生み出したい人、自分のアイデア力を試したい人におすすめです。

##### 使い方
- 単語生成をクリックしお題単語を出力します
- 解答欄にビジネス案を200文字以内で入力します
- 採点ボタンを押すとAIが採点してくれます（平均は70点です）
- 行き詰まったらAIによる解答例を見てみましょう
""")

if 'word1' not in st.session_state:
    st.session_state.word1 = ""
if 'word2' not in st.session_state:
    st.session_state.word2 = ""
if 'answer' not in st.session_state:
    st.session_state.answer = ""
if 'txt' not in st.session_state:
    st.session_state.answer = ""


# スタートボタンを作成
if st.button("単語生成"):
    # ランダムに単語を生成
    random_numbers = random.sample(range(1, len(nouns)), 2)
    st.session_state.word1 = nouns[random_numbers[0]]
    st.session_state.word2 = nouns[random_numbers[1]]

# 単語と社会課題を表示
st.write("単語１: **{}**".format(st.session_state.word1))
st.write("単語２: **{}**".format(st.session_state.word2))

st.session_state.txt = st.text_area(
    '解答欄', value='タイトル：\n概要：\n', height=150, max_chars=200
)

if st.button("AI採点"):
    if st.session_state.txt:
        # プロンプトを生成
        question = f"""
        あなたは優秀なビジネス評価者です。以下のビジネスに対して、採点およびコメントをしてください。
        ビジネス概要(200字)：{st.session_state.txt}

        なお、ビジネスはランダムに抽出された以下の２単語を使用しています。

        単語１：{st.session_state.word1}
        単語２：{st.session_state.word2}

        なお、出力の形式としては以下の通りにしてください。
        ・点数を明記する（平均点70程度とし、厳し目に採点すること）
        ・よかった点・改善点を述べる
        ・解答例を端的に提示する
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(question)
        st.write(response.text)
    else:
        st.warning("回答が入力されていません。先に回答を行なってください。")

if st.button("AIによる解答例"):
    if st.session_state.word1 and st.session_state.word2:
        # プロンプトを生成
        question = f"""
        あなたは優秀なビジネスイノベーターです。
        ランダムに抽出された以下の２単語を使用し、ビッグビジネスになるビジネスアイデアを考えてください。

        単語１：{st.session_state.word1}
        単語２：{st.session_state.word2}

        なお、出力の形式としては以下の通りにしてください。
        ・タイトルを記載する（単なる単語の繋ぎ合わせではなく、深みのあるタイトルを設定する）
        ・端的にビジネスについて答える
        ・ビジネス金額とその根拠も端的にフェルミ推定などに基づいて述べる
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(question)
        st.write(response.text)
    else:
        st.warning("単語が生成されていません。先に単語を生成してください。")
