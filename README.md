# dpgen-snakemake

[![Test workflow scripts](https://github.com/chazeon/dpgen-snakemake/actions/workflows/main.yml/badge.svg)](https://github.com/chazeon/dpgen-snakemake/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/chazeon/dpgen-snakemake/branch/v2/graph/badge.svg?token=Q6GQAIPTNI)](https://codecov.io/gh/chazeon/dpgen-snakemake)


A lightweight [Snakemake][1]-based workflow that implements the [DP-GEN][2] scheme.

[1]: https://snakemake.readthedocs.io/en/stable/
[2]: https://arxiv.org/abs/1910.12690

## Project structure

- [**`project`**](project): Actual project files.
  - [**`workflows`**](project/workflows): Snakemake workflow files.
  - [**`scripts`**](project/scripts): Scripts for transforming input / output.
  - [**`templates`**](project/templates): Templates for generating files.
  - [**`tests`**](project/tests): Tests for the Python scripts.
- [**`project_sidecar`**](project_sidecar): Project files on the CPU machine
- [**`envs`**](envs): conda environments for workflow orchestration and DeePMD-kit training / evaluation.

## Usage

### DP-GEN Iteration

In each iteration, specify the environment variable `DPGEN_ITER_ID` then execute one one of the following rules to generate the corresponding files.

| Machine | Name of the rule           | Description                                                  |
| ------- | -------------------------- | ------------------------------------------------------------ |
| GPU     | `dp_run_train_target`      | Prepare files for the training step.                         |
| GPU     | `dp_run_model_devi_target` | Collect the newly generated potential files, then prepare the input files for the LAMMPS model deviation step. |
| GPU     | `dp_run_fp_target`         | Prepare the structures for the VASP calculation and prepare a tarball for transfer. |
| CPU     | `dp_run_fp_input`          | Collect the tarball of structures from the GPU machine.      |
| CPU     | `dp_run_fp_target`         | Collect the structures from the GPU machine, then prepare the input files for the VASP calculation. |
| CPU     | `dp_run_fp_done_target`    | Collect the VASP results and prepare for transfer.           |
| GPU     | `dp_run_fp_collect2`       | Collect VASP results from the CPU machine, then prepare the training data for the next iteration. |

