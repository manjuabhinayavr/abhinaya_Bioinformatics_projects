import pandas as pd
import os
import glob

kleborate_path = "results/kleborate_output/kleborate_results.txt/klebsiella_pneumo_complex_output.txt"
kleborate_df = pd.read_csv(kleborate_path, sep="\t")

kleborate_df["accession"] = kleborate_df["strain"].str.extract(r"(GCA_\d+\.\d+)")

rename_map = {
    "enterobacterales__species__species": "species",
    "klebsiella_pneumo_complex__mlst__ST": "ST",
    "klebsiella_pneumo_complex__virulence_score__virulence_score": "virulence_score",
    "klebsiella_pneumo_complex__resistance_score__resistance_score": "resistance_score",
    "klebsiella_pneumo_complex__resistance_class_count__num_resistance_classes": "num_resistance_classes",
    "klebsiella_pneumo_complex__resistance_gene_count__num_resistance_genes": "num_resistance_genes",
}
kleborate_df = kleborate_df.rename(columns=rename_map)

mobsuite_dir = "results/mobsuite_output"
plasmid_counts = []

for accession_dir in glob.glob(f"{mobsuite_dir}/*/"):
    accession = os.path.basename(os.path.normpath(accession_dir))
    contig_report = os.path.join(accession_dir, "contig_report.txt")
    num_plasmids = 0
    if os.path.exists(contig_report):
        df = pd.read_csv(contig_report, sep="\t")
        if "molecule_type" in df.columns:
            plasmid_rows = df[df["molecule_type"] == "plasmid"]
            num_plasmids = plasmid_rows["primary_cluster_id"].nunique() if "primary_cluster_id" in df.columns else len(plasmid_rows)
    plasmid_counts.append({"accession": accession, "num_plasmids": num_plasmids})

plasmid_df = pd.DataFrame(plasmid_counts)

master_df = kleborate_df.merge(plasmid_df, on="accession", how="left")

summary_cols = ["accession", "species", "ST", "virulence_score", "resistance_score", "num_resistance_classes", "num_resistance_genes", "num_plasmids"]
summary_df = master_df[[c for c in summary_cols if c in master_df.columns]]

summary_df = summary_df.sort_values("ST")

os.makedirs("results/integration_output", exist_ok=True)
summary_df.to_csv("results/integration_output/master_summary.csv", index=False)

print("Master summary table saved to results/integration_output/master_summary.csv")
print(summary_df.to_string(index=False))
