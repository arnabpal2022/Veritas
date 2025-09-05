# Veritas - AI News Daily 📰

An intelligent news aggregation system that searches, summarizes, and presents AI-related news in a beautiful blog-style interface.

## Features

- 🔍 **Smart News Search**: Automatically finds the latest AI news from multiple sources
- 📝 **AI-Powered Summarization**: Creates concise, readable summaries of news articles
- 📰 **Blog-Style Interface**: Beautiful, responsive web interface with Inter font
- 📅 **Historical Reports**: Browse news reports from different dates
- 🎨 **Modern UI**: Clean, professional design with smooth animations

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Veritas

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file with your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Run the Application

#### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```

Access the application at: `http://localhost:8501`

#### Command Line
```bash
# Generate a new report
python main.py

# Dry run (safe fallback mode)
python main.py --dry-run
```

## How It Works

1. **Search**: The system searches for the latest AI news using web search APIs
2. **Summarize**: Each article is processed and summarized using LLM models
3. **Publish**: All summaries are compiled into a comprehensive daily report
4. **Display**: The web interface presents reports in an elegant blog format

## Web Interface Features

- **📊 Dashboard**: View statistics and generate new reports
- **📅 Date Selection**: Browse reports from different dates
- **🔄 One-Click Generation**: Generate new reports instantly
- **📱 Responsive Design**: Works perfectly on desktop and mobile
- **🎨 Inter Font**: Modern, readable typography

## Project Structure

```
Veritas/
├── app/                    # Main application code
│   ├── agents/            # AI agents (search, summarize, publish)
│   ├── workflow.py        # LangGraph workflow definition
│   ├── models.py          # Data models
│   └── prompts.py         # AI prompts
├── streamlit_app.py       # Web interface
├── main.py               # CLI entry point
└── requirements.txt      # Dependencies
```

## Requirements

- Python 3.9+
- Streamlit
- LangChain & LangGraph
- Groq API access
- Tavily API access (for news search)

## API Keys

If API keys are not set, the package uses safe fallbacks for local testing.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

