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
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    fps = 30
    # Set up video writer with H.264 codec
    # First create temporary raw video with MJPG codec since OpenCV doesn't directly support H.264
    temp_raw = os.path.join(os.path.dirname(output_mp4_path), "temp_raw.avi")
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
    out = cv2.VideoWriter(temp_raw, fourcc, fps, (640, 480))
    
    # Write black frames for duration of audio
    total_frames = int(duration * fps)
    for _ in range(total_frames):
        out.write(frame)
        
    out.release()
    
    # Convert raw video to H.264 using ffmpeg
    temp_h264 = os.path.join(os.path.dirname(output_mp4_path), "temp_h264.mp4")
    cmd = [
        'ffmpeg', '-i', temp_raw,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        temp_h264
    ]
    subprocess.call(cmd)
    
    # Add audio to H.264 video
    cmd = [
        'ffmpeg', '-i', temp_h264,
        '-i', wav_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        output_mp4_path
    ]
    subprocess.call(cmd)
    
    # Cleanup temp files
    os.remove(temp_raw)
    os.remove(temp_h264)
    
    return
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert WAV audio to MP4 video with black frames')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input WAV file path')
    parser.add_argument('--output', '-o', type=str, required=True, help='Output MP4 file path')
    
    args = parser.parse_args()
    convert_wav_to_mp4(wav_path=args.input, output_mp4_path=args.output)

