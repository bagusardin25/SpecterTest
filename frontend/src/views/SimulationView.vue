<template>
  <div class="simulation-view">
    <div class="simulation-header">
      <h2>> Simulation in Progress</h2>
      <button class="cyber-button danger" @click="abortSimulation">ABORT</button>
    </div>

    <div class="dashboard-grid">
      <!-- Target Map / Stats -->
      <div class="glass-panel stats-panel">
        <h3 class="text-mono">>> Swarm Metrics</h3>
        <div class="metrics-grid">
          <div class="metric">
            <span class="label">Total Agen</span>
            <span class="value">{{ totalAgents }}</span>
          </div>
          <div class="metric">
            <span class="label">Routes</span>
            <span class="value">{{ totalRoutes }}</span>
          </div>
          <div class="metric highlight-danger">
            <span class="label">Flaws Found</span>
            <span class="value">{{ flawsFound }}</span>
          </div>
          <div class="metric highlight-warning">
            <span class="label">Security Issues</span>
            <span class="value">{{ securityIssues }}</span>
          </div>
        </div>
        <div class="status-bar">
          <span class="status-label text-mono">STATUS:</span>
          <span class="status-value" :class="scanStatus">{{ scanStatus.toUpperCase() }}</span>
        </div>
      </div>

      <!-- Agent Status Matrix -->
      <div class="glass-panel agents-panel">
        <h3 class="text-mono">>> Agent Matrix</h3>
        <div class="agent-list">
          <div v-for="agent in agents" :key="agent.id" class="agent-card" :class="agent.status">
            <div class="agent-icon" :title="agent.role">
              {{ getRoleIcon(agent.role) }}
            </div>
            <div class="agent-details">
              <span class="agent-id text-mono">{{ agent.id }}</span>
              <span class="agent-action">{{ agent.action || 'Waiting...' }}</span>
            </div>
            <div class="agent-status-dot"></div>
          </div>
        </div>
      </div>

      <!-- Terminal / Live Log -->
      <div class="glass-panel terminal-panel">
        <div class="terminal-header">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
          <span class="title text-mono">specter-swarm.log</span>
        </div>
        <div class="terminal-body text-mono" ref="terminalBody">
          <div v-for="(log, idx) in logs" :key="idx" class="log-entry" :class="log.level">
            <span class="timestamp">[{{ log.time }}]</span>
            <span class="source">[{{ log.source }}]</span>
            <span class="message">{{ log.message }}</span>
          </div>
          <div class="cursor">_</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const terminalBody = ref(null)

const scanId = ref('')
const scanStatus = ref('binding')
const totalAgents = ref(0)
const totalRoutes = ref(0)
const flawsFound = ref(0)
const securityIssues = ref(0)

const logs = ref([])
const agents = ref([])

let eventSource = null

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

  // Auto-scroll
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
    // Update agent in list
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

    // Make the discovering agent "danger" status
    const agent = agents.value.find(a => a.id === data.agent_id)
    if (agent) {
      agent.status = 'danger'
    }
  })

  eventSource.addEventListener('simulation_completed', (e) => {
    const data = JSON.parse(e.data)
    addLog('SYSTEM', `Simulation complete. ${data.total_findings} findings in ${data.duration_seconds}s.`, 'success')
    scanStatus.value = 'reporting'

    // Mark all agents as completed
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

    // Navigate to report after a short delay
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
    // SSE will auto-reconnect, just log it
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

<style scoped>
.simulation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.simulation-header h2 {
  color: var(--primary-color);
  text-shadow: var(--glow-primary);
  margin: 0;
  text-transform: uppercase;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto 1fr;
  gap: 1.5rem;
  height: calc(100vh - 200px);
}

.stats-panel {
  grid-column: 1 / 2;
  grid-row: 1 / 2;
  padding: 1.5rem;
}

.agents-panel {
  grid-column: 2 / 3;
  grid-row: 1 / 3;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.terminal-panel {
  grid-column: 1 / 2;
  grid-row: 2 / 3;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

h3 {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}

/* Status */
.status-bar {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.status-label { color: var(--text-muted); margin-right: 0.5rem; }
.status-value { font-weight: bold; }
.status-value.binding { color: var(--accent-color); }
.status-value.spawning { color: var(--primary-color); }
.status-value.executing { color: var(--warning-color); animation: pulse-text 1s infinite; }
.status-value.reporting { color: var(--primary-color); }
.status-value.completed { color: #27c93f; }
.status-value.error { color: var(--danger-color); }

@keyframes pulse-text { 50% { opacity: 0.5; } }

/* Metrics */
.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.metric {
  background: rgba(0, 0, 0, 0.3);
  padding: 1rem;
  border-radius: var(--border-radius-sm);
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid transparent;
}

.metric .label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.metric .value {
  font-size: 2rem;
  font-weight: bold;
  font-family: var(--font-mono);
  color: var(--primary-color);
}

.metric.highlight-danger {
  border-color: rgba(252, 129, 129, 0.3);
}
.metric.highlight-danger .value {
  color: var(--danger-color);
  text-shadow: var(--glow-danger);
}

.metric.highlight-warning .value {
  color: var(--warning-color);
}

/* Agents */
.agent-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
  flex: 1;
  padding-right: 0.5rem;
}

.agent-card {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius-sm);
  border-left: 3px solid var(--text-muted);
  transition: all 0.3s ease;
}

.agent-card.active { border-left-color: var(--primary-color); }
.agent-card.danger { border-left-color: var(--danger-color); background: rgba(252, 129, 129, 0.05); }

.agent-icon {
  font-size: 1.5rem;
  margin-right: 1rem;
  background: rgba(255, 255, 255, 0.1);
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
}

.agent-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.agent-id {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: bold;
}

.agent-action {
  font-size: 0.9rem;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 250px;
}

.agent-status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-muted);
}

.agent-card.active .agent-status-dot {
  background: var(--primary-color);
  box-shadow: var(--glow-primary);
  animation: pulse 2s infinite;
}

.agent-card.danger .agent-status-dot {
  background: var(--danger-color);
  box-shadow: var(--glow-danger);
  animation: pulse 1s infinite;
}

/* Terminal */
.terminal-header {
  background: #1a1a2e;
  padding: 0.5rem 1rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #000;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 6px;
}

.dot.red { background: #ff5f56; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #27c93f; }

.terminal-header .title {
  margin-left: 1rem;
  color: var(--text-muted);
  font-size: 0.85rem;
}

.terminal-body {
  background: #000;
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
  font-size: 0.9rem;
}

.log-entry { margin-bottom: 0.25rem; }
.log-entry .timestamp { color: var(--text-muted); margin-right: 0.5rem; }
.log-entry .source { color: var(--accent-color); margin-right: 0.5rem; }
.log-entry .message { color: var(--text-primary); }

.log-entry.warning .source { color: var(--warning-color); }
.log-entry.warning .message { color: var(--warning-color); }
.log-entry.error .source { color: var(--danger-color); }
.log-entry.error .message { color: var(--danger-color); }
.log-entry.success .source { color: #27c93f; }
.log-entry.success .message { color: #27c93f; }

.cursor {
  display: inline-block;
  color: var(--primary-color);
  animation: blink 1s step-end infinite;
}

@keyframes blink { 50% { opacity: 0; } }
@keyframes pulse {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(var(--primary-color), 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(var(--primary-color), 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(var(--primary-color), 0); }
}
</style>
