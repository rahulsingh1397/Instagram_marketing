# Instagram Marketing Automation

A powerful Python-based automation tool for Instagram marketing that leverages AI to streamline content creation, scheduling, and engagement.

## ✨ Features

- **AI-Powered Content Generation**: Create engaging Instagram posts using advanced AI models
- **Automated Scheduling**: Plan and schedule posts for optimal engagement times
- **Hashtag Research**: Automatically find trending and relevant hashtags
- **Audience Engagement**: Automate likes, comments, and follows based on target criteria
- **Analytics**: Track post performance and audience growth
- **Multi-Agent System**: Utilizes CrewAI for intelligent task delegation

## 🚀 Prerequisites

- Python 3.9+
- pip (Python package manager)
- Instagram Business or Creator Account
- API keys (OpenAI, Serper, etc.)

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/instagram-marketing.git
   cd instagram-marketing
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Copy the example environment file and update with your API keys:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your credentials:
   ```
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_ORGANIZATION=your_org_id
   
   # Serper API Key for search functionality
   SERPER_API_KEY=your_serper_api_key
   
   # Optional: Gemini API Key
   GEMINI_API_KEY=your_gemini_api_key
   ```

## 🚦 Usage

1. Run the main application:
   ```bash
   python instagram/src/instagram/main.py
   ```

2. Follow the interactive prompts to:
   - Generate content ideas
   - Create posts
   - Schedule content
   - Analyze performance

## 📁 Project Structure

```
instagram-marketing/
├── instagram/
│   └── src/
│       └── instagram/
│           ├── __init__.py
│           ├── main.py           # Main application entry point
│           ├── crew.py           # CrewAI configuration
│           ├── agents/           # AI agent definitions
│           ├── tasks/            # Task definitions
│           └── tools/            # Custom tools for agents
├── .env.example                  # Example environment variables
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `OPENAI_ORGANIZATION` | No | Your OpenAI organization ID |
| `SERPER_API_KEY` | Yes | Serper API key for search functionality |
| `GEMINI_API_KEY` | No | Google Gemini API key (alternative to OpenAI) |
| `MODEL` | No | Default AI model to use (default: gemini-pro) |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [Your Name] | [Website](https://your-website.com)
