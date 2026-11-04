# VBM_Random_Cell_Migration
A repository that contains the code for a vertex based model for random single cell migration, explained in more detail in the document `VertexBasedModel.pdf`. Within this repository, there is also an implementation of this model where there are also springs located between every other vertex to help maintain shape (located in the folder `Springs_EveryOther_Vertex`) and two different implementations of directed cell migration (located in the folders `directed_migration_omega_biased` and `directed_migration_onrate_biased`).

## Set up
To create the conda environment, navigate to the directory of this repository in your terminal and run the following: 
```
conda env create -f vbm_model.yml
```

Next, activate the conda environment: `conda activate vbm_model`


## Running random single cell migration
To run a simulation of one cell undergoing random migration using the mathematical framework outlined in `VertexBasedModel.pdf`, run:
```
python Run_One_Cell.py
```

To run a simulation with many cells, run:
```
python Run_Many_Cells.py
```

### An implementation with additional springs placed between every other vertex
Included in the folder `Springs_EveryOther_Vertex` is an implementation of the same model, but with the addition of springs placed between every other vertex. This framework can help the cell maintain its shape throughout the simulation.

## Implementing directed migration
Directed migration has been implemented by using the framework for the model outlined in `VertexBasedModel.pdf`, but with two different approaches by biasing different processes within the model (code located in folders `directed_migration_omega_biased` and `directed_migration_onrate_biased`). In both cases, the gradient that is explored is a simple linear gradient in the $x$ direction, defined by the function `lin_grad(x_pos)` in the file `directed_pol_dir_VBM_func.py`.

The first approach is biasing the internal polarity direction towards the increasing signal of the gradient and the second approach is biasing the on rate at each vertex so that it increases with increasing signal of the gradient.

### Biasing the internal polarity direction in `directed_migration_omega_biased`
In this approach, the internal cell direction is biased so that it tries to align with the direction of increasing signal from the gradient rather than the direction of greatest net tension along the boundary. This is implemented in the function `UpdateVertices()` with the parameter `F_a` in the file `directed_pol_dir_VBM_func.py`.

### Biasing the on rate in `directed_migration_onrate_biased`
In this approach, the on rate at a vertex is biases such that the on rate at each vertex increases as the signal from the gradient increases. This bias in the increase of on rate is in addition to the on rate dictated from the tension at that vertex and is implemented in the function `find_onrate()` in the file `directed_pol_dir_VBM_func.py`.
