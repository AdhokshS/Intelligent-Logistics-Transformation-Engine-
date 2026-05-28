def generate_insights(df):
    insights = []

    for region in df["region"].unique():
        region_data = df[df["region"] == region]

        avg_latency = region_data["latency"].mean()
        avg_error = region_data["error_rate"].mean()
        avg_adoption = region_data["adoption_rate"].mean()
        avg_delay = region_data["workflow_delay"].mean()
        avg_override = region_data["manual_override_rate"].mean()

        def impact_score():
            return round(
                avg_delay * 0.4 +
                avg_error * 5 +
                (100 - avg_adoption) * 0.6 +
                avg_override * 0.5,
                2
            )

        if avg_delay > 25 and avg_adoption < 65:
            insights.append({
                "region": region,
                "issue": "High workflow delays with low adoption",
                "root_cause": "Usability issues or lack of training",
                "recommendation": "Improve UX and conduct user training",
                "business_impact": "Delivery delays and customer dissatisfaction",
                "impact_score": impact_score()
            })

        if avg_error > 5:
            insights.append({
                "region": region,
                "issue": "High error rates",
                "root_cause": "System integration issues",
                "recommendation": "Improve system integration",
                "business_impact": "Order failures and rework cost",
                "impact_score": impact_score()
            })

        if avg_override > 10:
            insights.append({
                "region": region,
                "issue": "High manual overrides",
                "root_cause": "Workflow inefficiency or lack of trust",
                "recommendation": "Improve automation",
                "business_impact": "Process inconsistency and audit risk",
                "impact_score": impact_score()
            })

    insights = sorted(insights, key=lambda x: x["impact_score"], reverse=True)
    return insights