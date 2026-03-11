#!/bin/bash

# Dizinlerdeki tüm wav dosyalarını bul ve doğru formata çevir
for f in master/*.wav; do
  name=$(basename "$f")

  # MİMARİ ZORUNLULUK: 
  # -ar 8000 (Telekom standardı)
  # -ac 1 (Mono)
  # -c:a pcm_s16le (16-bit Signed Integer Little Endian - Internal DSP Formatımız)
  ffmpeg -y -i "$f" \
  -af "highpass=f=200,lowpass=f=3400,aresample=resampler=soxr,loudnorm,adelay=30|30" \
  -ar 8000 \
  -ac 1 \
  -c:a pcm_s16le \
  "system/$name"

done