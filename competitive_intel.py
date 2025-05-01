#!/usr/bin/env python3
import os
import re
import json
import time
import random
import requests
import pyfiglet
import datetime
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk

# Initialize console
console = Console()

class CompetitiveData:
    """Data structure for competitive intelligence"""
    def __init__(self):
        self.competitors = {}
        self.market_insights = []
        self.trends = []
        self.news = []
        self.metrics = {}
        self.timestamp = datetime.datetime.utcnow().isoformat()

class BannerManager:
    @staticmethod
    def display_banner():
        # Create banner using pyfiglet
        banner_text = pyfiglet.figlet_format("Competitive Intel", font="slant")
        console.print(Panel(f"[bold cyan]{banner_text}[/bold cyan]"))
        
        # Create info table
        info_table = Table.grid(padding=1)
        info_table.add_row("[bold green]User:[/bold green]", "gaytri1111")
        info_table.add_row("[bold blue]Time (UTC):[/bold blue]", "2025-05-01 02:48:00")
        info_table.add_row("[bold yellow]Mode:[/bold yellow]", "Advanced Analysis")
        
        console.print(Panel(info_table))
        
        # Tool information
        console.print(Panel(
            "[bold magenta]Competitive Intelligence Gatherer[/bold magenta]\n"
            "• Automated Data Collection\n"
            "• Market Analysis\n"
            "• Trend Detection\n"
            "• Sentiment Analysis",
            title="Tool Information",
            border_style="blue"
        ))

class CompetitiveIntelligence:
    def __init__(self):
        self.setup_environment()
        self.initialize_webdriver()
        self.data = CompetitiveData()
        self.load_nltk_resources()

    def setup_environment(self):
        """Initialize directories and configurations"""
        self.config_dir = Path.home() / '.competitive_intel'
        self.data_dir = self.config_dir / 'data'
        self.cache_dir = self.config_dir / 'cache'
        
        for directory in [self.config_dir, self.data_dir, self.cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            directory.chmod(0o700)

    def load_nltk_resources(self):
        """Download required NLTK resources"""
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')

    def initialize_webdriver(self):
        """Initialize Chrome webdriver with stealth settings"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def gather_intelligence(self, company: str, competitors: List[str]) -> CompetitiveData:
        """Main method to gather competitive intelligence"""
        try:
            with Progress() as progress:
                # Initialize progress
                task1 = progress.add_task("[cyan]Gathering market data...", total=100)
                
                # Gather company data
                self.gather_company_data(company, progress, task1)
                progress.update(task1, advance=20)
                
                # Analyze competitors
                self.analyze_competitors(competitors, progress, task1)
                progress.update(task1, advance=20)
                
                # Gather market insights
                self.gather_market_insights(company, competitors, progress, task1)
                progress.update(task1, advance=20)
                
                # Analyze trends
                self.analyze_trends(company, progress, task1)
                progress.update(task1, advance=20)
                
                # Gather news and updates
                self.gather_news(company, competitors, progress, task1)
                progress.update(task1, advance=20)
                
            return self.data
            
        except Exception as e:
            console.print(f"[bold red]Error gathering intelligence: {str(e)}[/bold red]")
            return None

    def gather_company_data(self, company: str, progress: Progress, task: int):
        """Gather detailed data about the main company"""
        search_query = f"{company} company information financials products"
        
        try:
            self.driver.get(f"https://www.google.com/search?q={search_query}")
            time.sleep(random.uniform(2, 4))
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract relevant information
            self.data.competitors[company] = {
                'name': company,
                'description': self._extract_description(soup),
                'products': self._extract_products(soup),
                'metrics': self._extract_metrics(soup),
                'recent_news': self._extract_news(soup)
            }
            
            progress.update(task, advance=10)
            
        except Exception as e:
            console.print(f"[yellow]Warning: Error gathering company data: {str(e)}[/yellow]")

    def analyze_competitors(self, competitors: List[str], progress: Progress, task: int):
        """Analyze competitor information"""
        for competitor in competitors:
            try:
                search_query = f"{competitor} company information products market share"
                self.driver.get(f"https://www.google.com/search?q={search_query}")
                time.sleep(random.uniform(2, 4))
                
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                self.data.competitors[competitor] = {
                    'name': competitor,
                    'description': self._extract_description(soup),
                    'products': self._extract_products(soup),
                    'metrics': self._extract_metrics(soup),
                    'recent_news': self._extract_news(soup)
                }
                
                progress.update(task, advance=5)
                
            except Exception as e:
                console.print(f"[yellow]Warning: Error analyzing competitor {competitor}: {str(e)}[/yellow]")

    def gather_market_insights(self, company: str, competitors: List[str], progress: Progress, task: int):
        """Gather market insights and trends"""
        all_companies = [company] + competitors
        market_query = f"market analysis {' '.join(all_companies)}"
        
        try:
            self.driver.get(f"https://www.google.com/search?q={market_query}")
            time.sleep(random.uniform(2, 4))
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract market insights
            self.data.market_insights = self._extract_market_insights(soup)
            
            progress.update(task, advance=10)
            
        except Exception as e:
            console.print(f"[yellow]Warning: Error gathering market insights: {str(e)}[/yellow]")

    def analyze_trends(self, company: str, progress: Progress, task: int):
        """Analyze market trends"""
        trend_query = f"{company} industry trends market development"
        
        try:
            self.driver.get(f"https://www.google.com/search?q={trend_query}")
            time.sleep(random.uniform(2, 4))
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract trends
            self.data.trends = self._extract_trends(soup)
            
            progress.update(task, advance=10)
            
        except Exception as e:
            console.print(f"[yellow]Warning: Error analyzing trends: {str(e)}[/yellow]")

    def gather_news(self, company: str, competitors: List[str], progress: Progress, task: int):
        """Gather recent news about the company and competitors"""
        all_companies = [company] + competitors
        news_query = f"news {' OR '.join(all_companies)}"
        
        try:
            self.driver.get(f"https://www.google.com/search?q={news_query}&tbm=nws")
            time.sleep(random.uniform(2, 4))
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract news
            self.data.news = self._extract_news_articles(soup)
            
            progress.update(task, advance=10)
            
        except Exception as e:
            console.print(f"[yellow]Warning: Error gathering news: {str(e)}[/yellow]")

    def _extract_description(self, soup) -> str:
        """Extract company description from search results"""
        try:
            description = soup.find('div', class_='VwiC3b')
            return description.text.strip() if description else ""
        except Exception:
            return ""

    def _extract_products(self, soup) -> List[str]:
        """Extract product information"""
        products = []
        try:
            product_elements = soup.find_all('div', class_='BNeawe')
            for element in product_elements:
                text = element.text.strip()
                if 'product' in text.lower() or 'service' in text.lower():
                    products.append(text)
        except Exception:
            pass
        return products

    def _extract_metrics(self, soup) -> Dict[str, Any]:
        """Extract company metrics"""
        metrics = {}
        try:
            # Look for common metric patterns
            metric_patterns = {
                'revenue': r'\$[\d.,]+ [bm]illion',
                'employees': r'[\d,]+ employees',
                'market_share': r'[\d.]+% market share'
            }
            
            text = soup.get_text()
            for metric, pattern in metric_patterns.items():
                matches = re.findall(pattern, text)
                if matches:
                    metrics[metric] = matches[0]
        except Exception:
            pass
        return metrics

    def _extract_news(self, soup) -> List[Dict[str, str]]:
        """Extract recent news"""
        news_items = []
        try:
            news_elements = soup.find_all('div', class_='g')
            for element in news_elements[:5]:  # Get top 5 news items
                title = element.find('h3')
                link = element.find('a')
                if title and link:
                    news_items.append({
                        'title': title.text.strip(),
                        'url': link['href']
                    })
        except Exception:
            pass
        return news_items

    def _extract_market_insights(self, soup) -> List[str]:
        """Extract market insights"""
        insights = []
        try:
            # Look for market-related information
            text_elements = soup.find_all('div', class_='BNeawe')
            for element in text_elements:
                text = element.text.strip()
                if any(keyword in text.lower() for keyword in ['market', 'industry', 'sector']):
                    insights.append(text)
        except Exception:
            pass
        return insights

    def _extract_trends(self, soup) -> List[str]:
        """Extract market trends"""
        trends = []
        try:
            trend_elements = soup.find_all('div', class_='BNeawe')
            for element in trend_elements:
                text = element.text.strip()
                if any(keyword in text.lower() for keyword in ['trend', 'growth', 'development']):
                    trends.append(text)
        except Exception:
            pass
        return trends

    def _extract_news_articles(self, soup) -> List[Dict[str, str]]:
        """Extract detailed news articles"""
        articles = []
        try:
            news_elements = soup.find_all('div', class_='g')
            for element in news_elements:
                title = element.find('h3')
                link = element.find('a')
                snippet = element.find('div', class_='VwiC3b')
                if title and link:
                    articles.append({
                        'title': title.text.strip(),
                        'url': link['href'],
                        'snippet': snippet.text.strip() if snippet else "",
                        'date': self._extract_date(element)
                    })
        except Exception:
            pass
        return articles

    def _extract_date(self, element) -> str:
        """Extract publication date from news element"""
        try:
            date_element = element.find('span', class_='r0bn4c')
            return date_element.text.strip() if date_element else ""
        except Exception:
            return ""

    def generate_report(self, data: CompetitiveData) -> str:
        """Generate a comprehensive report"""
        report = []
        
        # Add header
        report.append("# Competitive Intelligence Report")
        report.append(f"Generated on: {data.timestamp}\n")
        
        # Add competitor analysis
        report.append("## Competitor Analysis")
        for company, info in data.competitors.items():
            report.append(f"### {company}")
            report.append(f"Description: {info['description']}")
            report.append("\nProducts/Services:")
            for product in info['products']:
                report.append(f"- {product}")
            report.append("\nKey Metrics:")
            for metric, value in info['metrics'].items():
                report.append(f"- {metric}: {value}")
            report.append("")
        
        # Add market insights
        report.append("## Market Insights")
        for insight in data.market_insights:
            report.append(f"- {insight}")
        
        # Add trends
        report.append("\n## Market Trends")
        for trend in data.trends:
            report.append(f"- {trend}")
        
        # Add news
        report.append("\n## Recent News")
        for article in data.news:
            report.append(f"### {article['title']}")
            report.append(f"Date: {article['date']}")
            report.append(f"Summary: {article['snippet']}")
            report.append(f"Source: {article['url']}\n")
        
        return "\n".join(report)

    def save_report(self, report: str, format: str = 'md') -> str:
        """Save the report in specified format"""
        timestamp = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        output_file = self.data_dir / f"competitive_intel_{timestamp}.{format}"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            return str(output_file)
        except Exception as e:
            console.print(f"[bold red]Error saving report: {str(e)}[/bold red]")
            return ""

    def cleanup(self):
        """Clean up resources"""
        try:
            self.driver.quit()
        except Exception:
            pass

def main():
    try:
        # Display banner
        BannerManager.display_banner()
        
        # Initialize intelligence gatherer
        intel = CompetitiveIntelligence()
        
        # Get target company
        company = Prompt.ask("\n[bold cyan]Enter target company name")
        
        # Get competitors
        competitors = []
        while True:
            competitor = Prompt.ask("[bold cyan]Enter competitor name (or 'done' to finish)")
            if competitor.lower() == 'done':
                break
            competitors.append(competitor)
        
        # Gather intelligence
        console.print("\n[bold cyan]Gathering competitive intelligence...[/bold cyan]")
        data = intel.gather_intelligence(company, competitors)
        
        if data:
            # Generate report
            report = intel.generate_report(data)
            
            # Save report
            if Confirm.ask("\nSave report?"):
                output_file = intel.save_report(report)
                if output_file:
                    console.print(f"[green]Report saved to: {output_file}[/green]")
            
            # Display summary
            console.print(Markdown(report))
        
        # Cleanup
        intel.cleanup()
        console.print("\n[bold green]Intelligence gathering completed![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        raise

if __name__ == "__main__":
    main()
