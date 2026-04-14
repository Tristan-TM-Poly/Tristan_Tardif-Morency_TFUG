import React, { useState } from 'react';
import PublicReleaseHubGenerated from './PublicReleaseHubGenerated';
import LifeProjectsPageGenerated from './LifeProjectsPageGenerated';
import PublicDemosPageGenerated from './PublicDemosPageGenerated';
import PublicCollaborationsPageGenerated from './PublicCollaborationsPageGenerated';
import PublicYggdrasilPageGenerated from './PublicYggdrasilPageGenerated';
import AIBotsPageGenerated from './AIBotsPageGenerated';
import MembershipDonationPortalGenerated from './MembershipDonationPortalGenerated';
import SignInPageGenerated from './SignInPageGenerated';
import SignUpPageGenerated from './SignUpPageGenerated';
import MemberAdminDashboardShellGenerated from './MemberAdminDashboardShellGenerated';
import PlansPricingPageGenerated from './PlansPricingPageGenerated';
import PublicTopNavigationGenerated from './PublicTopNavigationGenerated';

const routes = [
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
] as const;

type Route = typeof routes[number];

export default function PublicAppRouterGeneratedV3() {
  const [route, setRoute] = useState<Route>('release');

  const renderRoute = () => {
    switch (route) {
      case 'life-projects':
        return <LifeProjectsPageGenerated />;
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
      case 'release':
      default:
        return <PublicReleaseHubGenerated />;
    }
  };

  return (
    <main>
      <PublicTopNavigationGenerated onNavigate={(item) => setRoute(item as Route)} />
      {renderRoute()}
    </main>
  );
}
