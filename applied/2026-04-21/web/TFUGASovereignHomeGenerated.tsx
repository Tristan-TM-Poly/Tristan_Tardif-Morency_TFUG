import React, { useMemo, useState } from 'react';

const domains = [
  {
    id: 'axiomatique',
    title: 'Théorie & Fondations',
    description: 'Axiomes, invariants, compression, Exp(*), noyaux de vérité.',
    children: ['Axiomes', 'Invariants', 'Compression', 'Exp(*)'],
  },
  {
    id: 'yggdrasil',
    title: 'Yggdrasil & Mycélium',
    description: 'Arbre profond, ponts transversaux, hypergraphes, propagation.',
    children: ['Branches', 'Ponts', 'Hypergraphes', 'Propagation'],
  },
  {
    id: 'ai7',
    title: 'AI-7 Métabolisme',
    description: 'Produire, vérifier, tester, analyser, optimiser, reproduire.',
    children: ['Packets', 'Runtime', 'Guides', 'Boucles'],
  },
  {
    id: 'tristan2',
    title: 'TRISTAN2 Gouvernance',
    description: 'Scorecards, review, rollback, discipline, immunité canonique.',
    children: ['Scores', 'Review', 'Rollback', 'Promotion'],
  },
  {
    id: 'labs',
    title: 'Laboratoires & Pilotes',
    description: 'Fractal-Loop, Raman, LDK, circuits, matériaux, pilots fermables.',
    children: ['Fractal-Loop', 'Raman', 'LDK', 'Pilotes'],
  },
  {
    id: 'publication',
    title: 'Drive, Docs & Publication',
    description: 'Canon, atlas, packets, ladder master-doctorat-postdoc-publication.',
    children: ['Canon', 'Atlas', 'Packets', 'Thesis Ladder'],
  },
];

const edges = [
  ['axiomatique', 'yggdrasil'],
  ['axiomatique', 'ai7'],
  ['axiomatique', 'tristan2'],
  ['yggdrasil', 'ai7'],
  ['ai7', 'tristan2'],
  ['ai7', 'labs'],
  ['tristan2', 'publication'],
  ['labs', 'publication'],
  ['yggdrasil', 'publication'],
];

function pointFor(index: number, total: number) {
  const angle = ((Math.PI * 2) / total) * index - Math.PI / 2;
  const radius = 208;
  return {
    x: 320 + Math.cos(angle) * radius,
    y: 290 + Math.sin(angle) * radius,
  };
}

export default function TFUGASovereignHomeGenerated() {
  const [selected, setSelected] = useState('axiomatique');
  const [zoom, setZoom] = useState(1);
  const [query, setQuery] = useState('');

  const filteredDomains = useMemo(() => {
    if (!query.trim()) return domains;
    const q = query.toLowerCase();
    return domains.filter(
      (domain) =>
        domain.title.toLowerCase().includes(q) ||
        domain.description.toLowerCase().includes(q) ||
        domain.children.some((child) => child.toLowerCase().includes(q)),
    );
  }, [query]);

  const selectedDomain = domains.find((domain) => domain.id === selected) || domains[0];
  const visibleSet = new Set(filteredDomains.map((domain) => domain.id));

  return (
    <section style={{ padding: '24px', background: '#05060a', color: '#f5f5f5' }}>
      <div style={{ maxWidth: '1600px', margin: '0 auto' }}>
        <div
          style={{
            border: '1px solid rgba(250, 204, 21, 0.22)',
            borderRadius: '28px',
            padding: '24px',
            background: 'radial-gradient(circle at top, rgba(245, 158, 11, 0.12), transparent 28%), radial-gradient(circle at bottom right, rgba(168, 85, 247, 0.12), transparent 26%), #080a10',
            boxShadow: '0 20px 60px rgba(0,0,0,0.35)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', gap: '24px', flexWrap: 'wrap' }}>
            <div style={{ maxWidth: '760px' }}>
              <div style={{ fontSize: '14px', letterSpacing: '0.28em', textTransform: 'uppercase', color: '#fbbf24', marginBottom: '12px' }}>
                TFUGA · Hypergraphe fractal mycélien
              </div>
              <h1 style={{ margin: 0, fontSize: '48px', lineHeight: 1.1 }}>Sovereign interactive surface</h1>
              <p style={{ marginTop: '16px', color: 'rgba(255,255,255,0.72)', lineHeight: 1.7 }}>
                Une seule racine souveraine pour le site public: TFUGA comme cœur, AI-7 comme métabolisme,
                TRISTAN2 comme filtre immunitaire, Yggdrasil comme profondeur, et les pilotes comme points de
                fermeture honnête. Le zoom augmente la densité locale et non le bruit décoratif.
              </p>
            </div>
            <div style={{ minWidth: '280px', flex: 1 }}>
              <div style={{ display: 'grid', gap: '12px' }}>
                <input
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                  placeholder="Chercher un domaine, une boucle, un packet..."
                  style={{
                    width: '100%',
                    borderRadius: '16px',
                    border: '1px solid rgba(255,255,255,0.12)',
                    background: 'rgba(255,255,255,0.04)',
                    color: 'white',
                    padding: '14px 16px',
                  }}
                />
                <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                  <button onClick={() => setZoom((value) => Math.min(1.6, Number((value + 0.1).toFixed(2))))} style={buttonPrimary}>Zoom +</button>
                  <button onClick={() => setZoom((value) => Math.max(0.8, Number((value - 0.1).toFixed(2))))} style={buttonSecondary}>Zoom -</button>
                  <button onClick={() => { setZoom(1); setQuery(''); setSelected('axiomatique'); }} style={buttonSecondary}>Reset</button>
                </div>
              </div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 360px', gap: '20px', marginTop: '24px' }}>
            <div
              style={{
                position: 'relative',
                minHeight: '700px',
                overflow: 'hidden',
                borderRadius: '28px',
                border: '1px solid rgba(255,255,255,0.08)',
                background: 'radial-gradient(circle at center, rgba(245,158,11,0.12), transparent 20%), radial-gradient(circle at 80% 20%, rgba(59,130,246,0.12), transparent 22%), radial-gradient(circle at 10% 90%, rgba(217,70,239,0.12), transparent 20%), #03050a',
              }}
            >
              <svg viewBox="0 0 640 580" style={{ width: '100%', height: '100%', transform: `scale(${zoom})`, transition: 'transform 220ms ease' }}>
                {edges.map(([source, target]) => {
                  if (!visibleSet.has(source) || !visibleSet.has(target)) return null;
                  const sIndex = domains.findIndex((domain) => domain.id === source);
                  const tIndex = domains.findIndex((domain) => domain.id === target);
                  const s = pointFor(sIndex, domains.length);
                  const t = pointFor(tIndex, domains.length);
                  return (
                    <path
                      key={`${source}-${target}`}
                      d={`M ${s.x} ${s.y} C 320 290, 320 290, ${t.x} ${t.y}`}
                      stroke="url(#flowGradient)"
                      strokeOpacity="0.5"
                      strokeWidth="2"
                      fill="none"
                    />
                  );
                })}
                <defs>
                  <linearGradient id="flowGradient" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stopColor="#f59e0b" />
                    <stop offset="50%" stopColor="#60a5fa" />
                    <stop offset="100%" stopColor="#e879f9" />
                  </linearGradient>
                </defs>
                <circle cx="320" cy="290" r="88" fill="rgba(0,0,0,0.78)" stroke="rgba(245, 158, 11, 0.65)" strokeWidth="2" />
                <circle cx="320" cy="290" r="102" fill="none" stroke="rgba(245, 158, 11, 0.22)" strokeWidth="1" />
                <text x="320" y="278" fill="#fde68a" textAnchor="middle" fontSize="20" letterSpacing="8">T</text>
                <text x="320" y="305" fill="#fef3c7" textAnchor="middle" fontSize="28">TFUGA</text>
                <text x="320" y="330" fill="rgba(255,255,255,0.62)" textAnchor="middle" fontSize="11">Cœur axiomatique</text>

                {filteredDomains.map((domain, index) => {
                  const position = pointFor(domains.findIndex((entry) => entry.id === domain.id), domains.length);
                  const isSelected = domain.id === selected;
                  return (
                    <g key={domain.id} onClick={() => setSelected(domain.id)} style={{ cursor: 'pointer' }}>
                      <circle
                        cx={position.x}
                        cy={position.y}
                        r={isSelected ? 58 : 50}
                        fill="rgba(0,0,0,0.78)"
                        stroke={isSelected ? 'rgba(255,255,255,0.75)' : 'rgba(255,255,255,0.16)'}
                        strokeWidth="2"
                      />
                      <text x={position.x} y={position.y - 3} fill="#f3f4f6" textAnchor="middle" fontSize="12">
                        {domain.title}
                      </text>
                      <text x={position.x} y={position.y + 16} fill="rgba(255,255,255,0.52)" textAnchor="middle" fontSize="10">
                        {domain.children[0]}
                      </text>
                    </g>
                  );
                })}
              </svg>
            </div>

            <aside style={{ display: 'grid', gap: '16px' }}>
              <div style={panelStyle}>
                <div style={panelLabelStyle}>Nœud sélectionné</div>
                <h3 style={{ margin: '6px 0 10px 0', fontSize: '28px' }}>{selectedDomain.title}</h3>
                <p style={{ color: 'rgba(255,255,255,0.7)', lineHeight: 1.7 }}>{selectedDomain.description}</p>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '14px' }}>
                  {selectedDomain.children.map((child) => (
                    <span key={child} style={chipStyle}>{child}</span>
                  ))}
                </div>
              </div>

              <div style={panelStyle}>
                <div style={panelLabelStyle}>Niveaux de vue</div>
                <ol style={{ margin: '12px 0 0 18px', lineHeight: 1.9, color: 'rgba(255,255,255,0.72)' }}>
                  <li>Vue globale</li>
                  <li>Domaines principaux</li>
                  <li>Sous-domaines</li>
                  <li>Modules et composants</li>
                  <li>Information locale</li>
                  <li>Complexité mycélienne</li>
                </ol>
              </div>

              <div style={panelStyle}>
                <div style={panelLabelStyle}>Métriques globales</div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: '12px' }}>
                  {[
                    ['Nœuds', '∞'],
                    ['Connexions', '∞'],
                    ['Packets', 'Actifs'],
                    ['Canon', 'Vivant'],
                    ['Scorecards', 'Visibles'],
                    ['Zoom', `${zoom.toFixed(2)}x`],
                  ].map(([label, value]) => (
                    <div key={label} style={{ borderRadius: '16px', padding: '12px', background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.06)' }}>
                      <div style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: 'rgba(255,255,255,0.4)' }}>{label}</div>
                      <div style={{ marginTop: '6px', color: '#fde68a', fontWeight: 600 }}>{value}</div>
                    </div>
                  ))}
                </div>
              </div>
            </aside>
          </div>
        </div>
      </div>
    </section>
  );
}

const panelStyle: React.CSSProperties = {
  borderRadius: '24px',
  padding: '18px',
  border: '1px solid rgba(255,255,255,0.08)',
  background: 'rgba(255,255,255,0.03)',
};

const panelLabelStyle: React.CSSProperties = {
  fontSize: '11px',
  textTransform: 'uppercase',
  letterSpacing: '0.18em',
  color: '#fbbf24',
};

const chipStyle: React.CSSProperties = {
  borderRadius: '999px',
  padding: '8px 12px',
  background: 'rgba(245, 158, 11, 0.12)',
  border: '1px solid rgba(245, 158, 11, 0.16)',
  color: '#fde68a',
  fontSize: '12px',
};

const buttonPrimary: React.CSSProperties = {
  borderRadius: '14px',
  border: '1px solid rgba(245, 158, 11, 0.25)',
  background: 'rgba(245, 158, 11, 0.16)',
  color: '#fde68a',
  padding: '12px 16px',
  cursor: 'pointer',
};

const buttonSecondary: React.CSSProperties = {
  borderRadius: '14px',
  border: '1px solid rgba(255,255,255,0.12)',
  background: 'rgba(255,255,255,0.04)',
  color: 'white',
  padding: '12px 16px',
  cursor: 'pointer',
};
