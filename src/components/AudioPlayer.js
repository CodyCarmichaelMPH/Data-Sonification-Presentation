import React, { useState, useRef } from 'react';
import styled from 'styled-components';
import { downloadAudio } from '../utils/audioUtils';

const AudioContainer = styled.div`
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
`;

const AudioHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
`;

const AudioTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const AudioInfo = styled.div`
  font-size: 14px;
  color: #64748b;
  margin-bottom: 16px;
`;

const AudioControls = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
`;

const DownloadButton = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: #f8fafc;
  color: #475569;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  gap: 6px;
  
  &:hover {
    background-color: #e2e8f0;
    transform: translateY(-1px);
  }
`;

const AudioPlayer = ({ 
  audioData, 
  sampleRate = 44100, 
  title, 
  icon, 
  duration,
  filename 
}) => {
  const [audioUrl, setAudioUrl] = useState(null);
  const audioRef = useRef(null);

  React.useEffect(() => {
    if (audioData && audioData.length > 0) {
      // Create proper WAV blob using the utility function
      const blob = createAudioBlob(audioData, sampleRate);
      if (blob) {
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);
        
        return () => {
          URL.revokeObjectURL(url);
        };
      }
    }
  }, [audioData, sampleRate]);

  const handleDownload = () => {
    if (audioData && filename) {
      downloadAudio(audioData, filename, sampleRate);
    }
  };

  const formatDuration = (duration) => {
    if (!duration) return '0:00';
    const minutes = Math.floor(duration / 60);
    const seconds = Math.floor(duration % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  if (!audioData || audioData.length === 0) {
    return (
      <AudioContainer>
        <AudioHeader>
          <AudioTitle>
            {icon} {title}
          </AudioTitle>
        </AudioHeader>
        <div style={{ textAlign: 'center', color: '#64748b', padding: '20px' }}>
          No audio available
        </div>
      </AudioContainer>
    );
  }

  return (
    <AudioContainer>
      <AudioHeader>
        <AudioTitle>
          {icon} {title}
        </AudioTitle>
        <DownloadButton onClick={handleDownload}>
          📥 Download
        </DownloadButton>
      </AudioHeader>
      
      <AudioInfo>
        Duration: {formatDuration(duration)} | 
        Sample Rate: {sampleRate}Hz | 
        Samples: {audioData.length.toLocaleString()}
      </AudioInfo>
      
      <AudioControls>
        {audioUrl && (
          <audio 
            ref={audioRef}
            controls 
            style={{ width: '100%' }}
            src={audioUrl}
          >
            Your browser does not support the audio element.
          </audio>
        )}
      </AudioControls>
    </AudioContainer>
  );
};

export default AudioPlayer;
