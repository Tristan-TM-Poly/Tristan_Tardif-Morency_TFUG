import React from 'react';
import PublicInteractiveNavigationGenerated from './PublicInteractiveNavigationGenerated';
import AI7HubPublicSurfaceGenerated from './AI7HubPublicSurfaceGenerated';
import YggdrasilNodeExplorerGenerated from './YggdrasilNodeExplorerGenerated';
import AIBotNPCGuidePanelGenerated from './AIBotNPCGuidePanelGenerated';

export default function PublicSystemShellGenerated() {
  return (
    <main>
      <PublicInteractiveNavigationGenerated />

      <section>
        <h1>Public System Shell</h1>
        <p>
          A bounded shell joining navigation, AI-7 public metabolism, Yggdrasil exploration,
          and AI-BOT guidance into one public-interactive surface.
        </p>
      </section>

      <AI7HubPublicSurfaceGenerated />
      <YggdrasilNodeExplorerGenerated />
      <AIBotNPCGuidePanelGenerated />
    </main>
  );
}
