// Audio processing utilities
export const generateWaveformData = () => {
  const x = [];
  const y = [];
  
  for (let i = 0; i < 200; i++) {
    x.push(i * 0.05);
    const t = i * 0.05;
    // Create a pitch-based waveform (frequency changes over time)
    const value = 
      Math.sin(t * 2) * 0.3 + 
      Math.sin(t * 4) * 0.2 + 
      Math.sin(t * 1.5) * 0.15 + 
      Math.cos(t * 3) * 0.1 +
      (Math.random() - 0.5) * 0.05;
    y.push(value);
  }
  
  return { x, y };
};

// Analyze pitch of audio segment using autocorrelation
const analyzePitch = (audioSegment, sampleRate) => {
  if (audioSegment.length === 0) return 4; // Default to A4 if no audio
  
  // Calculate autocorrelation
  const correlation = [];
  const maxLag = Math.floor(sampleRate / 50); // Minimum frequency ~50Hz
  const minLag = Math.floor(sampleRate / 2000); // Maximum frequency ~2000Hz
  
  for (let lag = minLag; lag < maxLag; lag++) {
    let sum = 0;
    for (let i = 0; i < audioSegment.length - lag; i++) {
      sum += audioSegment[i] * audioSegment[i + lag];
    }
    correlation.push(sum);
  }
  
  // Find the peak in autocorrelation (fundamental frequency)
  let maxCorrelation = 0;
  let bestLag = minLag;
  
  for (let i = 0; i < correlation.length; i++) {
    if (correlation[i] > maxCorrelation) {
      maxCorrelation = correlation[i];
      bestLag = minLag + i;
    }
  }
  
  // Convert lag to frequency
  const frequency = sampleRate / bestLag;
  
  // Convert frequency to octave (relative to A4 = 440Hz)
  const octave = Math.log2(frequency / 440) + 4;
  
  // Clamp to reasonable range
  return Math.max(0, Math.min(8, octave));
};

// Simple and fast pitch shifting using sample rate conversion
const simplePitchShift = (audioData, pitchRatio) => {
  const outputLength = Math.floor(audioData.length / pitchRatio);
  const output = new Float32Array(outputLength);
  
  for (let i = 0; i < outputLength; i++) {
    const sourceIndex = i * pitchRatio;
    const sourceIndexInt = Math.floor(sourceIndex);
    const sourceIndexFrac = sourceIndex - sourceIndexInt;
    
    // Linear interpolation
    const sample1 = audioData[sourceIndexInt] || 0;
    const sample2 = audioData[sourceIndexInt + 1] || 0;
    output[i] = sample1 * (1 - sourceIndexFrac) + sample2 * sourceIndexFrac;
  }
  
  return output;
};

export const applyWaveformTransformation = (audioData, waveformData) => {
  if (!audioData || audioData.length === 0) {
    console.log('No audio data provided');
    return null;
  }
  
  if (!waveformData || waveformData.length === 0) {
    console.log('No waveform data provided');
    return null;
  }
  
  console.log('Audio length:', audioData.length);
  console.log('Waveform data length:', waveformData.length);
  
  try {
    const audioLength = audioData.length;
    const sampleRate = 44100;
    const segmentDuration = 0.1; // 0.1 second segments
    const samplesPerSegment = Math.floor(sampleRate * segmentDuration);
    
    // Find min/max Y values from waveform for octave mapping
    const maxY = Math.max(...waveformData.y);
    const minY = Math.min(...waveformData.y);
    const yRange = maxY - minY;
    
    // Calculate total duration and number of segments
    const totalDuration = audioLength / sampleRate;
    const numSegments = Math.ceil(totalDuration / segmentDuration);
    
    const transformedAudio = new Float32Array(audioLength);
    const originalOctaves = []; // Track original pitch analysis
    const octaveChanges = []; // Track octave changes for visualization
    
    // Create a smoother autotune effect
    for (let segment = 0; segment < numSegments; segment++) {
      const segmentStartSample = segment * samplesPerSegment;
      const segmentEndSample = Math.min((segment + 1) * samplesPerSegment, audioLength);
      const segmentAudio = audioData.slice(segmentStartSample, segmentEndSample);
      
      // Analyze original pitch of this segment
      const originalOctave = analyzePitch(segmentAudio, sampleRate);
      originalOctaves.push(originalOctave);
      
      // Debug first few segments
      if (segment < 3) {
        console.log(`Segment ${segment}: original octave = ${originalOctave}`);
      }
      
      // Sample the waveform at the middle of this time segment
      const sampleTime = segment * segmentDuration + (segmentDuration / 2);
      const waveformIndex = (sampleTime / 10) * (waveformData.x.length - 1); // 10 seconds total waveform
      const waveformIndexInt = Math.floor(waveformIndex);
      const waveformIndexFrac = waveformIndex - waveformIndexInt;
      
      // Interpolate Y value from waveform
      const y1 = waveformData.y[waveformIndexInt] || 0;
      const y2 = waveformData.y[Math.min(waveformIndexInt + 1, waveformData.y.length - 1)] || 0;
      const yValue = y1 * (1 - waveformIndexFrac) + y2 * waveformIndexFrac;
      
      // Map Y value to target octave (0-8 octaves, A0 to A8)
      const targetOctave = ((yValue - minY) / yRange) * 8;
      octaveChanges.push(targetOctave);
      
      // Debug first few segments
      if (segment < 3) {
        console.log(`Segment ${segment}: yValue = ${yValue}, target octave = ${targetOctave}`);
      }
      
      // Calculate gentle pitch correction (limited to ±2 octaves for intelligibility)
      const pitchDifference = targetOctave - originalOctave;
      const limitedPitchDifference = Math.max(-2, Math.min(2, pitchDifference));
      const pitchRatio = Math.pow(2, limitedPitchDifference);
      
      // Apply gentle pitch correction using simple pitch shifting
      const correctedSegment = simplePitchShift(segmentAudio, pitchRatio);
      
      // Blend the corrected segment with original for natural sound
      const blendFactor = 0.6; // 60% corrected, 40% original for more natural sound
      for (let i = 0; i < correctedSegment.length && segmentStartSample + i < audioLength; i++) {
        const originalSample = audioData[segmentStartSample + i] || 0;
        const correctedSample = correctedSegment[i] || 0;
        transformedAudio[segmentStartSample + i] = 
          (correctedSample * blendFactor) + (originalSample * (1 - blendFactor));
      }
    }
    
    // Apply subtle compression to smooth out any artifacts
    const compressedAudio = new Float32Array(audioLength);
    const threshold = 0.8;
    const ratio = 4;
    
    for (let i = 0; i < audioLength; i++) {
      const sample = transformedAudio[i];
      if (Math.abs(sample) > threshold) {
        const excess = Math.abs(sample) - threshold;
        const compressedExcess = excess / ratio;
        const sign = sample >= 0 ? 1 : -1;
        compressedAudio[i] = sign * (threshold + compressedExcess);
      } else {
        compressedAudio[i] = sample;
      }
    }
    
    // Normalize audio
    const maxAudio = Math.max(...compressedAudio.map(Math.abs));
    let finalAudio;
    if (maxAudio > 0) {
      finalAudio = compressedAudio.map(sample => (sample / maxAudio) * 0.9);
    } else {
      finalAudio = compressedAudio;
    }
    
    // Store octave data for visualization
    finalAudio.originalOctaves = originalOctaves;
    finalAudio.octaveChanges = octaveChanges;
    
    console.log('Original octaves:', originalOctaves.length);
    console.log('Target octaves:', octaveChanges.length);
    console.log('Final audio length:', finalAudio.length);
    console.log('Sample original octaves:', originalOctaves.slice(0, 5));
    console.log('Sample target octaves:', octaveChanges.slice(0, 5));
    
    return finalAudio;
  } catch (error) {
    console.error('Transformation error:', error);
    return null;
  }
};

export const createAudioBlob = (audioData, sampleRate = 44100) => {
  try {
    // Convert audio data to WAV format
    const buffer = new ArrayBuffer(44 + audioData.length * 2);
    const view = new DataView(buffer);
    
    // WAV header
    const writeString = (offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };
    
    writeString(0, 'RIFF');
    view.setUint32(4, 36 + audioData.length * 2, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, 1, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, audioData.length * 2, true);
    
    // Audio data
    for (let i = 0; i < audioData.length; i++) {
      const sample = Math.max(-1, Math.min(1, audioData[i]));
      view.setInt16(44 + i * 2, sample * 0x7FFF, true);
    }
    
    return new Blob([buffer], { type: 'audio/wav' });
  } catch (error) {
    console.error('Audio blob creation error:', error);
    return null;
  }
};

export const downloadAudio = (audioData, filename, sampleRate = 44100) => {
  const blob = createAudioBlob(audioData, sampleRate);
  if (!blob) return;
  
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
