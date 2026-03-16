<template>
  <div class="report-view">
    <div class="report-header">
      <div class="title-area">
        <h2 class="text-mono">>> SPECTER_REPORT // GENERATED</h2>
        <p class="subtitle">Target: https://staging.myapp.com | Duration: 05:23 | Agents: 10</p>
      </div>
      <div class="actions">
        <button class="cyber-button" @click="goHome">New Scan</button>
        <button class="cyber-button info">Export PDF</button>
      </div>
    </div>

    <div class="report-content glass-panel">
      <div class="summary-cards">
        <div class="summary-card danger">
          <div class="count">3</div>
          <div class="label">Logic Flaws</div>
        </div>
        <div class="summary-card warning">
          <div class="count">1</div>
          <div class="label">Security Issues</div>
        </div>
        <div class="summary-card info">
          <div class="count">12</div>
          <div class="label">Performance Hits</div>
        </div>
      </div>

      <div class="narrative-report">
        <h3>1. Executive Summary</h3>
        <p>
          Simulasi memakan waktu 5 menit 23 detik dengan total 10 agen swarm yang bertindak secara otonom. 
          Hasil simulasi mengidentifikasi bahwa terdapat celah keamanan signifikan terkait <strong>Logic Flaw</strong> dan <strong>IDOR</strong>.
        </p>

        <h3>2. Critical Findings</h3>
        <div class="finding-card critical">
          <div class="finding-header">
            <h4>[FLAW-01] IDOR pada Endpoint Profil Pengguna</h4>
            <span class="badge red">Critical</span>
          </div>
          <p>
            Agen <code>ATK-02</code> menemukan bahwa Endpoint <code>/profile/{id}</code> tidak memvalidasi otorisasi dari user yang sedang login. 
            Hal ini memungkinkan agen untuk mengakses data pengguna lain dengan hanya mengubah parameter ID pada URL.
          </p>
          <div class="code-snippet text-mono">
            > GET /api/v1/profile/134 HTTP/1.1<br>
            > Authorization: Bearer {user_01_token}<br>
            <br>
            < HTTP/1.1 200 OK<br>
            < { "status": "success", "data": { "email": "admin@myapp.com" } }
          </div>
        </div>

        <div class="finding-card high">
          <div class="finding-header">
            <h4>[FLAW-02] Race Condition pada Endpoint Checkout</h4>
            <span class="badge orange">High</span>
          </div>
          <p>
            Agen <code>USR-01</code> dan <code>USR-04</code> melakukan checkout untuk item yang sama secara paralel di saat kuota hanya tersisa 1.
            Logika di backend untuk validasi ketersediaan stok gagal menangani serangan bersamaan sehingga stok akhir menjadi negatif.
          </p>
          <div class="code-snippet text-mono">
            > POST /api/v1/checkout<br>
            > {"item_id": 42, "qty": 1}<br>
            [Parallel execution from 2 distinct IP sessions]<br>
            < HTTP/1.1 200 OK (Both requests succeeded)
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.report-view {
  min-height: calc(100vh - 120px);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

.title-area h2 {
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.title-area .subtitle {
  color: var(--text-secondary);
  font-family: var(--font-mono);
  font-size: 0.9rem;
}

.actions {
  display: flex;
  gap: 1rem;
}

.cyber-button.info {
  border-color: var(--accent-color);
  color: var(--accent-color);
}
.cyber-button.info:hover {
  background: rgba(11, 197, 234, 0.1);
  box-shadow: var(--glow-accent);
}

.report-content {
  padding: 2rem;
}

.summary-cards {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.summary-card {
  flex: 1;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.summary-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
}

.summary-card.danger::before { background: var(--danger-color); }
.summary-card.warning::before { background: var(--warning-color); }
.summary-card.info::before { background: var(--accent-color); }

.summary-card .count {
  font-size: 3rem;
  font-family: var(--font-mono);
  font-weight: bold;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.summary-card.danger .count { color: var(--danger-color); text-shadow: var(--glow-danger); }
.summary-card.warning .count { color: var(--warning-color); }
.summary-card.info .count { color: var(--accent-color); }

.summary-card .label {
  color: var(--text-secondary);
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 1px;
}

/* Narrative */
.narrative-report h3 {
  color: var(--primary-color);
  border-bottom: 1px dashed rgba(159, 122, 234, 0.3);
  padding-bottom: 0.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.narrative-report p {
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  font-size: 1.05rem;
}

.finding-card {
  background: rgba(0,0,0,0.4);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border-left-width: 4px;
}

.finding-card.critical { border-left-color: var(--danger-color); }
.finding-card.high { border-left-color: var(--warning-color); }

.finding-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.finding-header h4 {
  margin: 0;
  font-family: var(--font-mono);
  color: var(--text-primary);
}

.badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.badge.red { background: rgba(252, 129, 129, 0.2); color: var(--danger-color); border: 1px solid var(--danger-color); }
.badge.orange { background: rgba(246, 173, 85, 0.2); color: var(--warning-color); border: 1px solid var(--warning-color); }

.code-snippet {
  background: #0d0914;
  border: 1px solid #333;
  padding: 1rem;
  border-radius: var(--border-radius-sm);
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
  overflow-x: auto;
}
</style>
