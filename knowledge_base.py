"""
Basis Pengetahuan – Sistem Pakar Diagnosis Kerusakan Bahan Makanan & Skincare
Forward Chaining
"""

# ─────────────────────────────────────────
# Daftar Semua Gejala
# ─────────────────────────────────────────

ALL_SYMPTOMS = [
    # Sayuran
    "sayur_layu",
    "tepi_kecoklatan",
    "sayur_layu_cepat",
    "buah_berair_lendir",
    # Daging
    "daging_pucat",
    "daging_cair_merah",
    "freezer_bau_amis",
    "kristal_es",
    # Susu
    "susu_basi_sebelum_exp",
    # Skincare
    "skincare_vit_c_berubah_warna",
    "skincare_pecah",
    # Herbal
    "herbal_gumpal",
    "bau_apek",
    # Kondisi Kulkas/Freezer
    "suhu_kulkas_diatas_5",
    "kulkas_sering_dibuka",
    "kulkas_penuh",
    "dekat_sayur_daun",
]

# ─────────────────────────────────────────
# Kelompok Gejala per Kategori (untuk UI)
# ─────────────────────────────────────────

SYMPTOM_GROUPS = {
    "Sayuran & Buah": {
        "icon": "fa-leaf",
        "color": "#10b981",
        "symptoms": [
            ("sayur_layu",          "Sayur tampak layu / tidak segar"),
            ("tepi_kecoklatan",     "Tepi/pinggir sayur berwarna kecoklatan"),
            ("sayur_layu_cepat",    "Sayur layu lebih cepat dari biasanya"),
            ("buah_berair_lendir",  "Buah berair dan berlendir"),
        ],
    },
    "Daging & Ikan": {
        "icon": "fa-drumstick-bite",
        "color": "#ef4444",
        "symptoms": [
            ("daging_pucat",        "Daging tampak pucat dan berubah warna"),
            ("kristal_es",          "Terdapat kristal es pada permukaan daging"),
            ("daging_cair_merah",   "Daging mengeluarkan cairan merah saat dicairkan"),
            ("freezer_bau_amis",    "Freezer berbau amis yang menyengat"),
        ],
    },
    "Produk Susu": {
        "icon": "fa-bottle-water",
        "color": "#f59e0b",
        "symptoms": [
            ("susu_basi_sebelum_exp", "Susu basi sebelum tanggal kedaluwarsa"),
        ],
    },
    "Skincare": {
        "icon": "fa-flask",
        "color": "#8b5cf6",
        "symptoms": [
            ("skincare_vit_c_berubah_warna", "Produk vitamin C berubah warna (kecoklatan/oranye)"),
            ("skincare_pecah",               "Tekstur produk pecah atau terpisah (emulsi rusak)"),
        ],
    },
    "Herbal & Kering": {
        "icon": "fa-seedling",
        "color": "#84cc16",
        "symptoms": [
            ("herbal_gumpal", "Herbal/rempah menggumpal"),
            ("bau_apek",      "Bau apek atau lembab pada produk kering"),
        ],
    },
    "Kondisi Penyimpanan": {
        "icon": "fa-refrigerator",
        "color": "#0ea5e9",
        "symptoms": [
            ("suhu_kulkas_diatas_5",  "Suhu kulkas di atas 5°C"),
            ("kulkas_sering_dibuka",  "Kulkas/freezer sering dibuka-tutup"),
            ("kulkas_penuh",          "Isi kulkas terlalu penuh"),
            ("dekat_sayur_daun",      "Buah/produk disimpan dekat sayur daun"),
        ],
    },
}

# ─────────────────────────────────────────
# Basis Aturan
# ─────────────────────────────────────────

RULES = [
    # ── 1 ──
    {
        "id": 1,
        "conditions": ["sayur_layu", "tepi_kecoklatan", "suhu_kulkas_diatas_5"],
        "conclusion": {
            "diagnosis": "Suhu penyimpanan terlalu tinggi untuk sayur daun",
            "saran":     "Turunkan suhu kulkas ke 2–4°C. Gunakan crisper drawer dan jangan letakkan sayur di dekat ventilasi udara dingin yang terlalu kuat.",
        },
    },
    # ── 2 ──
    {
        "id": 2,
        "conditions": ["daging_pucat", "kristal_es"],
        "conclusion": {
            "diagnosis": "Freezer burn akibat kemasan tidak kedap udara",
            "saran":     "Potong bagian yang rusak, gunakan vacuum seal atau wrapping aluminium foil berlapis. Pastikan semua udara keluar dari kemasan.",
        },
    },
    # ── 3 ──
    {
        "id": 3,
        "conditions": ["skincare_vit_c_berubah_warna"],
        "conclusion": {
            "diagnosis": "Vitamin C teroksidasi akibat paparan cahaya dan fluktuasi suhu",
            "saran":     "Pindahkan ke dry cabinet pada suhu stabil 20–25°C. Gunakan kemasan gelap dan tutup rapat setelah digunakan.",
        },
    },
    # ── 4 ──
    {
        "id": 4,
        "conditions": ["herbal_gumpal", "bau_apek"],
        "conclusion": {
            "diagnosis": "Kelembaban ruangan terlalu tinggi (>60% RH) menyebabkan absorbsi uap air",
            "saran":     "Pindahkan ke wadah kedap udara dengan silica gel. Simpan di tempat sejuk dan kering (suhu 10–15°C, RH <40%).",
        },
    },
    # ── 5 ──
    {
        "id": 5,
        "conditions": ["susu_basi_sebelum_exp", "kulkas_sering_dibuka"],
        "conclusion": {
            "diagnosis": "Fluktuasi suhu parah akibat kulkas sering dibuka",
            "saran":     "Jangan simpan susu di rak pintu kulkas. Letakkan di rak tengah atau belakang dengan suhu paling stabil (1–3°C).",
        },
    },
    # ── 6 ──
    {
        "id": 6,
        "conditions": ["buah_berair_lendir", "dekat_sayur_daun"],
        "conclusion": {
            "diagnosis": "Gas etilena dari sayur daun mempercepat pematangan dan pembusukan buah",
            "saran":     "Pisahkan ruang penyimpanan buah dan sayur. Gunakan laci crisper terpisah atau wadah tertutup.",
        },
    },
    # ── 7 ──
    {
        "id": 7,
        "conditions": ["freezer_bau_amis"],
        "conclusion": {
            "diagnosis": "Kemasan daging atau ikan tidak rapat sehingga kontaminasi bau menyebar",
            "saran":     "Gunakan wadah kedap udara atau vacuum bag untuk semua produk hewani. Bersihkan freezer dengan larutan baking soda.",
        },
    },
    # ── 8 ──
    {
        "id": 8,
        "conditions": ["skincare_pecah"],
        "conclusion": {
            "diagnosis": "Suhu terlalu dingin merusak formula emulsi (krim/lotion memisah)",
            "saran":     "Simpan di suhu ruang 20–22°C. Jangan masukkan produk emulsi ke kulkas atau freezer.",
        },
    },
    # ── 9 ──
    {
        "id": 9,
        "conditions": ["sayur_layu_cepat", "kulkas_penuh"],
        "conclusion": {
            "diagnosis": "Sirkulasi udara dingin terhambat akibat kulkas terlalu penuh",
            "saran":     "Atur ulang tata letak isi kulkas, jangan isi lebih dari 75% kapasitas. Beri ruang antar bahan agar udara bersirkulasi.",
        },
    },
    # ── 10 ──
    {
        "id": 10,
        "conditions": ["daging_cair_merah"],
        "conclusion": {
            "diagnosis": "Proses pembekuan lambat menyebabkan kristal es besar merusak jaringan daging",
            "saran":     "Bekukan daging dalam porsi kecil dan pipih (flat) agar membeku lebih cepat. Atur freezer ke suhu -18°C atau lebih rendah.",
        },
    },
    # ── 11 ──
    {
        "id": 11,
        "conditions": ["sayur_layu", "kulkas_penuh"],
        "conclusion": {
            "diagnosis": "Sayur layu karena suhu tidak merata dan kelembaban rendah di kulkas penuh",
            "saran":     "Kurangi isi kulkas dan simpan sayur dalam kantong plastik berlubang atau wadah tertutup dengan kertas tisu untuk menjaga kelembaban.",
        },
    },
    # ── 12 ──
    {
        "id": 12,
        "conditions": ["kristal_es", "kulkas_sering_dibuka"],
        "conclusion": {
            "diagnosis": "Bunga es berlebihan akibat uap air dari luar masuk setiap kali pintu dibuka",
            "saran":     "Kurangi frekuensi membuka kulkas/freezer. Lakukan defrost rutin dan periksa karet seal pintu apakah masih rapat.",
        },
    },
    # ── 13 ──
    {
        "id": 13,
        "conditions": ["susu_basi_sebelum_exp", "suhu_kulkas_diatas_5"],
        "conclusion": {
            "diagnosis": "Suhu kulkas terlalu tinggi mempercepat pertumbuhan bakteri pada produk susu",
            "saran":     "Pastikan suhu bagian susu berada di 1–3°C. Periksa termometer kulkas dan jangan letakkan susu di rak pintu.",
        },
    },
    # ── 14 ──
    {
        "id": 14,
        "conditions": ["herbal_gumpal"],
        "conclusion": {
            "diagnosis": "Herbal menyerap kelembaban dari udara sekitar",
            "saran":     "Simpan dalam wadah kaca kedap udara dengan silica gel. Jauhkan dari kompor atau sumber panas.",
        },
    },
    # ── 15 ──
    {
        "id": 15,
        "conditions": ["buah_berair_lendir"],
        "conclusion": {
            "diagnosis": "Buah membusuk karena suhu penyimpanan tidak optimal atau terlalu lama disimpan",
            "saran":     "Periksa dan sortir buah secara rutin. Simpan buah lunak pada 4–8°C dan konsumsi dalam 3–5 hari.",
        },
    },
    # ── 16 ──
    {
        "id": 16,
        "conditions": ["daging_pucat", "suhu_kulkas_diatas_5"],
        "conclusion": {
            "diagnosis": "Daging mengalami oksidasi mioglobin akibat suhu penyimpanan terlalu tinggi",
            "saran":     "Turunkan suhu kulkas ke 0–2°C untuk daging segar. Jika tidak segera dimasak, bekukan pada -18°C.",
        },
    },
]
