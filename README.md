# MDDP-Corpus

Source code for **MDDP-Corpus: A FAIR-oriented infrastructure of multi-domain data papers for scientific data discovery**

This repository provides the source code used for corpus construction, metadata preprocessing, automated data paper identification, and classification model evaluation described in the manuscript.

The provided scripts enable reproduction of the MDDP-Corpus construction workflow and the machine learning experiments conducted for automated data paper identification.

---

## Overview

Data papers provide structured descriptions of scientific datasets and play an important role in promoting data sharing, discovery, and reuse. However, identifying data papers from large-scale scholarly publications remains challenging due to disciplinary differences and variations in publication practices.

MDDP-Corpus is a multi-domain corpus containing **25,952 data papers** collected from multiple scientific disciplines. The dataset was developed to support automated data paper identification and facilitate the discovery of scientific data resources.

This repository contains the computational workflow used for:

- publication metadata preprocessing;
- corpus construction and standardization;
- automated data paper identification;
- classification model training and evaluation.

---

## Repository Structure
MDDP-Corpus/
│
├── preprocessing/
│ ├── Content Extraction from HTML-type Articles.py
│ ├── Content Extraction from PDF-type Articles.py
│ └── Content Extraction from XML-type Articles.py
│
├── models/
│ ├── svm_classifier.py
│ ├── bert_classifier.py
│ ├── scibert_classifier.py
│ └── llama3_classifier.py
│
├── evaluation/
│ └── incremental_classification_metrics.py
│ └── incremental_data_classification.py
│ └── label_consistency_comparison.py
│
├── data/
│ └── README.md
│
├── docs/
│ └── reproduction_notes.md
│
├── requirements.txt
│
├── LICENSE
│
└── README.md

---

## Dataset Availability

The MDDP-Corpus dataset generated in this study is publicly available through Zenodo:

**Dataset DOI:**  

https://doi.org/10.5281/zenodo.21722806

The dataset contains standardized metadata records of **25,952 data papers**, including bibliographic information and classification labels.

The dataset is released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

Due to copyright restrictions, the original publications used for corpus construction are not included in this repository.

---

## Software Requirements

The code was developed and tested using:

- Python 3.9
- PyTorch 1.7.1
- Transformers 4.44.2

The required Python packages are provided in:
requirements.txt

---

## Installation

Clone this repository:

```bash
git clone https://github.com/MDDP-Corpus/MDDP-Corpus.git

cd MDDP-Corpus

Install dependencies:
pip install -r requirements.txt

License

This project is released under the MIT License.

See the LICENSE file for details.
Citation

If you use the MDDP-Corpus dataset or source code, please cite:

Citation information will be added after publication.

Contact

For questions regarding the dataset or source code, please contact the corresponding author.

