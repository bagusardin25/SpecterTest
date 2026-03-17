<template>
  <div class="report-view">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p class="text-mono">Loading report for scan {{ scanId }}...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state glass-panel">
      <h2 class="text-mono">>> Error</h2>
      <p>{{ error }}</p>
      <button class="cyber-button" @click="goHome">Go Back</button>
    </div>

    <!-- Report Content -->
    <template v-else>
      <div class="report-header">
        <div class="title-area">
          <h2 class="text-mono">>> SPECTER_REPORT // GENERATED</h2>
          <p class="subtitle">
            Target: {{ reportData.target_url }} |
            Duration: {{ formatDuration(reportData.duration_seconds) }} |
            Agents: {{ reportData.agents?.length || 0 }}
          </p>
        </div>
        <div class="actions">
          <button class="cyber-button" @click="goHome">New Scan</button>
        </div>
      </div>

      <div class="report-content glass-panel">
        <div class="summary-cards">
          <div class="summary-card danger">
            <div class="count">{{ reportData.summary?.logic_flaws || 0 }}</div>
            <div class="label">Logic Flaws</div>
          </div>
          <div class="summary-card warning">
            <div class="count">{{ reportData.summary?.security_issues || 0 }}</div>
            <div class="label">Security Issues</div>
          </div>
          <div class="summary-card info">
            <div class="count">{{ reportData.summary?.performance_issues || 0 }}</div>
            <div class="label">Performance Hits</div>
          </div>
        </div>

        <!-- AI-Generated Narrative Report -->
        <div class="narrative-report" v-if="reportData.report_markdown">
          <div class="report-markdown" v-html="renderMarkdown(reportData.report_markdown)"></div>
        </div>

        <!-- Findings Details (fallback if no markdown) -->
        <div class="narrative-report" v-else-if="findings.length > 0">
          <h3>Findings</h3>
          <div v-for="finding in findings" :key="finding.id" class="finding-card" :class="finding.severity">
            <div class="finding-header">
              <h4>{{ finding.title }}</h4>
              <span class="badge" :class="getSeverityClass(finding.severity)">{{ finding.severity }}</span>
            </div>
            <p>{{ finding.description }}</p>
            <div v-if="finding.evidence" class="code-snippet text-mono">
              {{ finding.evidence }}
            </div>
          </div>
        </div>

        <!-- No Findings -->
        <div class="narrative-report" v-else>
          <h3>Results</h3>
          <p class="no-findings">✅ No vulnerability findings detected during this scan.</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const scanId = ref('')
const loading = ref(true)
const error = ref('')
const reportData = ref({})
const findings = ref([])

const goHome = () => {
  router.push('/')
}

const formatDuration = (seconds) => {
  if (!seconds) return 'N/A'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const getSeverityClass = (severity) => {
  switch (severity) {
    case 'critical': return 'red'
    case 'high': return 'orange'
    case 'medium': return 'yellow'
    case 'low': return 'blue'
    default: return 'gray'
  }
}

const renderMarkdown = (md) => {
  // Simple markdown to HTML converter for the report
  return md
    .replace(/^### (.*$)/gm, '<h4>$1</h4>')
    .replace(/^## (.*$)/gm, '<h3>$1</h3>')
    .replace(/^# (.*$)/gm, '<h2>$1</h2>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/```[\s\S]*?```/g, (match) => {
      const code = match.replace(/```\w*\n?/g, '').replace(/```/g, '')
      return `<div class="code-snippet text-mono">${code}</div>`
    })
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
}

const fetchReport = async () => {
  try {
    const response = await fetch(`/api/report/${scanId.value}`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    const data = await response.json()
    reportData.value = data

    // Also fetch findings separately for structured view
    const findingsRes = await fetch(`/api/report/${scanId.value}/findings`)
    if (findingsRes.ok) {
      const findingsData = await findingsRes.json()
      findings.value = findingsData.findings || []
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const pollUntilReady = async () => {
  // Poll scan status until report is ready
  const maxAttempts = 60
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const res = await fetch(`/api/scan/${scanId.value}`)
      if (res.ok) {
        const data = await res.json()
        if (data.status === 'completed' || data.status === 'error') {
          await fetchReport()
          return
        }
      }
    } catch {
      // ignore
    }
    await new Promise(resolve => setTimeout(resolve, 2000))
  }
  error.value = 'Report generation timed out'
  loading.value = false
}

onMounted(async () => {
  scanId.value = route.query.scan_id || ''

  if (!scanId.value) {
    error.value = 'No scan_id provided'
    loading.value = false
    return
  }

  // First try to fetch directly (report might already be ready)
  try {
    const res = await fetch(`/api/scan/${scanId.value}`)
    const data = await res.json()
    if (data.status === 'completed') {
      await fetchReport()
    } else {
      // Poll until ready
      await pollUntilReady()
    }
  } catch {
    await pollUntilReady()
  }
})
</script>

<style scoped>
.report-view {
  min-height: calc(100vh - 120px);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  gap: 1rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.error-state {
  padding: 2rem;
  text-align: center;
  max-width: 500px;
  margin: 4rem auto;
}

.error-state h2 { color: var(--danger-color); margin-bottom: 1rem; }
.error-state p { color: var(--text-secondary); margin-bottom: 2rem; }

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
.narrative-report h3,
.report-markdown :deep(h3) {
  color: var(--primary-color);
  border-bottom: 1px dashed rgba(159, 122, 234, 0.3);
  padding-bottom: 0.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.report-markdown :deep(h2) {
  color: var(--primary-color);
  margin-top: 2.5rem;
  margin-bottom: 1rem;
}

.report-markdown :deep(h4) {
  color: var(--text-primary);
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

.narrative-report p,
.report-markdown :deep(p) {
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  font-size: 1.05rem;
  line-height: 1.7;
}

.report-markdown :deep(ul) {
  list-style: disc;
  padding-left: 2rem;
  margin-bottom: 1rem;
}

.report-markdown :deep(li) {
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.report-markdown :deep(strong) {
  color: var(--primary-color);
}

.report-markdown :deep(code) {
  background: rgba(0, 0, 0, 0.4);
  padding: 0.1rem 0.4rem;
  border-radius: 3px;
  font-family: var(--font-mono);
  font-size: 0.9em;
  color: var(--accent-color);
}

.no-findings {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #27c93f;
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
.finding-card.medium { border-left-color: var(--accent-color); }
.finding-card.low { border-left-color: var(--text-muted); }

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
.badge.yellow { background: rgba(234, 179, 8, 0.2); color: #eab308; border: 1px solid #eab308; }
.badge.blue { background: rgba(59, 130, 246, 0.2); color: #3b82f6; border: 1px solid #3b82f6; }

.code-snippet {
  background: #0d0914;
  border: 1px solid #333;
  padding: 1rem;
  border-radius: var(--border-radius-sm);
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
  overflow-x: auto;
  white-space: pre-wrap;
}
</style>
