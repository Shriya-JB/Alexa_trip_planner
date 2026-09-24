from flask import Flask, request, jsonify, render_template_string
from server import search_flights, search_hotels, build_itinerary, plan_trip

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Trip Orchestrator - Alexa+ Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; background: #f4f4f4; }
        h1 { text-align: center; color: #232f3e; }
        #chat { background: white; border-radius: 10px; padding: 20px; min-height: 300px; margin-bottom: 20px; }
        .bubble { padding: 12px 16px; border-radius: 16px; margin: 10px 0; max-width: 80%; white-space: pre-wrap; }
        .user { background: #007185; color: white; margin-left: auto; text-align: right; }
        .alexa { background: #eee; color: #111; }
        form { display: flex; flex-wrap: wrap; gap: 14px; background: white; padding: 16px; border-radius: 10px; }
        .field { display: flex; flex-direction: column; font-size: 12px; color: #444; }
        .field label { margin-bottom: 4px; font-weight: bold; }
        input { padding: 8px; font-size: 14px; }
        button { background: #ff9900; border: none; border-radius: 6px; cursor: pointer; padding: 10px 16px; font-size: 14px; align-self: flex-end; }
    </style>
</head>
<body>
    <h1>Alexa+ Trip Orchestrator (Demo)</h1>
    <div id="chat"></div>
    <form id="tripForm">
        <div class="field">
            <label for="origin">Origin airport code</label>
            <input type="text" id="origin" placeholder="e.g. LHR" required>
        </div>
        <div class="field">
            <label for="destination_airport">Destination airport code</label>
            <input type="text" id="destination_airport" placeholder="e.g. JFK" required>
        </div>
        <div class="field">
            <label for="destination_city">Destination city name</label>
            <input type="text" id="destination_city" placeholder="e.g. New York" required>
        </div>
        <div class="field">
            <label for="departure_date">Flight departure date</label>
            <input type="date" id="departure_date" required>
        </div>
        <div class="field">
            <label for="check_in">Hotel check-in date</label>
            <input type="date" id="check_in" required>
        </div>
        <div class="field">
            <label for="check_out">Hotel check-out date</label>
            <input type="date" id="check_out" required>
        </div>
        <div class="field">
            <label for="num_days">Trip length (days)</label>
            <input type="number" id="num_days" placeholder="e.g. 4" required>
        </div>
        <button type="submit">Plan Trip</button>
    </form>

    <script>
        const form = document.getElementById('tripForm');
        const chat = document.getElementById('chat');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const data = {
                origin: document.getElementById('origin').value,
                destination_airport: document.getElementById('destination_airport').value,
                destination_city: document.getElementById('destination_city').value,
                departure_date: document.getElementById('departure_date').value,
                check_in: document.getElementById('check_in').value,
                check_out: document.getElementById('check_out').value,
                num_days: document.getElementById('num_days').value,
            };

            if (data.check_out <= data.check_in) {
                alert('Check-out date must be after check-in date.');
                return;
            }

            const userBubble = document.createElement('div');
            userBubble.className = 'bubble user';
            userBubble.innerText = `Plan me a ${data.num_days}-day trip from ${data.origin} to ${data.destination_city}`;
            chat.appendChild(userBubble);

            const loadingBubble = document.createElement('div');
            loadingBubble.className = 'bubble alexa';
            loadingBubble.innerText = 'Thinking...';
            chat.appendChild(loadingBubble);

            const response = await fetch('/plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();

            loadingBubble.innerText = result.plan;
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/plan", methods=["POST"])
def plan():
    data = request.get_json()
    result = plan_trip(
        origin=data["origin"],
        destination_airport=data["destination_airport"],
        destination_city=data["destination_city"],
        departure_date=data["departure_date"],
        check_in=data["check_in"],
        check_out=data["check_out"],
        num_days=int(data["num_days"]),
    )
    return jsonify({"plan": result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)