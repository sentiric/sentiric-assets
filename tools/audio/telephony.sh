for f in master/*.wav; do
  name=$(basename "$f")

  ffmpeg -y -i "$f" \
  -af "highpass=f=200,lowpass=f=3400,aresample=resampler=soxr,loudnorm,adelay=30|30" \
  -ar 8000 \
  -ac 1 \
  -c:a pcm_mulaw \
  "system/$name"

done