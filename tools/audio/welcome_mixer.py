from pydub import AudioSegment
import argparse

def create_welcome(hold_path, connection_path, output_path, bg_volume=-15, delay=500):
    # Load files
    hold = AudioSegment.from_wav(hold_path)
    connection = AudioSegment.from_wav(connection_path)

    # Target length = mesaj uzunluğu + 2s
    target_length_ms = len(connection) + 2000

    # Extend background if too short
    if len(hold) < target_length_ms:
        hold = hold * (target_length_ms // len(hold) + 1)

    # Trim hold
    hold = hold[:target_length_ms]

    # Softer background
    hold_quiet = hold + bg_volume

    # Overlay
    welcome = hold_quiet.overlay(connection, position=delay)

    # Export in telecom standard format
    welcome.export(
        output_path,
        format="wav",
        codec="pcm_s16le",
        parameters=["-ar", "8000", "-ac", "1"]
    )
    print(f"✅ Created (telecom standard 8kHz mono PCM): {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mix hold music and connection message into telecom-grade welcome.wav")
    parser.add_argument("--hold", required=True, help="Path to hold.wav")
    parser.add_argument("--connection", required=True, help="Path to connecting.wav")
    parser.add_argument("--output", default="welcome.wav", help="Output file path")
    parser.add_argument("--volume", type=int, default=-15, help="Background volume adjustment (dB)")
    parser.add_argument("--delay", type=int, default=500, help="Delay before connection message (ms)")

    args = parser.parse_args()

    create_welcome(args.hold, args.connection, args.output, args.volume, args.delay)

# python tools/audio/welcome_mixer.py --hold audio/en/system/hold.wav --connection audio/en/system/connecting.wav --output audio/en/welcome.wav
# python tools/audio/welcome_mixer.py --hold audio/tr/system/hold.wav --connection audio/tr/system/connecting.wav --output audio/tr/welcome.wav
