# Analisis Emosi Terhadap Opini Masyarakat Tentang Vaksin Covid-19 Pada Sosial Media Twitter Menggunakan Support Vector Machine

![love](https://img.shields.io/badge/Made%20with-🖤-white)
[![Python](https://img.shields.io/badge/Python-≥3.8-green?logo=python)](https://www.python.org/)
[![Test](https://github.com/Hyuto/skripsi/actions/workflows/testing.yaml/badge.svg)](https://github.com/Hyuto/skripsi/actions/workflows/testing.yaml)
[![Lint](https://github.com/Hyuto/skripsi/actions/workflows/linting.yaml/badge.svg)](https://github.com/Hyuto/skripsi/actions/workflows/linting.yaml)
[![codecov](https://codecov.io/gh/Hyuto/skripsi/branch/master/graph/badge.svg?token=6L0ICORI22)](https://codecov.io/gh/Hyuto/skripsi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Main repository untuk project skripsi berjudul
`Analisis Emosi Terhadap Opini Masyarakat Tentang Vaksin Covid-19 Pada Sosial Media Twitter Menggunakan Support Vector Machine`.

## Setup

Setup local environment. Buat _virtual environments_ baru kemudian install dependencies pada
`requirements.txt`

```bash
$ pip install -r requirements.txt
```

## [App](https://github.com/Hyuto/skripsi-app)

Implementasi model yang telah di latih dalam bentuk aplikasi dengan mendeploy model yang
telah di latih, model tersebut kemudian diconvert ke bentuk `onnx` yang selanjutnya akan di deploy
di `android` dan `web` dengan menggunakan `react-native` dan `onnxruntime`.

## [Dataset](./data)

Dataset yang digunakan adalah data hasil web scraping twitter pada topik `vaksin covid-19` pada tahun 2021 selama
12 bulan. Library yang digunakan untuk melakukan scraping adalah [`snscrape`](https://github.com/JustAnotherArchivist/snscrape)
dengan query yang digunakan untuk pencarian adalah `vaksin (covid OR corona)`. Data dapat diakses
langsung secara online dengan format link berikut:

```
https://raw.githubusercontent.com/Hyuto/skripsi/master/data/<NAMA FILE>
```

## Development

Install `poetry` terlebih dahulu, panduan instalasinya dapat dilihat
[python-poetry](https://python-poetry.org/docs/#installation).
Setelah proses penginstallan `poetry` run command berikut pada terminal

```bash
$ make setup-dev
```
