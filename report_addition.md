# FINAL PROJECT — BIG DATA ANALYTICS
## Arsitektur Big Data untuk Prediksi Risiko Kredit pada Platform Peer-to-Peer Lending

**Nama:** Emmanuel Daniel W
**NIM:** 2702751271
**Course:** COMP8035041 — Big Data Analytics

---

## EXECUTIVE SUMMARY

Platform Peer-to-Peer (P2P) lending menghadapi tantangan fundamental dalam mengelola risiko kredit secara akurat dan skalabel. Data historis Lending Club periode 2007–2018 menunjukkan tingkat gagal bayar (default) sebesar 13,02% dari 2,26 juta pinjaman yang disetujui, dengan kerugian yang dapat mencapai ratusan juta dolar jika tidak dikelola dengan baik. Sistem credit scoring konvensional berbasis skor FICO terbukti tidak memadai karena hanya mempertimbangkan variabel terbatas dan tidak mampu menangkap hubungan non-linear antar faktor risiko.

Penelitian ini merancang dan mengimplementasikan pipeline Big Data end-to-end untuk memprediksi risiko gagal bayar pada platform P2P lending. Solusi yang dibangun mencakup arsitektur Data Lakehouse berbasis Apache Spark, pipeline machine learning dengan tujuh algoritma (sklearn dan Spark MLlib), serta sistem visualisasi interaktif berbasis Streamlit.

Hasil utama penelitian menunjukkan bahwa model XGBoost mencapai AUC-ROC 0,7109 dengan F2-Score 0,3544 menggunakan threshold optimal 0,471. Optimasi threshold berbasis cost-benefit analysis menghasilkan pengurangan biaya bisnis sebesar 23,5% dibandingkan threshold default 0,5. Analisis SHAP mengkonfirmasi bahwa kombinasi grade rendah, interest rate tinggi, dan rasio cicilan terhadap pendapatan yang besar merupakan indikator utama risiko default.

Dari perspektif bisnis, implementasi model ini berpotensi menghemat biaya kredit macet secara signifikan, meningkatkan kualitas portofolio pinjaman, dan mendukung inklusi keuangan bagi segmen peminjam yang selama ini tidak terlayani oleh perbankan tradisional. Roadmap pengembangan mencakup deployment real-time scoring API, pipeline retraining otomatis, dan integrasi data alternatif untuk memperluas jangkauan ke segmen unbanked.

---

## BAB I — ANALISIS MASALAH DAN BUSINESS DRIVERS

### 1.1 Latar Belakang dan Urgensi Masalah

Akses terhadap pembiayaan merupakan fondasi pertumbuhan ekonomi, namun jutaan individu masih kesulitan memperoleh kredit dari lembaga keuangan formal akibat keterbatasan sistem credit scoring konvensional. Sistem berbasis skor FICO hanya mempertimbangkan variabel terbatas seperti riwayat pembayaran, jumlah utang, dan lama riwayat kredit — menghasilkan skor tunggal yang menjadi dasar keputusan kredit. Akibatnya, kelompok unbanked, pelaku usaha kecil, dan peminjam baru yang sebenarnya layak secara finansial sering kali ditolak.

Platform P2P lending muncul sebagai alternatif, namun pertumbuhannya menghasilkan volume data masif yang melampaui kemampuan metode analisis konvensional. Dataset Lending Club mencakup 29,9 juta record aplikasi pinjaman — memenuhi karakteristik Big Data 5V: Volume (29,9 juta record), Velocity (arus aplikasi terus meningkat), Variety (data terstruktur dan semi-terstruktur), Veracity (kualitas data tidak konsisten), dan Value (potensi insight untuk keputusan kredit).

**Urgensi:** Tingkat default 13,02% secara keseluruhan, mencapai 39,74% pada segmen Grade G, menunjukkan kebutuhan mendesak akan sistem prediksi risiko yang lebih akurat. Pertumbuhan industri dari 603 pinjaman (USD 4,79 juta) pada 2007 menjadi 495.242 pinjaman (USD 7,94 miliar) pada 2018 mempertegas skala permasalahan ini.

### 1.2 Market and Business Drivers

| Driver | Deskripsi | Dampak |
|--------|-----------|--------|
| Pertumbuhan Fintech | Volume pinjaman P2P tumbuh 1.000x dalam 11 tahun | Kebutuhan sistem scoring yang skalabel |
| Tekanan Regulasi | FCRA, ECOA, GDPR, OJK POJK 77/2016 | Sistem harus transparan, adil, akuntabel |
| Risiko Kredit Tinggi | Default rate 13,02%, Grade G mencapai 39,74% | Urgensi model prediksi yang akurat |
| Keunggulan Kompetitif | Kemampuan analitik data = diferensiasi platform | Investasi dalam Big Data Analytics |
| Inklusi Keuangan | Agenda World Bank & IFC untuk unbanked segment | Perluasan akses kredit berbasis data alternatif |
| Penurunan Biaya Cloud | AWS, GCP, Azure semakin terjangkau | Implementasi Big Data semakin feasible |

### 1.3 Pemangku Kepentingan

| Stakeholder | Peran | Kepentingan Utama |
|-------------|-------|-------------------|
| Peminjam (Borrowers) | Pengguna layanan kredit | Akses pembiayaan yang adil dan cepat |
| Investor (Lenders) | Penyedia modal | Return optimal dengan risiko terukur |
| Platform (LendingClub) | Penghubung ekosistem | Pertumbuhan bisnis + kualitas kredit |
| Regulator (OJK, CFPB, SEC) | Pengawas industri | Kepatuhan, transparansi, perlindungan konsumen |
| Tim Data Science | Implementor teknis | Pipeline yang andal dan reproducible |
| Komunitas Akademik | Validator metodologi | Rigor ilmiah dan inovasi metodologi |

### 1.4 Project Success Indicators (KPI)

| KPI | Baseline | Target | Hasil Aktual |
|-----|----------|--------|--------------|
| AUC-ROC Model Terbaik | 0,50 (random) | ≥ 0,70 | **0,7109 ✅** |
| F2-Score (recall-weighted) | — | ≥ 0,30 | **0,3544 ✅** |
| Pengurangan Biaya Kredit Macet | 0% | ≥ 15% | **23,5% ✅** |
| Recall Default Detection | — | ≥ 60% | **69,06% ✅** |
| Waktu Training (sklearn) | — | ≤ 10 detik | **2,86 detik ✅** |
| Skalabilitas (Spark MLlib) | Single-machine | Distributed-ready | **✅ Pipeline siap scale** |
| Interpretabilitas Model | Black-box | SHAP explainability | **✅ SHAP diimplementasikan** |

---

## BAB II — DESAIN ARSITEKTUR DAN PEMILIHAN TEKNOLOGI

### 2.1 Arsitektur Big Data End-to-End

Arsitektur yang dirancang mengikuti pola **Lambda Architecture** yang disederhanakan, dengan fokus pada batch processing untuk prototype dan kesiapan scale ke streaming di masa depan.

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                             │
│  Kaggle API (CSV.GZ) │ Platform Logs │ External Credit Bureau   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER                            │
│  Batch: Pandas Chunking (300K rows/iter)                        │
│  [Prod] Apache Kafka + Apache Flume                             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       STORAGE LAYER                             │
│  Raw Layer    → CSV.GZ (Data Lake — Google Drive / S3)          │
│  Processed    → Apache Parquet (Curated Zone — partisi by year) │
│  Model Store  → .pkl files (Model Registry)                     │
│  Results      → CSV (model_results, feature_importance, grades) │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PROCESSING LAYER                            │
│  Data Cleaning    → Pandas (imputation, outlier handling)       │
│  Feature Eng.     → Pandas + NumPy (29 features)                │
│  ML Training      → Scikit-learn + XGBoost + Spark MLlib        │
│  Graph Analytics  → NetworkX (correlation, hierarchy, bipartite)│
│  [Prod] Orchestration → Apache Airflow (DAG-based pipeline)     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVING LAYER                              │
│  Batch Scoring    → XGBoost model (.pkl)                        │
│  Dashboard        → Streamlit (interactive visualization)       │
│  [Prod] API       → FastAPI + Docker                            │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Justifikasi Pemilihan Teknologi

| Komponen | Teknologi Dipilih | Alternatif | Alasan Pemilihan |
|----------|-------------------|------------|------------------|
| Processing Engine | Apache Spark (PySpark) | Hadoop MapReduce, Dask | In-memory processing, native Parquet support, ekosistem MLlib lengkap |
| Storage Format | Apache Parquet | CSV, ORC, Avro | Kompresi 70–80% lebih kecil dari CSV, columnar read untuk query efisien |
| ML Framework | XGBoost + Scikit-learn | TensorFlow, PyTorch | Performa tinggi pada tabular data, training cepat, interpretable |
| Distributed ML | Spark MLlib | H2O.ai, Dask-ML | Native integration dengan Spark DataFrame, horizontal scalability |
| Explainability | SHAP | LIME, ELI5 | Model-agnostic, konsisten secara matematis (Shapley values) |
| Dashboard | Streamlit | Tableau, Power BI, Dash | Open-source, Python-native, deployment mudah |
| Orchestration (Prod) | Apache Airflow | Prefect, Luigi | DAG-based, monitoring built-in, komunitas besar |
| Storage (Prod) | Google Cloud Storage / S3 | HDFS, Azure Blob | Managed service, cost-efficient, integrasi cloud native |

### 2.3 IT Governance

**Security**
- Enkripsi at-rest: AES-256 untuk semua data tersimpan
- Enkripsi in-transit: TLS 1.3 untuk komunikasi antar komponen
- Access Control: Role-Based Access Control (RBAC) — analis hanya akses data teranonimisasi
- Audit Trail: Log seluruh aktivitas akses dan modifikasi data, immutable storage

**Compliance**
- FCRA (Fair Credit Reporting Act): Transparansi keputusan penolakan kredit
- ECOA (Equal Credit Opportunity Act): Tidak ada diskriminasi berbasis ras, gender, usia — fitur sensitif dieksklusi
- GDPR: Right to erasure, data portability, lawful basis for processing
- OJK POJK 77/2016: Perlindungan konsumen dan tata kelola data P2P lending Indonesia

**Data Privacy**
- Anonimisasi PII: Nama, nomor identitas, alamat lengkap dihapus dari pipeline
- Data Minimization: Hanya 26 dari 151 kolom digunakan (prinsip need-to-know)
- Partial masking: Kode pos hanya ditampilkan parsial (481xx)
- Retention Policy: Data dihapus dengan cryptographic erasure setelah masa retensi berakhir

**Data Quality Framework**

| Dimensi | Masalah Ditemukan | Penanganan |
|---------|-------------------|------------|
| Completeness | Missing values pada Risk Score, Employment Length | Median imputation (numerik), "Unknown" (kategorikal) |
| Accuracy | Outlier ekstrem DTI hingga 1.690.800% | Clipping (0–100%), Winsorization persentil 99 |
| Consistency | Format string pada int_rate ("13%"), emp_length ("10+ years") | Type conversion, mapping ke numerik |
| Validity | Nilai negatif pada DTI | Clip ke rentang valid |
| Uniqueness | Skema berbeda accepted vs rejected (151 vs 9 kolom) | Pipeline terpisah per subset |

---

## BAB III — PROSES DATA DAN MODEL ANALISIS

### 3.1 Identifikasi Format Data

| Tipe Data | Contoh Kolom | Format | Penanganan |
|-----------|-------------|--------|------------|
| Structured | loan_amnt, int_rate, fico_range_low | Numerik (float/int) | StandardScaler, clipping |
| Structured | grade, purpose, home_ownership | Kategorikal (string) | Label Encoding |
| Semi-structured | issue_d ("Jan-2015"), emp_length ("10+ years") | String dengan format khusus | Regex extraction, mapping |
| Temporal | issue_d | Date string | Ekstraksi issue_year, issue_month |
| Text (tidak digunakan) | desc (deskripsi pinjaman) | Free text | Dieksklusi dari ML pipeline |

### 3.2 Pipeline Transformasi Data

```
Raw CSV.GZ
    │
    ▼
[1] Column Pruning → 26 kolom dari 151 (accepted), 9 kolom (rejected)
    │
    ▼
[2] Target Engineering → loan_status → is_default (binary: 0/1)
    │
    ▼
[3] Type Conversion → term_months, int_rate (%), revol_util (%), emp_length_num
    │
    ▼
[4] Missing Value Imputation → median (numerik), "Unknown" (kategorikal)
    │
    ▼
[5] Outlier Handling → clipping DTI/revol_util (0–100%), winsorization annual_inc (p99)
    │
    ▼
[6] Feature Engineering → fico_avg, credit_utilization, loan_to_income,
    │                      installment_to_income, total_risk_indicators,
    │                      issue_year, issue_month
    ▼
[7] Encoding → Label Encoding untuk 7 fitur kategorikal
    │
    ▼
[8] Time-Based Split → Train: 2007–2016 | Test: 2017–2018
    │
    ▼
[9] Undersampling → Random undersampling kelas mayoritas (non-default) di training set
    │
    ▼
[10] Normalisasi → StandardScaler (fit pada train, transform pada val & test)
    │
    ▼
NumPy Array → Input Model Machine Learning (X: 29 fitur, y: is_default)
```

### 3.3 Pemilihan Model Data

Model data yang digunakan adalah **flat-file tabular (denormalized wide table)** — setiap baris merepresentasikan satu record pinjaman dengan seluruh atribut dalam satu tabel tanpa relasi join. Pendekatan ini dipilih karena:
- Efisiensi komputasi untuk ML (tidak perlu join)
- Kompatibel dengan semua framework ML (sklearn, XGBoost, Spark MLlib)
- Sesuai dengan karakteristik data transaksional P2P lending

---

## BAB IV — VISUALISASI DAN INSIGHTS

### 4.1 Dashboard Interaktif

Dashboard interaktif dibangun menggunakan **Streamlit + Plotly** dan dapat dijalankan dengan perintah:

```bash
pip install streamlit plotly pandas numpy
streamlit run dashboard.py
```

Dashboard terdiri dari 5 halaman:

| Halaman | Konten |
|---------|--------|
| Overview | Key metrics, project summary, data split strategy |
| Model Performance | Bar chart perbandingan model, radar chart, threshold insight |
| Feature Importance | Interactive bar chart (slider top-N), pie chart per group, full table |
| Grade Risk Analysis | Default rate per grade, volume vs default rate dual-axis, grade table |
| Business Insights | Cost-benefit analysis, loan approval policy, risk-based pricing, portfolio strategy, roadmap |

### 4.2 Business Narrative — Bagaimana Insight Mempengaruhi Kebijakan

**Insight 1: Grade adalah sinyal risiko terkuat**

Sub_grade dan grade merupakan dua fitur terpenting (14,9% dan 14,4% importance). Ini mengkonfirmasi bahwa sistem grading Lending Club sudah mengandung sinyal risiko yang kuat. Implikasi kebijakan: platform dapat menggunakan grade sebagai filter pertama dalam proses screening, sebelum menjalankan model ML yang lebih kompleks.

**Insight 2: Threshold optimal berbeda dari default 0,5**

Dengan asumsi false negative (missed default) 5x lebih mahal dari false positive (rejected good borrower), threshold optimal adalah 0,471 — bukan 0,5. Penggunaan threshold ini menghasilkan pengurangan biaya 23,5%. Implikasi kebijakan: tim risk management harus menetapkan threshold berdasarkan cost matrix bisnis, bukan nilai default statistik.

**Insight 3: Grade D–E adalah sweet spot portofolio**

Grade D–E memiliki volume besar (460.063 pinjaman), return tinggi (18–22%), namun default rate 20–28%. Dengan model ML yang akurat, platform dapat mengidentifikasi peminjam Grade D–E yang berisiko rendah secara individual — membuka segmen yang selama ini dihindari secara keseluruhan. Implikasi kebijakan: strategi portofolio "balanced" dengan 40% Grade C–D dapat mengoptimalkan risk-adjusted return.

**Insight 4: FICO score bukan satu-satunya indikator**

Perbedaan FICO antar grade C–G relatif kecil (680–689), namun default rate berbeda signifikan (14,57%–39,74%). Ini menunjukkan bahwa keputusan kredit tidak bisa hanya bergantung pada FICO. Model ML yang mempertimbangkan 29 fitur secara simultan terbukti lebih akurat. Implikasi kebijakan: platform harus beralih dari single-score ke multi-factor scoring model.

**Insight 5: Lebih dari 30.000 peminjam skor tinggi ditolak**

Analisis bipartite graph menunjukkan adanya peminjam dengan skor kredit tinggi yang tetap ditolak. Ini mengindikasikan potensi false rejection yang merugikan inklusi keuangan. Implikasi kebijakan: model ML dapat digunakan untuk second-chance review pada aplikasi yang ditolak oleh sistem konvensional.

---

## BAB V — EVALUASI EFEKTIVITAS SOLUSI DAN RENCANA PENGEMBANGAN

### 5.1 Evaluasi Efektivitas Solusi

**Perbandingan Baseline vs Model ML**

| Aspek | Sistem Konvensional (FICO) | Sistem ML (XGBoost) | Improvement |
|-------|---------------------------|---------------------|-------------|
| Variabel yang dipertimbangkan | 5–7 variabel | 29 fitur | +314% |
| Kemampuan non-linear | Tidak | Ya (boosting) | Signifikan |
| AUC-ROC | ~0,60 (estimasi) | 0,7109 | +18,5% |
| Recall default detection | ~40% (estimasi) | 69,06% | +72,7% |
| Waktu keputusan | Hari (manual review) | < 1 detik (batch) | Drastis |
| Interpretabilitas | Tinggi (skor tunggal) | Tinggi (SHAP) | Setara |
| Skalabilitas | Rendah | Tinggi (Spark MLlib) | Signifikan |

**Estimasi Business Impact**

Dengan asumsi platform memproses 500.000 pinjaman per tahun dengan rata-rata nilai USD 15.000:
- Total portofolio: USD 7,5 miliar/tahun
- Default rate saat ini: 13,02% → potensi kerugian USD 976,5 juta
- Dengan model ML (recall 69,06%): dapat mendeteksi ~69% default sebelum terjadi
- Estimasi penghematan: USD 976,5 juta × 69,06% × asumsi recovery 30% = **USD 202 juta/tahun**
- Ditambah pengurangan biaya operasional dari otomasi: estimasi **USD 10–20 juta/tahun**

**Keterbatasan Solusi**

1. **Survivorship bias**: Pinjaman tahun 2017–2018 belum sepenuhnya jatuh tempo saat data dikumpulkan, sehingga default rate test set (7,07%) lebih rendah dari realita
2. **Concept drift**: Model dilatih pada data 2007–2016; kondisi ekonomi berubah (COVID-19, resesi) dapat menurunkan performa
3. **Single-node Spark**: Implementasi Spark MLlib pada single-node belum menunjukkan keunggulan distributed computing secara penuh
4. **Label imbalance**: Meskipun undersampling diterapkan, F1-Score masih rendah (0,20) karena imbalance yang ekstrem (7% default di test set)
5. **Fitur terbatas**: Tidak menggunakan data alternatif (perilaku digital, social media) yang berpotensi meningkatkan akurasi untuk segmen unbanked

### 5.2 Rencana Pengembangan (Development Roadmap)

**Phase 1 — Production Deployment (0–3 bulan)**
- Deploy model XGBoost sebagai batch scoring service
- Containerisasi dengan Docker
- Integrasi dengan sistem loan origination platform
- Target: Pengurangan biaya kredit macet 23,5%

**Phase 2 — Real-Time Scoring (3–6 bulan)**
- Bangun REST API menggunakan FastAPI
- Latency target: < 200ms per prediksi
- Implementasi Apache Kafka untuk streaming data
- A/B testing: model baru vs sistem lama
- Target: Keputusan kredit real-time < 1 detik

**Phase 3 — MLOps & Monitoring (6–9 bulan)**
- Pipeline retraining otomatis bulanan menggunakan Apache Airflow
- Model monitoring dengan MLflow (tracking drift, performance degradation)
- Data quality monitoring dengan Great Expectations
- Champion-challenger framework untuk model versioning
- Target: Model accuracy tidak turun > 5% dari baseline

**Phase 4 — Advanced Analytics (9–18 bulan)**
- Integrasi data alternatif: perilaku digital, e-commerce, telco data
- Graph Neural Networks untuk analisis jaringan peminjam
- Explainable AI yang lebih granular untuk regulatory compliance
- Ekspansi ke segmen unbanked menggunakan alternative credit scoring
- Target: Jangkauan ke 30% segmen yang sebelumnya tidak terlayani

**Phase 5 — Ecosystem Expansion (18–36 bulan)**
- Federated learning untuk kolaborasi antar platform tanpa berbagi data mentah
- Multi-modal model (teks, gambar dokumen, data numerik)
- Cross-border credit scoring untuk ekspansi regional Asia Tenggara
- Target: Platform menjadi credit infrastructure provider untuk fintech lain

---

*Dokumen ini merupakan tambahan konten untuk Final Project Big Data Analytics.*
*Konten teknis lengkap (implementasi, kode, output) tersedia di notebook: assignment_2_final.ipynb*
