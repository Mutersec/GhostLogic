import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import sys
from colorama import Fore, Style

class Harvester:
    def __init__(self, target_url, output_dir="output"):
        self.target_url = target_url
        self.output_dir = output_dir
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def fetch_html(self):
        try:
            print(f"{Fore.CYAN}[*] Bağlantı kuruluyor: {self.target_url}{Style.RESET_ALL}")
            response = self.session.get(self.target_url, headers=self.headers, timeout=15, verify=True)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[!] Hata: Hedefe ulaşılamadı. {e}{Style.RESET_ALL}")
            sys.exit(1)

    def get_js_links(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        scripts = soup.find_all('script')
        js_links = set()
        print(f"{Fore.BLUE}[*] HTML taranıyor...{Style.RESET_ALL}")
        for script in scripts:
            src = script.get('src')
            if src:
                full_url = urljoin(self.target_url, src)
                if ".js" in full_url:
                    js_links.add(full_url)
        return list(js_links)

    def download_file(self, url):
        try:
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename or not filename.endswith('.js'):
                filename = f"script_{hash(url)}.js"
            local_path = os.path.join(self.output_dir, filename)
            print(f"{Fore.GREEN}[+] İndiriliyor: {filename}{Style.RESET_ALL}")
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                with open(local_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(response.text)
                return local_path
        except Exception as e:
            print(f"{Fore.YELLOW}[!] İndirme hatası ({url}): {e}{Style.RESET_ALL}")
        return None

    def run(self):
        html = self.fetch_html()
        links = self.get_js_links(html)
        print(f"{Fore.CYAN}[*] Toplam {len(links)} adet JS dosyası bulundu.{Style.RESET_ALL}")
        downloaded_files = []
        for link in links:
            path = self.download_file(link)
            if path:
                downloaded_files.append(path)
        return downloaded_files