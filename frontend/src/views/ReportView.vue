<template>
  <div :class="isDark ? 'dark' : ''">
    <div class="min-h-screen bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 transition-colors duration-300">
      <div class="max-w-[1100px] mx-auto px-4 sm:px-8 lg:px-12 py-8">

        <!-- Loading State -->
        <div v-if="loading" class="flex flex-col items-center justify-center h-[60vh] gap-4 animate-fade-in-up">
          <div class="w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin"></div>
          <p class="text-sm font-mono text-slate-500 dark:text-slate-400">Loading report for scan {{ scanId }}...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="flex flex-col items-center justify-center h-[50vh] gap-6 animate-fade-in-up">
          <div class="rounded-xl border border-red-300 dark:border-red-800/50 bg-white dark:bg-background-dark/50 p-8 text-center max-w-md">
            <span class="material-symbols-outlined text-5xl text-red-500 mb-4">error</span>
            <h2 class="text-xl font-bold text-red-500 font-mono mb-2">Error</h2>
            <p class="text-slate-600 dark:text-slate-400 mb-6">{{ error }}</p>
            <button @click="goHome" class="flex h-10 items-center justify-center rounded-lg px-6 bg-primary text-white text-sm font-bold hover:bg-primary/90 transition-all mx-auto">
              Go Back
            </button>
          </div>
        </div>

        <!-- Report Content -->
        <template v-else>
          <!-- Report Header -->
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8 pb-6 border-b border-primary/20 animate-fade-in-up">
            <div class="flex items-center gap-4">
              <button @click="goHome" class="flex items-center justify-center w-10 h-10 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-primary hover:text-white transition-all">
                <span class="material-symbols-outlined text-lg">arrow_back</span>
              </button>
              <div>
                <h1 class="text-2xl font-bold text-primary flex items-center gap-2">
                  <span class="material-symbols-outlined text-2xl">summarize</span>
                  Scan Report
                </h1>
                <p class="text-xs text-slate-500 dark:text-slate-400 font-mono mt-1">
                  Target: {{ reportData.target_url || '...' }} |
                  Duration: {{ formatDuration(reportData.duration_seconds) }} |
                  Agents: {{ reportData.agents?.length || 0 }}
                </p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button @click="toggleTheme" class="flex items-center justify-center w-10 h-10 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-primary hover:text-white transition-all">
                <span class="material-symbols-outlined text-lg">{{ isDark ? 'light_mode' : 'dark_mode' }}</span>
              </button>
              <button @click="goHome" class="flex h-10 items-center justify-center rounded-lg px-5 bg-primary text-white text-sm font-bold hover:bg-primary/90 transition-all shadow-lg shadow-primary/20">
                <span class="material-symbols-outlined text-lg mr-1">add</span>
                New Scan
              </button>
            </div>
          </div>

          <!-- Summary Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8 animate-fade-in-up animate-delay-200">
            <div class="rounded-xl border-t-4 border-t-red-500 border border-red-200 dark:border-red-800/30 bg-white dark:bg-background-dark/50 p-6 text-center hover:shadow-lg hover:shadow-red-500/5 transition-shadow">
              <div class="text-4xl font-bold font-mono text-red-500 mb-1">{{ reportData.summary?.logic_flaws || 0 }}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">Logic Flaws</div>
            </div>
            <div class="rounded-xl border-t-4 border-t-amber-500 border border-amber-200 dark:border-amber-800/30 bg-white dark:bg-background-dark/50 p-6 text-center hover:shadow-lg hover:shadow-amber-500/5 transition-shadow">
              <div class="text-4xl font-bold font-mono text-amber-500 mb-1">{{ reportData.summary?.security_issues || 0 }}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">Security Issues</div>
            </div>
            <div class="rounded-xl border-t-4 border-t-blue-500 border border-blue-200 dark:border-blue-800/30 bg-white dark:bg-background-dark/50 p-6 text-center hover:shadow-lg hover:shadow-blue-500/5 transition-shadow">
              <div class="text-4xl font-bold font-mono text-blue-500 mb-1">{{ reportData.summary?.performance_issues || 0 }}</div>
              <div class="text-xs text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold">Performance Hits</div>
            </div>
          </div>

          <!-- Report Body -->
          <div class="rounded-xl border border-primary/20 bg-white dark:bg-background-dark/50 p-6 sm:p-8 shadow-sm animate-fade-in-up animate-delay-300">

            <!-- AI-Generated Narrative Report -->
            <div v-if="reportData.report_markdown" class="prose-report" v-html="renderMarkdown(reportData.report_markdown)"></div>

            <!-- Findings Details (fallback if no markdown) -->
            <div v-else-if="findings.length > 0">
              <h3 class="text-lg font-bold text-primary mb-6 flex items-center gap-2">
                <span class="material-symbols-outlined">bug_report</span>
                Findings
              </h3>
              <div v-for="finding in findings" :key="finding.id"
                class="rounded-lg border p-5 mb-4 transition-all hover:shadow-md"
                :class="{
                  'border-l-4 border-l-red-500 border-red-200 dark:border-red-800/30 bg-red-50/50 dark:bg-red-900/5': finding.severity === 'critical',
                  'border-l-4 border-l-amber-500 border-amber-200 dark:border-amber-800/30 bg-amber-50/50 dark:bg-amber-900/5': finding.severity === 'high',
                  'border-l-4 border-l-yellow-500 border-yellow-200 dark:border-yellow-800/30 bg-yellow-50/50 dark:bg-yellow-900/5': finding.severity === 'medium',
                  'border-l-4 border-l-blue-500 border-blue-200 dark:border-blue-800/30 bg-blue-50/50 dark:bg-blue-900/5': finding.severity === 'low',
                }">
                <div class="flex items-center justify-between mb-3">
                  <h4 class="font-bold text-slate-900 dark:text-slate-100 font-mono text-sm">{{ finding.title }}</h4>
                  <span class="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-full"
                    :class="{
                      'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400': finding.severity === 'critical',
                      'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400': finding.severity === 'high',
                      'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400': finding.severity === 'medium',
                      'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400': finding.severity === 'low',
                    }">{{ finding.severity }}</span>
                </div>
                <p class="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">{{ finding.description }}</p>
                <div v-if="finding.evidence" class="mt-3 bg-[#0d0914] text-slate-300 rounded-lg p-4 font-mono text-xs border border-slate-700 overflow-x-auto whitespace-pre-wrap">{{ finding.evidence }}</div>
              </div>
            </div>

            <!-- No Findings -->
            <div v-else class="text-center py-12">
              <span class="material-symbols-outlined text-5xl text-green-500 mb-3">verified</span>
              <p class="text-lg text-green-500 font-semibold">No vulnerability findings detected during this scan.</p>
            </div>
          </div>
        </template>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const isDark = ref(true)

const scanId = ref('')
const loading = ref(true)
const error = ref('')
const reportData = ref({})
const findings = ref([])

const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
}

const goHome = () => {
  router.push('/')
}

const formatDuration = (seconds) => {
  if (!seconds) return 'N/A'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const renderMarkdown = (md) => {
  return md
    .replace(/^### (.*$)/gm, '<h4 class="text-base font-bold text-slate-900 dark:text-slate-100 mt-6 mb-3">$1</h4>')
    .replace(/^## (.*$)/gm, '<h3 class="text-lg font-bold text-primary mt-8 mb-4 pb-2 border-b border-primary/20">$1</h3>')
    .replace(/^# (.*$)/gm, '<h2 class="text-xl font-bold text-primary mt-10 mb-4">$1</h2>')
    .replace(/\*\*(.*?)\*\*/g, '<strong class="text-primary font-semibold">$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code class="bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded text-sm font-mono text-primary">$1</code>')
    .replace(/```[\s\S]*?```/g, (match) => {
      const code = match.replace(/```\w*\n?/g, '').replace(/```/g, '')
      return `<div class="bg-[#0d0914] text-slate-300 rounded-lg p-4 font-mono text-xs border border-slate-700 overflow-x-auto whitespace-pre-wrap my-4">${code}</div>`
    })
    .replace(/^- (.*$)/gm, '<li class="text-slate-700 dark:text-slate-300 mb-1 ml-4">$1</li>')
    .replace(/(<li>.*<\/li>)/s, '<ul class="list-disc pl-4 mb-4">$1</ul>')
    .replace(/\n\n/g, '</p><p class="text-slate-700 dark:text-slate-300 leading-relaxed mb-4">')
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
  isDark.value = document.documentElement.classList.contains('dark')

  if (!scanId.value) {
    error.value = 'No scan_id provided'
    loading.value = false
    return
  }

  try {
    const res = await fetch(`/api/scan/${scanId.value}`)
    const data = await res.json()
    if (data.status === 'completed') {
      await fetchReport()
    } else {
      await pollUntilReady()
    }
  } catch {
    await pollUntilReady()
  }
})
</script>
