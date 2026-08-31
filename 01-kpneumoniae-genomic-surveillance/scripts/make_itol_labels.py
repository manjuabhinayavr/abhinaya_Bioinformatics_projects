import pandas as pd

strain_names = {
    "GCA_055721705.1": "KK22", "GCA_055721685.1": "KK33", "GCA_055721665.1": "KK35",
    "GCA_055721645.1": "KK45", "GCA_055721625.1": "KK47", "GCA_055721605.1": "KK50",
    "GCA_055721585.1": "KK53", "GCA_055721565.1": "KK54", "GCA_055721545.1": "KK55",
    "GCA_055721525.1": "KK66", "GCA_053309215.1": "KP1", "GCA_053309195.1": "KP2",
    "GCA_053309175.1": "KP3", "GCA_053309155.1": "KP4", "GCA_054952645.1": "SDS-K5",
    "GCA_054952405.1": "SDS-K9", "GCA_054952445.1": "SDS-K20", "GCA_060056565.1": "C8092",
    "GCA_060056645.1": "C2155", "GCA_055485485.1": "ST11-22-90", "GCA_055485515.1": "ST11-16-116",
}

df = pd.read_csv("results/integration_output/master_summary.csv")

with open("results/integration_output/itol_labels.txt", "w") as f:
    f.write("LABELS\\n")
    f.write("SEPARATOR TAB\\n")
    f.write("DATA\\n")
    for _, row in df.iterrows():
        acc = row["accession"]
        st = row["ST"]
        strain = strain_names.get(acc, acc)
        new_label = f"{st}_{strain}"
        f.write(f"{acc}\\t{new_label}\\n")

print("iTOL label file created with real strain names")
