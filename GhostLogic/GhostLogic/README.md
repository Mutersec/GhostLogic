# GhostLogic

⚠️ Yasal Uyarı
Bu araç sadece eğitim ve yasal güvenlik testleri (Pentest/Bug Bounty) içindir. İzinsiz kullanımdan doğacak sorumluluk kullanıcıya aittir. Hiçbir şekilde sorumluluk almıyorum 

> "Kontrol bir illüzyondur."

## Nedir?
GhostLogic, hedef sisteme tek bir "malicious" (zararlı) paket göndermeden, sadece halka açık istemci dosyalarını analiz ederek backend mimarisini ve potansiyel mantık hatalarını (Logic Flaws) ortaya çıkaran bir Keşif (Recon) aracıdır.

## Özellikler
- **Sessiz Mod:** WAF/IPS tetiklemez. Tamamen pasif analiz.
- **Webpack Deobfuscator:** Sıkıştırılmış JS dosyalarından okunabilir endpoint haritası çıkarır.
- **Role-Based Prediction:** İstemci kodunda "Admin" veya "SuperUser" rotalarını tespit eder.
- **Parametre Analizi:** Hangi endpoint'in hangi parametreleri beklediğini (id, uuid, token) koddan okur.

## Kurulum
```bash
git clone 
cd ghostlogic
pip install -r requirements.txt
python ghostlogic.py --url [https://hedef-sirket.com](https://hedef-sirket.com) --deep-scan

PROJE YAPISI 

GhostLogic/
├── ghostlogic.py       # Ana giriş noktası 
├── core/
│   ├── __init__.py     # Python paketi olması için
│   ├── requester.py    # JS dosyalarını çeken hasatçı
│   └── analyzer.py     # Analiz motoru
└── output/             # İndirilen dosyalar buraya gelecek


## 📸 Demo Output

![GhostLogic Taraması](img/demo.png)