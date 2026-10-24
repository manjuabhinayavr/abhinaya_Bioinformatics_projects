# K. pneumoniae Genomic Surveillance Project

## Complete Command Log (Phases 1-9) — Successful Steps Only

**Research question:** Among a curated set of publicly available K. pneumoniae genomes, to what extent do antimicrobial resistance and virulence determinants co-occur within the same lineages, and what role do plasmids play in that convergence?

**Dataset:** 21 complete-genome K. pneumoniae accessions from 5 BioProjects (Turkiye CRKP study, Turkiye small study, Pune India, Peking China, ST11 hospital study). 

\---

## Phase 1 — Environment Setup

```bash
# Verify environment
lsb\_release -a
python3 --version
git --version
```

**Result:** Ubuntu 24.04.4 LTS, Python 3.12.1, Git 2.53.0

```bash
# Create project folder structure
mkdir -p 01-kpneumoniae-genomic-surveillance/{data,scripts,results,figures,docs}
cd 01-kpneumoniae-genomic-surveillance
```

```bash
# Install Biopython
pip install biopython
python3 -c "import Bio; print(Bio.\_\_version\_\_)"
```

**Result:** Biopython 1.88

```bash
# Record dependency
echo "biopython==1.88" > requirements.txt
```

```bash
# Commit and push
git add -A
git commit -m "Phase 1: environment setup"
git push
```

\---

## Phase 2 — Dataset Selection

Genomes identified via NCBI Assembly/BioProject search (Complete Genome level, human clinical isolates only). Full selection process and final accession list documented in `docs/Phase2\_Final\_Dataset.md`.

\---

## Phase 3 — Genome QC \& Annotation

```bash
# Install NCBI datasets tool
curl -o datasets 'https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/v2/linux-amd64/datasets'
chmod +x datasets
```

```bash
# Download all 21 genomes
cd 01-kpneumoniae-genomic-surveillance/data
../../datasets download genome accession \\
  GCA\_055721705.1 GCA\_055721685.1 GCA\_055721665.1 GCA\_055721645.1 \\
  GCA\_055721625.1 GCA\_055721605.1 GCA\_055721585.1 GCA\_055721565.1 \\
  GCA\_055721545.1 GCA\_055721525.1 GCA\_053309215.1 GCA\_053309195.1 \\
  GCA\_053309175.1 GCA\_053309155.1 GCA\_054952645.1 GCA\_054952405.1 \\
  GCA\_054952445.1 GCA\_060056565.1 GCA\_060056645.1 GCA\_055485485.1 \\
  GCA\_055485515.1 --include genome
unzip ncbi\_dataset.zip
rm ncbi\_dataset.zip
```

**Result:** 21 genome FASTA (.fna) files, \~117MB total

```bash
# Install and run QUAST (genome quality check)
pip install quast
cd ..
quast.py data/ncbi\_dataset/data/\*/\*.fna -o results/quast\_report
```

**Result:** All 21 genomes passed QC — L50=1 for every genome (single-contig), genome sizes 5.49M-6.14M bp, GC content 56.5-57.2%, near-zero ambiguous bases.

```bash
# Install Prokka (via conda)
conda create -n prokka\_env -c conda-forge -c bioconda prokka -y
conda init
exec bash
conda activate prokka\_env
prokka --version
```

**Result:** Prokka 1.15.6

```bash
# Run Prokka annotation on all 21 genomes
mkdir -p results/prokka\_annotations
for genome in data/ncbi\_dataset/data/\*/\*.fna; do
    accession=$(basename $(dirname "$genome"))
    prokka --outdir results/prokka\_annotations/$accession --prefix $accession \\
      --kingdom Bacteria --genus Klebsiella --species pneumoniae \\
      --cpus 2 --force "$genome"
done
```

**Result:** All 21 genomes annotated. Gene counts ranged 5,100-5,849 per genome.

```bash
# Commit and push
cd /workspaces/abhinaya\_Bioinformatics\_projects
git add -A
git commit -m "Phase 3: Prokka annotation complete for all 21 genomes"
git push
```

\---

## Phase 4 — AMR Analysis (Kleborate)

```bash
# Install Kleborate
pip install kleborate pandas
conda activate kleborate\_env
kleborate --version
```

**Result:** Kleborate v3.2.4

```bash
# Run Kleborate on all 21 genomes
cd 01-kpneumoniae-genomic-surveillance
mkdir -p results/kleborate\_output
kleborate -a data/ncbi\_dataset/data/\*/\*.fna -o results/kleborate\_output/kleborate\_results.txt -p kpsc
```

**Result — 21 genomes span 11 distinct Sequence Types:**

|ST|Count|Notes|
|-|-|-|
|ST2096|4|High virulence AND high resistance (convergence)|
|ST11|4|Globally significant carbapenem-resistant clone; convergence|
|ST307|2||
|ST101|2||
|ST23|1|Virulence score 5 (highest), 0 resistance genes — pure hypervirulence|
|ST15, ST420, ST985, ST16, ST14, ST147, ST1418|1 each||

```bash
# Commit and push
cd /workspaces/abhinaya\_Bioinformatics\_projects
git add -A
git commit -m "Phase 4: Kleborate AMR/virulence/ST analysis complete for all 21 genomes"
git push
```

\---

## Phase 5 — Plasmid Analysis (MOB-suite)

```bash
# Install MOB-suite
conda create -n mobsuite\_env -c conda-forge -c bioconda mob\_suite -y
conda activate mobsuite\_env
mob\_typer --version
```

**Result:** mob\_typer 3.1.9

```bash
# Run MOB-suite on all 21 genomes
cd 01-kpneumoniae-genomic-surveillance
mkdir -p results/mobsuite\_output
for genome in data/ncbi\_dataset/data/\*/\*.fna; do
    accession=$(basename $(dirname "$genome"))
    mob\_recon --infile "$genome" --outdir results/mobsuite\_output/$accession --force
done
```

**Result:** Plasmid content detected in nearly all 21 genomes. Only ST147 (GCA\_055721665.1) showed zero plasmids — notably also the genome with the lowest resistance score.

```bash
# Commit and push
cd /workspaces/abhinaya\_Bioinformatics\_projects
git add -A
git commit -m "Phase 5: MOB-suite plasmid analysis complete for all 21 genomes"
git push
```

\---

## Phase 6 — Comparative Genomics (Panaroo)

```bash
# Install Panaroo
conda create -n panaroo\_env -c conda-forge -c bioconda panaroo -y
conda activate panaroo\_env
panaroo --version
```

**Result:** Panaroo 1.8.0

```bash
# Run Panaroo pangenome analysis
cd 01-kpneumoniae-genomic-surveillance
mkdir -p results/panaroo\_output
panaroo -i results/prokka\_annotations/\*/\*.gff -o results/panaroo\_output --clean-mode strict -t 2
```

**Result — Pangenome breakdown across 21 genomes:**

|Category|Count|
|-|-|
|Core genes (99-100% of strains)|4,104|
|Soft core genes (95-99%)|141|
|Shell genes (15-95%)|2,250|
|Cloud genes (0-15%)|3,188|
|**Total pangenome**|\~9,683 genes|

Confirms an "open" pangenome, consistent with published literature on K. pneumoniae.

```bash
# Commit and push (large intermediate files excluded via .gitignore)
cd /workspaces/abhinaya\_Bioinformatics\_projects
git add -A
git commit -m "Phase 6: Panaroo pangenome analysis results"
git push
```

\---

## Phase 7 — Multiple Sequence Alignment (MSA)

```bash
# Install MAFFT (used internally by Panaroo)
conda activate panaroo\_env
conda install -c bioconda mafft -y
```

```bash
# Rerun Panaroo with core genome alignment enabled
cd 01-kpneumoniae-genomic-surveillance
panaroo -i results/prokka\_annotations/\*/\*.gff -o results/panaroo\_output --clean-mode strict -t 2 -a core
```

**Result:** `core\_gene\_alignment\_filtered.aln` — 68MB, all 4,104 core genes aligned across all 21 genomes (confirmed via `grep -c ">" file` = 21).

```bash
# Commit and push
cd /workspaces/abhinaya\_Bioinformatics\_projects
git add 01-kpneumoniae-genomic-surveillance/results/panaroo\_output/core\_gene\_alignment\_filtered.aln
git commit -m "Phase 7: core genome alignment (MSA) complete via Panaroo/MAFFT"
git push
```

\---

## Phase 8 — Phylogenetics (IQ-TREE)

```bash
# Install IQ-TREE
conda create -n iqtree\_env -c conda-forge -c bioconda iqtree -y
conda activate iqtree\_env
iqtree --version
```

**Result:** IQ-TREE 3.1.3

```bash
# Build the phylogenetic tree
cd 01-kpneumoniae-genomic-surveillance
mkdir -p results/iqtree\_output
iqtree -s results/panaroo\_output/core\_gene\_alignment\_filtered.aln \\
  -pre results/iqtree\_output/kpneumoniae\_tree -nt 2 -bb 1000
```

**Result:** Maximum-likelihood tree with 1000 ultrafast bootstrap replicates. Output: `kpneumoniae\_tree.treefile`.

```bash
# Commit and push
cd /workspaces/abhinaya\_Bioinformatics\_projects
git add 01-kpneumoniae-genomic-surveillance/results/iqtree\_output/
git commit -m "Phase 8: phylogenetic tree built with IQ-TREE (1000 bootstrap replicates)"
git push
```

\---

## Phase 9 — Integration

```python
# scripts/integrate\_results.py — merges Kleborate + MOB-suite into one master table
import pandas as pd
import os
import glob

kleborate\_path = "results/kleborate\_output/kleborate\_results.txt/klebsiella\_pneumo\_complex\_output.txt"
kleborate\_df = pd.read\_csv(kleborate\_path, sep="\\t")
kleborate\_df\["accession"] = kleborate\_df\["strain"].str.extract(r"(GCA\_\\d+\\.\\d+)")

rename\_map = {
    "enterobacterales\_\_species\_\_species": "species",
    "klebsiella\_pneumo\_complex\_\_mlst\_\_ST": "ST",
    "klebsiella\_pneumo\_complex\_\_virulence\_score\_\_virulence\_score": "virulence\_score",
    "klebsiella\_pneumo\_complex\_\_resistance\_score\_\_resistance\_score": "resistance\_score",
    "klebsiella\_pneumo\_complex\_\_resistance\_class\_count\_\_num\_resistance\_classes": "num\_resistance\_classes",
    "klebsiella\_pneumo\_complex\_\_resistance\_gene\_count\_\_num\_resistance\_genes": "num\_resistance\_genes",
}
kleborate\_df = kleborate\_df.rename(columns=rename\_map)

mobsuite\_dir = "results/mobsuite\_output"
plasmid\_counts = \[]
for accession\_dir in glob.glob(f"{mobsuite\_dir}/\*/"):
    accession = os.path.basename(os.path.normpath(accession\_dir))
    contig\_report = os.path.join(accession\_dir, "contig\_report.txt")
    num\_plasmids = 0
    if os.path.exists(contig\_report):
        df = pd.read\_csv(contig\_report, sep="\\t")
        if "molecule\_type" in df.columns:
            plasmid\_rows = df\[df\["molecule\_type"] == "plasmid"]
            num\_plasmids = plasmid\_rows\["primary\_cluster\_id"].nunique() if "primary\_cluster\_id" in df.columns else len(plasmid\_rows)
    plasmid\_counts.append({"accession": accession, "num\_plasmids": num\_plasmids})
plasmid\_df = pd.DataFrame(plasmid\_counts)

master\_df = kleborate\_df.merge(plasmid\_df, on="accession", how="left")
summary\_cols = \["accession", "species", "ST", "virulence\_score", "resistance\_score",
                 "num\_resistance\_classes", "num\_resistance\_genes", "num\_plasmids"]
summary\_df = master\_df\[\[c for c in summary\_cols if c in master\_df.columns]]
summary\_df = summary\_df.sort\_values("ST")

os.makedirs("results/integration\_output", exist\_ok=True)
summary\_df.to\_csv("results/integration\_output/master\_summary.csv", index=False)
```

```bash
python scripts/integrate\_results.py
```

**Result — Final integrated master table:**

|ST|Virulence|Resistance|Plasmids|Interpretation|
|-|-|-|-|-|
|ST23|5 (highest)|0|1|Pure hypervirulence|
|ST420|4|0|1|Pure hypervirulence|
|ST2096 (4 genomes)|3-4|2-3|2-3|**True convergence**|
|ST11 (4 genomes)|1-4|1-2|2-4|**True convergence**|
|ST147|0|1|0|Lowest overall|
|ST101 (2 genomes)|1|0|3|Low virulence/resistance despite plasmids|

**Phylogenetic tree visualization (iTOL):** Tree tips relabeled with real strain names (ST\_strainname format) using a lookup built from Phase 2's accession-to-strain mapping. Key finding: ST2096 and ST11 (the two convergent lineages) occupy separate, well-distinguished clades on the tree — indicating independent evolutionary origin of the AMR-virulence convergence phenotype, consistent with plasmid-mediated convergent evolution rather than shared ancestry.

```bash
# Commit and push
cd /workspaces/abhinaya\_Bioinformatics\_projects
git add 01-kpneumoniae-genomic-surveillance/scripts/
git add 01-kpneumoniae-genomic-surveillance/results/integration\_output/
git add 01-kpneumoniae-genomic-surveillance/figures/
git add 01-kpneumoniae-genomic-surveillance/docs/
git commit -m "Phase 9: integration complete - master table, labeled tree, interpretation"
git push
```

\---

## Summary — Tools Used Across the Pipeline

|Phase|Tool|Version|
|-|-|-|
|1|Biopython|1.88|
|3|NCBI datasets CLI|18.36.0|
|3|QUAST|5.2.0|
|3|Prokka|1.15.6|
|4|Kleborate|3.2.4|
|5|MOB-suite|3.1.9|
|6-7|Panaroo|1.8.0|
|7|MAFFT|(via Panaroo)|
|8|IQ-TREE|3.1.3|
|9|pandas|(Python integration script)|
|9|iTOL|(web-based tree visualization)|



