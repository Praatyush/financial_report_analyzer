# Financial Report Analyzer

A Python script that downloads PDF financial reports, extracts text, and generates comprehensive summaries using OpenAI's GPT models.

## 🚀 Features

- **Batch Processing**: Analyze multiple PDF reports from URLs
- **Smart Chunking**: Handles large documents by splitting into manageable chunks
- **AI-Powered Analysis**: Uses OpenAI GPT models for intelligent financial analysis
- **Company Recognition**: Automatically extracts company names from URLs
- **Individual Reports**: Generates separate analysis files for each company
- **Configurable Prompts**: Customizable analysis prompts via external files
- **Professional Output**: Email-ready executive summaries

## 📋 Requirements

- Python 3.7+
- OpenAI API key
- Required packages: `pdfplumber`, `openai`, `requests`

## 🛠️ Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd financial-report-analyzer
```

2. Install required packages:
```bash
pip install pdfplumber openai requests
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 📖 Usage

### Basic Usage

1. Add PDF URLs to `urls.txt` (one URL per line):
```
https://www.novartis.com/sites/novartis_com/files/q2-2025-media-release-en.pdf
https://www.gsk.com/media/fcgpta0r/q2-2025-pre-announcement-aide-memoire.pdf
```

2. Run the analyzer:
```bash
python3 financial_report_analyzer.py --api-key "your-api-key"
```

3. Find individual analyses in the `individual_analysis/` folder:
- `novartis_analysis.txt`
- `gsk_analysis.txt`
- etc.

### Command Line Options

```bash
python3 financial_report_analyzer.py [OPTIONS]

Options:
  --api-key TEXT          OpenAI API key (or set OPENAI_API_KEY env var)
  --model TEXT           OpenAI model to use (default: gpt-4o-mini)
  --chunk-size INTEGER   Words per chunk (default: 2500)
  --output-dir TEXT      Output directory (default: individual_analysis)
  --prompt-file TEXT     Path to prompts file (default: prompts.txt)
  --url-file TEXT        Path to URLs file (default: urls.txt)
  --verbose, -v          Enable verbose logging
  --help                 Show help message
```

## 📁 File Structure

```
financial-report-analyzer/
├── financial_report_analyzer.py  # Main script
├── prompts.txt                   # Analysis prompts
├── urls.txt                      # PDF URLs to analyze
├── individual_analysis/          # Output folder (auto-created)
│   ├── novartis_analysis.txt
│   ├── gsk_analysis.txt
│   └── ...
└── README.md
```

## 🔧 Configuration

### Customizing Analysis Prompts

Edit `prompts.txt` to customize the analysis prompts:

```
[CHUNK_ANALYSIS_PROMPT]
You are analyzing a financial report...

[SUMMARY_COMBINATION_PROMPT]
You are a senior financial analyst...
```

### Supported URL Formats

The script automatically recognizes major pharmaceutical companies:
- Novartis
- GSK
- Takeda
- Pfizer
- Roche
- J&J
- Merck
- AbbVie
- Amgen
- Gilead

## 📊 Analysis Categories

Each report analyzes:

1. **Financial Performance**: Revenue, profits, key metrics, YoY changes
2. **Strategic Direction**: New initiatives, partnerships, market expansion
3. **Risks and Uncertainties**: Challenges, regulatory concerns
4. **Future Outlook**: Guidance, projections, planned investments
5. **Regional Performance**: North America and Europe analysis

## 🎯 Workflow

For each URL:
1. Download PDF
2. Extract and clean full text
3. Split into chunks (~2500 words)
4. Analyze each chunk with LLM
5. Combine chunk analyses into final report
6. Save as individual company file

## 🚀 PyInstaller Ready

This script is designed to be packaged as an executable:

```bash
pip install pyinstaller
pyinstaller --onefile financial_report_analyzer.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This tool is for informational purposes only. Always verify financial analysis with professional advisors.

## 🆘 Support

For issues or questions, please create an issue in the GitHub repository. 