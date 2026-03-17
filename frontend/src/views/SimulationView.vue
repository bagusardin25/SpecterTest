<template>
  <div :class="isDark ? 'dark' : ''">
    <div class="min-h-screen bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 transition-colors duration-300">
      <div class="max-w-[1400px] mx-auto px-4 sm:px-8 lg:px-12 py-8">

        <!-- Header -->
        <div class="flex items-center justify-between mb-8 animate-fade-in-up">
          <div class="flex items-center gap-4">
            <button @click="$router.push('/')" class="flex items-center justify-center w-10 h-10 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-primary hover:text-white transition-all">
              <span class="material-symbols-outlined text-lg">arrow_back</span>
            </button>
            <div>
              <h1 class="text-2xl font-bold text-primary flex items-center gap-2">
                <span class="material-symbols-outlined text-2xl">radar</span>
                Simulation in Progress
              </h1>
              <p class="text-sm text-slate-500 dark:text-slate-400 font-mono mt-1">scan_id: {{ scanId || '...' }}</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button @click="toggleTheme" class="flex items-center justify-center w-10 h-10 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-primary hover:text-white transition-all">
              <span class="material-symbols-outlined text-lg">{{ isDark ? 'light_mode' : 'dark_mode' }}</span>
            </button>
            <button @click="abortSimulation" class="flex h-10 items-center justify-center rounded-lg px-5 bg-red-600 hover:bg-red-700 text-white text-sm font-bold transition-all shadow-lg shadow-red-600/20">
              <span class="material-symbols-outlined text-lg mr-1">cancel</span>
              ABORT
            </button>
          </div>
        </div>

        <!-- Dashboard Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-fade-in-up animate-delay-200">

          <!-- Swarm Metrics -->
          <div class="lg:col-span-1 rounded-xl border border-primary/20 bg-white dark:bg-background-dark/50 p-6 shadow-sm">
            <h3 class="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
              <span class="material-symbols-outlined text-primary text-lg">monitoring</span>
              Swarm Metrics
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div class="rounded-lg bg-slate-100 dark:bg-slate-800/60 p-4 text-center border border-transparent hover:border-primary/30 transition-colors">
                <div class="text-3xl font-bold font-mono text-primary">{{ totalAgents }}</div>
                <div class="text-xs text-slate-500 dark:text-slate-400 uppercase mt-1">Total Agents</div>
              </div>
              <div class="rounded-lg bg-slate-100 dark:bg-slate-800/60 p-4 text-center border border-transparent hover:border-primary/30 transition-colors">
                <div class="text-3xl font-bold font-mono text-primary">{{ totalRoutes }}</div>
                <div class="text-xs text-slate-500 dark:text-slate-400 uppercase mt-1">Routes</div>
              </div>
              <div class="rounded-lg bg-red-50 dark:bg-red-900/10 p-4 text-center border border-red-200 dark:border-red-800/30">
                <div class="text-3xl font-bold font-mono text-red-500">{{ flawsFound }}</div>
                <div class="text-xs text-slate-500 dark:text-slate-400 uppercase mt-1">Flaws Found</div>
              </div>
              <div class="rounded-lg bg-amber-50 dark:bg-amber-900/10 p-4 text-center border border-amber-200 dark:border-amber-800/30">
                <div class="text-3xl font-bold font-mono text-amber-500">{{ securityIssues }}</div>
                <div class="text-xs text-slate-500 dark:text-slate-400 uppercase mt-1">Security Issues</div>
              </div>
            </div>

            <!-- Status -->
            <div class="mt-4 px-4 py-3 rounded-lg bg-slate-100 dark:bg-slate-800/60 font-mono text-sm flex items-center gap-2">
              <span class="text-slate-500 dark:text-slate-400">STATUS:</span>
              <span :class="statusColor" class="font-bold uppercase">{{ scanStatus }}</span>
              <span v-if="scanStatus === 'executing'" class="inline-block w-2 h-2 rounded-full bg-amber-400 animate-pulse ml-1"></span>
            </div>
          </div>

          <!-- Agent Matrix -->
          <div class="lg:col-span-1 rounded-xl border border-primary/20 bg-white dark:bg-background-dark/50 p-6 shadow-sm flex flex-col max-h-[600px]">
            <h3 class="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
              <span class="material-symbols-outlined text-primary text-lg">groups</span>
              Agent Matrix
            </h3>
            <div class="flex flex-col gap-3 overflow-y-auto flex-1 pr-1">
              <div v-for="agent in agents" :key="agent.id"
                class="flex items-center gap-3 p-3 rounded-lg border transition-all"
                :class="{
                  'border-primary/30 bg-primary/5': agent.status === 'active',
                  'border-red-400/30 bg-red-500/5': agent.status === 'danger',
                  'border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/40': agent.status === 'idle'
                }">
                <div class="w-10 h-10 rounded-full flex items-center justify-center text-lg bg-slate-200 dark:bg-slate-700">
                  {{ getRoleIcon(agent.role) }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-xs font-mono font-bold text-slate-500 dark:text-slate-400">{{ agent.id }}</div>
                  <div class="text-sm text-slate-700 dark:text-slate-200 truncate">{{ agent.action || 'Waiting...' }}</div>
                </div>
                <div class="w-2.5 h-2.5 rounded-full flex-shrink-0"
                  :class="{
                    'bg-primary shadow-[0_0_6px_rgba(127,19,236,0.6)] animate-pulse': agent.status === 'active',
                    'bg-red-500 shadow-[0_0_6px_rgba(239,68,68,0.6)] animate-pulse': agent.status === 'danger',
                    'bg-slate-400': agent.status === 'idle'
                  }">
                </div>
              </div>
              <div v-if="agents.length === 0" class="text-center text-slate-400 py-8 text-sm">
                Waiting for agents to spawn...
              </div>
            </div>
          </div>

          <!-- Terminal / Live Log -->
          <div class="lg:col-span-1 rounded-xl border border-primary/20 overflow-hidden shadow-sm flex flex-col max-h-[600px]">
            <!-- Terminal chrome -->
            <div class="flex items-center gap-2 px-4 py-2.5 bg-slate-100 dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700">
              <span class="w-3 h-3 rounded-full bg-red-400"></span>
              <span class="w-3 h-3 rounded-full bg-amber-400"></span>
              <span class="w-3 h-3 rounded-full bg-green-400"></span>
              <span class="ml-3 text-xs font-mono text-slate-500 dark:text-slate-400">specter-swarm.log</span>
            </div>
            <!-- Terminal body -->
            <div class="bg-[#0d0914] flex-1 p-4 overflow-y-auto font-mono text-[13px] leading-relaxed" ref="terminalBody">
              <div v-for="(log, idx) in logs" :key="idx" class="mb-1">
                <span class="text-slate-600">[{{ log.time }}]</span>
                <span :class="{
                  'text-primary': log.level === 'info',
                  'text-green-400': log.level === 'success',
                  'text-amber-400': log.level === 'warning',
                  'text-red-400': log.level === 'error',
                }" class="mx-1">[{{ log.source }}]</span>
                <span :class="{
                  'text-slate-300': log.level === 'info',
                  'text-green-300': log.level === 'success',
                  'text-amber-300': log.level === 'warning',
                  'text-red-300': log.level === 'error',
                }">{{ log.message }}</span>
              </div>
              <div class="text-primary animate-pulse inline-block">_</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const terminalBody = ref(null)
const isDark = ref(true)

const scanId = ref('')
const scanStatus = ref('binding')
const totalAgents = ref(0)
const totalRoutes = ref(0)
const flawsFound = ref(0)
const securityIssues = ref(0)

const logs = ref([])
const agents = ref([])

let eventSource = null

const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
}

const statusColor = computed(() => {
  switch (scanStatus.value) {
    case 'binding': return 'text-primary'
    case 'spawning': return 'text-primary'
    case 'executing': return 'text-amber-500'
    case 'reporting': return 'text-primary'
    case 'completed': return 'text-green-500'
    case 'error': return 'text-red-500'
    case 'aborted': return 'text-red-500'
    default: return 'text-slate-500'
  }
})

const getRoleIcon = (role) => {
  if (role === 'user') return '👤'
  if (role === 'admin') return '👑'
  if (role === 'attacker') return '🥷'
  return '🤖'
}

const getTimestamp = () => {
  const now = new Date()
  return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
}

const addLog = (source, message, level = 'info') => {
  logs.value.push({
    time: getTimestamp(),
    source,
    level,
    message,
  })
  if (logs.value.length > 100) logs.value.shift()

  if (terminalBody.value) {
    setTimeout(() => {
      terminalBody.value.scrollTop = terminalBody.value.scrollHeight
    }, 50)
  }
}

const connectSSE = (id) => {
  eventSource = new EventSource(`/api/simulation/${id}/stream`)

  eventSource.addEventListener('crawl_started', (e) => {
    const data = JSON.parse(e.data)
    addLog('SYSTEM', `Crawling target: ${data.target_url}`)
    scanStatus.value = 'binding'
  })

  eventSource.addEventListener('route_discovered', (e) => {
    const data = JSON.parse(e.data)
    totalRoutes.value++
    addLog('CRAWLER', `Discovered: ${data.method} ${data.path}${data.has_form ? ' [FORM]' : ''}${data.has_auth ? ' [AUTH]' : ''}`)
  })

  eventSource.addEventListener('crawl_completed', (e) => {
    const data = JSON.parse(e.data)
    addLog('CRAWLER', `Crawling complete. ${data.total_routes} routes discovered.`, 'success')
  })

  eventSource.addEventListener('agent_spawned', (e) => {
    const data = JSON.parse(e.data)
    agents.value.push({
      id: data.agent_id,
      role: data.role,
      action: 'Initializing...',
      status: 'idle',
    })
    totalAgents.value = agents.value.length
    addLog('SPAWNER', `Agent ${data.agent_id} (${data.role}) spawned`)
  })

  eventSource.addEventListener('all_agents_spawned', (e) => {
    const data = JSON.parse(e.data)
    addLog('SYSTEM', `All ${data.total} agents spawned: ${data.users}U/${data.admins}A/${data.attackers}ATK`, 'success')
    scanStatus.value = 'executing'
  })

  eventSource.addEventListener('simulation_started', (e) => {
    addLog('SYSTEM', 'Simulation started — agents are now active', 'success')
    scanStatus.value = 'executing'
  })

  eventSource.addEventListener('agent_action', (e) => {
    const data = JSON.parse(e.data)
    const agent = agents.value.find(a => a.id === data.agent_id)
    if (agent) {
      agent.action = data.action
      agent.status = 'active'
    }
    addLog(data.agent_id, data.action)
  })

  eventSource.addEventListener('finding_discovered', (e) => {
    const data = JSON.parse(e.data)
    const level = data.severity === 'critical' ? 'error' : 'warning'

    if (data.category === 'logic_flaw' || data.category === 'security_issue') {
      flawsFound.value++
    }
    if (data.category === 'security_issue') {
      securityIssues.value++
    }

    addLog(data.agent_id || 'SYSTEM', `[${data.severity?.toUpperCase()}] ${data.title}`, level)

    const agent = agents.value.find(a => a.id === data.agent_id)
    if (agent) {
      agent.status = 'danger'
    }
  })

  eventSource.addEventListener('simulation_completed', (e) => {
    const data = JSON.parse(e.data)
    addLog('SYSTEM', `Simulation complete. ${data.total_findings} findings in ${data.duration_seconds}s.`, 'success')
    scanStatus.value = 'reporting'

    agents.value.forEach(a => {
      a.status = 'idle'
      a.action = 'Completed'
    })
  })

  eventSource.addEventListener('report_generating', (e) => {
    addLog('LLM', 'Generating narrative report via AI...', 'info')
  })

  eventSource.addEventListener('report_ready', (e) => {
    const data = JSON.parse(e.data)
    addLog('SYSTEM', 'Report ready! Redirecting...', 'success')
    scanStatus.value = 'completed'

    setTimeout(() => {
      if (eventSource) eventSource.close()
      router.push({ path: '/report', query: { scan_id: data.scan_id } })
    }, 2000)
  })

  eventSource.addEventListener('scan_error', (e) => {
    const data = JSON.parse(e.data)
    addLog('ERROR', data.error, 'error')
    scanStatus.value = 'error'
  })

  eventSource.addEventListener('scan_aborted', () => {
    addLog('SYSTEM', 'Scan aborted by user.', 'warning')
    scanStatus.value = 'aborted'
  })

  eventSource.onerror = () => {
    addLog('SYSTEM', 'Connection interrupted, reconnecting...', 'warning')
  }
}

onMounted(() => {
  scanId.value = route.query.scan_id || ''

  if (!scanId.value) {
    addLog('ERROR', 'No scan_id provided! Returning to home...', 'error')
    setTimeout(() => router.push('/'), 2000)
    return
  }

  // Sync theme
  isDark.value = document.documentElement.classList.contains('dark')

  addLog('SYSTEM', `Connecting to scan ${scanId.value}...`)
  connectSSE(scanId.value)
})

onUnmounted(() => {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
})

const abortSimulation = async () => {
  try {
    await fetch(`/api/scan/${scanId.value}`, { method: 'DELETE' })
  } catch (err) {
    // ignore
  }
  if (eventSource) eventSource.close()
  router.push('/')
}
</script>
