from applied.quebec_org_game.engine.ai7_auto_loop_connector import run_ai7_auto_loop


if __name__ == "__main__":
    print("--- AI7 FULL AUTO LOOP ---")

    result = run_ai7_auto_loop(
        "data/tfuga_drive",
        "applied/quebec_org_game/config/drive_dataset_config.json"
    )

    print("Graph:", result["graph_path"])
    print("Profiles:", result["profiles"])
