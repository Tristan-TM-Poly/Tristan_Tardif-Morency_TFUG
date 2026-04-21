import React, { useState } from 'react';

const nodeFamilies = [
  {
    id: 'tfuga-objects',
    title: 'TFUGA objects',
    detail: 'Idées, théories, applications, preuves, opérateurs, noyaux.',
  },
  {
    id: 'ai7-loops',
    title: 'AI-7 loops',
    detail: 'Produire, vérifier, tester, analyser, optimiser, reproduire.',
  },
  {
    id: 'tristan2-gates',
    title: 'TRISTAN2 gates',
    detail: 'Scorecards, discipline, review, rollback, immunité.',
  },
  {
    id: 'life-projects',
    title: 'Life projects',
    detail: 'Branches de mission, laboratoire, publication, architecture.',
  },
  {
    id: 'centrales',
    title: 'AI-7 fractal centrales',
    detail: 'Systèmes d’énergie, de calcul, et de gouvernance distribuée.',
  },
  {
    id: 'demos',
    title: 'Public demos',
    detail: 'Fractal-Loop, LDK, Raman, observabilité, surfaces publiques.',
  },
  {
    id: 'collab-routes',
    title: 'Collaboration routes',
    detail: 'Passages entre canon, repo, drive, runtime et communauté.',
  },
];

export default function YggdrasilNodeExplorerGenerated() {
  const [selected, setSelected] = useState(nodeFamilies[0].id);
  const current = nodeFamilies.find((family) => family.id === selected) || nodeFamilies[0];

  return (
    <section
      style={{
        borderRadius: '26px',
        border: '1px solid rgba(168,85,247,0.18)',
        background: 'radial-gradient(circle at top left, rgba(168,85,247,0.14), transparent 28%), rgba(255,255,255,0.03)',
        padding: '22px',
      }}
    >
      <div style={{ color: '#d8b4fe', fontSize: '12px', letterSpacing: '0.22em', textTransform: 'uppercase' }}>
        Yggdrasil explorer
      </div>
      <h2 style={{ margin: '8px 0 0 0', fontSize: '30px' }}>Familles de nœuds et liens de branches</h2>
      <p style={{ color: 'rgba(255,255,255,0.72)', lineHeight: 1.7 }}>
        Surface d’exploration bornée pour parcourir les familles profondes de TFUGA. La logique n’est pas
        décorative: chaque nœud représente une famille exploitable par packets, scorecards et routes de promotion.
      </p>
      <div style={{ display: 'grid', gridTemplateColumns: '320px minmax(0, 1fr)', gap: '14px', marginTop: '16px' }}>
        <div style={{ display: 'grid', gap: '10px' }}>
          {nodeFamilies.map((family) => (
            <button
              key={family.id}
              onClick={() => setSelected(family.id)}
              style={{
                textAlign: 'left',
                borderRadius: '18px',
                border: selected === family.id ? '1px solid rgba(216,180,254,0.3)' : '1px solid rgba(255,255,255,0.08)',
                background: selected === family.id ? 'rgba(168,85,247,0.16)' : 'rgba(255,255,255,0.03)',
                color: 'white',
                padding: '14px',
                cursor: 'pointer',
              }}
            >
              <div style={{ fontWeight: 600 }}>{family.title}</div>
              <div style={{ color: 'rgba(255,255,255,0.56)', marginTop: '6px', lineHeight: 1.5 }}>{family.detail}</div>
            </button>
          ))}
        </div>
        <div
          style={{
            borderRadius: '22px',
            border: '1px solid rgba(255,255,255,0.08)',
            background: 'rgba(255,255,255,0.03)',
            padding: '18px',
          }}
        >
          <div style={{ color: '#e9d5ff', fontSize: '12px', letterSpacing: '0.18em', textTransform: 'uppercase' }}>
            Branche active
          </div>
          <h3 style={{ margin: '10px 0 0 0', fontSize: '28px' }}>{current.title}</h3>
          <p style={{ color: 'rgba(255,255,255,0.72)', lineHeight: 1.7 }}>{current.detail}</p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: '10px', marginTop: '18px' }}>
            {['Inspect node family', 'Inspect branch links', 'Inspect next path'].map((action) => (
              <button key={action} style={actionButton}>{action}</button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

const actionButton: React.CSSProperties = {
  borderRadius: '14px',
  border: '1px solid rgba(255,255,255,0.1)',
  background: 'rgba(255,255,255,0.04)',
  color: 'white',
  padding: '12px 14px',
  cursor: 'pointer',
};
