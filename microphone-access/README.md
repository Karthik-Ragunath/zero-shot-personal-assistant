# Microphone Access Web App

A simple web application that demonstrates how to:
1. Request microphone permissions
2. Record audio from the microphone
3. Save the recording to the local filesystem

## Features

- Clean, responsive UI
- Real-time audio visualization
- Recording controls (start/stop)
- Preview recordings before download
- Save recordings as .webm audio files

## Requirements

- A modern web browser that supports:
  - MediaDevices API
  - MediaRecorder API
  - Web Audio API
- Node.js (to run the local server)

## Getting Started

1. Navigate to the project directory:
   ```
   cd microphone-access
   ```

2. Start the local server:
   ```
   node server.js
   ```

3. Open your browser and visit:
   ```
   http://localhost:3000
   ```

## Usage

1. Click "Request Microphone Permission" to grant microphone access
2. Click "Start Recording" to begin recording audio
3. Click "Stop Recording" when you're done
4. Preview your recording in the Recordings list
5. Click "Save Recording" to download the audio file to your computer

## Browser Compatibility

This application uses modern Web APIs and works best in:
- Chrome/Edge (latest versions)
- Firefox (latest versions)
- Safari (latest versions)

## Notes

- Audio is saved in WebM format, which is widely supported
- The audio visualization shows the waveform of your microphone input
- For security reasons, microphone access requires HTTPS in production environments, but works with HTTP on localhost