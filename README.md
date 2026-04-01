# WeatherDash 🌤️

A simple weather dashboard that aggregates data from multiple APIs.

## Features
- Real-time weather data from OpenWeatherMap
- AI-powered weather summaries using GPT-4
- Cloud storage for historical data (AWS S3)
- Stripe integration for premium tier
- Slack notifications for severe weather alerts

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python app/main.py
```

## Configuration

Copy `.env.example` to `.env` and fill in your API keys. See `config.py` for additional settings.

## TODO
- [ ] Add Redis caching
- [ ] Migrate to PostgreSQL
- [ ] Deploy to AWS ECS
- [ ] Fix the memory leak in /forecast endpoint

## License
MIT
