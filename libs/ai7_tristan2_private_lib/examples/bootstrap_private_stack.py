from ai7_tristan2_private_lib import (
    ActorProfile,
    ActorType,
    ArtifactRecord,
    BranchStatus,
    DrivePayload,
    DrivePointer,
    KMetaSynergyReport,
    ModuleSynergy,
    SynergyLevel,
    evaluate_promotion,
)
from ai7_tristan2_private_lib.config import SovereignConfig
from ai7_tristan2_private_lib.scoreboard_bridge import ScoreRow
from ai7_tristan2_private_lib.theory_runtime_conservation import TheoryRuntimeConservation


config = SovereignConfig()

tristan = ActorProfile(
    actor_type=ActorType.TRISTAN,
    actor_id="tristan-primary",
    display_name="Tristan",
)

artifact = ArtifactRecord(
    artifact_id="TFUGA-BOOT-001",
    title="Fractal-Loop Pilot Bootstrap",
    owner=tristan.display_name,
    source_of_truth=config.sovereign_repo,
    branch_status=BranchStatus.CRYSTALLIZABLE,
    tags=["pilot", "fractal-loop", "ai7", "tristan2"],
)

drive_payload = DrivePayload(
    pointer=DrivePointer(
        provider="google_drive",
        file_id=config.cloud_master_doc_id,
        url=f"https://docs.google.com/document/d/{config.cloud_master_doc_id}",
        mime_type="application/vnd.google-apps.document",
    ),
    metadata={"artifact_id": artifact.artifact_id, "role": "cloud-master"},
)

synergy_report = KMetaSynergyReport(
    module_name="Fractal-Loop Pilot Bootstrap",
    synergies=[
        ModuleSynergy(
            source_module="fractal-loop",
            target_module="scoreboard",
            level=SynergyLevel.K_SYNERGY,
            description="Pilot generates score rows and closure evidence",
            gain_score=8.5,
        ),
        ModuleSynergy(
            source_module="fractal-loop",
            target_module="publication-ladder",
            level=SynergyLevel.K_META_SYNERGY,
            description="Pilot can be converted into thesis/publication packets",
            gain_score=7.5,
        ),
    ],
)

conservation = TheoryRuntimeConservation(
    object_name=artifact.title,
    implementation_depth=0.58,
    theory_amplitude=0.82,
)

score_row = ScoreRow(
    artifact_id=artifact.artifact_id,
    score_total=8.4,
    branch_status=evaluate_promotion(8.4).value,
    metadata={
        "conservation_ratio": conservation.conservation_ratio(),
        "conservation_interpretation": conservation.interpretation(),
        "total_synergy_gain": synergy_report.total_gain(),
        "drive_record": drive_payload.as_record(),
    },
)

print(score_row.as_dict())
