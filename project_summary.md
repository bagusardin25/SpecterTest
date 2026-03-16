# 👻 SpecterTest — Project Summary

> *"Ratusan agen tak terlihat menembus sistem Anda, menemukan kelemahan yang manusia lewatkan."*

---

## 1. Mengapa SpecterTest?

Dari dua opsi nama — **Wuwei Engine** dan **SpecterTest** — dipilih **SpecterTest** berdasarkan pertimbangan:

| Kriteria | Wuwei Engine | **SpecterTest** ✅ |
|---|---|---|
| Mudah diingat | ❌ "Wuwei" asing bagi non-Chinese | ✅ Universal, catchy |
| Relevansi branding | ⚠️ Filosofis, tapi abstrak | ✅ Langsung menggambarkan produk |
| SEO & discoverability | ❌ Sulit dicari | ✅ "Specter" + "Test" = jelas |
| Vibe produk | Calm, zen | Mysterious, powerful, cybersecurity |
| Tagline potential | Terbatas | *"Ghost-test your app before hackers do"* |

**Specter** (hantu/bayangan) secara sempurna merepresentasikan agen-agen tak terlihat yang menembus routing, autentikasi, dan logika bisnis tanpa wujud fisik — persis seperti cara attacker sungguhan bekerja, tapi di pihak developer.

---

## 2. Konsep Aplikasi

### Problem Statement
Developer saat ini mengandalkan **static testing** (unit test, integration test) yang hanya menguji skenario yang *sudah diketahui*. Bug produksi justru muncul dari **kombinasi aksi tak terduga** — race condition, logic flaw, IDOR — yang hampir mustahil ditemukan tanpa simulasi realistis.

### Solusi: Behavioral Sandbox
SpecterTest menciptakan **Digital Twin** dari aplikasi web target, kemudian melepaskan ratusan agen AI dengan persona berbeda (pengguna biasa, admin, attacker) untuk mengeksplorasi, berinteraksi, dan **merusak** aplikasi secara bersamaan. Hasilnya adalah laporan analitik naratif tentang kelemahan yang ditemukan.

### Alur Kerja Utama

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. BINDING  │────▶│ 2. SPAWNING  │────▶│ 3. EXECUTION │────▶│  4. REPORT   │
│  Pemetaan    │     │  Buat Agen   │     │  Simulasi    │     │  Analisis    │
│  Target App  │     │  + Persona   │     │  Paralel     │     │  Naratif     │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **Binding** — User memasukkan URL target → sistem memetakan routes, DOM, dan endpoint
2. **Spawning** — Generate agen dengan role: User, Admin, Chaos/Attacker
3. **Execution** — Agen dilepas bersamaan, saling berkomunikasi saat menemukan celah
4. **Report** — AI menyusun laporan naratif tentang kelemahan yang ditemukan

---

## 3. Market Research

### Kompetitor: TestSprite

| Aspek | TestSprite | **SpecterTest** (Proposed) |
|---|---|---|
| Pendekatan | AI-powered test generation | Swarm Intelligence behavioral sandbox |
| Tipe testing | Functional & UI testing | Logic flaw, security, race condition |
| Agen | Single AI agent | Multi-agent swarm dengan persona berbeda |
| Output | Test cases + execution | Narasi analitik + attack replay log |
| Keunikan | Auto-generate test dari kode | Agen saling berkoordinasi menemukan celah |

### Celah Pasar yang Diisi SpecterTest
- TestSprite fokus pada **"apakah fitur bekerja?"** → SpecterTest fokus pada **"bagaimana fitur bisa dirusak?"**
- Belum ada tool yang menggabungkan **swarm intelligence + security testing + behavioral simulation** dalam satu platform
- Developer butuh tool yang menemukan **logic flaw** — bukan syntax error

---

## 4. MVP Scope

### Tech Stack

| Layer | Teknologi | Alasan |
|---|---|---|
| **Frontend** | Vue.js 3 + Vite | Reactive UI, cepat, cocok untuk dashboard real-time |
| **Styling** | Tailwind CSS | Utility-first, mempercepat styling, cocok untuk aesthetic cyber |
| **Backend** | Python + Flask | Ekosistem AI/ML terbaik, integrasi LLM mudah |
| **Agent Browser** | Playwright (Python) | Headless browser automation, multi-context paralel |
| **LLM** | OpenAI-compatible API | Fleksibel, bisa pakai Qwen/GPT/Claude/local LLM |
| **Real-time** | Server-Sent Events (SSE) | Streaming update simulasi ke frontend |
| **Database** | SQLite | Zero-config, cukup untuk MVP |
| **Package Manager** | uv (Python) + npm (Node) | Modern, cepat |

### Core Features MVP

#### ✅ Feature 1: Target Binding & Route Discovery
- Input URL target (localhost/staging)
- Auto-crawl dan petakan semua routes yang bisa diakses
- Deteksi form fields, auth pages, CRUD endpoints
- Visualisasi "peta dunia" aplikasi target

#### ✅ Feature 2: Agent Persona Generator
- Generate 3 tipe agen: **User**, **Admin**, **Attacker**
- Setiap agen punya behavior profile (kecepatan, agresivitas, pola interaksi)
- User bisa kustomisasi jumlah dan parameter agen
- MVP: mulai dari **5-10 agen** (scalable nanti)

#### ✅ Feature 3: Swarm Simulation Engine
- Jalankan semua agen secara paralel via Playwright
- Agen berkomunikasi: jika satu menemukan celah, yang lain ikut menyerang titik yang sama
- Real-time progress streaming ke frontend via SSE
- Durasi simulasi bisa dikonfigurasi (default: 5 menit untuk MVP)

#### ✅ Feature 4: Analytical Report Generator
- LLM menganalisis semua log interaksi agen
- Output: laporan naratif (bukan sekadar error log)
- Kategorisasi temuan: **Logic Flaw**, **Security Issue**, **Performance Issue**
- Severity rating per temuan (Critical / High / Medium / Low)

#### 🔮 Future Features (Post-MVP)
- Attack replay: *putar ulang* langkah-langkah agen menemukan bug
- CI/CD integration (GitHub Actions, GitLab CI)
- Support multi-framework (bukan hanya Laravel)
- Agent count scaling hingga 500+
- Custom attack scenario builder

---

## 5. Arsitektur MVP

```
┌─────────────────────────────────────────────┐
│            Frontend (Vue 3 + Vite)          │
│               Port 3000                     │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ Binding │ │ Sim View │ │ Report View  │ │
│  │  Page   │ │(realtime)│ │  (markdown)  │ │
│  └─────────┘ └──────────┘ └──────────────┘ │
└───────────────────┬─────────────────────────┘
                    │ REST API + SSE
                    ▼
┌─────────────────────────────────────────────┐
│          Backend (Flask + Python)            │
│               Port 5001                     │
│  ┌──────────────────────────────────────┐   │
│  │           API Layer (Flask)          │   │
│  ├──────────────────────────────────────┤   │
│  │  Route     │  Agent      │ Report   │   │
│  │  Crawler   │  Manager    │ Agent    │   │
│  ├──────────────────────────────────────┤   │
│  │      Playwright Engine (Headless)    │   │
│  ├──────────────────────────────────────┤   │
│  │   LLM Client (OpenAI-compatible)    │   │
│  ├──────────────────────────────────────┤   │
│  │         SQLite Database              │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    │
                    ▼ Playwright
┌─────────────────────────────────────────────┐
│        Target App (Laravel/Any Web)         │
│          localhost:8000 (contoh)             │
└─────────────────────────────────────────────┘
```

---

## 6. Positioning Statement

> **SpecterTest** adalah platform behavioral testing berbasis swarm intelligence yang melepaskan ratusan agen AI ke dalam aplikasi web Anda — menemukan logic flaw, celah keamanan, dan race condition yang tidak bisa ditemukan oleh unit test tradisional.
>
> *"Ghost-test your app before hackers do."* 👻
