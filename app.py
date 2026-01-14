
import streamlit as st
from groq import Groq

# แทนที่จะพิมพ์ Key ลงไปตรงๆ ให้ใช้ st.secrets แทน
# ระบบจะไปดึงค่าจากหน้าตั้งค่าของ Streamlit มาให้เองครับ
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("กรุณาตั้งค่า API Key ใน Streamlit Secrets ก่อนใช้งาน")
    st.stop()

client = Groq(api_key=API_KEY)

# --- ส่วนที่เหลือของโค้ดคงเดิมตามที่ผมให้ไปครั้งก่อน ---
st.set_page_config(page_title="Relationship Coach", page_icon="❤️")
st.title("❤️ AI ที่ปรึกษาด้านความสัมพันธ์")
# ... (โค้ดส่วนเดิมทั้งหมด)if "model" not in st.session_state:
st.session_state.model = "llama3-70b-8192"

# ตัวจัดการประวัติการสนทนา
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "คุณเป็นที่ปรึกษาด้านความสัมพันธ์ที่เชี่ยวชาญ ให้คำปรึกษาอย่างอบอุ่นและไม่ตัดสิน"}
    ]

# แสดงประวัติการแชท
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# รับข้อความจากผู้ใช้
if prompt := st.chat_input("มีอะไรอยากเล่าให้ฟังไหมคะ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model=st.session_state.model,
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")