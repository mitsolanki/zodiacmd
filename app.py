from flask import Flask, render_template, request, jsonify
import requests
import json
import random

app = Flask(__name__)

# OpenRouter API configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Zodiac signs data
ZODIAC_SIGNS = {
    "aries": "♈ Aries",
    "taurus": "♉ Taurus", 
    "gemini": "♊ Gemini",
    "cancer": "♋ Cancer",
    "leo": "♌ Leo",
    "virgo": "♍ Virgo",
    "libra": "♎ Libra",
    "scorpio": "♏ Scorpio",
    "sagittarius": "♐ Sagittarius",
    "capricorn": "♑ Capricorn",
    "aquarius": "♒ Aquarius",
    "pisces": "♓ Pisces"
}

# Lucky colors and moods for extra features
LUCKY_COLORS = ["Golden", "Silver", "Ruby Red", "Emerald Green", "Sapphire Blue", "Amethyst Purple", "Rose Gold", "Turquoise", "Coral", "Ivory"]
MOODS = ["Energetic", "Peaceful", "Confident", "Creative", "Adventurous", "Romantic", "Focused", "Optimistic", "Mysterious", "Cheerful"]

@app.route('/')
def index():
    """Serve the homepage"""
    return render_template('index.html')

@app.route('/get_horoscope', methods=['POST'])
def get_horoscope():
    """Generate horoscope using OpenRouter AI API"""
    try:
        # Get zodiac sign from request
        data = request.get_json()
        zodiac_sign = data.get('zodiac_sign', '').lower()
        
        if zodiac_sign not in ZODIAC_SIGNS:
            return jsonify({'error': 'Invalid zodiac sign'}), 400
        
        # Prepare the AI prompt
        prompt = f"Generate a short, positive, and fun horoscope for {ZODIAC_SIGNS[zodiac_sign]} for today. Make it engaging, optimistic, and about 2-3 sentences long. Focus on love, career, health, or general life advice."
        
        # Make request to OpenRouter API
        headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
    
}

        
        payload = {
            "model": "deepseek/deepseek-chat-v3.1:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        ai_response = response.json()
        horoscope_text = ai_response['choices'][0]['message']['content']
        
        # Generate additional fun features
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
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except KeyError as e:
        return jsonify({'error': f'API response format error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
