import React, { useMemo, useState } from 'react';

const quests = [
  {
    id: 'quest-ygg',
    title: 'Cartographe Yggdrasil',
    level: 'Niveau 1',
    type: 'Exploration',
    objective: 'Repérer les branches fertiles et les ponts mycéliens.',
    reward: 'Carte de nœuds + badge de cartographie',
  },
  {
    id: 'quest-packets',
    title: 'Forgeron de Packets',
    level: 'Niveau 2',
    type: 'Système',
    objective: 'Assembler Packet, ScoreRow, ReviewDecision et RollbackPointer.',
    reward: 'Paquet canonisable + route de promotion',
  },
  {
    id: 'quest-fractal-loop',
    title: 'Pilote Fractal-Loop',
    level: 'Niveau 3',
    type: 'Pilotage',
    objective: 'Fermer honnêtement un pilote et mesurer le gain réel.',
    reward: 'Score de fermeture + ouverture du hub LDK',
  },
  {
    id: 'quest-raman',
    title: 'Spectre Raman',
    level: 'Niveau 4',
    type: 'Science',
    objective: 'Relier signal, aire sous la courbe et preuve documentaire.',
    reward: 'Fragment de canon scientifique',
  },
  {
    id: 'quest-governance',
    title: 'Tribunal TRISTAN2',
    level: 'Niveau 5',
    type: 'Gouvernance',
    objective: 'Choisir promouvoir, geler, rollback ou détruire.',
    reward: 'Immunité canonique et scorecard débloquée',
  },
];

const npcGuides = [
  'Guide conceptuel',
  'Guide système',
  'Guide expérience',
  'Guide review',
  'Guide collaboration',
];

export default function TFUGAEduGameHubGenerated() {
  const [selectedQuest, setSelectedQuest] = useState(quests[0].id);
  const [difficulty, setDifficulty] = useState('borné');
  const [mode, setMode] = useState('solo');

  const quest = useMemo(() => quests.find((entry) => entry.id === selectedQuest) || quests[0], [selectedQuest]);

  return (
    <section style={{ padding: '24px 0' }}>
      <div
        style={{
          borderRadius: '28px',
          border: '1px solid rgba(255,255,255,0.08)',
          background: 'linear-gradient(180deg, rgba(12,18,32,0.92), rgba(8,10,16,0.98))',
          padding: '24px',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px', flexWrap: 'wrap' }}>
          <div style={{ maxWidth: '760px' }}>
            <div style={{ color: '#fbbf24', fontSize: '12px', letterSpacing: '0.22em', textTransform: 'uppercase' }}>
              TFUGA · Educational game corridor
            </div>
            <h2 style={{ margin: '10px 0 0 0', fontSize: '34px' }}>Jeux vidéo éducatifs gouvernés</h2>
            <p style={{ color: 'rgba(255,255,255,0.72)', lineHeight: 1.7, marginTop: '12px' }}>
              Ici, l’interactivité n’est pas décorative. Chaque boucle de jeu sert à apprendre une structure,
              mesurer un gain réel, naviguer dans Yggdrasil, ou faire passer un objet par la chaîne
              packet → score → review → promotion ou rollback.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', alignItems: 'start' }}>
            {['solo', 'collaboration', 'runtime-lab'].map((entry) => (
              <button
                key={entry}
                onClick={() => setMode(entry)}
                style={{
                  borderRadius: '999px',
                  border: mode === entry ? '1px solid rgba(250,204,21,0.32)' : '1px solid rgba(255,255,255,0.12)',
                  background: mode === entry ? 'rgba(245,158,11,0.16)' : 'rgba(255,255,255,0.04)',
                  color: mode === entry ? '#fde68a' : 'white',
                  padding: '10px 14px',
                  cursor: 'pointer',
                }}
              >
                {entry}
              </button>
            ))}
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '340px minmax(0, 1fr) 280px', gap: '18px', marginTop: '24px' }}>
          <div style={panelStyle}>
            <div style={panelTitleStyle}>Quêtes disponibles</div>
            <div style={{ display: 'grid', gap: '10px', marginTop: '14px' }}>
              {quests.map((entry) => (
                <button
                  key={entry.id}
                  onClick={() => setSelectedQuest(entry.id)}
                  style={{
                    textAlign: 'left',
                    borderRadius: '18px',
                    padding: '14px',
                    border: selectedQuest === entry.id ? '1px solid rgba(250,204,21,0.26)' : '1px solid rgba(255,255,255,0.08)',
                    background: selectedQuest === entry.id ? 'rgba(245,158,11,0.12)' : 'rgba(255,255,255,0.03)',
                    color: 'white',
                    cursor: 'pointer',
                  }}
                >
                  <div style={{ fontSize: '12px', color: '#fbbf24', textTransform: 'uppercase', letterSpacing: '0.12em' }}>{entry.level}</div>
                  <div style={{ fontSize: '18px', fontWeight: 600, marginTop: '6px' }}>{entry.title}</div>
                  <div style={{ marginTop: '4px', color: 'rgba(255,255,255,0.6)', fontSize: '14px' }}>{entry.type}</div>
                </button>
              ))}
            </div>
          </div>

          <div style={panelStyle}>
            <div style={panelTitleStyle}>Mission active</div>
            <h3 style={{ margin: '12px 0 8px 0', fontSize: '28px' }}>{quest.title}</h3>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '16px' }}>
              <span style={chipStyle}>{quest.level}</span>
              <span style={chipStyle}>{quest.type}</span>
              <span style={chipStyle}>Mode: {mode}</span>
              <span style={chipStyle}>Difficulté: {difficulty}</span>
            </div>
            <p style={{ color: 'rgba(255,255,255,0.76)', lineHeight: 1.7 }}>
              <strong>Objectif:</strong> {quest.objective}
            </p>
            <p style={{ color: 'rgba(255,255,255,0.76)', lineHeight: 1.7 }}>
              <strong>Récompense:</strong> {quest.reward}
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginTop: '18px' }}>
              {[
                ['Packets visibles', 'Oui'],
                ['Scorecards', 'Oui'],
                ['Rollback', 'Toujours'],
                ['TRISTAN2 Gate', 'Active'],
              ].map(([label, value]) => (
                <div key={label} style={{ borderRadius: '18px', padding: '12px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                  <div style={{ color: 'rgba(255,255,255,0.44)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.12em' }}>{label}</div>
                  <div style={{ color: '#fde68a', fontWeight: 600, marginTop: '6px' }}>{value}</div>
                </div>
              ))}
            </div>

            <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginTop: '18px' }}>
              <button style={primaryButton}>Lancer mission</button>
              <button style={secondaryButton}>Inspecter packet</button>
              <button style={secondaryButton}>Voir scorecard</button>
              <button style={secondaryButton}>Ouvrir review gate</button>
            </div>
          </div>

          <div style={panelStyle}>
            <div style={panelTitleStyle}>Guides IA-BOT</div>
            <div style={{ display: 'grid', gap: '10px', marginTop: '14px' }}>
              {npcGuides.map((guide) => (
                <div key={guide} style={{ borderRadius: '16px', padding: '12px', background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.06)' }}>
                  {guide}
                </div>
              ))}
            </div>
            <div style={{ marginTop: '18px' }}>
              <div style={panelTitleStyle}>Difficulté</div>
              <div style={{ display: 'grid', gap: '8px', marginTop: '10px' }}>
                {['borné', 'canonique', 'hard'].map((entry) => (
                  <button
                    key={entry}
                    onClick={() => setDifficulty(entry)}
                    style={{
                      borderRadius: '14px',
                      border: difficulty === entry ? '1px solid rgba(250,204,21,0.3)' : '1px solid rgba(255,255,255,0.08)',
                      background: difficulty === entry ? 'rgba(245,158,11,0.16)' : 'rgba(255,255,255,0.03)',
                      color: difficulty === entry ? '#fde68a' : 'white',
                      padding: '10px 12px',
                      cursor: 'pointer',
                    }}
                  >
                    {entry}
                  </button>
                ))}
              </div>
            </div>
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
  background: 'rgba(255,255,255,0.02)',
};

const panelTitleStyle: React.CSSProperties = {
  color: '#fbbf24',
  fontSize: '11px',
  textTransform: 'uppercase',
  letterSpacing: '0.18em',
};

const chipStyle: React.CSSProperties = {
  borderRadius: '999px',
  padding: '8px 12px',
  background: 'rgba(99,102,241,0.14)',
  border: '1px solid rgba(99,102,241,0.18)',
  fontSize: '12px',
  color: '#e5e7eb',
};

const primaryButton: React.CSSProperties = {
  borderRadius: '14px',
  border: '1px solid rgba(245,158,11,0.28)',
  background: 'rgba(245,158,11,0.16)',
  color: '#fde68a',
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
