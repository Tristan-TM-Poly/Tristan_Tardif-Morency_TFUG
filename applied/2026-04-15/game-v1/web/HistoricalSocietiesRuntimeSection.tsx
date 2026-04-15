import React from 'react';
import HistoricalSocietiesExplorerPanel from './HistoricalSocietiesExplorerPanel';
import SocietyReviewGate from './SocietyReviewGate';
import PublicSummaryCard from './PublicSummaryCard';
import ComparativeCivilizationsMap from './ComparativeCivilizationsMap';
import { historicalSocietiesActionCards, historicalSocietiesSample } from './historical-societies-sample';

export default function HistoricalSocietiesRuntimeSection() {
  const activeSociety = historicalSocietiesSample[0];
  const activeSocietyCards = historicalSocietiesActionCards.filter((card) => card.society_id === activeSociety.id);

  return (
    <section className="space-y-6">
      <HistoricalSocietiesExplorerPanel
        societies={historicalSocietiesSample}
        actionCards={historicalSocietiesActionCards}
      />

      <section className="grid gap-6 xl:grid-cols-2">
        <SocietyReviewGate society={activeSociety} actionCards={activeSocietyCards} />
        <PublicSummaryCard society={activeSociety} actionCards={activeSocietyCards} />
      </section>

      <ComparativeCivilizationsMap
        societies={historicalSocietiesSample}
        actionCards={historicalSocietiesActionCards}
      />
    </section>
  );
}
