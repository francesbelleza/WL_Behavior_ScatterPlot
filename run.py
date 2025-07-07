import pandas as pd
import numpy as np
import plotly.express as px

# 1) load & clean
df = pd.read_csv("LadderTestData.csv")
df.columns = df.columns.str.strip()

df["Run"] = df["Run"].astype(str).str.strip()
df = df[df["Run"].notna() & (df["Run"] != "") & (df["Run"].str.lower() != "nan")]

# 2) map Genotype to numeric codes
code_map = {"Saline": 0, "VIN": 1}
df["Genotype_code"] = df["Genotype"].map(code_map)

# 3) add tiny horizontal noise
df["x_jitter"] = df["Genotype_code"] + np.random.uniform(-0.15, 0.15, size=len(df))

for run_name, group in df.groupby("Run"):
    fig = px.scatter(
        group,
        x="x_jitter",
        y="Missteps Total",
        color="Genotype",
        title=f"Missteps by Genotype — Run {run_name}",
        labels={"Missteps Total": "Number of Missteps", "x_jitter": "Genotype"}
    )
    # reset ticks to categorical names
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=[0,1],
            ticktext=["Saline","VIN"]
        )
    )
    fig.update_traces(marker=dict(opacity=0.6, size=10))
    fig.show()
    fig.write_image(f"missteps_run_{run_name}.png")



