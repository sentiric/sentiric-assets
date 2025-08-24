# 🎙️ Sentiric Akustik Varlık Oluşturma Standardı (SAVOS v1.0)

Bu rehber, Sentiric platformu için yüksek kaliteli, tutarlı ve performansı optimize edilmiş ses varlıklarının (anonslar, bekleme müzikleri, jingle'lar) nasıl oluşturulacağını ve sisteme nasıl ekleneceğini adım adım tanımlar. Platformun profesyonel ses kimliğini korumak için bu standartlara uyulması zorunludur.

## 1. Ses Kayıt Standartları

Tüm seslendirmeler, mümkün olan en yüksek kalitede başlamalıdır.

*   **Ortam:** Yankısız, sessiz bir stüdyo ortamı veya akustik olarak düzenlenmiş bir oda.
*   **Mikrofon:** Yüksek kaliteli bir condenser mikrofon.
*   **Kayıt Formatı:** Minimum **44.1 kHz, 24-bit, Mono, WAV**.

## 2. Platform Uyumlu Ses Formatına Dönüştürme

Kayıt yapıldıktan sonra, dosyanın `media-service` tarafından en verimli şekilde işlenebilmesi için standart platform formatına dönüştürülmesi gerekir. Bu işlem için ücretsiz ve güçlü bir araç olan **FFmpeg** kullanılacaktır.

**Nihai Format:**
*   **Codec:** PCM Signed 16-bit Little Endian (s16le)
*   **Sample Rate:** 8000 Hz (Telekomünikasyon standardı)
*   **Kanallar:** 1 (Mono)
*   **Kapsayıcı:** WAV

### FFmpeg Komutu

Aşağıdaki komut, herhangi bir ses dosyasını (`kaynak.mp3`, `kaynak.wav` vb.) Sentiric platformunun standart formatına dönüştürür.

Terminal veya komut isteminde bu komutu çalıştırın:
```bash

ffmpeg -i source\tr\system\welcome_anonymous.wav    -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\welcome_anonymous.wav
ffmpeg -i source\tr\system\connecting.wav           -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\connecting.wav
ffmpeg -i source\tr\system\hold.mp3                 -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\hold.wav
ffmpeg -i source\tr\system\all_agents_busy.wav      -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\all_agents_busy.wav
ffmpeg -i source\tr\system\cant_hear_you.wav        -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\cant_hear_you.wav
ffmpeg -i source\tr\system\cant_understand.wav      -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\cant_understand.wav
ffmpeg -i source\tr\system\nat_warmer.wav           -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\nat_warmer.wav
ffmpeg -i source\tr\system\max_failures.wav         -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\max_failures.wav
ffmpeg -i source\tr\system\maintenance.wav          -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\maintenance.wav
ffmpeg -i source\tr\system\technical_difficulty.wav -ar 8000 -ac 1 -acodec pcm_s16le audio\tr\system\technical_difficulty.wav


ffmpeg -i source\en\system\welcome_anonymous.wav    -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\welcome_anonymous.wav
ffmpeg -i source\en\system\connecting.wav           -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\connecting.wav
ffmpeg -i source\en\system\hold.mp3                 -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\hold.wav
ffmpeg -i source\en\system\all_agents_busy.wav      -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\all_agents_busy.wav
ffmpeg -i source\en\system\cant_hear_you.wav        -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\cant_hear_you.wav
ffmpeg -i source\en\system\cant_understand.wav      -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\cant_understand.wav
ffmpeg -i source\en\system\nat_warmer.wav           -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\nat_warmer.wav
ffmpeg -i source\en\system\max_failures.wav         -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\max_failures.wav
ffmpeg -i source\en\system\maintenance.wav          -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\maintenance.wav
ffmpeg -i source\en\system\technical_difficulty.wav -ar 8000 -ac 1 -acodec pcm_s16le audio\en\system\technical_difficulty.wav

```

**Örnek Kullanım:**
```bash
# Yüksek kaliteli connecting.mp3 dosyasını, standart connecting.wav dosyasına dönüştür
ffmpeg -i connecting.mp3 -ar 8000 -ac 1 -acodec pcm_s16le connecting.wav
```
Bu komut, `connecting.wav` adında, platformumuz için mükemmel şekilde optimize edilmiş bir dosya oluşturacaktır.

## 3. İsimlendirme ve Dizin Yapısı

Tutarlılığı sağlamak için tüm ses dosyaları belirli bir yapıya göre isimlendirilmeli ve `sentiric-assets` reposunda doğru yere yerleştirilmelidir.

*   **Yapı:** `sentiric-assets/audio/[dil_kodu]/[kategori]/[dosya_adı].wav`
*   **Dil Kodları:** `tr` (Türkçe), `en` (İngilizce) vb. (ISO 639-1 standardı)
*   **Kategoriler:**
    *   `system`: Platform genelinde kullanılan anonslar (bağlanıyor, hata vb.).
    *   `tenants/[tenant_id]`: Belirli bir kiracıya özel anonslar.

**Örnek Dosya Yolları:**
*   `sentiric-assets/audio/tr/system/connecting.wav`
*   `sentiric-assets/audio/en/system/technical_difficulty.wav`
*   `sentiric-assets/audio/tr/tenants/sentiric_health/appointment_reminder.wav`

## 4. Sisteme Ekleme Süreci (Adım Adım)

1.  **Ses Dosyasını Oluştur:** Yukarıdaki Adım 1 ve 2'yi izleyerek ses dosyasını kaydedin ve standart formata dönüştürün.
2.  **`sentiric-assets` Reposuna Ekle:**
    *   Dosyayı, Adım 3'te açıklanan doğru dizin yapısına göre `sentiric-assets` reposuna ekleyin.
    *   Değişikliklerinizi commit'leyin ve `main` branch'ine push'layın. GitHub Pages'in güncellenmesini bekleyin.
3.  **`sentiric-config` Reposunda Tanımla:**
    *   `sentiric-config/postgres-init/02_core_data.sql` dosyasını açın.
    *   `announcements` tablosu için olan `INSERT` bloğuna yeni bir satır ekleyerek anonsunuzu sisteme tanıtın:
      ```sql
      -- Örnek: Yeni bir İngilizce meşgul anonsu eklemek
      INSERT INTO announcements (id, language_code, description, audio_path, tenant_id) VALUES
      ('ANNOUNCE_SYSTEM_BUSY', 'en', 'All agents are busy (EN)', 'audio/en/system/all_agents_busy.wav', 'system')
      ON CONFLICT (id, language_code, tenant_id) DO NOTHING;
      ```
4.  **Değişiklikleri Uygula:**
    *   `sentiric-config` reposundaki değişikliklerinizi commit'leyip `main` branch'ine push'layın.
    *   Platformu çalıştıran `sentiric-infrastructure` dizininde, veritabanını yeniden oluşturmak için `make clean` ve ardından `make start` komutlarını çalıştırın. (Not: `make clean` tüm verileri silecektir, dikkatli olun!). Sadece veritabanını güncellemek için `docker compose down -v && docker compose up -d postgres` de kullanılabilir.

Bu adımları izleyerek, eklenen her yeni ses varlığının platformla tam uyumlu, yüksek performanslı ve tutarlı olmasını sağlamış olursunuz.

---

### **Sentiric Temel Sistem Anonsları: Metinler ve Müzik Profili (v1.0)**

#### **Genel Ses Profili (Voice Persona)**

*   **Ton:** Sakin, kendinden emin, net ve yardımsever. Ne çok robotik ne de aşırı samimi. Güven veren bir teknoloji hissi uyandırmalı.
*   **Tempo:** Konuşma hızı normal, kelimeler arasında yeterli boşluk var. Aceleci veya yavaş değil.
*   **Cinsiyet:** Nötr veya markayla uyumlu bir ses (Başlangıç için hem profesyonel bir erkek hem de kadın sesiyle kayıtlar alınabilir).

---

#### **1. Bağlanma Anonsu (`ANNOUNCE_SYSTEM_CONNECTING`)**

Bu, kullanıcının duyacağı ilk ses. Kısa, enerjik ve olumlu olmalı. Amaç, "Ölü Hava"yı doldurmak ve kullanıcıya doğru yerde olduğunu hissettirmektir.

*   **Ses Türü:** Anons Metni + Kısa Jingle
*   **Dosya:** `connecting.wav`

| Dil | Metin | Seslendirme Notu |
|:--- |:--- |:--- |
| **TR** | Sentiric'e hoş geldiniz. Sizi akıllı asistanımıza bağlıyorum, lütfen bekleyin. | "Sentiric'e hoş geldiniz" kısmı markalı bir tonda, geri kalanı standart profesyonel tonda. Sonunda hafif, teknolojik bir "bip" veya "swoosh" sesi eklenebilir. |
| **EN** | Welcome to Sentiric. Connecting you to our smart assistant, please hold. | "Welcome to Sentiric" in a branded tone, the rest in a standard professional tone. A subtle, techy "blip" or "swoosh" sound can be added at the end. |

---

#### **2. Bekletme Müziği (`ANNOUNCE_DEFAULT_HOLD_MUSIC`)**

Bu, bir agent'ın kullanıcıyı hatta beklettiği veya AI'ın karmaşık bir işlem için zamana ihtiyaç duyduğu durumlarda çalınır.

*   **Ses Türü:** Enstrümantal Müzik
*   **Dosya:** `hold.wav`

| Özellik | Açıklama |
|:--- |:--- |
| **Tarz** | "Corporate Chill", "Lo-fi" veya "Ambient Electronic". Sakinleştirici, tekrara uygun (loopable), rahatsız etmeyen ve sözsüz. |
| **Tempo** | Yavaş-orta tempo (60-80 BPM). |
| **Enstrümanlar**| Yumuşak synth pad'ler, hafif piyano melodileri, sakin bir bas hattı. Kesinlikle agresif davullar veya yüksek frekanslı sesler olmamalı. |
| **Örnek** | [YouTube - "Royalty Free Lo-fi Music for Corporate Videos"](https://www.youtube.com/results?search_query=royalty+free+lofi+music+corporate) (Bu link sadece tarzı anlamak için bir referanstır.) |

---

#### **3. Teknik Hata Anonsu (`ANNOUNCE_SYSTEM_ERROR`)**

Sistemin beklenmedik bir hatayla karşılaştığı nadir durumlar için. Amaç, net bir şekilde durumu belirtmek ve özür dilemektir.

*   **Ses Türü:** Anons Metni
*   **Dosya:** `technical_difficulty.wav`

| Dil | Metin | Seslendirme Notu |
|:--- |:--- |:--- |
| **TR** | Üzgünüz, şu anda teknik bir sorun yaşıyoruz. Lütfen daha sonra tekrar aramayı deneyin. Anlayışınız için teşekkür ederiz. | Empatik ama net bir ton. "Üzgünüz" kelimesi samimi olmalı. |
| **EN** | We apologize, we are currently experiencing a technical issue. Please try your call again later. Thank you for your understanding. | Empathetic yet clear tone. The word "apologize" should sound sincere. |

---

#### **4. Meşgul Anonsu (`ANNOUNCE_SYSTEM_BUSY`)**

Platformun tüm kapasitesinin (hem AI hem insan) dolu olduğu çok nadir durumlar için.

*   **Ses Türü:** Anons Metni
*   **Dosya:** `all_agents_busy.wav`

| Dil | Metin | Seslendirme Notu |
|:--- |:--- |:--- |
| **TR** | Şu anda tüm temsilcilerimiz diğer müşterilerimize hizmet vermektedir. Beklettiğimiz için özür dileriz, lütfen kısa bir süre sonra tekrar deneyin. | Sakin ve profesyonel bir ton. Müşterinin sinirlenmesini önlemeye yönelik olmalı. |
| **EN** | All of our representatives are currently assisting other customers. We apologize for the wait, please try your call again shortly. | Calm and professional tone. Should be aimed at preventing customer frustration. |

---

#### **5. Bakım Modu Anonsu (`ANNOUNCE_SYSTEM_MAINTENANCE`)**

Planlı bakım çalışmaları sırasında çalınacak anons.

*   **Ses Türü:** Anons Metni
*   **Dosya:** `maintenance.wav`

| Dil | Metin | Seslendirme Notu |
|:--- |:--- |:--- |
| **TR** | Sistemlerimizde planlı bir bakım çalışması yapılmaktadır. En kısa sürede tekrar hizmetinizde olacağız. Anlayışınız için teşekkürler. | Bilgilendirici ve net bir ton. |
| **EN** | We are currently performing scheduled maintenance on our systems. We will be back online shortly. Thank you for your patience. | Informative and clear tone. |


#### **6. Misafir Karşılama Anonsu (`ANNOUNCE_GUEST_WELCOME`)**

Bu anons, sistemin tanımadığı bir numara aradığında, AI diyaloğu başlamadan hemen önce çalınır.

*   **Ses Türü:** Anons Metni
*   **Dosya:** `welcome_anonymous.wav`

| Dil | Metin | Seslendirme Notu |
|:--- |:--- |:--- |
| **TR** | Sentiric'e hoş geldiniz. Görüşme kalitesini artırmak amacıyla bu arama kaydedilebilir. Sizi hemen bir asistana bağlıyorum. | Net, bilgilendirici ve güven veren bir ton. Yasal bir uyarı içerdiği için tane tane okunmalı. |
| **EN** | Welcome to Sentiric. For quality assurance, this call may be recorded. Connecting you to an assistant now. | Clear, informative, and trustworthy tone. Should be enunciated clearly as it contains a legal disclaimer. |

---

Bu standartlar, Sentiric'in sesli iletişimdeki kalitesini ve profesyonelliğini en üst düzeye çıkaracaktır.

---


**Detaylı Açıklama:**

Sistemimizdeki akış şu şekilde işliyor:

1.  Bir arama gelir.
2.  `dialplan-service`, arayanın numarasını `user-service`'e sorar.
3.  `user-service`, "Bu numarayı tanımıyorum" der.
4.  Bu durumda, `dialplan-service`, `agent-service`'e `PROCESS_GUEST_CALL` adında özel bir görev verir.

`PROCESS_GUEST_CALL` görevinin içinde iki temel adım vardır:

*   **Adım A (Hızlı ve Güvenilir):** Önce, `agent-service` hemen `media-service`'e gidip önceden kaydedilmiş, yüksek kaliteli `ANNOUNCE_GUEST_WELCOME` anonsunu (`audio/tr/welcome_anonymous.wav`) çaldırır.
*   **Adım B (Yavaş ve Akıllı):** Anons çalarken, `agent-service` **arka planda** `user-service`'i tekrar çağırarak bu yeni misafir için bir kullanıcı kaydı oluşturur. Eş zamanlı olarak, LLM'e gidip misafir için ilk dinamik AI cümlesini hazırlamaya başlar.

**Neden Bu Şekilde Tasarlandı?**

*   **Hız ve Kullanıcı Deneyimi:** Yeni bir misafir aradığında, ona anında bir geri bildirim vermek isteriz. LLM'in ilk yanıtı üretmesi 1-2 saniye sürebilir. Bu "ölü havayı", önceden kaydedilmiş ve anında çalınabilen bu standart karşılama anonsuyla doldururuz. Bu, kullanıcının hatta kalmasını sağlar.
*   **Verimlilik:** Sistem, anonsu çalarken arka planda veritabanı kaydı gibi diğer işleri yaparak zaman kazanır.
*   **Marka Kimliği:** Misafirler için her zaman aynı, tutarlı ve profesyonel bir ilk karşılama sunmuş oluruz.