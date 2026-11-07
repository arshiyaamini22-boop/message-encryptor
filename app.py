
import streamlit as st
from cryptography.fernet import Fernet, InvalidToken

# تنظیمات صفحه
st.set_page_config(
    page_title="رمزنگار فارسی",
    page_icon="🔐",
    layout="centered"
)

# طراحی ظاهری
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Vazirmatn', sans-serif;
}

.stApp {
    direction: rtl;
    text-align: right;
}

h1, h2, h3, p, label {
    text-align: right;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-weight: bold;
    min-height: 45px;
}
</style>
""", unsafe_allow_html=True)


# مدیریت کلید
if "secret_key" not in st.session_state:
    st.session_state.secret_key = ""


def generate_key():
    st.session_state.secret_key = Fernet.generate_key().decode("ascii")


# عنوان برنامه
st.title("🔐 رمزنگار پیام")
st.caption("ابزار رمزنگاری و رمزگشایی متن فارسی")

st.divider()


# بخش مدیریت کلید
st.subheader("🔑 کلید اختصاصی")

st.text_input(
    "کلید رمزنگاری و رمزگشایی:",
    key="secret_key",
    placeholder="کلید خود را وارد کنید..."
)

st.button(
    "✨ تولید کلید جدید",
    on_click=generate_key
)

st.info(
    "کلید خود را در مکانی امن ذخیره کنید. "
    "بدون کلید صحیح امکان رمزگشایی وجود ندارد."
)

st.divider()


# تب‌های برنامه
tab1, tab2 = st.tabs([
    "🔒 رمزنگاری",
    "🔓 رمزگشایی"
])


# =========================
# بخش رمزنگاری
# =========================

with tab1:

    st.subheader("🔒 رمزنگاری پیام")

    message = st.text_area(
        "متن موردنظر را وارد کنید:",
        height=150,
        placeholder="پیام خود را اینجا بنویسید..."
    )

    if st.button("رمزنگاری متن", key="encrypt"):

        key = st.session_state.secret_key

        if not message:
            st.warning("ابتدا متن خود را وارد کنید.")

        elif not key:
            st.warning("ابتدا یک کلید تولید یا وارد کنید.")

        else:
            try:
                cipher = Fernet(key.encode("ascii"))

                encrypted = cipher.encrypt(
                    message.encode("utf-8")
                ).decode("ascii")

                st.success("پیام با موفقیت رمزنگاری شد!")

                st.text_area(
                    "متن رمزنگاری‌شده:",
                    value=encrypted,
                    height=120
                )

            except (ValueError, UnicodeError):
                st.error("کلید واردشده معتبر نیست.")


# =========================
# بخش رمزگشایی
# =========================

with tab2:

    st.subheader("🔓 رمزگشایی پیام")

    encrypted_text = st.text_area(
        "متن رمزنگاری‌شده را وارد کنید:",
        height=150,
        placeholder="متن رمزنگاری‌شده را اینجا قرار دهید..."
    )

    if st.button("رمزگشایی متن", key="decrypt"):

        decrypt_key = st.session_state.secret_key

        if not encrypted_text:
            st.warning("متن رمزنگاری‌شده را وارد کنید.")

        elif not decrypt_key:
            st.warning("کلید رمزگشایی را وارد کنید.")

        else:
            try:
                decryptor = Fernet(
                    decrypt_key.encode("ascii")
                )

                decrypted = decryptor.decrypt(
                    encrypted_text.encode("ascii")
                ).decode("utf-8")

                st.success("رمزگشایی با موفقیت انجام شد!")

                st.text_area(
                    "متن اصلی:",
                    value=decrypted,
                    height=120
                )

            except (InvalidToken, ValueError, UnicodeError):
                st.error(
                    "خطا: کلید یا متن رمزنگاری‌شده نامعتبر است."
                )


# پاورقی
st.divider()

st.caption(
    "🔐 Message Encryptor | Powered by Python & Fernet"
)
