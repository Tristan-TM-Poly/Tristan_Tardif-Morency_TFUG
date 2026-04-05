from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SovereignConfig:
    library_name: str = "ai7_tristan2_private_lib"
    privacy_scope: str = "private"
    sovereign_repo: str = "Tristan-TM-Poly/Tristan_Tardif-Morency_TFUG"
    default_scoreboard_spreadsheet_id: str = "19HTHbKfrBQUWvTWZ3R7l7ISXT94WGOqksDFGgfC4Rt8"
    closure_doc_id: str = "1wdY6XZvcTKB4Q8lNxtVE2D7KyjQRmCpMFwccKoKDE8s"
    cloud_master_doc_id: str = "1KPk64wMm5WjsIysWT7UNMVp5I33vD9rDDeaUiHIVY5Y"
