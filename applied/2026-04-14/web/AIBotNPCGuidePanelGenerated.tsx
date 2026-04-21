import React from 'react';

const npcModes = [
  {
    title: 'Concept Guide',
    detail: 'Traduit un objet TFUGA en carte lisible sans le vider de sa profondeur.',
  },
  {
    title: 'System Guide',
    detail: 'Montre où un module, un packet ou une boucle se place dans le système.',
  },
  {
    title: 'Experiment Guide',
    detail: 'Accompagne les pilotes Fractal-Loop, Raman, LDK et circuits.',
  },
  {
    title: 'Review Guide',
    detail: 'Aide à préparer scorecards, gates et décisions TRISTAN2.',
  },
  {
    title: 'Collaboration Guide',
    detail: 'Explique la prochaine étape gouvernée pour contribuer sans bruit.',
  },
];

export default function AIBotNPCGuidePanelGenerated() {
  return (
    <section
      style={{
        borderRadius: '26px',
        border: '1px solid rgba(16,185,129,0.18)',
        background: 'radial-gradient(circle at bottom right, rgba(16,185,129,0.12), transparent 24%), rgba(255,255,255,0.03)',
        padding: '22px',
      }}
    >
      <div style={{ color: '#86efac', fontSize: '12px', letterSpacing: '0.22em', textTransform: 'uppercase' }}>
        AI-BOT guidance
      </div>
      <h2 style={{ margin: '8px 0 0 0', fontSize: '30px' }}>NPC guides pour apprendre en jouant</h2>
      <p style={{ color: 'rgba(255,255,255,0.72)', lineHeight: 1.7 }}>
        Les guides IA-BOT deviennent ici des aides jouables: indices bornés, liens d’artefacts, prochaines étapes,
        et aide à la navigation entre théorie, système, expérience et gouvernance.
      </p>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '12px', marginTop: '16px' }}>
        {npcModes.map((mode) => (
          <div
            key={mode.title}
            style={{
              borderRadius: '18px',
              border: '1px solid rgba(255,255,255,0.08)',
              background: 'rgba(255,255,255,0.03)',
              padding: '14px',
            }}
          >
            <div style={{ color: '#dcfce7', fontWeight: 600 }}>{mode.title}</div>
            <div style={{ color: 'rgba(255,255,255,0.62)', marginTop: '8px', lineHeight: 1.6 }}>{mode.detail}</div>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginTop: '18px' }}>
        <button style={primaryButton}>Ask for bounded hint</button>
        <button style={secondaryButton}>Inspect linked artifact</button>
        <button style={secondaryButton}>See next governed step</button>
      </div>
    </section>
  );
}

const primaryButton: React.CSSProperties = {
  borderRadius: '14px',
  border: '1px solid rgba(16,185,129,0.24)',
  background: 'rgba(16,185,129,0.16)',
  color: '#dcfce7',
  padding: '12px 16px',
  cursor: 'pointer',
};

const secondaryButton: React.CSSProperties = {
  borderRadius: '14px',
  border: '1px solid rgba(255,255,255,0.1)',
  background: 'rgba(255,255,255,0.04)',
  color: 'white',
  padding: '12px 16px',
  cursor: 'pointer',
};
