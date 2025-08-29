import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import AudioRecorder from './components/AudioRecorder';
import WaveformChart from './components/WaveformChart';
import AudioPlayer from './components/AudioPlayer';
import { HowToUse, About } from './components/Instructions';
import { generateWaveformData, applyWaveformTransformation } from './utils/audioUtils';

const AppContainer = styled.div`
  min-height: 100vh;
  background-color: #f8fafc;
  padding: 20px 0;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 40px;
`;

const Title = styled.h1`
  font-size: 48px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const Subtitle = styled.p`
  font-size: 18px;
  color: #64748b;
  margin: 0;
`;

const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
`;

const Section = styled.section`
  margin-bottom: 40px;
`;

const SectionTitle = styled.h2`
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 16px;
  text-align: center;
`;

const Grid = styled.div`
  display: grid;
  gap: 24px;
  
  @media (min-width: 768px) {
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  }
`;

const SuccessMessage = styled.div`
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
  text-align: center;
  font-weight: 500;
`;

function App() {
  const [waveformData, setWaveformData] = useState(null);
  const [originalAudio, setOriginalAudio] = useState(null);
  const [transformedAudio, setTransformedAudio] = useState(null);
  const [sampleRate, setSampleRate] = useState(44100);
  const [showSuccess, setShowSuccess] = useState(false);
  const [recorderKey, setRecorderKey] = useState(0);

  // Generate waveform data on component mount
  useEffect(() => {
    setWaveformData(generateWaveformData());
  }, []);

  const handleRecordingComplete = (audioData, rate) => {
    // Clear previous data first
    setOriginalAudio(null);
    setTransformedAudio(null);
    
    // Use setTimeout to ensure state is cleared before setting new data
    setTimeout(() => {
      setOriginalAudio(audioData);
      setSampleRate(rate);
      
      // Apply transformation
      if (waveformData) {
        console.log('Applying transformation with waveform data:', waveformData);
        const transformed = applyWaveformTransformation(audioData, waveformData);
        console.log('Transformation result:', transformed);
        console.log('Octave changes:', transformed?.octaveChanges);
        setTransformedAudio(transformed);
      } else {
        console.log('No waveform data available');
      }
      
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 3000);
      
      // Force re-render of recorder for next recording
      setRecorderKey(prev => prev + 1);
    }, 100);
  };

  const getTimestamp = () => {
    const now = new Date();
    return now.toISOString().replace(/[:.]/g, '-').slice(0, 19);
  };

  const originalDuration = originalAudio ? originalAudio.length / sampleRate : 0;
  const transformedDuration = transformedAudio ? transformedAudio.length / sampleRate : 0;

  return (
    <AppContainer>
      <Header>
        <Title>Data Notes</Title>
        <Subtitle>Transform your voice with data waveforms</Subtitle>
      </Header>

      <MainContent>
        {/* Step 1: Waveform Display */}
        <Section>
          <SectionTitle>📊 Observe this waveform and describe what you see</SectionTitle>
          {waveformData && (
            <WaveformChart 
              data={waveformData} 
              title="Data Waveform"
              height={400}
            />
          )}
        </Section>

        {/* Step 2: Voice Recording */}
        <Section>
          <SectionTitle>🎙️ Record Your Voice</SectionTitle>
          <AudioRecorder key={recorderKey} onRecordingComplete={handleRecordingComplete} />
        </Section>

        {/* Success Message */}
        {showSuccess && (
          <SuccessMessage>
            ✅ Recording completed! Your audio has been transformed.
          </SuccessMessage>
        )}

        {/* Step 3: Audio Playback */}
        {originalAudio && transformedAudio && (
          <Section>
            <SectionTitle>🔊 Audio Playback</SectionTitle>
            <Grid>
              <AudioPlayer
                audioData={originalAudio}
                sampleRate={sampleRate}
                title="Original Recording"
                icon="🎵"
                duration={originalDuration}
                filename={`original_${getTimestamp()}.wav`}
              />
              
              <AudioPlayer
                audioData={transformedAudio}
                sampleRate={sampleRate}
                title="Transformed Audio"
                icon="🎛️"
                duration={transformedDuration}
                filename={`transformed_${getTimestamp()}.wav`}
              />
            </Grid>
          </Section>
        )}

        {/* Step 4: Audio Waveform Visualization */}
        {originalAudio && transformedAudio && (
          <Section>
            <SectionTitle>📈 Audio Pitch Analysis</SectionTitle>
            {console.log('Transformed audio object:', transformedAudio)}
            {console.log('Original octaves:', transformedAudio.originalOctaves)}
            {console.log('Target octaves:', transformedAudio.octaveChanges)}
            {transformedAudio.octaveChanges && transformedAudio.originalOctaves ? (
              <div>
                <WaveformChart 
                  data={{
                    x: Array.from({ length: transformedAudio.originalOctaves.length }, (_, i) => i * 0.1),
                    y: transformedAudio.originalOctaves
                  }}
                  title="Original Audio Pitch Analysis (0.1s segments)"
                  height={200}
                  showGrid={true}
                  yAxisTitle="Octave (A4 = 4)"
                  yAxisRange={[0, 8]}
                  yAxisTicks={[0, 1, 2, 3, 4, 5, 6, 7, 8]}
                  yAxisTickLabels={['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']}
                  showMarkers={true}
                />
                
                <div style={{ marginTop: '32px' }}>
                  <WaveformChart 
                    data={{
                      x: Array.from({ length: transformedAudio.octaveChanges.length }, (_, i) => i * 0.1),
                      y: transformedAudio.octaveChanges
                    }}
                    title="Autotuned Audio Pitch Target (0.1s segments)"
                    height={200}
                    showGrid={true}
                    yAxisTitle="Octave (A4 = 4)"
                    yAxisRange={[0, 8]}
                    yAxisTicks={[0, 1, 2, 3, 4, 5, 6, 7, 8]}
                    yAxisTickLabels={['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']}
                    showMarkers={true}
                  />
                </div>
              </div>
            ) : (
              <div style={{ textAlign: 'center', color: '#64748b', padding: '40px' }}>
                Pitch analysis not available. Audio transformation completed successfully.
              </div>
            )}
          </Section>
        )}

        {/* Instructions */}
        <HowToUse />
        <About />
      </MainContent>
    </AppContainer>
  );
}

export default App;
