import requests
import re
import os
import shutil
import sys
import time
from urllib.parse import quote

def main():
    print("🚀 PyGoals M3U8 Kanal İndirici Başlatılıyor...")
    print("⏰ Lütfen işlemin tamamlanmasını bekleyin...")
    
    # Trgoals domain kontrol
    base = "https://trgoals"
    domain = ""
    
    print("\n🔍 Domain aranıyor: trgoals1393.xyz → trgoals2100.xyz")
    for i in range(1393, 2101):
        test_domain = f"{base}{i}.xyz"
        try:
            response = requests.head(test_domain, timeout=3)
            if response.status_code == 200:
                domain = test_domain
                print(f"✅ Domain bulundu: {domain}")
                break
            else:
                print(f"⏳ Denenen domain: {test_domain} (Status: {response.status_code})")
        except Exception as e:
            print(f"⏳ Denenen domain: {test_domain} (Hata: {str(e)[:30]}...)")
            continue
    
    if not domain:
        print("❌ UYARI: Hiçbir domain çalışmıyor - boş klasör oluşturulacak")
    
    # Kanallar - benzersiz isimler kullanıyoruz
    channel_ids = {
        "yayinzirve": "beIN Sports 1 Zirve",
        "yayininat": "beIN Sports 1 Yildiz",
        "yayin1": "beIN Sports 1 Sonsuz",
        "yayinb2": "beIN Sports 2",
        "yayinb3": "beIN Sports 3",
        "yayinb4": "beIN Sports 4",
        "yayinb5": "beIN Sports 5",
        "yayinbm1": "beIN Sports 1 Max",
        "yayinbm2": "beIN Sports 2 Max",
        "yayinss": "Saran Sports 1",
        "yayinss2": "Saran Sports 2",
        "yayint1": "Tivibu Sports 1",
        "yayint2": "Tivibu Sports 2",
        "yayint3": "Tivibu Sports 3",
        "yayint4": "Tivibu Sports 4",
        "yayinsmarts": "Smart Sports",
        "yayinsms2": "Smart Sports 2",
        "yayintrtspor": "TRT Spor",
        "yayintrtspor2": "TRT Spor 2",
        "yayinas": "A Spor",
        "yayinatv": "ATV",
        "yayintv8": "TV8",
        "yayintv85": "TV8.5",
        "yayinnbatv": "NBA TV",
        "yayinex1": "Tabii 1",
        "yayinex2": "Tabii 2",
        "yayinex3": "Tabii 3",
        "yayinex4": "Tabii 4",
        "yayinex5": "Tabii 5",
        "yayinex6": "Tabii 6",
        "yayinex7": "Tabii 7",
        "yayinex8": "Tabii 8",
        "yayintrt1": "TRT1",
    }
    
    # Klasör işlemleri
    folder_name = "channels_files"
    
    print(f"\n📁 Klasör işlemleri: {folder_name}")
    
    # Klasörü temizleme
    if os.path.exists(folder_name):
        try:
            shutil.rmtree(folder_name)
            print(f"🗑️  Eski klasör silindi: {folder_name}")
        except Exception as e:
            print(f"⚠️  Klasör silinemedi: {e}")
    
    # Klasörü oluşturma
    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"✅ Klasör oluşturuldu: {folder_name}")
    except Exception as e:
        print(f"❌ KRİTİK HATA: Klasör oluşturulamadı: {e}")
        sys.exit(1)
    
    # Domain yoksa işlemi sonlandır
    if not domain:
        print("\nℹ️  Domain bulunamadığı için dosya oluşturulmayacak.")
        print("📂 Sadece boş klasör oluşturuldu.")
        return
    
    # Kanalları işleme
    print(f"\n📺 {len(channel_ids)} kanal işleniyor...")
    created = 0
    failed = 0
    
    for i, (channel_id, channel_name) in enumerate(channel_ids.items(), 1):
        try:
            print(f"\n[{i}/{len(channel_ids)}] {channel_name} işleniyor...")
            
            url = f"{domain}/channel.html?id={channel_id}"
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            
            if response.status_code != 200:
                print(f"❌ HTTP Hatası: {response.status_code}")
                failed += 1
                continue
            
            match = re.search(r'const baseurl = "(.*?)"', response.text)
            if not match:
                print("❌ BaseURL bulunamadı")
                failed += 1
                continue
            
            baseurl = match.group(1)
            encoded_url = quote(f"{baseurl}{channel_id}.m3u8", safe='')
            full_url = f"http://proxylendim101010.mywire.org/proxy.php?url={encoded_url}"
            
            content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=5500000,AVERAGE-BANDWIDTH=8976000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2",FRAME-RATE=25
{full_url}
"""
            # Güvenli ve benzersiz dosya adı oluşturma
            safe_name = re.sub(r'[^\w\s.-]', '_', channel_name)
            safe_name = safe_name.replace(' ', '_')
            
            # Benzersizlik sağlamak için channel_id ekleyelim
            file_name = f"{safe_name}_{channel_id}.m3u8"
            path = os.path.join(folder_name, file_name)
            
            # Aynı isimde dosya var mı kontrol et
            counter = 1
            original_path = path
            while os.path.exists(path):
                file_name = f"{safe_name}_{channel_id}_{counter}.m3u8"
                path = os.path.join(folder_name, file_name)
                counter += 1
            
            # Dosyayı yazma
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ {channel_name} → {file_name}")
            created += 1
            
            # Kısa bir bekleme süresi ekleyerek sunucu yükünü azalt
            time.sleep(0.1)
            
        except requests.exceptions.Timeout:
            print("❌ İstek zaman aşımına uğradı")
            failed += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ Ağ hatası: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            failed += 1
    
    # Sonuç raporu
    print("\n" + "="*50)
    print("📊 İŞLEM SONUÇLARI")
    print("="*50)
    print(f"✅ Başarılı: {created}")
    print(f"❌ Başarısız: {failed}")
    print(f"📂 Klasör: {os.path.abspath(folder_name)}")
    
    if created > 0:
        print("\n🎉 İşlem başarıyla tamamlandı!")
    else:
        print("\nℹ️  Hiç dosya oluşturulamadı, lütfen internet bağlantınızı kontrol edin.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ KRİTİK HATA: {e}")
        sys.exit(1)
