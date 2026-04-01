"""
WeatherDash - Main Application
"""
from flask import Flask, jsonify, request, render_template
from config import config_map
import openai
import boto3
import os

app = Flask(__name__)
app.config.from_object(config_map.get(os.getenv("FLASK_ENV", "development")))

# Initialize OpenAI client
openai.api_key = app.config["OPENAI_API_KEY"]

# Initialize AWS S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather/<city>")
def get_weather(city):
    """Fetch current weather for a city."""
    import requests

    api_key = app.config["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = resp.json()
    return jsonify({
        "city": data["name"],
        "temp": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
    })


@app.route("/api/forecast/<city>")
def get_forecast(city):
    """Get AI-generated weather summary."""
    import requests

    api_key = app.config["OPENWEATHER_API_KEY"]
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return jsonify({"error": "Forecast unavailable"}), 404

    weather_data = resp.json()

    # Use GPT-4 to summarize
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize this weather forecast in a friendly way."},
            {"role": "user", "content": str(weather_data["list"][:8])},
        ],
        max_tokens=200,
    )

    return jsonify({
        "city": city,
        "summary": completion.choices[0].message.content,
    })


@app.route("/api/history/<city>")
def get_history(city):
    """Fetch historical weather data from S3."""
    try:
        obj = s3_client.get_object(
            Bucket=app.config["AWS_S3_BUCKET"],
            Key=f"history/{city}.json",
        )
        data = obj["Body"].read().decode("utf-8")
        return jsonify({"city": city, "history": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    """Handle Stripe payment webhooks for premium tier."""
    import stripe
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]

    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return jsonify({"error": "Invalid signature"}), 400

    if event["type"] == "checkout.session.completed":
        # Grant premium access
        pass

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
