# Modelling and visualization/reporting tools for Covid-19 data of Molise

[English](README.md) - [Italiano](README_IT.md)<br><br>

[![GitHub license](https://img.shields.io/badge/License-Apache%202.0-blue)](https://github.com/clissa/covid-Molise/blob/main/LICENSE)
[![GitHub commit](https://img.shields.io/github/last-commit/clissa/covid-Molise)](https://github.com/clissa/covid-Molise)

This repository is intended to explore modelling and visualization/reporting tools while describing recent trends in
Covid-19 pandemic. To do so, data published by the Protezione Civile on
their [GitHub repository](https://github.com/pcm-dpc/COVID-19) are analysed and the Italian region of Molise is taken as
benchmark. However, the whole code is structured so to be easily modified in case different configurations are of
interest.

## Installation

In order to re-create a suitable environment to run the code in this repository it is sufficient to follow the steps
below:

```commandline
# clone repository
git clone https://github.com/clissa/covid-Molise.git

# move into the project folder
cd covid-Molise

# create conda environment through .yml file
conda env create --file environment.yml
```

## Repository structure

## Struttura del repository

This repository is organised with:

- configuration files as *environment.yml, requirements.txt, README and LICENSE* in the root directory
- python modules that contain management, modelling and visualization utils in the root directory
- *notebooks* folder with Jupyter Notebooks that leverages custom utils to perform data analysis and
  visualization/reporting
    - *sample_results* folder contains samples of the results one can obtain from the notebooks

The complete tree of the repository is reported below:

```
covid-Molise/
├── environment.yml
├── LICENSE
├── models.py
├── notebooks
│   ├── Forecast Hospitalizations (SARIMAX).ipynb
│   └── sample_results
│       ├── 2021-02-08
│       │   ├── terapia_intensiva.html
│       │   └── terapia_intensiva.png
│       └── 2021-02-13
│           ├── terapia_intensiva.html
│           └── terapia_intensiva.png
├── README.md
├── requirements.txt
├── utils.py
└── visualization.py
```

## License

[Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0)
- [See License](https://github.com/pcm-dpc/COVID-19/blob/master/LICENSE)