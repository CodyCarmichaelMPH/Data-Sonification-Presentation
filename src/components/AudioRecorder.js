import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';

const RecorderContainer = styled.div`
  text-align: center;
  padding: 24px;
`;

const RecordingStatus = styled.div`
  padding: 16px;
  border-radius: 12px;
  margin: 16px 0;
  font-weight: 600;
  font-size: 16px;
  transition: all 0.3s ease;
  border: 2px solid;
  
  ${props => props.isRecording ? `
    background-color: #fef2f2;
    color: #dc2626;
    border-color: #dc2626;
    animation: pulse 1.5s infinite;
    
    @keyframes pulse {
      0% { border-color: #dc2626; }
      50% { border-color: #fca5a5; }
      100% { border-color: #dc2626; }
    }
  ` : `
    background-color: #f8fafc;
    color: #64748b;
    border-color: #e2e8f0;
  `}
`;

const RecordButton = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 16px 32px;
  border: none;
  border-radius: 50px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  gap: 12px;
  min-width: 200px;
  
  ${props => props.isRecording ? `
    background-color: #dc2626;
    color: white;
    
    &:hover {
      background-color: #b91c1c;
      transform: scale(1.05);
    }
  ` : `
    background-color: #3b82f6;
    color: white;
    
    &:hover {
      background-color: #2563eb;
      transform: scale(1.05);
    }
  `}
`;

const AudioRecorder = ({ onRecordingComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [error, setError] = useState(null);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const durationIntervalRef = useRef(null);

  useEffect(() => {
    return () => {
      if (durationIntervalRef.current) {
        clearInterval(durationIntervalRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          sampleRate: 44100,
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      });
      
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const arrayBuffer = await audioBlob.arrayBuffer();
        const audioContext = new AudioContext();
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        
        // Convert to mono and normalize
        const channelData = audioBuffer.getChannelData(0);
        const audioData = Array.from(channelData);
        
        // Normalize audio
        const maxAmplitude = Math.max(...audioData.map(Math.abs));
        if (maxAmplitude > 0) {
          const normalizedAudio = audioData.map(sample => (sample / maxAmplitude) * 0.8);
          onRecordingComplete(normalizedAudio, audioBuffer.sampleRate);
        }
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingDuration(0);
      
      // Start duration timer
      durationIntervalRef.current = setInterval(() => {
        setRecordingDuration(prev => prev + 0.1);
      }, 100);
      
    } catch (err) {
      setError('Microphone access denied. Please allow microphone permissions and try again.');
      console.error('Recording error:', err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (durationIntervalRef.current) {
        clearInterval(durationIntervalRef.current);
        durationIntervalRef.current = null;
      }
    }
  };

  const formatDuration = (duration) => {
    const minutes = Math.floor(duration / 60);
    const seconds = Math.floor(duration % 60);
    const tenths = Math.floor((duration % 1) * 10);
    return `${minutes}:${seconds.toString().padStart(2, '0')}.${tenths}`;
  };

  return (
    <RecorderContainer>
      <RecordingStatus isRecording={isRecording}>
        {isRecording 
          ? `Recording... ${formatDuration(recordingDuration)}`
          : 'Ready to record'
        }
      </RecordingStatus>
      
      {error && (
        <div style={{ color: '#dc2626', marginBottom: '16px', fontSize: '14px' }}>
          {error}
        </div>
      )}
      
      <RecordButton 
        onClick={isRecording ? stopRecording : startRecording}
        isRecording={isRecording}
      >
        {isRecording ? (
          <>
            <span>⏹️</span>
            Stop Recording
          </>
        ) : (
          <>
            <span>🎙️</span>
            Start Recording
          </>
        )}
      </RecordButton>
      
      <div style={{ marginTop: '16px', fontSize: '14px', color: '#64748b' }}>
        {isRecording 
          ? 'Click to stop recording'
          : 'Click to start recording your voice'
        }
      </div>
    </RecorderContainer>
  );
};

export default AudioRecorder;
