# ABC_atlas_celltyping
Allen Brain Institute cell type mapper to map the cells to the Allen Brain Institute taxonomy, subsetting specific brain regions of interest. Particularly, we are interested in regions that are present in a coronal brain section. 

## Custom Docker image (Linux HPC compatible):
```bash
module load apptainer
apptainer pull celltypemapper.sif docker://ghcr.io/neurogeek03/celltypemapper:atlas_access
```

## Approach:
To assign cell types on a coronal mouse section, the 10xv3 reference from the Allen Brain institute (https://alleninstitute.github.io/abc_atlas_access/descriptions/WMB-10Xv3.html) is subset to regions that are present in a coronal section. 

This subsets the reference taxonomy tree to cell types found in the brain regions of interest. 

Using the subsetted taxonomy, we can assign more biologically informed cell types. 

## Overview of how the algorithm works: 
