# Project Skripsi

![love](https://img.shields.io/badge/Made%20with-🖤-white)
[![Python](https://img.shields.io/badge/Python-3.8-green?logo=python)](https://www.python.org/)

Main repository untuk project skripsi.

## To Do's

1. Labelling data
2. Preprocess & Visualisasi (TSNE visualization on corpus)
   - liat apakah _linearly separable_
3. Modelling dengan SVM (setiap kernel)
4. Export model ke onnx dan deploy di app

## [App](https://github.com/Hyuto/skripsi-app)

Implementasi model yang telah di latih.

## [Dataset](.data)

Dataset adalah data hasil web scraping twitter pada topik `vaksin covid-19` pada tahun 2021 selama
12 bulan. Library yang digunakan untuk melakukan scraping adalah [`snscrape`](https://github.com/JustAnotherArchivist/snscrape)
dengan query yang digunakan untuk pencarian adalah `vaksin (covid OR corona)`. Data dapat diakses
langsung secara online dengan format link berikut:

```
https://raw.githubusercontent.com/Hyuto/skripsi/master/data/<NAMA FILE>
```
