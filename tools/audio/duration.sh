echo "# Audio Duration Report" > duration.md
echo "| File | Duration (s) | Codec | Sample Rate | Channels | Bitrate |" >> duration.md
echo "|------|-------------|-------|-------------|----------|---------|" >> duration.md

for f in *.wav; do
  ffprobe -v error -select_streams a:0 \
  -show_entries stream=codec_name,sample_rate,channels,bit_rate \
  -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "$f" | \
  {
    read codec
    read sample
    read channels
    read bitrate
    read duration
    printf "| %s | %.2f | %s | %s Hz | %s | %s |\n" \
      "$f" "$duration" "$codec" "$sample" "$channels" "$bitrate"
  }
done >> duration.md