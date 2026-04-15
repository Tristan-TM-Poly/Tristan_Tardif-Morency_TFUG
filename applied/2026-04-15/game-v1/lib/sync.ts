export type SyncStamp = {
  sourceOfTruth: 'drive' | 'github' | 'site';
  version: string;
  updatedAt: string;
};

export type SyncBundle = {
  worldGraphVersion: string;
  registriesVersion: string;
  missionsVersion: string;
  gatesVersion: string;
  sourceOfTruth: 'drive' | 'github' | 'site';
};

export function buildSyncBundle(version: string, sourceOfTruth: 'drive' | 'github' | 'site'): SyncBundle {
  return {
    worldGraphVersion: version,
    registriesVersion: version,
    missionsVersion: version,
    gatesVersion: version,
    sourceOfTruth,
  };
}

export function isBundleAligned(a: SyncBundle, b: SyncBundle): boolean {
  return (
    a.worldGraphVersion === b.worldGraphVersion &&
    a.registriesVersion === b.registriesVersion &&
    a.missionsVersion === b.missionsVersion &&
    a.gatesVersion === b.gatesVersion
  );
}
