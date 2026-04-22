# TFUGA Deployment Status

## Current state
- Root landing page present at repository root
- `vercel.json` present with rewrites for `/current`, `/publication`, `/portal`, `/app`
- Current checkpoint page published
- Publication page published
- True interactive portal page published
- Contracts/revenue app page published
- GitHub Action validates the web surfaces on push to `main`

## What is now handled in-repo
- root entry
- route rewrites
- web surface presence validation
- publication index layer

## Remaining external step
The remaining likely blocker is the Vercel project deployment state. If the site still shows 404, redeploy the project and verify:
- production branch = `main`
- root directory = repository root
- latest commit includes `index.html` and `vercel.json`

## Commit landmarks
- Vercel rewrites added
- web automation workflow added
- unified root landing page added
