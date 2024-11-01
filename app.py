import os
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# OpenAI API 키 설정 (환경 변수에서 가져오기)
openai.api_key = os.getenv("OPENAI_API_KEY")

# 날씨 설명 생성 함수
def describe_weather(temperature, humidity, wind_speed):
    if temperature >= 30:
        temp_desc = "덥고"
    elif 20 <= temperature < 30:
        temp_desc = "따뜻하고"
    elif 10 <= temperature < 20:
        temp_desc = "선선하고"
    elif 0 <= temperature < 10:
        temp_desc = "쌀쌀하고"
    else:
        temp_desc = "추운"

    if humidity >= 70:
        humidity_desc = "습한"
    elif 40 <= humidity < 70:
        humidity_desc = "적절한 습도의"
    else:
        humidity_desc = "건조한"

    if wind_speed <= 1:
        wind_desc = "바람이 거의 없는 날씨입니다."
    elif 1.1 <= wind_speed <= 3:
        wind_desc = "약한 바람이 부는 날씨입니다."
    elif 3.1 <= wind_speed <= 5:
        wind_desc = "조금 강한 바람이 부는 날씨입니다."
    elif 5.1 <= wind_speed < 10:
        wind_desc = "강한 바람이 부는 날씨입니다."
    else:
        wind_desc = "매우 강한 바람이 부는 날씨입니다."

    return f"{temp_desc} {humidity_desc} {wind_desc}"

# 홈페이지 경로
@app.route('/')
def index():
    return render_template('index.html')

# ChatGPT와 날씨 설명 생성 API
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    wind_speed = data.get("wind_speed")

    # 날씨 설명 생성
    weather_description = describe_weather(temperature, humidity, wind_speed)

    try:
        # ChatGPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "당신은 기상 관측을 도와주는 도우미봇입니다."},
                      {"role": "user", "content": f"대답하는 날씨는 다음과 같습니다.: {weather_description}"}]
        )
        chatbot_reply = response['choices'][0]['message']['content']
        return jsonify({"reply": chatbot_reply})

    except Exception as e:
        print("Error during API call:", e)
        return jsonify({"reply": "API 요청 중 오류가 발생했습니다. 다시 시도해 주세요."})

if __name__ == '__main__':
    # 환경 변수에서 포트를 가져오고, 0.0.0.0에 바인딩하여 외부 접근 허용
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
