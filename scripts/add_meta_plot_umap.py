import os
import anndata as ad
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

cell_identifier_in_meta = 'barcode'
project_folder = Path ('/scratch/mfafouti/ABC_atlas_celltyping')
mommybrain_folder = Path('/project/rrg-shreejoy/MommyBrain/Slide_tags/Pipeline_data/objects')
h5ad_dir = project_folder / 'celltyped_post_bender'
#metadata_dir = project_folder / 'scratch' 
metadata_dir = Path('/scratch/mfafouti/Mommybrain/Slide_tags/Doublet_detection/scanpy/doublet_metadata')
#'NO_training_baseline_csv_mapping_output.csv'
output_dir = project_folder / 'celltyped_doublets'
output_dir.mkdir(parents=True, exist_ok=True)

for file in h5ad_dir.glob("*.h5ad"):
    sample = file.stem.split("_")[2]
    print(f"Loading metadata for sample {sample}...")
    
    metadata_file = next(metadata_dir.glob(f"{sample}*.csv"))
    metadata_df = pd.read_csv(metadata_file)
    print(f"Loading metadata from {metadata_file}...") 
    print(f"Metadata shape: {metadata_df.shape}")
    print(f"Metadata columns: {metadata_df.columns.tolist()}")

    print("Loading object data...")
    adata = sc.read_h5ad(file)
    print(f"Object shape: {adata.shape}")
    print(f"Object obs columns: {adata.obs.columns.tolist()}")

    print(f"Metadata cell IDs: {metadata_df.iloc[:5, 0].tolist()}")
    print(f"Object cell IDs: {adata.obs.index[:5].tolist()}")
    metadata_df = metadata_df.set_index(cell_identifier_in_meta)
    # adata.obs.set_index("barcode", inplace=True)
    print(metadata_df.index.name)
    print(adata.obs.index.name)

    print("Merging metadata...")
    n_total = len(metadata_df)
    n_matched = metadata_df.index.isin(adata.obs.index).sum()
    print(f"🧬 Metadata: matched {n_matched} of {n_total} barcodes ({n_matched / n_total:.2%})")
    adata.obs = adata.obs.drop(columns=metadata_df.columns.intersection(adata.obs.columns))
    adata.obs = adata.obs.join(metadata_df, how="left")

    adata.obs['subclass_name'] = adata.obs['subclass_name'].astype('category')

    output_path = output_dir / f'obs_annotated_{sample}.h5ad'
    adata.write(output_path)

    print(f"Object obs columns: {adata.obs.columns.tolist()}")
    print(f"💾 Saved updated AnnData to: {output_path}\n")

# # Use Scanpy's default categorical color palette
# adata.uns['subclass_name_colors'] = sc.pl.palettes.default_20[:adata.obs['subclass_name'].nunique()]

# # GET COLORS
# color_df = pd.read_csv("/scratch/mfafouti/Mommybrain/cluster_annotation_term.csv", usecols=["name", "color_hex_triplet"])
# #color_df["name"] = color_df["name"].str.replace(r"[ /-]", "_", regex=True)

# # Create mapping from label number (prefix before _) to hex color
# def get_num_prefix(label):
#     try:
#         return int(str(label).split("_")[0])
#     except:
#         return -1

# color_df["num_prefix"] = color_df["name"].apply(get_num_prefix)

# # Sort CSV by numeric prefix
# color_df = color_df.sort_values("num_prefix")

# # Build dictionary mapping label to hex
# label_to_hex = dict(zip(color_df["name"], color_df["color_hex_triplet"]))

# # umap
# coloring = 'subclass_name'
# sc.pl.umap(
#     adata,
#     color=coloring,
#     show=True,
#     palette=label_to_hex,
#     title=f"Subclass name (n = {adata.n_obs})"
# )

# output_fig = output_dir / f'new_{sample}_umap_colored_by_{coloring}.png'
# plt.savefig(output_fig, dpi=300, bbox_inches='tight')
# print(f"Plot saved to: {output_fig}")