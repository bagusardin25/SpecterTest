<template>
  <div class="simulation-view">
    <div class="simulation-header">
      <h2>Simulation in Progress</h2>
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
            <span class="label">Requests/s</span>
            <span class="value">142.5</span>
          </div>
          <div class="metric highlight-danger">
            <span class="label">Flaws Found</span>
            <span class="value">3</span>
          </div>
          <div class="metric highlight-warning">
            <span class="label">Security Issues</span>
            <span class="value">1</span>
          </div>
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
              <span class="agent-action">{{ agent.action }}</span>
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
import { useRouter } from 'vue-router'

const router = useRouter()
const terminalBody = ref(null)

const totalAgents = ref(10)
const logs = ref([
  { time: '14:02:11', source: 'SYSTEM', level: 'info', message: 'Swarm initialized. Spawning 10 agents.' },
  { time: '14:02:12', source: 'MAPPER', level: 'info', message: 'Discovered 42 endpoints on target https://staging.myapp.com' },
])

const agents = ref([
  { id: 'usr-01', role: 'user', action: 'Browsing /products', status: 'idle' },
  { id: 'usr-02', role: 'user', action: 'Filling form /register', status: 'active' },
  { id: 'adm-01', role: 'admin', action: 'Accessing /api/users', status: 'active' },
  { id: 'atk-01', role: 'attacker', action: 'Testing SQLi on /search', status: 'danger' },
  { id: 'atk-02', role: 'attacker', action: 'IDOR attempt on /profile/12', status: 'danger' },
])

const getRoleIcon = (role) => {
  if (role === 'user') return '👤'
  if (role === 'admin') return '👑'
  if (role === 'attacker') return '🥷'
  return '🤖'
}

let intervalId = null;

onMounted(() => {
  // Simulate incoming logs
  intervalId = setInterval(() => {
    const now = new Date()
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
    
    logs.value.push({
      time: timeStr,
      source: 'ATK-01',
      level: Math.random() > 0.8 ? 'warning' : 'info',
      message: `Injecting payload on input parameter "id". Status: ${Math.random() > 0.8 ? '200 OK (Vulnerable)' : '403 Forbidden'}`
    })
    
    if (logs.value.length > 50) logs.value.shift()
    
    // Auto-scroll terminal
    if (terminalBody.value) {
      terminalBody.value.scrollTop = terminalBody.value.scrollHeight
    }
  }, 1500)
  
  // Transition to report after 15 seconds for demo
  setTimeout(() => {
    router.push('/report')
  }, 15000)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})

const abortSimulation = () => {
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
