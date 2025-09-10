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

def generate_fallback_horoscope(zodiac_sign):
    """Generate a fallback horoscope if API fails"""
    horoscopes = {
        "aries": "Today brings exciting opportunities! Your fiery energy is at its peak, making it perfect for new beginnings and bold moves. The universe supports your courageous spirit.",
        "taurus": "Stability and comfort are your themes today. Focus on practical matters and enjoy life's simple pleasures. Your patience will be rewarded beautifully.",
        "gemini": "Your communication skills shine brightly today! Connect with others and share your brilliant ideas. Social interactions bring unexpected joys.",
        "cancer": "Emotional clarity arrives today. Trust your intuition in personal matters and nurture your relationships. Home and family bring deep satisfaction.",
        "leo": "Creativity and confidence flow through you! Express yourself boldly and attract positive attention. Your radiant energy inspires everyone around you.",
        "virgo": "Organization brings peace and productivity. Tackle tasks methodically for best results. Attention to detail leads to significant accomplishments.",
        "libra": "Harmony prevails in relationships today. Seek balance in all your interactions and make time for beauty. Your diplomatic skills smooth any tensions.",
        "scorpio": "Powerful transformation opportunities arise. Embrace change with confidence and trust your inner strength. Deep connections bring profound insights.",
        "sagittarius": "Adventure calls! Explore new horizons with optimism and joy. Learning something new expands your perspective in wonderful ways.",
        "capricorn": "Career progress is highlighted today. Your hard work is about to pay off significantly. Ambitious goals feel within reach.",
        "aquarius": "Innovative ideas emerge from your unique perspective. Think outside the box and inspire others with your vision. Originality leads to success.",
        "pisces": "Compassion and intuition guide you today. Your empathy creates meaningful connections and artistic inspiration flows freely. Dreams hold important messages."
    }
    return horoscopes.get(zodiac_sign, "Today is a beautiful day filled with infinite potential! Embrace the magic around you and trust that wonderful opportunities are coming your way.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/get_horoscope', methods=['POST'])
def get_horoscope():
    try:
        data = request.get_json()
        zodiac_sign = data.get('zodiac_sign', '').lower()

        if zodiac_sign not in ZODIAC_SIGNS:
            return jsonify({'error': 'Invalid zodiac sign'}), 400

        # Try to use OpenRouter API first
        try:
            prompt = f"Generate a short, positive, and fun horoscope for {ZODIAC_SIGNS[zodiac_sign]} for today. Make it engaging, optimistic, and about 2-3 sentences long. Focus on love, career, health, or general life advice."

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": request.host_url,
                "X-Title": "Horoscope App"
            }

            payload = {
                "model": "openai/gpt-3.5-turbo",  # Use a more reliable model
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150
            }

            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=10)
            response.raise_for_status()

            ai_response = response.json()
            horoscope_text = ai_response['choices'][0]['message']['content']
            api_used = True
            
        except Exception as api_error:
            # If API fails, use the fallback horoscope
            horoscope_text = generate_fallback_horoscope(zodiac_sign)
            api_used = False

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
            'mood': mood,
            'api_used': api_used
        })

    except Exception as e:
        # Ultimate fallback in case of any other errors
        horoscope_text = generate_fallback_horoscope(zodiac_sign if 'zodiac_sign' in locals() else '')
        
        return jsonify({
            'success': True,
            'zodiac_sign': ZODIAC_SIGNS.get(zodiac_sign, "Unknown Sign"),
            'horoscope': horoscope_text,
            'lucky_number': random.randint(1, 99),
            'lucky_color': random.choice(LUCKY_COLORS),
            'mood': random.choice(MOODS),
            'api_used': False,
            'fallback': True
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
