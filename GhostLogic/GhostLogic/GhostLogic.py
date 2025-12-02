import argparse
import os
import sys
import json
from datetime import datetime

# Modül yollarını ekle
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    from core.requester import Harvester
    from core.analyzer import GhostAnalyzer
    from colorama import init, Fore, Style
except ImportError as e:
    print(f"Hata: Kütüphaneler eksik veya 'core' klasörü bulunamadı. {e}")
    sys.exit(1)

init(autoreset=True)

def print_banner():
    print(Fore.MAGENTA + r"""
      _____ _               _   _             _      
     / ____| |             | | | |           (_)     
    | |  __| |__   ___  ___| |_| | ___   __ _ _  ___ 
    | | |_ | '_ \ / _ \/ __| __| |/ _ \ / _` | |/ __|
    | |__| | | | | (_) \__ \ |_| | (_) | (_| | | (__ 
     \_____|_| |_|\___/|___/\__|_|\___/ \__, |_|\___|
                                         __/ |       
                                        |___/        
    """ + Style.RESET_ALL + Fore.WHITE + "    v1.0 - The Quiet Observer" + Style.RESET_ALL + "\n")

def save_report(results, domain):
    """Sonuçları JSON formatında kaydeder."""
    if not results:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{domain}_{timestamp}.json"
    
    report_data = {
        "target": domain,
        "scan_date": timestamp,
        "findings": results
    }

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        print(f"\n{Fore.GREEN}[OK] Rapor kaydedildi: {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Rapor kaydetme hatası: {e}{Style.RESET_ALL}")

def report_results(results):
    print(f"\n{Fore.MAGENTA}=== SONUÇ ÖZETİ ==={Style.RESET_ALL}")
    if not results:
        print("Kayda değer bir şey bulunamadı.")
        return

    total_findings = sum(len(v) for v in results.values())
    print(f"Toplam {total_findings} adet kritik veri bulundu.\n")

    for filename, findings in results.items():
        print(f"{Fore.CYAN}> {filename}{Style.RESET_ALL}")
        for item in findings:
            color = Fore.WHITE
            if item['type'] == 'SENSITIVE_KEYS': color = Fore.RED
            if item['type'] == 'API_ENDPOINTS': color = Fore.GREEN
            print(f"  {color}[{item['line']}] {item['data']}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="GhostLogic: Passive JS Recon Tool")
    parser.add_argument("-u", "--url", required=True, help="Hedef URL (örn: https://example.com)")
    parser.add_argument("--keep", action="store_true", help="İndirilen dosyaları silme")
    args = parser.parse_args()

    print_banner()

    # Domain ismini rapor için temizle
    domain = args.url.split("//")[-1].split("/")[0]

    # Adım 1: Hasat
    harvester = Harvester(args.url)
    js_files = harvester.run()

    if not js_files:
        print(f"{Fore.RED}[!] Hiç JS dosyası bulunamadı. Çıkılıyor.{Style.RESET_ALL}")
        return

    # Adım 2: Analiz
    analyzer = GhostAnalyzer(js_files)
    results = analyzer.run()

    # Adım 3: Raporlama
    report_results(results)
    save_report(results, domain)

if __name__ == "__main__":
    main()