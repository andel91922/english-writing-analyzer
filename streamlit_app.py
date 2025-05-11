import streamlit as st
import requests

# 分析語法錯誤與建議
def analyze_text(text):
    url = "https://api.languagetoolplus.com/v2/check"
    params = {
        "text": text,
        "language": "en-US"
    }

    response = requests.post(url, data=params)
    matches = response.json()["matches"]

    errors = []
    for match in matches:
        error = text[match["offset"]: match["offset"] + match["length"]]
        message = match["message"]
        replacements = match["replacements"]
        rule_type = match["rule"]["issueType"]
        errors.append({
            "error": error,
            "suggestion": replacements[0]["value"] if replacements else "無",
            "explanation": message,
            "type": rule_type
        })

    return errors

# 粗略估計 CEFR 程度
def estimate_cefr_level(text, num_errors):
    words = len(text.split())
    if words == 0:
        return "無法評估"
    error_ratio = num_errors / words
    if error_ratio > 0.2:
        return "A2 以下"
    elif error_ratio > 0.1:
        return "B1"
    else:
        return "B2 以上"

# Streamlit 主頁面
st.set_page_config(page_title="LingoScope 英文寫作診斷工具")

st.title("📘 LingoScope 英文寫作診斷工具")
st.write("輸入一段英文寫作，我們會幫你分析文法錯誤與程度判斷。")

text_input = st.text_area("✏️ 請輸入你的英文作文", height=200)

if st.button("🔍 分析我的寫作"):
    if not text_input.strip():
        st.warning("請先輸入英文內容！")
    else:
        with st.spinner("分析中，請稍候..."):
            errors = analyze_text(text_input)
            level = estimate_cefr_level(text_input, len(errors))

        st.subheader("🔎 你的寫作分析結果")
        if not errors:
            st.success("恭喜你，未檢測到明顯錯誤！🎉")
        else:
            for i, e in enumerate(errors, 1):
                st.markdown(f"""
                **錯誤 {i}**
                - 錯誤部分：`{e['error']}`
                - 建議：{e['suggestion']}
                - 說明：{e['explanation']}
                - 錯誤類型：{e['type']}
                """)

            # 統計錯誤類型
            type_count = {}
            for e in errors:
                type_count[e["type"]] = type_count.get(e["type"], 0) + 1

            st.subheader("📊 錯誤統計")
            for t, c in type_count.items():
                st.write(f"- {t}：{c} 筆")

        st.subheader("🧠 推估英文程度")
        st.success(f"你的英文程度大約為：**{level}**")