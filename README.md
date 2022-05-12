# dpgen-snakemake

[![Test workflow scripts](https://github.com/chazeon/dpgen-snakemake/actions/workflows/main.yml/badge.svg)](https://github.com/chazeon/dpgen-snakemake/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/chazeon/dpgen-snakemake/branch/v2/graph/badge.svg?token=Q6GQAIPTNI)](https://codecov.io/gh/chazeon/dpgen-snakemake)


A lightweight [Snakemake][1]-based workflow that implements the [DP-GEN][2] scheme.

[1]: https://snakemake.readthedocs.io/en/stable/
[2]: https://arxiv.org/abs/1910.12690

## Project structure

- **`project`**: Actrual project files.
  - **`workflows`**: Snakemake workflow files.
  - **`scripts`**: Scripts for transforming input / output.
  - **`templates`**: Templates for genrating files.
- **`envs`**: conda environments for workflow orchestration and DeePMD-kit training / evaluation.
