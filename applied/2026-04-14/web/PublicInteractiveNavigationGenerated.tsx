import React from 'react';

const items = [
  'Home',
  'TFUGA Sovereign',
  'Interactive Trinity',
  'Yggdrasil',
  'Edu-Game Hub',
  'Fractal-Loop',
  'LDK',
  'Raman',
  'Collaborations',
];

export default function PublicInteractiveNavigationGenerated() {
  return (
    <nav
      style={{
        position: 'sticky',
        top: 0,
        zIndex: 20,
        backdropFilter: 'blur(16px)',
        background: 'rgba(5, 8, 16, 0.82)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: '22px',
        padding: '14px 18px',
        marginBottom: '18px',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
        <div>
          <div style={{ fontSize: '12px', letterSpacing: '0.22em', textTransform: 'uppercase', color: '#fbbf24' }}>TFUGA</div>
          <div style={{ fontSize: '20px', fontWeight: 700, color: '#fef3c7' }}>Sovereign interactive public shell</div>
        </div>
        <ul style={{ display: 'flex', gap: '10px', listStyle: 'none', margin: 0, padding: 0, flexWrap: 'wrap' }}>
          {items.map((item) => (
            <li
              key={item}
              style={{
                borderRadius: '999px',
                padding: '9px 12px',
                background: 'rgba(255,255,255,0.04)',
                border: '1px solid rgba(255,255,255,0.08)',
                color: 'rgba(255,255,255,0.86)',
                fontSize: '13px',
              }}
            >
              {item}
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
