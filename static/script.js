async function sendWeather() {
    const temperature = document.getElementById("temperature").value;
    const humidity = document.getElementById("humidity").value;
    const windSpeed = document.getElementById("wind_speed").value;

    // 사용자의 메시지를 채팅 박스에 표시
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p class="user-msg"><strong>사용자:</strong> 온도: ${temperature}°C, 습도: ${humidity}%, 풍속: ${windSpeed}m/s</p>`;

    try {
        // 서버로 데이터 전송 및 GPT 응답 받기
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ temperature: Number(temperature), humidity: Number(humidity), wind_speed: Number(windSpeed) })
        });

        const data = await response.json();
        if (data.reply) {
            chatbox.innerHTML += `<p class="bot-msg"><strong>챗봇:</strong> ${data.reply}</p>`;
        } else {
            chatbox.innerHTML += `<p class="bot-msg"><strong>오류:</strong> 응답을 받을 수 없습니다.</p>`;
        }

    } catch (error) {
        chatbox.innerHTML += `<p class="bot-msg"><strong>오류:</strong> 서버 연결에 문제가 발생했습니다.</p>`;
    }

    // 스크롤을 맨 아래로 이동
    chatbox.scrollTop = chatbox.scrollHeight;
}
