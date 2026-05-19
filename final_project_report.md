# FINAL PROJECT AOL — BIG DATA ANALYTICS

## Arsitektur Big Data untuk Prediksi Risiko Kredit pada Platform Peer-to-Peer Lending: Pendekatan Skoring Kredit Alternatif bagi Peminjam Tanpa Akses Perbankan

**Mata Kuliah:** COMP8035041 — Big Data Analytics  
**Nama:** Emmanuel Daniel W  
**NIM:** 2702751271  

---

# DAFTAR ISI

1. Executive Summary  
2. Problem Analysis and Business Drivers  
   2.1 Background of the Problem and Urgency  
   2.2 Market and Business Drivers  
   2.3 Stakeholders Involved  
   2.4 Project Success Indicators  
3. Architecture Design and Technology Selection  
   3.1 Big Data Architecture Overview  
   3.2 Data Ingestion Methods  
   3.3 Storage Technologies  
   3.4 Processing Framework  
   3.5 IT Governance Considerations  
4. Data Process and Analysis Model  
   4.1 Data Acquisition  
   4.2 Data Elements and Formats  
   4.3 Data Cleaning and Organization  
   4.4 Data Model Selection  
   4.5 Machine Learning Pipeline  
   4.6 Graph Analytics  
5. Visualization and Insights  
   5.1 Dashboard Design  
   5.2 Visualization Components  
   5.3 Key Analytical Insights  
   5.4 Business Narrative and Strategic Impact  
6. Solution Effectiveness Evaluation and Development Plan  
   6.1 Model Performance Evaluation  
   6.2 Business Effectiveness Evaluation  
   6.3 Limitations  
   6.4 Development Plan  

---

# 1. EXECUTIVE SUMMARY

Platform Peer-to-Peer (P2P) lending menjadi salah satu solusi pembiayaan digital bagi masyarakat dan pelaku usaha yang tidak sepenuhnya terlayani oleh lembaga keuangan tradisional. Namun, pertumbuhan volume pinjaman digital juga meningkatkan risiko kredit, terutama risiko gagal bayar atau default. Pada dataset Lending Club periode 2007–2018, terdapat 2.260.701 data pinjaman yang disetujui dan 27.648.741 aplikasi pinjaman yang ditolak. Dari data pinjaman yang disetujui, tingkat default keseluruhan mencapai 13,02%, bahkan mencapai 39,74% pada kelompok pinjaman dengan risiko tertinggi.

Permasalahan utama yang diangkat dalam proyek ini adalah bagaimana memanfaatkan pendekatan Big Data dan machine learning untuk meningkatkan kualitas prediksi risiko gagal bayar pada platform P2P lending. Sistem credit scoring konvensional, seperti pendekatan berbasis FICO score, memiliki keterbatasan karena hanya menggunakan sejumlah variabel terbatas dan tidak mampu menangkap hubungan non-linear antar faktor risiko. Oleh karena itu, proyek ini merancang pipeline Big Data yang mampu mengelola data berskala besar, melakukan preprocessing, feature engineering, machine learning, graph analytics, dan visualisasi interaktif untuk mendukung pengambilan keputusan kredit.

Solusi yang dikembangkan menggunakan dataset Lending Club Loan Data dari Kaggle dengan lisensi CC0-1.0. Pipeline analitik mencakup proses data ingestion dari file `.csv.gz`, pemrosesan data menggunakan Pandas dan Apache Spark, penyimpanan hasil dalam format yang lebih efisien seperti Apache Parquet, serta pengembangan model machine learning menggunakan Logistic Regression, Random Forest, XGBoost, dan Spark MLlib. Model terbaik diperoleh dari XGBoost dengan nilai AUC-ROC sebesar 0,7109, recall sebesar 0,6906, F1-Score sebesar 0,2048, dan F2-Score sebesar 0,3544.

Selain evaluasi teknis, proyek ini juga melakukan threshold tuning berbasis kebutuhan bisnis. Dalam konteks credit scoring, kesalahan false negative, yaitu gagal mendeteksi peminjam yang berisiko default, lebih mahal dibandingkan false positive. Dengan asumsi biaya false negative lima kali lebih besar dibanding false positive, threshold optimal model berada pada nilai 0,471. Threshold ini menghasilkan pengurangan estimasi biaya sebesar 23,5% dibandingkan threshold default 0,5.

Graph analytics juga digunakan untuk melengkapi analisis machine learning. Feature correlation network menunjukkan adanya kelompok fitur yang saling berkorelasi kuat, seperti fitur FICO, fitur jumlah pinjaman, dan fitur bunga. Grade risk hierarchy menunjukkan bahwa tingkat default meningkat konsisten dari Grade A hingga Grade G. Analisis ini membantu menjelaskan bahwa risiko kredit tidak hanya dipengaruhi oleh satu variabel, melainkan kombinasi dari grade, sub-grade, interest rate, debt-to-income ratio, credit utilization, dan rasio cicilan terhadap pendapatan.

Untuk mendukung penyampaian hasil kepada stakeholder, proyek ini juga menambahkan dashboard interaktif menggunakan Streamlit dan Plotly. Dashboard menyajikan ringkasan performa model, feature importance, analisis risiko berdasarkan grade, serta rekomendasi kebijakan bisnis seperti loan approval threshold, risk-based pricing, dan strategi portofolio investor.

Secara keseluruhan, proyek ini menunjukkan bahwa pendekatan Big Data Analytics mampu menghasilkan sistem credit scoring yang lebih adaptif, skalabel, dan berbasis data. Solusi ini tidak hanya membantu mengurangi risiko kredit, tetapi juga mendukung inklusi keuangan dengan memberikan peluang evaluasi yang lebih adil bagi peminjam yang tidak memiliki riwayat kredit konvensional yang kuat.

---

# 2. PROBLEM ANALYSIS AND BUSINESS DRIVERS

## 2.1 Background of the Problem and Urgency

Akses terhadap pembiayaan merupakan komponen penting dalam mendorong pertumbuhan ekonomi. Namun, masih banyak individu dan pelaku usaha yang mengalami kesulitan memperoleh kredit dari lembaga keuangan formal. Salah satu penyebab utamanya adalah keterbatasan sistem credit scoring konvensional. Sistem seperti FICO score umumnya menilai kelayakan kredit berdasarkan riwayat pembayaran, jumlah utang, durasi riwayat kredit, dan beberapa indikator lain. Pendekatan ini menghasilkan skor tunggal yang menjadi dasar keputusan kredit.

Masalah muncul ketika calon peminjam tidak memiliki riwayat kredit formal yang cukup. Kelompok unbanked, pelaku usaha kecil, pekerja informal, dan peminjam baru sering kali tidak dapat dinilai secara komprehensif. Akibatnya, mereka berpotensi ditolak meskipun secara finansial sebenarnya layak memperoleh pinjaman. Pada saat yang sama, platform P2P lending harus tetap menjaga risiko kredit agar tidak menimbulkan kerugian besar bagi investor dan platform.

Pertumbuhan P2P lending memperbesar urgensi masalah ini. Data Lending Club menunjukkan peningkatan jumlah pinjaman dari 603 pinjaman senilai USD 4,79 juta pada tahun 2007 menjadi 495.242 pinjaman senilai USD 7,94 miliar pada tahun 2018. Pertumbuhan ini menghasilkan data dalam skala besar yang tidak lagi efektif dianalisis dengan metode manual atau statistik sederhana.

Dalam perspektif Big Data, data P2P lending memiliki karakteristik 5V:

| Karakteristik | Penjelasan |
|---|---|
| Volume | Dataset mencakup sekitar 29,9 juta record aplikasi pinjaman |
| Velocity | Aplikasi pinjaman masuk secara terus-menerus seiring pertumbuhan platform |
| Variety | Data terdiri dari numerik, kategorikal, temporal, dan semi-terstruktur |
| Veracity | Terdapat missing values, outlier, dan inkonsistensi format |
| Value | Data memiliki nilai tinggi untuk prediksi risiko dan strategi bisnis |

Berdasarkan kondisi tersebut, pendekatan Big Data dan machine learning menjadi relevan untuk meningkatkan kualitas sistem credit scoring. Machine learning mampu memproses banyak variabel secara simultan, menangkap hubungan non-linear, dan menghasilkan prediksi risiko yang lebih granular dibandingkan pendekatan konvensional.

## 2.2 Market and Business Drivers

Pengembangan solusi Big Data untuk prediksi risiko kredit didorong oleh beberapa faktor pasar dan bisnis berikut.

| Driver | Penjelasan | Dampak terhadap Proyek |
|---|---|---|
| Pertumbuhan industri fintech | Platform P2P lending berkembang pesat sebagai alternatif pembiayaan | Membutuhkan sistem credit scoring yang cepat dan skalabel |
| Risiko gagal bayar | Default rate keseluruhan mencapai 13,02%, dan mencapai 39,74% pada Grade G | Dibutuhkan model prediksi risiko yang lebih akurat |
| Inklusi keuangan | Banyak calon peminjam tidak memiliki akses kredit formal | Dibutuhkan pendekatan penilaian alternatif berbasis data |
| Tekanan regulasi | FCRA, ECOA, GDPR, dan regulasi OJK menuntut transparansi dan fairness | Model harus dapat dijelaskan dan diaudit |
| Kompetisi bisnis | Platform dengan model risiko lebih baik dapat menawarkan pinjaman lebih kompetitif | Analytics menjadi keunggulan kompetitif |
| Ketersediaan teknologi | Apache Spark, cloud storage, dan ML framework semakin matang | Implementasi Big Data menjadi lebih feasible |

Dari sisi bisnis, model prediksi default membantu platform dalam:

1. Mengurangi risiko kerugian akibat kredit macet.
2. Meningkatkan kualitas portofolio investor.
3. Mempercepat proses approval pinjaman.
4. Menyediakan pricing berbasis risiko yang lebih akurat.
5. Membuka akses pembiayaan bagi calon peminjam yang sebelumnya sulit dinilai.

## 2.3 Stakeholders Involved

Pengembangan solusi Big Data untuk credit scoring melibatkan banyak pemangku kepentingan.

| Stakeholder | Peran | Kepentingan |
|---|---|---|
| Borrowers | Pihak yang mengajukan pinjaman | Mendapat akses pembiayaan yang adil dan cepat |
| Investors / Lenders | Penyedia modal dalam platform P2P lending | Mendapat return optimal dengan risiko terkendali |
| Platform P2P Lending | Pengelola ekosistem pinjaman | Menjaga pertumbuhan bisnis dan kualitas kredit |
| Regulator | OJK, CFPB, SEC, dan lembaga terkait | Memastikan kepatuhan, fairness, dan perlindungan konsumen |
| Data Science Team | Pengembang model analitik | Membangun model yang akurat dan interpretabel |
| Data Engineering Team | Pengelola pipeline data | Menjamin data dapat diproses secara skalabel dan reliable |
| Risk Management Team | Pengguna output model | Menentukan kebijakan approval, pricing, dan mitigasi risiko |
| Academic Community | Evaluator metodologi | Memberikan validasi ilmiah terhadap pendekatan analitik |

## 2.4 Project Success Indicators

Agar keberhasilan proyek dapat dinilai secara objektif, ditetapkan beberapa indikator keberhasilan berikut.

| Success Indicator | Target | Hasil Proyek | Status |
|---|---:|---:|---|
| AUC-ROC model terbaik | ≥ 0,70 | 0,7109 | Tercapai |
| Recall deteksi default | ≥ 60% | 69,06% | Tercapai |
| F2-Score | ≥ 0,30 | 0,3544 | Tercapai |
| Pengurangan estimasi biaya | ≥ 15% | 23,5% | Tercapai |
| Model interpretability | Ada explainability | SHAP analysis | Tercapai |
| Scalability | Pipeline siap dikembangkan ke Spark cluster | Spark MLlib digunakan | Tercapai |
| Dashboard | Ada visualisasi interaktif | Streamlit dashboard | Tercapai |

---

# 3. ARCHITECTURE DESIGN AND TECHNOLOGY SELECTION

## 3.1 Big Data Architecture Overview

Arsitektur Big Data yang dirancang menggunakan pendekatan Data Lakehouse, yaitu kombinasi antara fleksibilitas Data Lake dan struktur analitik Data Warehouse. Pada tahap prototype, implementasi dilakukan di Google Colaboratory dan local environment. Untuk skenario produksi, arsitektur dapat dikembangkan ke cloud object storage dan distributed Spark cluster.

```text
+----------------------+        +----------------------+        +----------------------+
|      Data Sources    |        |    Ingestion Layer   |        |     Storage Layer    |
|----------------------|        |----------------------|        |----------------------|
| Lending Club CSV.GZ  | -----> | Kaggle API           | -----> | Raw Data Lake        |
| Accepted Loans       |        | Batch Ingestion      |        | CSV.GZ               |
| Rejected Loans       |        | Pandas Chunking      |        | Processed Parquet    |
+----------------------+        +----------------------+        +----------------------+
                                                                      |
                                                                      v
+----------------------+        +----------------------+        +----------------------+
|    Serving Layer     |        |   Analytics Layer    |        |   Processing Layer   |
|----------------------|        |----------------------|        |----------------------|
| Streamlit Dashboard  | <----- | ML Evaluation        | <----- | Pandas               |
| Business Reports     |        | SHAP Explainability  |        | Apache Spark         |
| Decision Policy      |        | Graph Analytics      |        | Spark MLlib          |
+----------------------+        +----------------------+        +----------------------+
```

Arsitektur ini mendukung beberapa kebutuhan utama:

1. Penyimpanan raw data sebagai source of truth.
2. Pemrosesan data secara batch untuk data historis.
3. Penyimpanan processed data dalam format efisien.
4. Machine learning untuk prediksi risiko default.
5. Graph analytics untuk analisis hubungan antar fitur dan risiko.
6. Dashboard interaktif untuk mendukung pengambilan keputusan.

## 3.2 Data Ingestion Methods

Metode ingestion yang digunakan adalah batch ingestion. Dataset diperoleh dari Kaggle dalam format `.csv.gz` menggunakan Kaggle API. Dataset terdiri dari dua file utama:

| Dataset | Jumlah Baris | Jumlah Kolom | Ukuran File | Format |
|---|---:|---:|---:|---|
| accepted_2007_to_2018Q4.csv.gz | 2.260.701 | 151 | 375 MB | CSV terkompresi |
| rejected_2007_to_2018Q4.csv.gz | 27.648.741 | 9 | 244 MB | CSV terkompresi |

Untuk mengatasi keterbatasan memori, digunakan strategi:

1. **Column pruning** — hanya kolom relevan yang digunakan.
2. **Chunking** — data dapat dimuat bertahap dalam potongan baris.
3. **Compression-aware loading** — membaca langsung dari file `.csv.gz`.
4. **Persistent output** — hasil analisis disimpan ke file CSV agar dashboard dapat berjalan tanpa memuat ulang raw data besar.

Pada skenario produksi, ingestion layer dapat dikembangkan menggunakan:

- Apache Kafka untuk streaming aplikasi pinjaman real-time.
- Apache Flume atau cloud ingestion service untuk data batch besar.
- Apache Airflow untuk orkestrasi pipeline ingestion harian atau bulanan.

## 3.3 Storage Technologies

Teknologi penyimpanan dirancang menggunakan pendekatan berlapis.

| Layer | Teknologi Prototype | Teknologi Produksi | Fungsi |
|---|---|---|---|
| Raw Layer | Google Drive / local file system | Amazon S3 / Google Cloud Storage / HDFS | Menyimpan data mentah tanpa modifikasi |
| Processed Layer | Apache Parquet / CSV output | Parquet on Data Lake / BigQuery / Hive | Menyimpan data hasil cleaning dan transformasi |
| Model Layer | Pickle / model object | MLflow Model Registry | Menyimpan model machine learning |
| Result Layer | CSV summary files | Data mart / analytical database | Menyimpan hasil agregasi untuk dashboard |

Apache Parquet direkomendasikan untuk processed data karena:

1. Format kolumnar, sehingga hanya kolom yang diperlukan yang dibaca.
2. Kompresi lebih efisien dibanding CSV.
3. Kompatibel dengan Spark, Hive, BigQuery, dan berbagai engine analitik.
4. Mendukung partitioning berdasarkan `issue_year` untuk mempercepat query temporal.

## 3.4 Processing Framework

Framework utama yang digunakan adalah:

| Framework | Fungsi |
|---|---|
| Pandas | Data loading, preprocessing, feature engineering, EDA |
| NumPy | Representasi matriks fitur untuk machine learning |
| Scikit-learn | Logistic Regression, Random Forest, preprocessing, evaluation metrics |
| XGBoost | Model boosting utama untuk data tabular |
| Apache Spark / PySpark | Distributed processing dan Spark MLlib |
| Spark MLlib | Logistic Regression, Decision Tree, Random Forest, GBTClassifier |
| NetworkX | Graph analytics |
| SHAP | Explainable AI untuk interpretasi model |
| Streamlit + Plotly | Dashboard interaktif |

Apache Spark dipilih karena memiliki kemampuan in-memory processing, mendukung distributed computing, kompatibel dengan Parquet, serta menyediakan MLlib untuk machine learning berskala besar. Walaupun prototype dijalankan dalam mode local single-node, struktur kode Spark dapat dikembangkan ke cluster multi-node dengan perubahan minimal.

## 3.5 IT Governance Considerations

### 3.5.1 Security

Sistem credit scoring mengelola data finansial yang sensitif, sehingga perlu menerapkan keamanan berlapis:

1. Enkripsi data at rest menggunakan AES-256.
2. Enkripsi data in transit menggunakan TLS 1.3.
3. Role-Based Access Control untuk membatasi akses berdasarkan peran.
4. Audit trail untuk mencatat akses, perubahan, dan penghapusan data.
5. Pemisahan akses antara raw data dan data yang sudah dianonimisasi.

### 3.5.2 Compliance

Sistem perlu mempertimbangkan regulasi berikut:

| Regulasi | Relevansi |
|---|---|
| FCRA | Transparansi penggunaan data kredit dan keputusan penolakan |
| ECOA | Larangan diskriminasi dalam keputusan kredit |
| GDPR | Hak penghapusan data, portabilitas data, dan dasar hukum pemrosesan |
| POJK P2P Lending | Perlindungan konsumen dan tata kelola platform pinjaman online |

Model juga perlu dijelaskan kepada stakeholder. Oleh karena itu, SHAP digunakan untuk membantu interpretasi faktor yang mendorong prediksi default.

### 3.5.3 Data Privacy

Privasi data dijaga melalui:

1. Anonimisasi dan pseudonimisasi PII.
2. Data minimization — hanya 26 dari 151 kolom accepted loans digunakan.
3. Penghapusan fitur yang tidak relevan atau berpotensi sensitif.
4. Retention policy agar data tidak disimpan lebih lama dari kebutuhan analisis.
5. Masking lokasi seperti zip code parsial.

### 3.5.4 Data Quality

Permasalahan kualitas data yang ditemukan meliputi:

| Masalah | Contoh | Penanganan |
|---|---|---|
| Missing values | Risk Score, Employment Length | Median imputation dan kategori `Unknown` |
| Outlier | DTI ekstrem, annual income sangat tinggi | Clipping dan winsorization |
| Format tidak konsisten | `int_rate` berisi `%`, `term` berisi `months` | Type conversion dan regex extraction |
| Skema berbeda | Accepted 151 kolom, rejected 9 kolom | Pipeline terpisah dan pemanfaatan berbeda |
| Class imbalance | Default hanya 13,02% | Undersampling pada training set |

---

# 4. DATA PROCESS AND ANALYSIS MODEL

## 4.1 Data Acquisition

Data yang digunakan adalah Lending Club Loan Data periode 2007–2018 dari Kaggle. Dataset ini dipilih karena:

1. Bersifat real-world dan berskala besar.
2. Memiliki data accepted dan rejected loans.
3. Memuat atribut pinjaman, profil peminjam, histori kredit, dan status pinjaman.
4. Memiliki target variable yang dapat digunakan untuk supervised learning.
5. Relevan dengan permasalahan credit scoring pada P2P lending.

Proses akuisisi dilakukan melalui Kaggle API. Data disimpan dalam format `.csv.gz` agar ukuran file lebih kecil dan mudah dipindahkan. Dataset accepted digunakan sebagai sumber utama machine learning karena memiliki `loan_status`, sedangkan rejected digunakan sebagai pendukung analisis graph dan insight bisnis.

## 4.2 Data Elements and Formats

Dataset accepted loans memiliki 151 atribut, namun hanya 26 atribut utama yang dipilih untuk efisiensi dan relevansi analisis. Setelah feature engineering, total fitur model menjadi 29 fitur.

### 4.2.1 Structured Data

Structured data adalah data berbentuk tabel dengan skema jelas. Contohnya:

| Kolom | Tipe | Deskripsi |
|---|---|---|
| loan_amnt | Numerik | Jumlah pinjaman |
| funded_amnt | Numerik | Jumlah pinjaman yang didanai |
| int_rate | Numerik | Suku bunga |
| installment | Numerik | Cicilan bulanan |
| annual_inc | Numerik | Pendapatan tahunan |
| dti | Numerik | Debt-to-income ratio |
| fico_range_low | Numerik | Batas bawah skor FICO |
| fico_range_high | Numerik | Batas atas skor FICO |
| loan_status | Kategorikal | Status akhir pinjaman |

### 4.2.2 Semi-Structured Data

Beberapa data memiliki format string yang perlu diproses sebelum menjadi numerik:

| Kolom | Contoh | Transformasi |
|---|---|---|
| term | `36 months` | `term_months = 36` |
| emp_length | `10+ years` | `emp_length_num = 10` |
| issue_d | `Dec-2015` | `issue_year = 2015`, `issue_month = 12` |
| revol_util | `55.3%` | `revol_util = 55.3` |

### 4.2.3 Unstructured Data

Kolom `desc` berisi deskripsi pinjaman dalam bentuk teks bebas. Dalam proyek ini, kolom tersebut tidak digunakan dalam model utama karena fokus analisis berada pada fitur tabular. Namun, pada pengembangan selanjutnya, kolom ini dapat diolah menggunakan NLP untuk mengekstraksi sinyal risiko tambahan.

## 4.3 Data Cleaning and Organization

Tahapan data cleaning dilakukan sebagai berikut:

1. **Target variable transformation**  
   Kolom `loan_status` diubah menjadi target biner `is_default`.

   Status yang dianggap default:
   - Charged Off
   - Default
   - Late (31–120 days)
   - Late (16–30 days)

2. **Type conversion**  
   Kolom `term`, `int_rate`, `revol_util`, `issue_d`, dan `emp_length` dikonversi ke format numerik atau temporal.

3. **Missing value handling**  
   - Numerik: imputasi median.
   - Kategorikal: imputasi `Unknown`.

4. **Outlier handling**  
   - `annual_inc` dibatasi pada persentil ke-99.
   - `dti` dan `revol_util` dibatasi pada rentang 0–100.

5. **Feature engineering**  
   Fitur baru yang dibuat:
   - `fico_avg`
   - `credit_utilization`
   - `loan_to_income`
   - `installment_to_income`
   - `total_risk_indicators`
   - `issue_year`
   - `issue_month`

6. **Encoding categorical variables**  
   Fitur kategorikal seperti `grade`, `sub_grade`, `home_ownership`, `verification_status`, `purpose`, `addr_state`, dan `application_type` diubah ke format numerik menggunakan label encoding.

7. **Time-based train-test split**  
   Untuk menghindari temporal leakage:
   - Train: 2007–2016
   - Test: 2017–2018

8. **Class imbalance handling**  
   Training set diseimbangkan menggunakan random undersampling pada kelas non-default.

## 4.4 Data Model Selection

Model data yang digunakan adalah flat-file tabular model atau denormalized wide table. Setiap baris merepresentasikan satu pinjaman, sedangkan setiap kolom merepresentasikan fitur pinjaman atau peminjam.

Alasan pemilihan model data ini:

1. Sesuai dengan karakteristik dataset Lending Club.
2. Efisien untuk machine learning karena tidak membutuhkan join antar tabel.
3. Mudah diproses oleh Pandas, Spark, Scikit-learn, dan XGBoost.
4. Cocok untuk penyimpanan dalam format Parquet.
5. Mendukung feature engineering secara langsung.

Pipeline representasi data:

```text
Raw CSV.GZ
   ↓
Pandas DataFrame
   ↓
Cleaned and Feature-Engineered DataFrame
   ↓
Apache Parquet / CSV Output
   ↓
NumPy Array / Spark DataFrame
   ↓
Machine Learning Model Input
```

## 4.5 Machine Learning Pipeline

### 4.5.1 Feature Engineering

Fitur utama yang digunakan dikelompokkan sebagai berikut:

| Kelompok Fitur | Contoh Fitur | Tujuan |
|---|---|---|
| Loan characteristics | loan_amnt, funded_amnt, term_months, installment | Mengukur karakteristik pinjaman |
| Credit quality | grade, sub_grade, fico_avg, int_rate | Menilai kualitas kredit |
| Debt burden | dti_clean, loan_to_income, installment_to_income | Mengukur beban utang relatif terhadap pendapatan |
| Credit history | delinq_2yrs, pub_rec, total_acc, open_acc | Mengukur histori kredit |
| Borrower profile | annual_inc_clean, emp_length_num, home_ownership | Menggambarkan profil peminjam |
| Temporal | issue_year, issue_month | Menangkap pola waktu |

### 4.5.2 Algorithm Selection

Algoritma yang digunakan:

| Algoritma | Framework | Alasan Pemilihan |
|---|---|---|
| Logistic Regression | Scikit-learn | Baseline, cepat, interpretabel |
| Random Forest | Scikit-learn | Mampu menangkap non-linearitas dan robust terhadap overfitting |
| XGBoost | XGBoost | Performa tinggi untuk data tabular |
| Logistic Regression | Spark MLlib | Baseline distributed model |
| Decision Tree | Spark MLlib | Model tree sederhana di Spark |
| Random Forest | Spark MLlib | Ensemble distributed |
| GBTClassifier | Spark MLlib | Gradient boosting pada framework Spark |

XGBoost dipilih sebagai model terbaik karena memberikan AUC-ROC tertinggi sebesar 0,7109. Spark MLlib digunakan sebagai scalable option untuk menunjukkan kesiapan pipeline terhadap lingkungan Big Data yang lebih besar.

### 4.5.3 Model Evaluation

Metrik evaluasi yang digunakan:

| Metrik | Fungsi |
|---|---|
| Accuracy | Mengukur proporsi prediksi benar secara keseluruhan |
| Precision | Mengukur seberapa banyak prediksi default yang benar |
| Recall | Mengukur kemampuan model mendeteksi kasus default |
| F1-Score | Harmonic mean antara precision dan recall |
| F2-Score | Lebih menekankan recall, cocok untuk credit risk |
| AUC-ROC | Mengukur kemampuan model membedakan default dan non-default |

Hasil model:

| Model | Accuracy | Precision | Recall | F1 | AUC-ROC | Train Time |
|---|---:|---:|---:|---:|---:|---:|
| XGBoost | 0,6209 | 0,1202 | 0,6906 | 0,2048 | 0,7109 | 2,86s |
| Random Forest | 0,6424 | 0,1209 | 0,6473 | 0,2038 | 0,7031 | 2,84s |
| Logistic Regression | 0,6618 | 0,1212 | 0,6051 | 0,2019 | 0,6920 | 1,17s |
| GBTClassifier Spark | 0,6602 | 0,1244 | 0,6304 | 0,2078 | 0,6464 | 33,71s |
| RandomForest Spark | 0,6410 | 0,1206 | 0,6484 | 0,2034 | 0,6444 | 6,73s |
| DecisionTree Spark | 0,6249 | 0,1169 | 0,6569 | 0,1985 | 0,6397 | 1,63s |
| LogisticRegression Spark | 0,6563 | 0,1196 | 0,6069 | 0,1998 | 0,6335 | 7,34s |

## 4.6 Graph Analytics

Graph analytics digunakan untuk memahami hubungan struktural antar fitur dan risiko kredit.

### 4.6.1 Feature Correlation Network

Pada graph ini, fitur numerik direpresentasikan sebagai node, sedangkan edge menunjukkan korelasi antar fitur. Hubungan kuat ditemukan pada:

1. `fico_range_low`, `fico_range_high`, dan `fico_avg`.
2. `loan_amnt`, `funded_amnt`, dan `installment`.
3. Hubungan negatif antara FICO score dan interest rate.

Insight utama: beberapa fitur memiliki redundansi informasi, sedangkan interest rate dan grade merepresentasikan risk-based pricing.

### 4.6.2 Borrower Similarity Bipartite Graph

Graph ini membandingkan sampel accepted dan rejected borrowers berdasarkan fitur seperti FICO, DTI, dan loan amount. Analisis menunjukkan adanya peminjam yang secara karakteristik mirip dengan accepted borrowers namun berada pada kelompok rejected. Hal ini menunjukkan potensi false rejection dan peluang untuk second-chance review.

### 4.6.3 Grade Risk Hierarchy

Graph ini menunjukkan hubungan hierarkis antara Grade A hingga G. Default rate meningkat secara konsisten:

| Grade | Default Rate | Avg Interest Rate | Avg FICO |
|---|---:|---:|---:|
| A | 3,66% | 7,08% | 729,0 |
| B | 8,79% | 10,68% | 699,8 |
| C | 14,57% | 14,14% | 689,3 |
| D | 20,59% | 18,14% | 684,0 |
| E | 28,46% | 21,83% | 682,4 |
| F | 36,51% | 25,45% | 680,4 |
| G | 39,74% | 28,07% | 679,2 |

Insight utama: Grade berhasil memetakan risiko secara konsisten, tetapi perbedaan FICO antar grade menengah hingga tinggi relatif kecil. Ini menunjukkan bahwa risiko kredit bersifat multifaktor.

---

# 5. VISUALIZATION AND INSIGHTS

## 5.1 Dashboard Design

Untuk memenuhi kebutuhan visualization and insights, dibuat dashboard interaktif menggunakan Streamlit dan Plotly. Dashboard ini tidak memerlukan raw dataset besar, karena menggunakan tiga file hasil notebook:

1. `model_results.csv`
2. `feature_importance.csv`
3. `grade_statistics.csv`

Dashboard dapat dijalankan dengan:

```bash
pip install streamlit plotly pandas numpy
streamlit run dashboard.py
```

Pendekatan ini dipilih karena notebook tidak perlu dijalankan ulang. Raw data Lending Club berukuran besar dan proses training memakan waktu. Dengan menyimpan hasil agregasi ke CSV, dashboard tetap dapat menampilkan insight utama secara interaktif tanpa memproses ulang dataset asli.

## 5.2 Visualization Components

Dashboard terdiri dari lima halaman utama.

### 5.2.1 Overview

Halaman ini menampilkan:

- Total accepted loans: 2.260.701
- Total rejected loans: 27.648.741
- Overall default rate: 13,02%
- Best model AUC-ROC: 0,7109
- Train period: 2007–2016
- Test period: 2017–2018

Tujuannya adalah memberikan ringkasan cepat untuk stakeholder non-teknis.

### 5.2.2 Model Performance

Halaman ini menampilkan:

- Bar chart perbandingan model berdasarkan metrik pilihan.
- Radar chart untuk tiga model terbaik.
- Tabel seluruh metrik evaluasi.
- Insight threshold tuning.

Visualisasi ini membantu tim risk management memilih model yang seimbang antara performa dan kebutuhan bisnis.

### 5.2.3 Feature Importance

Halaman ini menampilkan:

- Interactive bar chart feature importance dengan slider top-N.
- Pie chart kontribusi fitur berdasarkan kelompok.
- Tabel lengkap feature importance.

Insight utama:

1. `sub_grade` adalah fitur paling penting.
2. `grade` dan `int_rate` juga sangat dominan.
3. Fitur debt burden seperti `dti_clean` dan `installment_to_income` penting untuk menilai kemampuan bayar.

### 5.2.4 Grade Risk Analysis

Halaman ini menampilkan:

- Default rate berdasarkan grade.
- Average interest rate berdasarkan grade.
- Dual-axis chart antara volume pinjaman dan default rate.
- Tabel statistik grade.

Insight utama: semakin rendah grade, semakin tinggi default rate dan interest rate. Ini mendukung konsep risk-based pricing.

### 5.2.5 Business Insights

Halaman ini menampilkan:

- Cost-benefit analysis threshold.
- Rekomendasi loan approval policy.
- Risk-based pricing table.
- Portfolio strategy untuk investor.
- Development roadmap.

Halaman ini menghubungkan hasil teknis dengan keputusan strategis bisnis.

## 5.3 Key Analytical Insights

### Insight 1 — XGBoost menjadi model terbaik

XGBoost menghasilkan AUC-ROC tertinggi sebesar 0,7109. Hal ini menunjukkan bahwa model boosting mampu menangkap hubungan non-linear antar fitur risiko lebih baik dibandingkan Logistic Regression dan beberapa model Spark MLlib pada setup single-node.

### Insight 2 — Threshold default 0,5 tidak optimal untuk bisnis

Threshold optimal berdasarkan F2-score dan cost-based optimization adalah 0,471. Penyesuaian threshold ini menurunkan estimasi biaya sebesar 23,5%. Dalam konteks kredit, recall lebih penting karena gagal mendeteksi peminjam berisiko dapat menyebabkan kerugian besar.

### Insight 3 — Grade dan sub-grade adalah sinyal risiko utama

Feature importance menunjukkan bahwa `sub_grade`, `grade`, dan `int_rate` merupakan fitur paling berpengaruh. Hal ini menunjukkan bahwa sistem grading internal Lending Club sudah memiliki sinyal risiko kuat.

### Insight 4 — FICO score tidak cukup sebagai indikator tunggal

Walaupun FICO score penting, perbedaan FICO antar grade C hingga G relatif kecil, sementara default rate berbeda signifikan. Ini menunjukkan bahwa risiko kredit harus dinilai menggunakan kombinasi banyak fitur.

### Insight 5 — Graph analytics memperkuat interpretasi model

Feature correlation network dan grade risk hierarchy menunjukkan bahwa risiko kredit terbentuk dari hubungan antar fitur, bukan hanya kontribusi fitur secara individual. Graph analytics membantu menjelaskan struktur risiko secara lebih intuitif.

## 5.4 Business Narrative and Strategic Impact

Output model dapat digunakan dalam proses bisnis P2P lending sebagai berikut.

### 5.4.1 Loan Approval Policy

Model menghasilkan probabilitas default untuk setiap aplikasi pinjaman. Probabilitas ini dapat digunakan untuk menentukan keputusan:

| Predicted Default Probability | Rekomendasi Keputusan |
|---:|---|
| < 0,471 | Approve |
| 0,471–0,650 | Manual Review |
| > 0,650 | Reject atau minta mitigasi tambahan |

Kebijakan ini membantu platform mengurangi risiko false negative tanpa sepenuhnya menolak peminjam yang masih memiliki potensi layak.

### 5.4.2 Risk-Based Pricing

Model dapat digunakan untuk menentukan bunga berdasarkan risiko individual, bukan hanya grade umum.

| Risk Tier | Default Probability | Rekomendasi |
|---|---:|---|
| Very Low | < 10% | Bunga rendah, auto approve |
| Low | 10–20% | Approve dengan bunga standar |
| Medium | 20–35% | Approve dengan bunga lebih tinggi |
| High | 35–50% | Manual review atau syarat tambahan |
| Very High | > 50% | Reject atau mitigasi kuat |

### 5.4.3 Portfolio Strategy

Investor dapat menggunakan hasil model untuk mengatur portofolio:

| Strategi | Komposisi |
|---|---|
| Conservative | Dominan Grade A–B |
| Balanced | Kombinasi Grade B–D |
| Aggressive | Porsi lebih besar Grade D–F dengan diversifikasi tinggi |

### 5.4.4 Financial Inclusion

Model multifaktor memungkinkan platform mengevaluasi peminjam yang tidak memiliki riwayat kredit kuat. Jika dikembangkan dengan data alternatif, sistem ini dapat membantu peminjam unbanked memperoleh akses pembiayaan yang lebih adil.

---

# 6. SOLUTION EFFECTIVENESS EVALUATION AND DEVELOPMENT PLAN

## 6.1 Model Performance Evaluation

Berdasarkan hasil evaluasi, XGBoost menjadi model terbaik dengan performa berikut:

| Metric | Value |
|---|---:|
| Accuracy | 0,6209 |
| Precision | 0,1202 |
| Recall | 0,6906 |
| F1-Score | 0,2048 |
| F2-Score | 0,3544 |
| AUC-ROC | 0,7109 |
| Optimal Threshold | 0,471 |
| Training Time | 2,86 detik |

AUC-ROC 0,7109 menunjukkan bahwa model memiliki kemampuan cukup baik dalam membedakan pinjaman default dan non-default. Recall 0,6906 menunjukkan bahwa model mampu mendeteksi sekitar 69 dari 100 kasus default. Precision yang rendah disebabkan oleh class imbalance, karena proporsi default pada test set hanya sekitar 7,07%.

Spark MLlib menunjukkan performa lebih rendah dibandingkan XGBoost pada eksperimen ini. Hal ini wajar karena Spark dijalankan pada mode local single-node, sehingga overhead distributed computing belum memberikan keuntungan penuh. Namun, pipeline Spark tetap penting karena menunjukkan kesiapan sistem untuk scale ke cluster multi-node.

## 6.2 Business Effectiveness Evaluation

Evaluasi bisnis dilakukan dengan pendekatan cost-based threshold optimization. Dalam credit risk, false negative lebih berbahaya dibanding false positive. False negative berarti model gagal mendeteksi peminjam yang akan default, sedangkan false positive berarti model terlalu konservatif terhadap peminjam yang sebenarnya baik.

Asumsi cost matrix:

| Error Type | Dampak | Bobot Biaya |
|---|---|---:|
| False Positive | Peminjam layak ditolak | 1x |
| False Negative | Peminjam default disetujui | 5x |

Hasil threshold tuning:

| Threshold | Keterangan | Estimasi Cost |
|---:|---|---:|
| 0,500 | Default threshold | 414.897 |
| 0,471 | F2-optimal threshold | Lebih optimal untuk recall |
| 0,703 | Cost-optimal threshold | 317.293 |

Cost reduction:

```text
Cost Reduction = (414.897 - 317.293) / 414.897
               = 23,5%
```

Ini menunjukkan bahwa model tidak hanya memiliki nilai teknis, tetapi juga memberikan dampak bisnis nyata dalam mengurangi risiko kerugian kredit.

### 6.2.1 Comparison with Conventional Credit Scoring

| Aspek | Credit Scoring Konvensional | Solusi Big Data ML |
|---|---|---|
| Jumlah variabel | Terbatas | 29 fitur |
| Hubungan non-linear | Sulit ditangkap | Dapat ditangkap oleh ensemble model |
| Skalabilitas | Terbatas | Siap scale dengan Spark |
| Interpretabilitas | Tinggi, tetapi sederhana | SHAP explainability |
| Adaptabilitas | Lebih statis | Bisa retrain berkala |
| Business optimization | Umumnya threshold tetap | Threshold dapat dioptimalkan berbasis cost |

## 6.3 Limitations

Beberapa keterbatasan proyek:

1. **Data historis terbatas hingga 2018**  
   Model belum mencerminkan perubahan perilaku kredit setelah 2018, seperti pandemi COVID-19 atau perubahan ekonomi makro.

2. **Survivorship bias**  
   Pinjaman pada tahun 2017–2018 mungkin belum sepenuhnya jatuh tempo, sehingga default rate test set dapat lebih rendah dari risiko sebenarnya.

3. **Spark masih single-node**  
   Prototype Spark dijalankan pada mode local, bukan cluster penuh.

4. **Precision rendah**  
   Precision model masih rendah karena distribusi default sangat imbalanced.

5. **Belum menggunakan data alternatif**  
   Data seperti transaksi digital, perilaku pembayaran utilitas, atau data e-commerce belum digunakan.

6. **Dashboard menggunakan hasil agregasi**  
   Dashboard tidak memuat raw data besar agar ringan dijalankan, sehingga analisis interaktif terbatas pada hasil yang sudah disimpan.

## 6.4 Development Plan

### Phase 1 — Batch Scoring Deployment (0–3 bulan)

Tujuan: menerapkan model terbaik untuk scoring aplikasi pinjaman secara batch.

Aktivitas:

1. Menyimpan model XGBoost sebagai model artifact.
2. Membuat batch scoring script.
3. Mengintegrasikan output score ke risk management dashboard.
4. Menentukan threshold approval berdasarkan cost matrix.

Output:

- Batch scoring pipeline.
- Risk score untuk setiap aplikasi.
- Policy threshold awal.

### Phase 2 — Real-Time Scoring API (3–6 bulan)

Tujuan: menyediakan prediksi default secara real-time.

Aktivitas:

1. Membuat REST API menggunakan FastAPI.
2. Containerization menggunakan Docker.
3. Integrasi API dengan loan origination system.
4. Monitoring latency dan error rate.

Target:

- Latency prediksi < 1 detik.
- Keputusan kredit lebih cepat.

### Phase 3 — MLOps and Model Monitoring (6–9 bulan)

Tujuan: menjaga performa model setelah deployment.

Aktivitas:

1. Model registry menggunakan MLflow.
2. Monitoring data drift dan concept drift.
3. Retraining bulanan menggunakan Apache Airflow.
4. Validasi data menggunakan Great Expectations.

Target:

- Model performance degradation tidak lebih dari 5%.
- Pipeline retraining berjalan otomatis.

### Phase 4 — Alternative Data Integration (9–18 bulan)

Tujuan: meningkatkan prediksi untuk segmen unbanked.

Aktivitas:

1. Menambahkan data transaksi digital.
2. Menambahkan data perilaku pembayaran utilitas.
3. Menambahkan data e-commerce atau telco jika tersedia dan legal.
4. Mengevaluasi fairness dan bias model.

Target:

- Meningkatkan coverage peminjam tanpa histori kredit formal.
- Mendukung inklusi keuangan.

### Phase 5 — Advanced Graph and AI Development (18–36 bulan)

Tujuan: memperluas kemampuan analitik dengan metode lanjutan.

Aktivitas:

1. Mengembangkan Graph Neural Networks untuk mendeteksi pola jaringan risiko.
2. Menggunakan NLP pada deskripsi pinjaman.
3. Menerapkan federated learning antar institusi tanpa berbagi raw data.
4. Membangun explainability report otomatis untuk regulator.

Target:

- Sistem credit scoring lebih akurat, adil, dan compliant.
- Platform dapat menjadi penyedia credit intelligence berbasis Big Data.

---

# KESIMPULAN

Final Project ini menunjukkan bahwa pendekatan Big Data Analytics dapat digunakan untuk membangun sistem prediksi risiko kredit yang lebih akurat, skalabel, dan bernilai bisnis pada platform P2P lending. Dengan menggunakan dataset Lending Club berskala besar, pipeline yang dikembangkan mampu mencakup seluruh proses mulai dari ingestion, cleaning, feature engineering, machine learning, graph analytics, hingga dashboard interaktif.

Model XGBoost menjadi model terbaik dengan AUC-ROC 0,7109 dan recall 0,6906. Threshold tuning menunjukkan bahwa keputusan berbasis model dapat mengurangi estimasi biaya sebesar 23,5%. Graph analytics memperkuat interpretasi bahwa risiko kredit bersifat multifaktor dan tidak cukup dijelaskan oleh FICO score saja. Dashboard interaktif membantu menyampaikan hasil analitik kepada stakeholder bisnis dalam bentuk yang mudah dipahami.

Dengan pengembangan lebih lanjut melalui real-time scoring, MLOps, dan integrasi data alternatif, solusi ini berpotensi meningkatkan kualitas keputusan kredit, mengurangi risiko default, dan mendukung inklusi keuangan bagi segmen peminjam yang belum terlayani oleh sistem perbankan tradisional.
