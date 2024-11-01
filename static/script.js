async function sendWeather() {
    const temperature = document.getElementById("temperature").value;
    const humidity = document.getElementById("humidity").value;
    const windSpeed = document.getElementById("wind_speed").value;

    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ temperature: Number(temperature), humidity: Number(humidity), wind_speed: Number(windSpeed) })
    });

    const data = await response.json();
    document.getElementById("chatbox").innerHTML = `<p><strong>챗봇:</strong> ${data.reply}</p>`;
}
