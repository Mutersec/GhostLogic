import re
import os
import jsbeautifier
from colorama import Fore, Style

class GhostAnalyzer:
    def __init__(self, js_files):
        self.js_files = js_files
        self.results = {}
        self.patterns = {
            "API_ENDPOINTS": r"""(?:"|')(((?:/api/|/v[0-9]+/|/graphql|/admin/|/auth/)[a-zA-Z0-9_\-/\.]+))(?:"|')""",
            "SENSITIVE_KEYS": r"""(?i)((access_key|access_token|admin_pass|api_key|apikey|auth_token|authorization|client_secret|secret|password|user_pass)['"]?\s*[:=]\s*['"]?([a-zA-Z0-9\-_]{10,}))""",
        }

    def beautify_js(self, content):
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        return jsbeautifier.beautify(content, opts)

    def analyze_file(self, file_path):
        filename = os.path.basename(file_path)
        print(f"{Fore.YELLOW}[*] Analiz ediliyor: {filename}...{Style.RESET_ALL}")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            beautified_content = self.beautify_js(content)
            file_findings = []
            for key, pattern in self.patterns.items():
                matches = re.finditer(pattern, beautified_content)
                for match in matches:
                    found_data = match.group(1) if match.lastindex else match.group(0)
                    line_num = beautified_content[:match.start()].count('\n') + 1
                    finding = {"type": key, "data": found_data, "line": line_num}
                    file_findings.append(finding)
            if file_findings:
                self.results[filename] = file_findings
                print(f"{Fore.GREEN}[+] {len(file_findings)} bulgu.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-] Temiz.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Hata: {e}{Style.RESET_ALL}")

    def run(self):
        print(f"\n{Fore.CYAN}--- DİJİTAL OTOPSİ BAŞLIYOR ---{Style.RESET_ALL}")
        for js_file in self.js_files:
            self.analyze_file(js_file)
        return self.results