# 🌟 AI Horoscope Generator

A beautiful, responsive web application that generates personalized daily horoscopes using AI. Built with Flask, HTML, CSS, and JavaScript, featuring a modern glassmorphism design and smooth animations.

## ✨ Features

- **AI-Powered Horoscopes**: Get personalized daily horoscopes generated using OpenRouter AI API
- **12 Zodiac Signs**: Complete support for all zodiac signs with their symbols and date ranges
- **Modern UI Design**: Beautiful glassmorphism design with galaxy/starry background
- **Dark/Light Theme**: Toggle between dark and light themes with persistent storage
- **Smooth Animations**: 
  - Typing effect for horoscope text
  - Hover effects with glow and scale animations
  - Particle effects on zodiac selection
  - Loading animations with spinning stars
- **Extra Features**:
  - Lucky Number generation
  - Lucky Color suggestion
  - Mood of the Day
  - Refresh functionality for new readings
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Accessibility**: Keyboard shortcuts and screen reader friendly
- **No Database Required**: Direct AI API integration without database dependencies

## 🎯 Demo

### Desktop View
- Click any zodiac sign to get your horoscope
- Watch the beautiful typing animation reveal your reading
- Use the theme toggle in the top-right corner
- Press 'R' to refresh your current horoscope

### Mobile View
- Responsive grid layout adapts to smaller screens
- Touch-friendly buttons and smooth scrolling
- All animations work smoothly on mobile devices

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- OpenRouter API Key (get one at [OpenRouter.ai](https://openrouter.ai))

### Quick Start

1. **Clone/Download the project**
   ```bash
   # If you have the files, navigate to the directory
   cd AI_Horoscope_Generator
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # On Windows
   python -m venv horoscope_env
   horoscope_env\\Scripts\\activate
   
   # On macOS/Linux  
   python3 -m venv horoscope_env
   source horoscope_env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   - Open `app.py`
   - Replace `OPENROUTER_API_KEY` with your actual OpenRouter API key
   ```python
   OPENROUTER_API_KEY = "your-api-key-here"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:5000`
   - Enjoy your AI-powered horoscope generator!

## 📁 Project Structure

```
AI_Horoscope_Generator/
│
├── app.py                 # Flask backend with API integration
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
│
├── templates/
│   └── index.html        # Main HTML template
│
└── static/
    ├── style.css         # Modern CSS with glassmorphism
    └── script.js         # JavaScript functionality
```

## 🔧 Technical Details

### Backend (Flask)
- **Routes**:
  - `/` - Serves the main homepage
  - `/get_horoscope` - API endpoint for generating horoscopes
- **AI Integration**: Uses OpenRouter API with DeepSeek Chat model
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Security**: API key stored securely on backend (not exposed to frontend)

### Frontend
- **HTML**: Semantic markup with accessibility features
- **CSS**: 
  - CSS Grid and Flexbox for responsive layouts
  - CSS Variables for easy theme switching
  - Advanced animations using keyframes
  - Glassmorphism design with backdrop-filter
- **JavaScript**:
  - Modern ES6+ syntax
  - Fetch API for AJAX requests
  - Local Storage for theme persistence
  - Intersection Observer for scroll animations

### Features Implementation

#### 🎨 Theme System
- Automatic theme detection and persistence
- Smooth transitions between themes
- Custom CSS variables for easy customization

#### 🌌 Animation System
- CSS-based animations for performance
- JavaScript-controlled timing for better UX
- Particle effects using DOM manipulation

#### 📱 Responsive Design
- Mobile-first approach
- Flexible grid system
- Touch-friendly interactions

## 🔮 How It Works

1. **User selects a zodiac sign** → Triggers zodiac card click event
2. **Frontend sends AJAX request** → POST request to `/get_horoscope` endpoint
3. **Backend calls AI API** → OpenRouter API generates horoscope text
4. **Response processed** → Additional features (lucky number, color, mood) added
5. **Frontend displays results** → Typing animation reveals the horoscope
6. **Extra features shown** → Lucky number, color, and mood displayed with animations

## 🎯 API Integration

The app uses OpenRouter AI API for horoscope generation:

```python
# Example API call structure
{
    "model": "deepseek/deepseek-chat-v3.1:free",
    "messages": [
        {
            "role": "user", 
            "content": "Generate a short, positive horoscope for [zodiac sign]"
        }
    ]
}
```

## 🚀 Deployment Options

### Local Development
- Use `python app.py` for development
- Flask development server runs on `localhost:5000`

### Production Deployment
- Use Gunicorn: `gunicorn app:app`
- Deploy to platforms like Heroku, DigitalOcean, or AWS
- Set environment variables for API keys in production

### Environment Variables (Production)
```bash
export OPENROUTER_API_KEY="your-api-key"
export FLASK_ENV="production"
```

## 🔧 Customization

### Adding New Features
- **New zodiac information**: Modify the `ZODIAC_SIGNS` dictionary in `app.py`
- **Different AI models**: Change the `model` parameter in the API call
- **Custom styling**: Update CSS variables in `style.css`
- **New animations**: Add keyframe animations in CSS or JavaScript

### Changing AI Prompts
Modify the prompt in `app.py`:
```python
prompt = f"Your custom prompt for {ZODIAC_SIGNS[zodiac_sign]}"
```

### UI Customization
All colors and styles are controlled by CSS variables in `:root` and `[data-theme="light"]` selectors.

## 📱 Browser Support

- ✅ Chrome 80+
- ✅ Firefox 78+  
- ✅ Safari 13+
- ✅ Edge 80+
- ⚠️ Internet Explorer: Not supported (uses modern CSS features)

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenRouter API key is valid and has credits
   - Check that the API key is correctly set in `app.py`

2. **Network Errors**
   - Check your internet connection
   - Verify OpenRouter API is accessible

3. **Installation Issues**
   - Make sure Python 3.7+ is installed
   - Try upgrading pip: `pip install --upgrade pip`

4. **Port Already in Use**
   - Change the port in `app.py`: `app.run(port=5001)`
   - Or kill the process using the port

## 🔐 Security Notes

- API keys are stored on the backend and never exposed to the client
- CORS is handled appropriately for same-origin requests
- Input validation prevents malicious zodiac sign inputs
- Error messages don't reveal sensitive system information

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Create an issue with detailed information about the problem

## 🌟 Acknowledgments

- **OpenRouter.ai** for providing the AI API
- **Font Awesome** for beautiful icons
- **Google Fonts (Poppins)** for typography
- **CSS Gradient** inspiration for background designs

---

**Made with ❤️ and ✨ by AI Horoscope Generator**

*For entertainment purposes only - May the stars guide your code!* 🌟
