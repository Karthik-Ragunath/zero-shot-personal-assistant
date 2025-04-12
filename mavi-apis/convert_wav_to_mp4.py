import cv2
import numpy as np
import soundfile as sf
import subprocess
import argparse
import os

def convert_wav_to_mp4(wav_path, output_mp4_path):
    # Read the audio file and get duration
    audio_data, sample_rate = sf.read(wav_path)
    duration = len(audio_data) / sample_rate
    
    # Create black frame
    frame = np.zeros((480,640,3), dtype=np.uint8)
    
    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    out = cv2.VideoWriter(output_mp4_path, fourcc, fps, (640,480))
    
    # Write black frames for duration of audio
    total_frames = int(duration * fps)
    for _ in range(total_frames):
        out.write(frame)
        
    out.release()
    
    # Add audio to video using ffmpeg
    output_dir = os.path.dirname(output_mp4_path)
    temp_output = os.path.join(output_dir, "temp_" + os.path.basename(output_mp4_path))
    subprocess.call(['mv', output_mp4_path, temp_output])
    
    cmd = [
        'ffmpeg', '-i', temp_output,
        '-i', wav_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        output_mp4_path
    ]
    subprocess.call(cmd)
    
    # Cleanup temp file
    subprocess.call(['rm', temp_output])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert WAV audio to MP4 video with black frames')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input WAV file path')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output MP4 file path')
    
    args = parser.parse_args()
    convert_wav_to_mp4(wav_path=args.input, output_mp4_path=args.output)

