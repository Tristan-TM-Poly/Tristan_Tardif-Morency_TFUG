import React from 'react';
import FractalLoopVisualizerGenerated from './FractalLoopVisualizerGenerated';
import BoundedLDKVisualizerGenerated from './BoundedLDKVisualizerGenerated';

export default function PublicDemosPageGenerated() {
  return (
    <main>
      <section>
        <h1>Public Demos</h1>
        <p>
          Explore bounded demos coupled to TFUGA objects, AI-7 interaction loops,
          and TRISTAN2 review and scoring layers.
        </p>
      </section>

      <FractalLoopVisualizerGenerated />
      <BoundedLDKVisualizerGenerated />

      <section>
        <h2>Next demo targets</h2>
        <ul>
          <li>Raman Observability Preview</li>
          <li>TFUGA Trinity Hub</li>
          <li>AT-1 Demo Gateway</li>
        </ul>
      </section>
    </main>
  );
}
