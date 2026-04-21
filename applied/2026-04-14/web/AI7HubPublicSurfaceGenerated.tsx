import React from 'react';

const functions = [
  {
    title: 'Produce → Verify → Test',
    detail: 'Boucle fondamentale visible sur la surface publique.',
  },
  {
    title: 'Analyze → Optimize → Reproduce',
    detail: 'Mesure les gains et prépare les prochains paquets.',
  },
  {
    title: 'Route contradictions',
    detail: 'Dirige les tensions vers review, rollback ou promotion.',
  },
  {
    title: 'Support life-project branches',
    detail: 'Relie théorie, systèmes, laboratoire et publication.',
  },
];

export default function AI7HubPublicSurfaceGenerated() {
  return (
    <section
      style={{
        borderRadius: '26px',
        border: '1px solid rgba(96,165,250,0.18)',
        background: 'radial-gradient(circle at top, rgba(59,130,246,0.14), transparent 28%), rgba(255,255,255,0.03)',
        padding: '22px',
      }}
    >
      <div style={{ color: '#93c5fd', fontSize: '12px', letterSpacing: '0.22em', textTransform: 'uppercase' }}>
        AI-7 public metabolism
      </div>
      <h2 style={{ margin: '8px 0 0 0', fontSize: '30px' }}>Hub des paquets et boucles de travail</h2>
      <p style={{ color: 'rgba(255,255,255,0.72)', lineHeight: 1.7 }}>
        Cette surface n’est plus juste une description. Elle expose les fonctions publiques du métabolisme
        AI-7: production, guidage, orchestration, et routage des contradictions sous gouvernance TRISTAN2.
      </p>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '12px', marginTop: '16px' }}>
        {functions.map((item) => (
          <div
            key={item.title}
            style={{
              borderRadius: '18px',
              border: '1px solid rgba(255,255,255,0.08)',
              background: 'rgba(255,255,255,0.03)',
              padding: '14px',
            }}
          >
            <div style={{ color: '#dbeafe', fontWeight: 600 }}>{item.title}</div>
            <div style={{ color: 'rgba(255,255,255,0.62)', marginTop: '8px', lineHeight: 1.6 }}>{item.detail}</div>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginTop: '18px' }}>
        <button style={primaryButton}>Inspect AI-7 packets</button>
        <button style={secondaryButton}>Inspect runtime routes</button>
        <button style={secondaryButton}>Inspect AI-BOT roles</button>
        <button style={secondaryButton}>Open review corridor</button>
      </div>
    </section>
  );
}

const primaryButton: React.CSSProperties = {
  borderRadius: '14px',
  border: '1px solid rgba(96,165,250,0.26)',
  background: 'rgba(59,130,246,0.16)',
  color: '#dbeafe',
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
