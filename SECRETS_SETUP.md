# 🔐 Streamlit Secrets Setup

لأن هذا التطبيق يستخدم Groq API (مجاني)، يجب إضافة مفتاحك السري في Streamlit Cloud:

## الخطوات:
1. اذهب إلى: https://share.streamlit.io
2. افتح إعدادات تطبيقك (Settings → Secrets)
3. أضف:
```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
4. احصل على المفتاح المجاني من: https://console.groq.com/keys
