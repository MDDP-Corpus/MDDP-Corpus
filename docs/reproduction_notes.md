# Reproduction Notes

This document provides additional information for reproducing the experiments reported in the MDDP-Corpus study.

## Overview

The MDDP-Corpus workflow consists of four main stages:

1. Metadata preprocessing;
2. Corpus construction;
3. Automated data paper identification;
4. Model performance evaluation.

The provided scripts are organized according to these stages.

---

## Environment

The experiments were conducted using the following software environment:

- Operating System: Linux-based environment
- Python: 3.9
- PyTorch: 1.7.1
- Transformers: 4.44.2

The required Python dependencies are listed in:
requirements.txt

---

## Workflow

### Step 1. Metadata Preprocessing

The preprocessing stage performs:

- metadata cleaning;
- missing value handling;
- DOI normalization;
- field standardization.

The processed metadata are used as input for corpus construction and classification experiments.

---

### Step 2. Corpus Construction

The corpus construction scripts generate standardized publication records for MDDP-Corpus.

The resulting dataset contains:

- publication metadata;
- textual information;
- classification labels.

The complete dataset is available through the Zenodo repository.

---

### Step 3. Model Training and Classification

The repository implements four classification approaches:

- Support Vector Machine (SVM);
- BERT;
- SciBERT;
- LLaMA3.

The models are trained and evaluated using the prepared publication records.

---

### Step 4. Performance Evaluation

The classification performance is assessed using:

- Precision;
- Recall;
- F1-score.

The evaluation scripts reproduce the performance comparisons reported in the manuscript.

---

## Notes on Data Access

The original publications used for corpus construction are not distributed with this repository due to copyright restrictions.

Researchers should obtain publication records through appropriate scholarly databases or use the publicly available MDDP-Corpus dataset from Zenodo.

---

## Reproducibility Recommendations

To reproduce the reported experiments:

1. Install all required dependencies.
2. Download the MDDP-Corpus dataset from Zenodo.
3. Prepare the input files according to the provided data format.
4. Run preprocessing scripts.
5. Execute the selected classification model.
6. Run evaluation scripts to obtain performance metrics.

Parameter settings and model configurations should be consistent with those reported in the associated manuscript.