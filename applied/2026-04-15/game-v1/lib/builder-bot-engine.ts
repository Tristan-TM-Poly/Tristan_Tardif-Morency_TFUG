export type BuilderBot = {
  id: string;
  name: string;
  builderType: string;
  domain: string;
  buildTargets: string[];
  stabilityWeight: number;
  integrationBias: number;
  linkedMissionIds: string[];
  linkedNodeIds: string[];
  linkedTripletIds: string[];
};

export type BuildPlan = {
  id: string;
  sourceBotId: string;
  targetKind: string;
  title: string;
  stability: number;
  integration: number;
  linkedMissionIds: string[];
  linkedNodeIds: string[];
};

export function createBuildPlan(bot: BuilderBot, missionId: string, index: number): BuildPlan {
  return {
    id: `${bot.id}-plan-${index}`,
    sourceBotId: bot.id,
    targetKind: bot.buildTargets[index % bot.buildTargets.length] ?? 'build-target',
    title: `${bot.name} plan ${index}`,
    stability: Math.min(0.99, bot.stabilityWeight),
    integration: Math.min(0.99, bot.integrationBias),
    linkedMissionIds: [missionId],
    linkedNodeIds: bot.linkedNodeIds,
  };
}

export function planToSummary(plan: BuildPlan): string {
  return `${plan.title} assembles ${plan.targetKind} with stability ${plan.stability.toFixed(2)} and integration ${plan.integration.toFixed(2)}.`;
}
