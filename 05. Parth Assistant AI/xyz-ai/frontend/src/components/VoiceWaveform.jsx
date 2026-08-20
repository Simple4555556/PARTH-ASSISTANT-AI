import React, { useEffect, useRef } from 'react';

const BAR_COUNT = 18;

export default function VoiceWaveform({ voiceState }) {
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const phaseRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width;
    const H = canvas.height;

    const draw = () => {
      ctx.clearRect(0, 0, W, H);
      phaseRef.current += 0.08;

      const bars = BAR_COUNT;
      const barW = W / (bars * 2 - 1);

      for (let i = 0; i < bars; i++) {
        let barH;

        if (voiceState === 'IDLE') {
          barH = 4;
        } else if (voiceState === 'LISTENING') {
          barH = Math.abs(Math.sin(phaseRef.current + i * 0.5)) * 28 + 4;
        } else if (voiceState === 'PROCESSING') {
          barH = Math.abs(Math.sin(phaseRef.current * 2 + i * 0.3)) * 16 + 4;
        } else if (voiceState === 'SPEAKING') {
          barH = Math.abs(Math.sin(phaseRef.current + i * 0.4)) * 22 + 6;
        } else {
          barH = 4;
        }

        const x = i * (barW * 2);
        const y = (H - barH) / 2;

        const gradient = ctx.createLinearGradient(0, y, 0, y + barH);
        if (voiceState === 'LISTENING') {
          gradient.addColorStop(0, '#ef4444');
          gradient.addColorStop(1, '#f97316');
        } else if (voiceState === 'SPEAKING') {
          gradient.addColorStop(0, '#22c55e');
          gradient.addColorStop(1, '#06b6d4');
        } else if (voiceState === 'PROCESSING') {
          gradient.addColorStop(0, '#f59e0b');
          gradient.addColorStop(1, '#eab308');
        } else {
          gradient.addColorStop(0, '#334155');
          gradient.addColorStop(1, '#475569');
        }

        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.roundRect(x, y, barW, barH, 3);
        ctx.fill();
      }

      animFrameRef.current = requestAnimationFrame(draw);
    };

    draw();
    return () => cancelAnimationFrame(animFrameRef.current);
  }, [voiceState]);

  return (
    <canvas
      ref={canvasRef}
      width={200}
      height={40}
      style={{
        display: 'block',
        margin: '0 auto',
        opacity: voiceState === 'IDLE' ? 0.35 : 1,
        transition: 'opacity 0.3s ease'
      }}
      aria-hidden="true"
    />
  );
}
