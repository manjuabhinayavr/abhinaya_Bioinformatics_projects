
cat > docs/Phase9_Tree_Interpretation.md << 'DOCEOF'
# Phase 9 - Phylogenetic Tree Interpretation
## K. pneumoniae Genomic Surveillance Project

## Tree construction summary
- Built from a core genome alignment (4,104 core genes shared across all 21 genomes, Panaroo + MAFFT)
- Maximum-likelihood tree via IQ-TREE, 1000 ultrafast bootstrap replicates
- Visualized in iTOL with tips relabeled as ST_strainname for readability

## Key observations

1. ST-based lineage assignment matches tree topology.
Every sequence type represented by more than one genome forms a tight cluster on the tree: ST2096 (KP4, KK54, KK53, KK50), ST11 (C2155, C8092, ST11-16-116, ST11-22-90), ST307 (KK47, KP3), ST101 (KK33, KP2), ST15 (SDS-K20, KK45).

2. Independent evolutionary origin of the AMR-virulence convergence phenotype.
ST2096 and ST11, the two lineages showing true convergence of high virulence and high resistance, occupy clearly separated positions on the tree, not adjacent or nested within each other. This suggests the dangerous combination emerged independently in two evolutionarily distinct lineages, supporting a model of convergent evolution via plasmid-mediated horizontal gene transfer rather than inheritance from one common resistant-virulent ancestor.

3. Pure hypervirulence lineages cluster near each other.
ST23 (SDS-K9) and ST420 (SDS-K5), both high-virulence and zero-resistance genomes, sit adjacent on the tree.

4. Lowest-risk lineage.
ST147 (KK35), with the lowest virulence score, lowest resistance score, and zero plasmids, appears distinct on the tree, consistent with its outlier profile across all analysis layers.

## Overall interpretation
Phylogenetic analysis confirms that sequence type accurately predicts evolutionary relatedness across these 21 isolates. The two AMR-virulence convergent lineages, ST2096 and ST11, occupy distinct, well-separated positions on the tree, indicating independent evolutionary origins of this concerning phenotype combination. Combined with the multi-plasmid content observed in both lineages, this supports a model of convergent evolution driven by mobile genetic elements rather than clonal expansion from a single ancestor. This directly supports the project's research question: AMR and virulence can converge within a lineage through independent, plasmid-mediated acquisition, not just shared ancestry.
