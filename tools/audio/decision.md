DERİN TEKNİK ANALİZ & MİMARİ KARARLAR

    Teknik Sorun:
    media-service/src/audio.rs içindeki hound::WavReader::open(path_owned) fonksiyonu, WAV dosyasını okuyup Vec<i16> (16-bit tamsayı) dizisine çevirmeye çalışır. pcm_s16le formatı tam olarak 16-bit ham sestir ve bu işlem kusursuz çalışır. Ancak siz dosyaları pcm_mulaw (8-bit sıkıştırılmış) yaptığınızda, hound kütüphanesi bu 8-bit sıkıştırılmış veriyi doğrudan 16-bit LPCM'e (i16) cast edemez ve panikleyerek "WAV açma hatası" fırlatır.

    Çözüm Stratejisi (Neden Kod Değil de Format Değişiyor?):
    Mimarimizin (rtp-core ve media-service) ana prensibi şudur: Tüm iç ses işleme, karıştırma ve filtreleme işlemleri 16-bit Linear PCM (Ham Ses) üzerinden yapılır.
    Ses, ağa (UDP) basılacağı son milisaniyede kullanıcının cihazının desteklediği kodeğe (PCMU, PCMA veya G729) dönüştürülür. Eğer siz kaynak dosyayı baştan pcm_mulaw yaparsanız, kodun içine bir de "Dosyadan mu-law oku -> Linear PCM'e çevir -> İşle -> Tekrar mu-law'a çevir -> Ağa bas" şeklinde gereksiz bir işlem yükü eklemiş oluruz. Diskte birkaç MB yer kazanmak için CPU döngülerini feda edemeyiz.

    Risk Analizi:
    Eğer kod tabanını pcm_mulaw okuyacak şekilde değiştirirsek, ileride eklenecek olan AI TTS sesleri (bunlar 16k/24k ham LPCM üretir) ile statik dosyaları aynı pipeline'da birleştiremeyiz. Bu yüzden kod dokunulmazdır. Dosyalar eski haline dönecektir.

Verification:

    sentiric-assets/tools/audio/telephony.sh betiğini çalıştırın.

    Ardından tools/audio/duration.sh betiğini çalıştırarak MD dosyasını güncelleyin. Tabloda Codec sütunu kesinlikle pcm_s16le olmalıdır. pcm_mulaw görüyorsanız hatalıdır.    