from flask import Flask, render_template, request, jsonify
import requests
import json
import random
import os

app = Flask(__name__)

# OpenRouter API configuration - Use environment variable for security
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', "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")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Zodiac signs data
ZODIAC_SIGNS = {
    "aries": "♈ Aries", "taurus": "♉ Taurus", "gemini": "♊ Gemini", "cancer": "♋ Cancer",
    "leo": "♌ Leo", "virgo": "♍ Virgo", "libra": "♎ Libra", "scorpio": "♏ Scorpio",
    "sagittarius": "♐ Sagittarius", "capricorn": "♑ Capricorn", "aquarius": "♒ Aquarius", "pisces": "♓ Pisces"
}

# Lucky extras
LUCKY_COLORS = ["Golden", "Silver", "Ruby Red", "Emerald Green", "Sapphire Blue", "Amethyst Purple", "Rose Gold", "Turquoise", "Coral", "Ivory"]
MOODS = ["Energetic", "Peaceful", "Confident", "Creative", "Adventurous", "Romantic", "Focused", "Optimistic", "Mysterious", "Cheerful"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/get_horoscope', methods=['POST'])
def get_horoscope():
    try:
        data = request.get_json()
        zodiac_sign = data.get('zodiac_sign', '').lower()

        if zodiac_sign not in ZODIAC_SIGNS:
            return jsonify({'error': 'Invalid zodiac sign'}), 400

        prompt = f"Generate a short, positive, and fun horoscope for {ZODIAC_SIGNS[zodiac_sign]} for today. Make it engaging, optimistic, and about 2-3 sentences long. Focus on love, career, health, or general life advice."

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": request.host_url,  # Required by OpenRouter
            "X-Title": "Horoscope App"  # Required by OpenRouter
        }

        payload = {
            "model": "openai/gpt-oss-120b:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 150
        }

        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        ai_response = response.json()
        horoscope_text = ai_response['choices'][0]['message']['content']

        # Fun extras
        lucky_number = random.randint(1, 99)
        lucky_color = random.choice(LUCKY_COLORS)
        mood = random.choice(MOODS)

        return jsonify({
            'success': True,
            'zodiac_sign': ZODIAC_SIGNS[zodiac_sign],
            'horoscope': horoscope_text,
            'lucky_number': lucky_number,
            'lucky_color': lucky_color,
            'mood': mood
        })

    except requests.exceptions.RequestException as e:
        # More detailed error handling
        error_msg = f'API request failed: {str(e)}'
        if hasattr(e.response, 'text'):
            error_msg += f" - Response: {e.response.text}"
        return jsonify({'error': error_msg}), 500
    except KeyError as e:
        return jsonify({'error': f'API response format error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
