<template>
  <div class="font-display bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 min-h-screen flex flex-col overflow-x-hidden">
    <div class="layout-container flex h-full grow flex-col">
      <div class="px-4 sm:px-10 lg:px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[1200px] w-full flex-1">
          <header class="flex items-center justify-between whitespace-nowrap border-b border-primary/20 px-4 sm:px-10 py-4 mb-8 rounded-xl bg-background-light dark:bg-background-dark/80 backdrop-blur-md sticky top-4 z-50">
            <div class="flex items-center gap-4 text-primary">
              <span class="material-symbols-outlined text-3xl">bug_report</span>
              <h2 class="text-slate-900 dark:text-slate-100 text-xl font-bold leading-tight tracking-[-0.015em]">SpecterTest</h2>
            </div>
            <div class="hidden md:flex flex-1 justify-end gap-8 items-center">
              <nav class="flex items-center gap-8">
                <a class="text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal" href="#">Home</a>
                <a class="text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal" href="#how-it-works">Features</a>
                <a class="text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal" href="#">Pricing</a>
              </nav>
              <button @click="scrollToBinding" class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-5 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 transition-colors shadow-[0_0_15px_rgba(127,19,236,0.5)]">
                <span class="truncate">Launch Simulation</span>
              </button>
            </div>
            <button class="md:hidden text-slate-900 dark:text-slate-100">
              <span class="material-symbols-outlined">menu</span>
            </button>
          </header>
          
          <main class="flex-1 flex flex-col gap-16 pb-16">
            <!-- Hero Section -->
            <section class="@container">
              <div class="flex flex-col gap-10 lg:flex-row lg:items-center px-4">
                <div class="flex flex-col gap-8 lg:w-1/2 lg:pr-8 z-10">
                  <div class="flex flex-col gap-4 text-left">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 w-fit">
                      <span class="material-symbols-outlined text-primary text-sm">visibility</span>
                      <span class="text-primary text-xs font-bold uppercase tracking-wider">Swarm Intelligence</span>
                    </div>
                    <h1 class="text-slate-900 dark:text-white text-5xl font-black leading-tight tracking-[-0.033em] lg:text-6xl">
                      Ghost-test your app <br/><span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#00f0ff]">before hackers do</span>
                    </h1>
                    <h2 class="text-slate-600 dark:text-slate-300 text-lg font-normal leading-relaxed max-w-xl">
                      Use AI swarm intelligence to find logic flaws and security vulnerabilities in your web applications before they are exploited. Stay one step ahead of the unknown.
                    </h2>
                  </div>
                  <div class="flex flex-col sm:flex-row gap-4">
                    <button @click="scrollToBinding" class="flex h-12 items-center justify-center rounded-lg px-8 bg-primary text-white text-base font-bold shadow-[0_0_20px_rgba(127,19,236,0.6)] hover:bg-primary/90 transition-all">
                      Start Testing Now
                    </button>
                    <button class="flex h-12 items-center justify-center rounded-lg px-8 border border-primary/50 text-slate-900 dark:text-white text-base font-bold hover:bg-primary/10 transition-all">
                      <span class="material-symbols-outlined mr-2">play_circle</span>
                      Watch Demo
                    </button>
                  </div>
                </div>
                
                <div class="lg:w-1/2 relative min-h-[400px] flex items-center justify-center">
                  <div class="absolute inset-0 bg-gradient-to-br from-primary/20 to-transparent rounded-full blur-[100px] -z-10"></div>
                  <div class="w-full h-full aspect-square max-h-[500px] rounded-2xl border border-primary/30 bg-background-dark relative overflow-hidden shadow-[0_0_40px_rgba(127,19,236,0.2)]" style="background-image: radial-gradient(circle at center, rgba(127,19,236,0.1) 0%, transparent 70%);">
                    <div class="absolute inset-0 flex items-center justify-center">
                      <span class="material-symbols-outlined text-9xl text-primary/50 animate-pulse">hub</span>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- How It Works Section -->
            <section id="how-it-works" class="flex flex-col gap-10 px-4 py-16 rounded-2xl bg-slate-100/5 dark:bg-black/20 border border-primary/10 mt-16">
              <div class="flex flex-col gap-4 text-center items-center">
                <h2 class="text-primary text-sm font-bold uppercase tracking-widest">How It Works</h2>
                <h3 class="text-slate-900 dark:text-white text-3xl md:text-4xl font-black leading-tight max-w-[720px]">
                  Automated Security Swarms
                </h3>
                <p class="text-slate-600 dark:text-slate-300 text-base font-normal leading-normal max-w-[600px]">
                  Our AI agents work together to simulate complex attacks and uncover deep logic flaws in four simple steps.
                </p>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 pt-8">
                <!-- Step 1 -->
                <div class="flex flex-col gap-4 rounded-xl border border-primary/20 bg-background-light dark:bg-background-dark/50 p-6 hover:border-primary/60 transition-colors shadow-lg shadow-primary/5 relative overflow-hidden group">
                  <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-primary/20 transition-colors"></div>
                  <div class="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center text-primary border border-primary/30 z-10">
                    <span class="material-symbols-outlined">link</span>
                  </div>
                  <div class="flex flex-col gap-2 z-10">
                    <h4 class="text-slate-900 dark:text-white text-lg font-bold">1. Binding</h4>
                    <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">Connect our platform to your application environment securely with a single integration point.</p>
                  </div>
                </div>
                <!-- Step 2 -->
                <div class="flex flex-col gap-4 rounded-xl border border-primary/20 bg-background-light dark:bg-background-dark/50 p-6 hover:border-primary/60 transition-colors shadow-lg shadow-primary/5 relative overflow-hidden group">
                  <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-primary/20 transition-colors"></div>
                  <div class="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center text-primary border border-primary/30 z-10">
                    <span class="material-symbols-outlined">memory</span>
                  </div>
                  <div class="flex flex-col gap-2 z-10">
                    <h4 class="text-slate-900 dark:text-white text-lg font-bold">2. Spawning</h4>
                    <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">Generate a localized swarm of intelligent AI agents specifically tailored to your app's architecture.</p>
                  </div>
                </div>
                <!-- Step 3 -->
                <div class="flex flex-col gap-4 rounded-xl border border-primary/20 bg-background-light dark:bg-background-dark/50 p-6 hover:border-primary/60 transition-colors shadow-lg shadow-primary/5 relative overflow-hidden group">
                  <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-primary/20 transition-colors"></div>
                  <div class="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center text-primary border border-primary/30 z-10">
                    <span class="material-symbols-outlined">route</span>
                  </div>
                  <div class="flex flex-col gap-2 z-10">
                    <h4 class="text-slate-900 dark:text-white text-lg font-bold">3. Execution</h4>
                    <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">Agents autonomously navigate, mutate, and attack your application's logic paths concurrently.</p>
                  </div>
                </div>
                <!-- Step 4 -->
                <div class="flex flex-col gap-4 rounded-xl border border-primary/20 bg-background-light dark:bg-background-dark/50 p-6 hover:border-primary/60 transition-colors shadow-lg shadow-primary/5 relative overflow-hidden group">
                  <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-primary/20 transition-colors"></div>
                  <div class="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center text-primary border border-primary/30 z-10">
                    <span class="material-symbols-outlined">description</span>
                  </div>
                  <div class="flex flex-col gap-2 z-10">
                    <h4 class="text-slate-900 dark:text-white text-lg font-bold">4. Report</h4>
                    <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed">Receive detailed vulnerability reports with reproduction steps and actionable remediation advice.</p>
                  </div>
                </div>
              </div>
            </section>

            <!-- Binding Configuration Panel -->
            <section id="binding-configuration" class="mt-16 mb-16 flex flex-col items-center">
              <div class="glass-panel w-full max-w-2xl p-8 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary to-transparent"></div>
                
                <div class="flex justify-between items-center mb-8 border-b border-primary/20 pb-4">
                  <h2 class="text-2xl font-bold text-white tracking-wide">Target Binding & Initiation</h2>
                  <div class="w-3 h-3 rounded-full bg-yellow-500 shadow-[0_0_10px_#eab308] animate-pulse"></div>
                </div>

                <div class="mb-8">
                  <label for="target-url" class="block mb-2 text-slate-400 font-mono text-sm">TARGET_URL</label>
                  <input 
                    id="target-url" 
                    type="url" 
                    class="cyber-input" 
                    placeholder="https://staging.myapp.com"
                    v-model="targetUrl"
                  />
                </div>

                <div class="bg-black/20 p-6 rounded border border-dashed border-primary/30 mb-8">
                  <h3 class="font-mono text-white mb-6">> Agent Swarm Configuration</h3>
                  
                  <div class="mb-6">
                    <label class="flex justify-between mb-2 font-mono text-sm text-slate-300">
                      User Agents: <span class="text-primary font-bold">{{ userAgents }}</span>
                    </label>
                    <input type="range" min="0" max="20" v-model="userAgents" class="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-primary">
                  </div>
                  
                  <div class="mb-6">
                    <label class="flex justify-between mb-2 font-mono text-sm text-slate-300">
                      Admin Agents: <span class="text-primary font-bold">{{ adminAgents }}</span>
                    </label>
                    <input type="range" min="0" max="10" v-model="adminAgents" class="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-primary">
                  </div>
                  
                  <div>
                    <label class="flex justify-between mb-2 font-mono text-sm text-slate-300">
                      Attacker Agents: <span class="text-red-400 font-bold">{{ attackerAgents }}</span>
                    </label>
                    <input type="range" min="0" max="15" v-model="attackerAgents" class="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-red-400">
                  </div>
                </div>

                <div class="flex justify-end">
                  <button @click="startSimulation" class="cyber-button w-full shadow-[0_0_15px_rgba(127,19,236,0.3)] bg-primary/10">
                    Initiate Swarm
                  </button>
                </div>
              </div>
            </section>
          </main>

          <footer class="flex flex-col gap-6 border-t border-primary/20 pt-10 pb-6 text-center mt-auto">
            <div class="flex flex-wrap items-center justify-center gap-6">
              <a class="text-slate-500 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium" href="#">Privacy Policy</a>
              <a class="text-slate-500 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium" href="#">Terms of Service</a>
              <a class="text-slate-500 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium" href="#">Security</a>
              <a class="text-slate-500 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium" href="#">Contact</a>
            </div>
            <div class="flex justify-center items-center gap-2 text-slate-500 dark:text-slate-500 text-sm">
              <span class="material-symbols-outlined text-sm">bug_report</span>
              <p>© 2026 SpecterTest Inc. All rights reserved.</p>
            </div>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const targetUrl = ref('')
const userAgents = ref(5)
const adminAgents = ref(2)
const attackerAgents = ref(3)

const scrollToBinding = () => {
  const el = document.getElementById('binding-configuration')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

const startSimulation = () => {
  if (!targetUrl.value) {
    alert("Please enter a Target URL before initiating the swarm.")
    return
  }
  router.push('/simulate')
}

onMounted(() => {
  // Add material symbols font and regular space grotesk dynamically if missing
  if (!document.getElementById('material-symbols')) {
    const link = document.createElement('link')
    link.id = 'material-symbols'
    link.rel = 'stylesheet'
    link.href = 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap'
    document.head.appendChild(link)
  }
  
  if (!document.getElementById('space-grotesk')) {
    const link = document.createElement('link')
    link.id = 'space-grotesk'
    link.rel = 'stylesheet'
    link.href = 'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700;900&display=swap'
    document.head.appendChild(link)
  }
})
</script>

<style scoped>
/* Scoped styles are mostly handled by Tailwind now, keep minimal overrides if needed */
</style>
