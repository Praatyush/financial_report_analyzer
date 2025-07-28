#!/usr/bin/env python3
"""
Financial Report Analyzer - Fixed Version

A script to download PDF financial reports, extract text, and generate
comprehensive summaries using OpenAI's GPT models.

This version is fixed to find config files correctly when packaged as an executable.
"""

import os
import sys
import requests
import tempfile
import re
from typing import List, Optional, Dict
from pathlib import Path
import logging
from urllib.parse import urlparse
import tkinter as tk
from tkinter import messagebox

# Third-party imports
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv

# Hide the root tkinter window (we only want message boxes)
root = tk.Tk()
root.withdraw()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_app_directory():
    """
    Get the directory where the app/config files should be located.
    Works for both .app bundles and regular executables.
    """
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        app_path = sys.executable
        
        # If it's a .app bundle, go up to the parent directory
        if '.app' in app_path:
            # Extract the .app bundle path
            app_bundle_path = app_path.split('.app')[0] + '.app'
            # Return the directory containing the .app bundle
            return os.path.dirname(app_bundle_path)
        else:
            # Regular executable - return its directory
            return os.path.dirname(app_path)
    else:
        # Running as Python script
        return os.path.dirname(os.path.abspath(__file__))


class FinancialReportAnalyzer:
    """Main class for analyzing financial reports from PDF URLs."""
    
    def __init__(self, openai_api_key: str, chunk_size: int = 2500, model: str = "gpt-4o-mini"):
        """
        Initialize the analyzer.
        
        Args:
            openai_api_key: API key for OpenAI
            chunk_size: Maximum words per chunk for processing
            model: OpenAI model to use (default: gpt-4o-mini)
        """
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.chunk_size = chunk_size
        self.model = model
        self.app_dir = get_app_directory()
        self.prompts = self._load_prompts()
        
    def _load_prompts(self) -> Dict[str, str]:
        """
        Load prompts from the prompts file.
        
        Returns:
            Dictionary containing the prompts
            
        Raises:
            Exception: If prompt file is not found or invalid
        """
        prompt_file = os.path.join(self.app_dir, "prompts.txt")
        logger.info(f"Loading prompts from: {prompt_file}")
        
        try:
            if not os.path.exists(prompt_file):
                raise FileNotFoundError(f"Prompt file 'prompts.txt' not found in {self.app_dir}")
            
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            prompts = {}
            sections = content.split('[')
            
            for section in sections[1:]:  # Skip empty first element
                if ']' not in section:
                    continue
                    
                section_name, section_content = section.split(']', 1)
                prompts[section_name.strip()] = section_content.strip()
            
            required_prompts = ['CHUNK_ANALYSIS_PROMPT', 'SUMMARY_COMBINATION_PROMPT']
            for required in required_prompts:
                if required not in prompts:
                    raise ValueError(f"Required prompt section '[{required}]' not found in prompts.txt")
            
            logger.info(f"Successfully loaded {len(prompts)} prompt sections")
            return prompts
            
        except Exception as e:
            logger.error(f"Failed to load prompts: {e}")
            raise
    
    def _read_urls_from_file(self) -> List[str]:
        """
        Read URLs from the URL file.
        
        Returns:
            List of URLs to process
            
        Raises:
            Exception: If URL file is not found or contains no valid URLs
        """
        url_file = os.path.join(self.app_dir, "urls.txt")
        logger.info(f"Reading URLs from: {url_file}")
        
        try:
            if not os.path.exists(url_file):
                raise FileNotFoundError(f"URL file 'urls.txt' not found in {self.app_dir}")
            
            with open(url_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            urls = []
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    if line.startswith('http'):
                        urls.append(line)
                    else:
                        logger.warning(f"Line {line_num} in urls.txt does not appear to be a valid URL: {line}")
            
            if not urls:
                raise ValueError(f"No valid URLs found in urls.txt. Please add URLs (one per line) to the file.")
            
            logger.info(f"Found {len(urls)} valid URLs to process")
            return urls
            
        except Exception as e:
            logger.error(f"Failed to read URLs from file: {e}")
            raise
    
    def _extract_company_name_from_url(self, url: str) -> str:
        """
        Extract a clean company name from the URL for filename generation.
        
        Args:
            url: The URL to extract company name from
            
        Returns:
            Clean company name suitable for filename
        """
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Remove common prefixes
            domain = re.sub(r'^(www\.|assets\.|assets-dam\.)', '', domain)
            
            # Extract main domain name (before TLD)
            domain_parts = domain.split('.')
            if len(domain_parts) >= 2:
                company_name = domain_parts[0]
                
                # Handle special cases for common patterns
                company_mapping = {
                    'novartis': 'novartis',
                    'gsk': 'gsk',
                    'takeda': 'takeda',
                    'pfizer': 'pfizer',
                    'roche': 'roche',
                    'jnj': 'johnson_and_johnson',
                    'merck': 'merck',
                    'abbvie': 'abbvie',
                    'amgen': 'amgen',
                    'gilead': 'gilead'
                }
                
                # Check if we have a known mapping
                for key, value in company_mapping.items():
                    if key in company_name:
                        return value
                
                # Clean up the company name
                company_name = re.sub(r'[^a-zA-Z0-9]', '_', company_name)
                return company_name.lower()
            
            # Fallback to cleaned domain
            clean_domain = re.sub(r'[^a-zA-Z0-9]', '_', domain.split('.')[0])
            return clean_domain.lower()
            
        except Exception as e:
            logger.warning(f"Could not extract company name from URL {url}: {e}")
            return None
        
    def download_pdf(self, url: str) -> str:
        """
        Download PDF from URL to temporary file.
        
        Args:
            url: URL of the PDF to download
            
        Returns:
            Path to downloaded PDF file
            
        Raises:
            requests.RequestException: If download fails
        """
        logger.info(f"Downloading PDF from: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Create temporary file with PDF extension
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_file.write(response.content)
            temp_file.close()
            
            logger.info(f"PDF downloaded successfully to: {temp_file.name}")
            return temp_file.name
            
        except requests.RequestException as e:
            logger.error(f"Failed to download PDF: {e}")
            raise
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            Exception: If PDF extraction fails
        """
        logger.info(f"Extracting text from PDF: {pdf_path}")
        
        try:
            text_content = []
            
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                logger.info(f"Processing {total_pages} pages")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    logger.debug(f"Processing page {page_num}/{total_pages}")
                    page_text = page.extract_text()
                    
                    if page_text:
                        # Clean up the text
                        page_text = self._clean_text(page_text)
                        text_content.append(page_text)
            
            full_text = '\n\n'.join(text_content)
            logger.info(f"Extracted {len(full_text)} characters from PDF")
            return full_text
            
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page numbers and headers/footers (basic cleanup)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        # Remove excessive line breaks
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks suitable for LLM processing.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        logger.info(f"Chunking text into ~{self.chunk_size} word chunks")
        
        words = text.split()
        chunks = []
        
        current_chunk = []
        current_word_count = 0
        
        for word in words:
            current_chunk.append(word)
            current_word_count += 1
            
            if current_word_count >= self.chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_word_count = 0
        
        # Add remaining words as final chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        logger.info(f"Created {len(chunks)} text chunks")
        return chunks
    
    def analyze_chunk(self, chunk: str, chunk_number: int, total_chunks: int) -> str:
        """
        Analyze a single text chunk using OpenAI API.
        
        Args:
            chunk: Text chunk to analyze
            chunk_number: Current chunk number
            total_chunks: Total number of chunks
            
        Returns:
            Summary of the chunk
        """
        logger.info(f"Analyzing chunk {chunk_number}/{total_chunks}")
        
        # Get prompt from loaded prompts and format with dynamic values
        prompt_template = self.prompts.get('CHUNK_ANALYSIS_PROMPT', '')
        if not prompt_template:
            raise ValueError("CHUNK_ANALYSIS_PROMPT not found in prompts file")
        
        prompt = prompt_template.format(
            chunk=chunk,
            chunk_number=chunk_number,
            total_chunks=total_chunks
        )
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert at summarizing business reports."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            summary = response.choices[0].message.content
            logger.debug(f"Chunk {chunk_number} analyzed successfully")
            return summary
            
        except Exception as e:
            logger.error(f"Failed to analyze chunk {chunk_number}: {e}")
            return f"Error analyzing chunk {chunk_number}: {str(e)}"
    
    def combine_summaries(self, chunk_summaries: List[str]) -> str:
        """
        Combine individual chunk summaries into a cohesive final summary.
        
        Args:
            chunk_summaries: List of individual chunk summaries
            
        Returns:
            Final combined summary
        """
        logger.info("Combining chunk summaries into final report")
        
        combined_text = "\n\n".join(chunk_summaries)
        
        # Get prompt from loaded prompts and format with dynamic values
        prompt_template = self.prompts.get('SUMMARY_COMBINATION_PROMPT', '')
        if not prompt_template:
            raise ValueError("SUMMARY_COMBINATION_PROMPT not found in prompts file")
        
        final_prompt = prompt_template.format(combined_text=combined_text)
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior financial analyst creating executive summaries."},
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            final_summary = response.choices[0].message.content
            logger.info("Final summary generated successfully")
            return final_summary
            
        except Exception as e:
            logger.error(f"Failed to generate final summary: {e}")
            return f"Error generating final summary: {str(e)}"
    
    def analyze_single_report(self, pdf_url: str, output_dir: str, url_index: int) -> bool:
        """
        Complete analysis pipeline for a single financial report.
        
        Args:
            pdf_url: URL of the PDF report to analyze
            output_dir: Directory to save the analysis
            url_index: Index of the URL for fallback naming
            
        Returns:
            True if successful, False otherwise
        """
        pdf_path = None
        
        try:
            logger.info(f"🔄 Starting analysis for: {pdf_url}")
            
            # Download PDF
            pdf_path = self.download_pdf(pdf_url)
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF")
            
            # Chunk text
            chunks = self.chunk_text(text)
            
            if not chunks:
                raise ValueError("No text chunks created")
            
            # Analyze each chunk
            chunk_summaries = []
            for i, chunk in enumerate(chunks, 1):
                summary = self.analyze_chunk(chunk, i, len(chunks))
                chunk_summaries.append(summary)
            
            # Combine summaries into final report
            final_summary = self.combine_summaries(chunk_summaries)
            
            # Generate filename
            company_name = self._extract_company_name_from_url(pdf_url)
            if company_name:
                filename = f"{company_name}_analysis.txt"
            else:
                filename = f"report_{url_index}_analysis.txt"
            
            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Save the analysis
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Financial Report Analysis\n")
                f.write(f"Source: {pdf_url}\n")
                f.write("="*80 + "\n\n")
                f.write(final_summary)
            
            logger.info(f"✅ Analysis saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Analysis failed for {pdf_url}: {e}")
            return False
        
        finally:
            # Clean up temporary file
            if pdf_path and os.path.exists(pdf_path):
                os.unlink(pdf_path)
                logger.debug("Temporary PDF file deleted")
    
    def analyze_all_reports(self) -> Dict[str, bool]:
        """
        Analyze all reports from URLs in the urls.txt file.
        
        Returns:
            Dictionary mapping URLs to success/failure status
        """
        output_dir = os.path.join(self.app_dir, "individual_analysis")
        
        try:
            urls = self._read_urls_from_file()
        except Exception as e:
            raise Exception(f"Failed to read URLs: {str(e)}")
        
        results = {}
        
        logger.info(f"📊 Starting analysis of {len(urls)} URLs")
        logger.info(f"💾 Individual analyses will be saved to: {output_dir}/")
        
        for i, url in enumerate(urls, 1):
            logger.info(f"📈 Processing URL {i}/{len(urls)}: {url}")
            
            success = self.analyze_single_report(url, output_dir, i)
            results[url] = success
            
            if success:
                logger.info(f"✅ Successfully completed analysis {i}/{len(urls)}")
            else:
                logger.error(f"❌ Failed analysis {i}/{len(urls)}")
        
        return results


def load_api_key() -> str:
    """
    Load OpenAI API key from .env file.
    
    Returns:
        OpenAI API key
        
    Raises:
        Exception: If API key is not found or invalid
    """
    # Get the app directory
    app_dir = get_app_directory()
    env_path = os.path.join(app_dir, '.env')
    
    # Load environment variables from .env file
    load_dotenv(env_path)
    
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key.strip() == '' or api_key == 'sk-your-openai-api-key-here':
        raise ValueError("OpenAI API key not found or invalid")
    
    return api_key.strip()


def show_error(title: str, message: str):
    """Show error message using GUI popup."""
    messagebox.showerror(title, message)


def show_success(title: str, message: str):
    """Show success message using GUI popup."""
    messagebox.showinfo(title, message)


def main():
    """
    Main function to run the financial report analyzer.
    
    This script is designed to be converted into an executable using PyInstaller.
    File paths are resolved relative to the app bundle location.
    """
    try:
        # Show debug info about where we're looking for files
        app_dir = get_app_directory()
        logger.info(f"App directory: {app_dir}")
        
        # Load API key from .env file
        try:
            api_key = load_api_key()
        except Exception as e:
            show_error(
                "Missing API Key",
                f"Please add your OpenAI API key to the .env file in:\n{app_dir}\n\nAs: OPENAI_API_KEY=sk-your-actual-key-here"
            )
            return 1
        
        # Initialize analyzer with default values
        try:
            logger.info("🚀 Initializing Financial Report Analyzer...")
            analyzer = FinancialReportAnalyzer(
                openai_api_key=api_key,
                chunk_size=2500,
                model="gpt-4o-mini"
            )
        except Exception as e:
            show_error(
                "Initialization Error",
                f"Failed to initialize analyzer:\n{str(e)}"
            )
            return 1
        
        # Analyze all reports
        try:
            logger.info("📊 Starting financial report analysis...")
            results = analyzer.analyze_all_reports()
        except Exception as e:
            show_error(
                "Analysis Error",
                f"Failed to analyze reports:\n{str(e)}"
            )
            return 1
        
        # Calculate results
        successful_analyses = sum(1 for success in results.values() if success)
        total_analyses = len(results)
        
        # Show appropriate message based on results
        if successful_analyses == total_analyses:
            show_success(
                "Analysis Complete!",
                f"All {successful_analyses} reports analyzed successfully!\n\nResults saved to:\n{app_dir}/individual_analysis/"
            )
        elif successful_analyses > 0:
            show_success(
                "Analysis Partially Complete",
                f"{successful_analyses} out of {total_analyses} reports analyzed successfully.\n\nResults saved to:\n{app_dir}/individual_analysis/\n\nCheck the log for details on failed analyses."
            )
        else:
            show_error(
                "Analysis Failed",
                f"All {total_analyses} analyses failed.\n\nPlease check your URLs and try again."
            )
        
        return 0 if successful_analyses > 0 else 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        show_error(
            "Unexpected Error",
            f"An unexpected error occurred:\n{str(e)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main()) 