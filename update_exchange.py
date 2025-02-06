import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
today = datetime.today().strftime("%Y%m%d")

API_KEY = os.getenv("AUTHKEY")
URL = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?{API_KEY}&searchdate={today}&data=AP01"

# README 파일 경로
README_PATH = "README.md"

def get_exchange():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        nm = next((item["cur_nm"] for item in data if item["cur_unit"] == "KRW"), None)
        ttb = next((item["ttb"] for item in data if item["cur_unit"] == "KRW"), None)
        tts = next((item["tts"] for item in data if item["cur_unit"] == "KRW"), None)
        return f"국가: {nm}, TTB(전신환받을때): {ttb}, TTS(전신환보낼때): {tts}"
    else:
        return "환율 정보를 가져오는 데 실패했습니다."

def update_readme():
    """README.md 파일을 업데이트"""
    exchange_info = get_exchange()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    readme_content = f"""
# Weather API Status

이 리포지토리는 OpenWeather API를 사용하여 서울의 날씨 정보를 자동으로 업데이트합니다.

## 현재 서울 날씨
> {exchange_info}

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()