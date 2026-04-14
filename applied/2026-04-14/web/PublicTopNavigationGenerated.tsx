import React from 'react';

type PublicTopNavigationProps = {
  onNavigate: (route: string) => void;
};

const navItems = [
  'release',
  'life-projects',
  'demos',
  'yggdrasil',
  'ai-bots',
  'membership',
  'plans',
  'sign-in',
  'dashboard',
];

export default function PublicTopNavigationGenerated({ onNavigate }: PublicTopNavigationProps) {
  return (
    <nav>
      <ul>
        {navItems.map((item) => (
          <li key={item}>
            <button onClick={() => onNavigate(item)}>{item}</button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
