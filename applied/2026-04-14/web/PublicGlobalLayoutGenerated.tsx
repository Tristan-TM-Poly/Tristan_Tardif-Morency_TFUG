import React from 'react';

type PublicGlobalLayoutProps = {
  title: string;
  subtitle: string;
  children: React.ReactNode;
};

export default function PublicGlobalLayoutGenerated({ title, subtitle, children }: PublicGlobalLayoutProps) {
  return (
    <main>
      <header>
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </header>
      <section>{children}</section>
      <footer>
        <p>TFUGA x AI-7 x TRISTAN2 public application layer</p>
      </footer>
    </main>
  );
}
