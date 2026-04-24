from applied.quebec_org_game.engine.hgfm_auto_loop import run_full_auto_loop


if __name__ == "__main__":
    print("--- FULL AUTO LOOP ---")

    graph_path = run_full_auto_loop(
        "data/tfuga_drive",
        "applied/quebec_org_game/config/drive_dataset_config.json"
    )

    print("Graph generated at:", graph_path)
