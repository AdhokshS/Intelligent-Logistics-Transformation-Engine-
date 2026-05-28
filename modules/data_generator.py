import pandas as pd
import numpy as np

def generate_data(rows=100):
    systems = ["CRM", "Ticketing", "Tracking"]
    regions = ["West", "East", "Central", "South"]

    data = []

    for _ in range(rows):
        system = np.random.choice(systems)
        region = np.random.choice(regions)

        # Base values
        latency = np.random.randint(100, 300)
        error = round(np.random.uniform(2, 6), 2)
        adoption = np.random.randint(60, 85)
        delay = np.random.randint(10, 30)
        override = np.random.randint(3, 10)
        downtime = np.random.randint(1, 6)

        # Inject real-world problem pattern (East region = worst)
        if region == "East":
            latency += 80
            error += 2
            adoption -= 15
            delay += 15
            override += 8
            downtime += 4

        data.append([
            system, region, latency, error, adoption,
            delay, override, downtime
        ])

    df = pd.DataFrame(data, columns=[
        "system_name", "region", "latency", "error_rate",
        "adoption_rate", "workflow_delay",
        "manual_override_rate", "system_downtime"
    ])

    return df