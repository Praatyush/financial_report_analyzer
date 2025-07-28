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
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
# Copy the template and add your API key
cp env_template.txt .env
# Edit .env file and replace with your actual API key
```

## 📖 Usage

### For End Users (Executable)

1. **Set up your API key**: Edit the `.env` file:
```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

2. **Add PDF URLs**: Edit `urls.txt` (one URL per line):
```
https://www.novartis.com/sites/novartis_com/files/q2-2025-media-release-en.pdf
https://www.gsk.com/media/fcgpta0r/q2-2025-pre-announcement-aide-memoire.pdf
```

3. **Customize prompts** (optional): Edit `prompts.txt` to modify analysis prompts

4. **Run the analysis**: 
   - **Windows**: Double-click `financial_report_analyzer.exe`
   - **Mac/Linux**: Double-click the executable or run `python3 financial_report_analyzer.py`

5. **View results**: Check the `individual_analysis/` folder for your reports:
   - `novartis_analysis.txt`
   - `gsk_analysis.txt`
   - etc.

### For Developers

```bash
# Run directly with Python
python3 financial_report_analyzer.py
```

**Default Settings:**
- Model: `gpt-4o-mini`
- Chunk size: `2500` words
- Output directory: `individual_analysis/`

## 📁 File Structure

```
financial-report-analyzer/
├── financial_report_analyzer.py  # Main script
├── prompts.txt                   # Analysis prompts (editable)
├── urls.txt                      # PDF URLs to analyze (editable)
├── .env                          # OpenAI API key (editable)
├── env_template.txt              # Template for .env file
├── requirements.txt              # Python dependencies
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

## 🚀 Building Executable with PyInstaller

### For Developers: Creating the Executable

1. **Install PyInstaller**:
```bash
pip install pyinstaller
```

2. **Build the executable**:
```bash
# For GUI version (no console window)
pyinstaller --onefile --noconsole financial_report_analyzer.py

# For console version (with debug output)
pyinstaller --onefile financial_report_analyzer.py
```

3. **Distribute to users**:
   - Copy the executable from `dist/` folder
   - Include these files alongside the executable:
     - `urls.txt` (for users to edit)
     - `prompts.txt` (for users to edit)
     - `env_template.txt` (for users to create `.env`)

### For Users: First-Time Setup

1. **Create your `.env` file**:
   - Rename `env_template.txt` to `.env`
   - Edit `.env` and add your OpenAI API key

2. **Add your URLs** to `urls.txt`

3. **Double-click the executable** to run analysis

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