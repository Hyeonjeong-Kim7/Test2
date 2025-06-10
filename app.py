# app.py

import streamlit as st
import numpy as np
import joblib
from urllib.parse import urlparse
import re

# URL feature 추출 함수
def extract_features_from_url(url):
    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname else ''
    path = parsed.path
    query = parsed.query
    
    num_dots = url.count('.')
    num_dash = url.count('-')
    num_numeric = sum(c.isdigit() for c in url)
    at_symbol = 1 if '@' in url else 0
    is_ip = 1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', hostname) else 0
    no_https = 1 if not url.startswith('https') else 0
    path_level = path.count('/')
    url_length = len(url)
    path_length = len(path)
    
    return [
        num_dots,
        num_dash,
        num_numeric,
        at_symbol,
        is_ip,
        no_https,
        path_level,
        url_length,
        path_length
    ]

# 모델 및 스케일러 로드
model = joblib.load('xgb_phishing_model.pkl')
scaler = joblib.load('scaler.pkl')

# Streamlit UI 구성
st.title("🔍 Phishing URL Detection App")
st.markdown("Enter a URL below to check if it is a phishing attempt.")

# URL 입력창
url_input = st.text_input("Enter a URL:")

# Predict 버튼 클릭 시 동작
if st.button("Predict"):
    if url_input:
        # URL feature 추출
        features = extract_features_from_url(url_input)
        X_input = np.array(features).reshape(1, -1)
        X_scaled = scaler.transform(X_input)
        
        # 모델 예측
        prediction = model.predict(X_scaled)[0]
        probability = model.predict_proba(X_scaled)[0].tolist()
        
        # 결과 표시
        result_text = "✅ Legitimate URL" if prediction == 0 else "⚠️ Phishing URL!"
        
        st.markdown(f"## Result: {result_text}")
        st.write(f"Probability: {probability}")
        st.write(f"Extracted Features: {features}")
    else:
        st.warning("Please enter a URL.")
