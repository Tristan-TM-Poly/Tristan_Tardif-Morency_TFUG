# PRINCIPE_MOINDRE_ACTION_FRACTALE_MYCELIENNE — Applied Note (2026-04-14)

## Objet
Fixer une première forme appliquée du principe de moindre action fractale mycélienne comme bloc canonique TFUGA-compatible.

## Forme canonique compacte
\[
\delta \int
\Big[
\sum_i \frac{m_i}{2}(D_t^\alpha \phi_i)^2
- \sum_i U_i(\phi_i)
- \sum_{(i,j)\in E}\frac{k_{ij}}{2}(\phi_i-\phi_j)^2
- \sum_{\gamma\in\mathcal M}\Lambda_\gamma \Omega_\gamma(\phi)
+ \mu\,\mathcal F(\phi)
\Big]dt
=0
\]

## Lecture
- terme local: dynamique propre de chaque noeud
- terme branch: transport et couplage entre noeuds relies
- terme mycelial/hypergraphique: recouplages de plus haut ordre
- terme de memoire fractale: derivee fractionnaire ou operateur memoriel
- terme de fertilite: capacite du systeme a engendrer des structures utiles et coherentes

## Cas Y minimal
On considere un coeur 0 et trois branches 1,2,3.
\[
S[\phi]
=
\int
\left[
\sum_{i=0}^{3} \frac{m_i}{2}\dot{\phi}_i^2
-
\sum_{i=0}^{3} \frac{\omega_i^2}{2}\phi_i^2
-
\sum_{a=1}^{3} \frac{k_a}{2}(\phi_a-\phi_0)^2
-
\frac{\lambda}{2}\sum_{1\le a<b\le 3}(\phi_a-\phi_b)^2
\right]dt.
\]

Les equations d'Euler-Lagrange associees deviennent
\[
m_0\ddot{\phi}_0+\omega_0^2\phi_0+\sum_{a=1}^{3}k_a(\phi_0-\phi_a)=0,
\]
\[
m_a\ddot{\phi}_a+\omega_a^2\phi_a+k_a(\phi_a-\phi_0)+\lambda\sum_{b\neq a}(\phi_a-\phi_b)=0.
\]

## Interpretation TFUGA
- le coeur 0 represente le tronc ou noyau canonique
- les branches representent theories, applications ou pilotes
- k regle l'ancrage tronc-branche
- lambda regle le recouplage transversal mycelien
- la memoire fractale encode l'historique documentaire, theorique ou experimental

## Decision de statut
- stable: forme canonique compacte et lecture organique
- crystallizable: equations variationnelles generalisees et note paper-ready
- exploratory: theorie complete sur hypergraphes arbitraires et preuves generales

## Loi
Le systeme ne choisit pas seulement le chemin localement le plus court. Il choisit la structure de propagation memorielle et ramifiee qui rend stationnaire le compromis entre cout local, transport, coherence mycelienne et fertilite generative.
