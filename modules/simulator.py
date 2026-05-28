def simulate_improvement(df, action):
    df_sim = df.copy()

    if action == "Improve Adoption":
        df_sim["adoption_rate"] += 12
        df_sim["workflow_delay"] -= 6
        df_sim["manual_override_rate"] -= 3

    elif action == "Reduce Latency":
        df_sim["latency"] -= 70
        df_sim["workflow_delay"] -= 4
        df_sim["system_downtime"] -= 2

    elif action == "Reduce Errors":
        df_sim["error_rate"] -= 2.5
        df_sim["workflow_delay"] -= 2
        df_sim["manual_override_rate"] -= 2

    numeric_cols = df_sim.select_dtypes(include=["number"]).columns
    df_sim[numeric_cols] = df_sim[numeric_cols].clip(lower=0)

    return df_sim