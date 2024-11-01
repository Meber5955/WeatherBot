from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__)

# OpenAI API 키 설정
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    wind_speed = data.get("wind_speed")

    # 날씨 설명 생성
    weather_description = describe_weather(temperature, humidity, wind_speed)

    # ChatGPT API 호출
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "당신은 기상관측을 도와주는 도우미봇입니다."},
                  {"role": "user", "content": f"온도, 습도, 풍속이 입력되면 날씨에 대한 대답은 다음과 같습니다: {weather_description}"}]
    )

    chatbot_reply = response['choices'][0]['message']['content']
    return jsonify({"reply": chatbot_reply})

if __name__ == '__main__':
    # 환경 변수를 통해 포트를 가져오고, 0.0.0.0으로 설정해 외부 접근 가능하게 만듦
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
