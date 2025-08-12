# 🖼️ Sentiric Assets

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

**Sentiric Assets**, tüm Sentiric platformu genelinde kullanılan statik varlıkları ve kaynakları (örn: anonslar için ses dosyaları, UI bileşenleri için ikonlar, genel yapılandırma şablonları) depolayan merkezi bir repodur.

## 🎯 Temel Sorumluluklar

*   Paylaşılan statik içerik için merkezi bir konum sağlamak.
*   Medya ve UI kaynaklarının sürüm kontrolünü ve yönetimini kolaylaştırmak.
*   GitHub Pages aracılığıyla, platformun dinamik olarak internet üzerinden erişebileceği bir **içerik dağıtım ağı (CDN)** görevi görmek.

## 📂 Dizin Yapısı

*   `/audio/`: `sentiric-media-service` tarafından kullanılan anons ve müzik dosyalarını (.wav, .mp3) içerir.
*   `/knowledge_base/`: `sentiric-knowledge-service`'in vektör indekslerini oluşturmak için kullandığı ham veri dosyalarını (.md, .txt, .csv) içerir.
*   (Gelecekte `/images/`, `/ui/`, `/templates/` gibi klasörler eklenecektir.)

## 🚀 Kullanım

Bu, çalışan bir servis **değildir**; bir **depolama reposu** ve **CDN kaynağıdır**. Diğer servisler (örn: `media-service`, `tts-service`) buradaki kaynaklara GitHub Pages üzerinden oluşturulan genel URL'ler aracılığıyla erişir.

**Canlı URL:** [https://sentiric.github.io/sentiric-assets/](https://sentiric.github.io/sentiric-assets/)

**Örnek:** `tts-service`'in bir sesi klonlamak için ihtiyaç duyduğu referans ses dosyasının URL'i:
`https://sentiric.github.io/sentiric-assets/audio/speakers/tr/default_male.wav`

## 🤝 Katkıda Bulunma

Yeni bir anons veya bilgi bankası dokümanı eklemek için:
1. Dosyanızı ilgili klasöre ekleyin.
2. Değişikliklerinizi `main` branch'ine commit'leyip push'layın.
3. GitHub Actions, değişikliği otomatik olarak canlı GitHub Pages sitesine yayınlayacaktır.

---
---
## 🏛️ Anayasal Konum

Bu servis, [Sentiric Anayasası'nın (v11.0)](https://github.com/sentiric/sentiric-governance/blob/main/docs/blueprint/Architecture-Overview.md) **Zeka & Orkestrasyon Katmanı**'nda yer alan merkezi bir bileşendir.