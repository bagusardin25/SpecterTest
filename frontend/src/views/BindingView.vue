<template>
  <div class="binding-view">
    <div class="glass-panel config-panel">
      <div class="panel-header">
        <h2>Target Binding & Initiation</h2>
        <div class="status-indicator"></div>
      </div>

      <div class="form-group">
        <label for="target-url" class="text-mono">TARGET_URL</label>
        <input 
          id="target-url" 
          type="url" 
          class="cyber-input" 
          placeholder="https://staging.myapp.com"
          v-model="targetUrl"
        />
      </div>

      <div class="agent-config">
        <h3 class="text-mono">> Agent Swarm Configuration</h3>
        
        <div class="slider-group">
          <label>User Agents: <span class="highlight">{{ userAgents }}</span></label>
          <input type="range" min="0" max="20" v-model="userAgents" class="cyber-slider">
        </div>
        
        <div class="slider-group">
          <label>Admin Agents: <span class="highlight">{{ adminAgents }}</span></label>
          <input type="range" min="0" max="10" v-model="adminAgents" class="cyber-slider">
        </div>
        
        <div class="slider-group danger">
          <label>Attacker Agents: <span class="highlight-danger">{{ attackerAgents }}</span></label>
          <input type="range" min="0" max="15" v-model="attackerAgents" class="cyber-slider">
        </div>
      </div>

      <div class="actions">
        <button class="cyber-button initiate-btn" @click="startSimulation">
          Initiate Swarm
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const targetUrl = ref('')
const userAgents = ref(5)
const adminAgents = ref(2)
const attackerAgents = ref(3)

const startSimulation = () => {
  if (!targetUrl.value) {
    alert("Please enter a Target URL")
    return
  }
  // In a real app we'd trigger an API call here.
  router.push('/simulate')
}
</script>

<style scoped>
.binding-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 150px);
}

.config-panel {
  width: 100%;
  max-width: 600px;
  padding: 2rem;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 1rem;
}

.panel-header h2 {
  margin: 0;
  text-transform: uppercase;
  color: var(--primary-color);
  text-shadow: 0 0 5px rgba(159, 122, 234, 0.3);
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--warning-color);
  box-shadow: 0 0 10px var(--warning-color);
  animation: pulse 2s infinite;
}

.form-group {
  margin-bottom: 2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.agent-config {
  background: rgba(0, 0, 0, 0.2);
  padding: 1.5rem;
  border-radius: var(--border-radius-sm);
  border: 1px dashed var(--border-color);
  margin-bottom: 2rem;
}

.agent-config h3 {
  font-size: 1.1rem;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.slider-group {
  margin-bottom: 1.5rem;
}

.slider-group:last-child {
  margin-bottom: 0;
}

.slider-group label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-family: var(--font-mono);
}

.highlight {
  color: var(--primary-color);
  font-weight: bold;
}

.highlight-danger {
  color: var(--danger-color);
  font-weight: bold;
}

/* Custom Cyber Slider */
.cyber-slider {
  appearance: none;
  -webkit-appearance: none;
  width: 100%;
  height: 4px;
  background: var(--surface-color-light);
  outline: none;
  border-radius: 2px;
}

.cyber-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  background: var(--primary-color);
  cursor: pointer;
  border-radius: 50%;
  box-shadow: var(--glow-primary);
}

.slider-group.danger .cyber-slider::-webkit-slider-thumb {
  background: var(--danger-color);
  box-shadow: var(--glow-danger);
}

.actions {
  display: flex;
  justify-content: flex-end;
}

.initiate-btn {
  width: 100%;
  font-size: 1.2rem;
  padding: 1rem;
  background: rgba(159, 122, 234, 0.1);
}

@keyframes pulse {
  0% { opacity: 0.5; transform: scale(0.95); }
  50% { opacity: 1; transform: scale(1.05); }
  100% { opacity: 0.5; transform: scale(0.95); }
}
</style>
