import React, { useState } from 'react';
import styled from 'styled-components';

const InstructionsContainer = styled.div`
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  margin-top: 24px;
`;

const InstructionsHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
  
  &:hover {
    background-color: #f8fafc;
  }
`;

const InstructionsTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const InstructionsContent = styled.div`
  color: #475569;
  line-height: 1.6;
  
  ${props => !props.isExpanded && `
    display: none;
  `}
`;

const StepList = styled.ol`
  margin: 16px 0;
  padding-left: 20px;
  
  li {
    margin-bottom: 12px;
    padding-left: 8px;
  }
`;

const TipsList = styled.ul`
  margin: 16px 0;
  padding-left: 20px;
  
  li {
    margin-bottom: 8px;
    padding-left: 8px;
  }
`;

const ExpandIcon = styled.span`
  font-size: 20px;
  transition: transform 0.2s ease;
  transform: ${props => props.isExpanded ? 'rotate(180deg)' : 'rotate(0deg)'};
`;

const Instructions = ({ title, icon, children, defaultExpanded = false }) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  return (
    <InstructionsContainer>
      <InstructionsHeader onClick={() => setIsExpanded(!isExpanded)}>
        <InstructionsTitle>
          {icon} {title}
        </InstructionsTitle>
        <ExpandIcon isExpanded={isExpanded}>▼</ExpandIcon>
      </InstructionsHeader>
      
      <InstructionsContent isExpanded={isExpanded}>
        {children}
      </InstructionsContent>
    </InstructionsContainer>
  );
};

export const HowToUse = () => (
  <Instructions title="How to use" icon="💡">
    <p><strong>Simple 4-step process:</strong></p>
    <StepList>
      <li><strong>Observe</strong> the waveform graph above</li>
      <li><strong>Record</strong> your voice describing what you see</li>
      <li><strong>Transform</strong> your voice with the waveform</li>
      <li><strong>Listen</strong> to both original and transformed audio</li>
    </StepList>
    
    <p><strong>Tips for best results:</strong></p>
    <TipsList>
      <li>Speak clearly and describe patterns you observe</li>
      <li>Record for at least 2-3 seconds</li>
      <li>Use headphones for better audio experience</li>
      <li>Try different descriptions to hear various effects</li>
    </TipsList>
  </Instructions>
);

export const About = () => (
  <Instructions title="About" icon="ℹ️">
    <p>
      <strong>Data Notes</strong> transforms your voice using data waveforms, creating a unique audio-visual experience.
    </p>
    <p>
      The transformation applies the amplitude characteristics of the waveform to your voice recording,
      creating a modulated version that reflects the data patterns you observed.
    </p>
    <p>
      Built with React, Web Audio API, and real-time audio processing.
    </p>
  </Instructions>
);

export default Instructions;
