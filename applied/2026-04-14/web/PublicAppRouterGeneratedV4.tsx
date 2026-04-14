import React, { useState } from 'react';
import PremiumHomePageGenerated from './PremiumHomePageGenerated';
import PublicReleaseHubGenerated from './PublicReleaseHubGenerated';
import LifeProjectsPageGeneratedV2 from './LifeProjectsPageGeneratedV2';
import PublicDemosPageGenerated from './PublicDemosPageGenerated';
import PublicCollaborationsPageGenerated from './PublicCollaborationsPageGenerated';
import PublicYggdrasilPageGenerated from './PublicYggdrasilPageGenerated';
import AIBotsPageGenerated from './AIBotsPageGenerated';
import MembershipDonationPortalGenerated from './MembershipDonationPortalGenerated';
import SignInPageGenerated from './SignInPageGenerated';
import SignUpPageGenerated from './SignUpPageGenerated';
import MemberAdminDashboardShellGenerated from './MemberAdminDashboardShellGenerated';
import PlansPricingPageGenerated from './PlansPricingPageGenerated';
import DeploymentChecklistPageGenerated from './DeploymentChecklistPageGenerated';
import PublicTopNavigationGenerated from './PublicTopNavigationGenerated';

const routes = [
  'home',
  'release',
  'life-projects',
  'demos',
  'collaborations',
  'yggdrasil',
  'ai-bots',
  'membership',
  'plans',
  'sign-in',
  'sign-up',
  'dashboard',
  'deployment',
] as const;

type Route = typeof routes[number];

export default function PublicAppRouterGeneratedV4() {
  const [route, setRoute] = useState<Route>('home');

  const renderRoute = () => {
    switch (route) {
      case 'release':
        return <PublicReleaseHubGenerated />;
      case 'life-projects':
        return <LifeProjectsPageGeneratedV2 />;
      case 'demos':
        return <PublicDemosPageGenerated />;
      case 'collaborations':
        return <PublicCollaborationsPageGenerated />;
      case 'yggdrasil':
        return <PublicYggdrasilPageGenerated />;
      case 'ai-bots':
        return <AIBotsPageGenerated />;
      case 'membership':
        return <MembershipDonationPortalGenerated />;
      case 'plans':
        return <PlansPricingPageGenerated />;
      case 'sign-in':
        return <SignInPageGenerated />;
      case 'sign-up':
        return <SignUpPageGenerated />;
      case 'dashboard':
        return <MemberAdminDashboardShellGenerated />;
      case 'deployment':
        return <DeploymentChecklistPageGenerated />;
      case 'home':
      default:
        return <PremiumHomePageGenerated />;
    }
  };

  return (
    <main>
      <PublicTopNavigationGenerated onNavigate={(item) => setRoute(item as Route)} />
      {renderRoute()}
    </main>
  );
}
