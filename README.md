# 🏦 Financial Report Analyzer

A powerful tool that downloads PDF financial reports, extracts text, and generates comprehensive AI-powered summaries using OpenAI's GPT models. **Designed for non-technical users** - just edit text files and double-click to run!

## ✨ Features

- **📄 PDF Processing**: Downloads and extracts text from financial report PDFs
- **🤖 AI Analysis**: Uses OpenAI GPT-4o-mini for intelligent financial analysis  
- **📊 Batch Processing**: Analyzes multiple reports automatically
- **💼 Executive Summaries**: Generates professional summaries ready for email/presentations
- **🎯 Non-Technical Friendly**: No coding or terminal knowledge required
- **🖱️ Double-Click Execution**: Packaged as standalone executable
- **🔧 Configurable**: Easy-to-edit text files for URLs and prompts
- **🌍 Regional Analysis**: Includes North America and Europe performance analysis

## 🚀 Quick Start for Non-Technical Users

### 📦 **Ready-to-Use Distribution Package**

1. **Download** the complete `distribution_package/` folder
2. **Setup API Key**: 
   - Rename `env_template.txt` to `.env`
   - Edit `.env` and add your OpenAI API key: `OPENAI_API_KEY=sk-your-key-here`
3. **Add URLs**: Edit `urls.txt` and add your PDF URLs (one per line)
4. **Run Analysis**: Double-click `financial_report_analyzer_fixed.app` (Mac)
5. **Get Results**: Check the `individual_analysis/` folder for your reports

### 📁 Distribution Package Contents
```
distribution_package/
├── financial_report_analyzer_fixed.app    # Main app (Mac) - WORKING VERSION
├── financial_report_analyzer              # Executable (Linux/Windows)
├── env_template.txt                       # API key template
├── urls.txt                              # PDF URLs to analyze (editable)
├── prompts.txt                           # Analysis prompts (editable)
├── USER_INSTRUCTIONS.txt                 # Detailed user guide
├── run_analysis.bat                      # Windows batch script
└── individual_analysis/                  # Results folder (auto-created)
```

## 🛠️ Installation & Setup

### For Developers

1. **Clone this repository:**
```bash
git clone https://github.com/Praatyush/financial_report_analyzer.git
cd financial_report_analyzer
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment:**
```bash
cp env_template.txt .env
# Edit .env and add your OpenAI API key
```

4. **Run directly:**
```bash
python3 financial_report_analyzer_fixed.py
```

### For Distribution

1. **Build executable:**
```bash
# Install PyInstaller
pip install pyinstaller

# Build GUI version (no console)
pyinstaller --onefile --noconsole financial_report_analyzer_fixed.py

# Build console version (for debugging)
pyinstaller --onefile financial_report_analyzer_fixed.py
```

2. **Distribute:**
   - Copy executable from `dist/` folder
   - Include `urls.txt`, `prompts.txt`, `env_template.txt`
   - Provide `USER_INSTRUCTIONS.txt`

## 📖 Usage

### For End Users (Recommended)

1. **Set up your API key**: Edit `.env` file:
```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

2. **Add PDF URLs**: Edit `urls.txt` (one URL per line):
```
https://www.novartis.com/sites/novartis_com/files/q2-2025-media-release-en.pdf
https://www.gsk.com/media/fcgpta0r/q2-2025-pre-announcement-aide-memoire.pdf
```

3. **Customize prompts** (optional): Edit `prompts.txt`

4. **Run analysis**: 
   - **Mac**: Double-click `financial_report_analyzer_fixed.app`
   - **Windows**: Double-click `run_analysis.bat`
   - **Linux**: Double-click the executable

5. **View results**: Check `individual_analysis/` folder

### For Developers

```bash
# Run the fixed version directly
python3 financial_report_analyzer_fixed.py
```

**Default Settings:**
- Model: `gpt-4o-mini`
- Chunk size: `2500` words
- Output directory: `individual_analysis/`

## 📁 File Structure

```
financial-report-analyzer/
├── financial_report_analyzer.py           # Original version
├── financial_report_analyzer_fixed.py     # WORKING VERSION ✅
├── test_gui.py                            # GUI test script
├── test_gui2.py                           # Enhanced GUI test
├── prompts.txt                            # Analysis prompts (editable)
├── urls.txt                               # PDF URLs to analyze (editable)
├── .env                                   # OpenAI API key (create from template)
├── env_template.txt                       # Template for .env file
├── requirements.txt                       # Python dependencies
├── distribution_package/                  # Complete user package
│   ├── financial_report_analyzer_fixed.app # Working Mac app ✅
│   ├── financial_report_analyzer         # Linux/Windows executable
│   ├── urls.txt                          # User-editable URLs
│   ├── prompts.txt                       # User-editable prompts
│   ├── .env                              # User's API key
│   ├── env_template.txt                  # API key template
│   ├── USER_INSTRUCTIONS.txt             # Detailed user guide
│   ├── run_analysis.bat                  # Windows launcher
│   └── individual_analysis/              # Results (auto-created)
├── individual_analysis/                   # Output folder (auto-created)
│   ├── novartis_analysis.txt
│   ├── gsk_analysis.txt
│   └── ...
└── README.md
```

## ⚙️ Configuration

### API Key Setup
Create `.env` file in the same directory as the executable:
```
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### URLs Configuration
Edit `urls.txt` file (one URL per line):
```
# Add your PDF URLs here
https://example.com/financial-report.pdf
https://another-company.com/quarterly-report.pdf
```

### Prompts Customization
Edit `prompts.txt` to modify analysis instructions:
```
[CHUNK_ANALYSIS_PROMPT]
Your analysis instructions here...

[SUMMARY_COMBINATION_PROMPT]
Your summary combination instructions here...
```

## 📊 Analysis Categories

The tool analyzes financial reports across these key areas:

1. **Executive Summary** - Key highlights and overview
2. **Financial Performance** - Revenue, profits, margins, cash flow, YoY changes  
3. **Strategic Initiatives** - New business developments, partnerships, investments
4. **Risk Factors** - Identified risks, challenges, regulatory concerns
5. **Future Outlook** - Guidance, projections, expected trends
6. **Regional Performance** - North America and Europe specific analysis

## 🔄 Workflow

### For Each URL:
1. **Download** PDF from the provided URL
2. **Extract** and clean text content
3. **Split** into chunks (~2500 words each) 
4. **Analyze** each chunk using LLM
5. **Combine** chunk analyses into final report
6. **Save** as individual company file

### Output Files:
- `novartis_analysis.txt` - Complete Novartis analysis
- `gsk_analysis.txt` - Complete GSK analysis  
- etc.

## 🚀 Building Executable with PyInstaller

### For Mac (GUI Version - Recommended)
```bash
pyinstaller --onefile --noconsole financial_report_analyzer_fixed.py
```

### For Windows/Linux (Console Version)
```bash
pyinstaller --onefile financial_report_analyzer_fixed.py
```

### Distribution Files
When distributing the executable, include:
- `financial_report_analyzer_fixed` (or `.exe`)
- `urls.txt` (for users to edit)
- `prompts.txt` (for users to edit)  
- `env_template.txt` (for users to create `.env`)
- `USER_INSTRUCTIONS.txt` (user guide)

## 🔧 Technical Implementation

### Key Features:
- **Smart Path Resolution**: Automatically finds config files relative to executable location
- **Cross-Platform**: Works on Mac, Windows, and Linux
- **GUI Feedback**: User-friendly popup messages for success/error states
- **Robust Error Handling**: Comprehensive error messages with helpful guidance
- **Chunked Processing**: Handles large documents by intelligent text chunking
- **Company Name Extraction**: Automatically names output files based on company URLs

### The Fixed Version
`financial_report_analyzer_fixed.py` includes critical improvements:

- ✅ **Correct File Path Resolution**: Uses `get_app_directory()` to find config files
- ✅ **App Bundle Support**: Works properly when packaged as Mac `.app` bundle
- ✅ **Enhanced Error Messages**: Shows exact paths for debugging
- ✅ **GUI-Only Interface**: No command line arguments needed
- ✅ **Non-Technical User Ready**: True double-click execution

## 🐛 Troubleshooting

### Common Issues:

**"Missing API Key" popup:**
- Check that `.env` file exists in the same folder as the executable
- Verify API key format: `OPENAI_API_KEY=sk-your-key-here`

**"No URLs found" popup:**
- Check that `urls.txt` file exists in the same folder  
- Ensure URLs start with `http` and aren't commented out with `#`

**"Cannot find prompts.txt":**
- Verify `prompts.txt` exists in the same folder as the executable
- Check file has correct section headers: `[CHUNK_ANALYSIS_PROMPT]`, `[SUMMARY_COMBINATION_PROMPT]`

**Mac Security Warning:**
- Right-click the app → **Open** → **Open** to bypass security warning
- This only needs to be done once

## 📝 Requirements

- Python 3.7+ (for developers)
- OpenAI API key with sufficient credits
- Internet connection for PDF downloads and API calls
- PDF files must be accessible via direct HTTP/HTTPS URLs

### Python Dependencies
```
pdfplumber>=0.7.0
openai>=1.0.0  
requests>=2.25.0
python-dotenv>=0.19.0
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Users are responsible for:
- Ensuring they have permission to download and analyze the PDFs
- Compliance with OpenAI's usage policies
- API costs and usage monitoring
- Accuracy verification of generated summaries

The AI-generated summaries should be reviewed and verified before use in business decisions.

## 🏆 Success Story

**✅ Fully Tested & Working!**

This tool has been successfully tested with:
- Multiple financial report PDFs (Novartis, GSK, Takeda)
- Complete non-technical user workflow
- Mac executable (.app bundle) functionality
- Robust error handling and user feedback
- Professional-quality financial analysis output

**Ready for production use by non-technical users!** 🎉 