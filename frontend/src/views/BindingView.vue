<template>
  <div class="font-display bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 min-h-screen flex flex-col overflow-x-hidden">
    <div class="layout-container flex h-full grow flex-col">
      <div class="px-4 sm:px-10 lg:px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[1200px] w-full flex-1 pt-20">
          <header :class="[
            'fixed top-0 left-0 w-full z-50 flex items-center justify-center px-4 sm:px-10 lg:px-40 transition-all duration-300 animate-fade-in-up',
            isScrolled ? 'py-3 border-b border-primary/20 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-md shadow-lg shadow-primary/5' : 'py-5 border-b-transparent bg-transparent shadow-none'
          ]">
            <div class="flex items-center justify-between w-full max-w-[1200px]">
              <div class="flex items-center gap-4 text-primary cursor-pointer hover:scale-105 transition-transform duration-300">
                <img src="/logo.png" alt="SpecterTest Logo" class="h-16 w-auto object-contain drop-shadow-[0_0_12px_rgba(127,19,236,0.8)] filter hover:brightness-125 transition-all">
                <!-- SpecterTest text removed per user request -->
              </div>
              <div class="hidden md:flex flex-1 justify-end gap-6 items-center">
                <nav class="flex items-center gap-6">
                  <a class="relative text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal group py-2" href="#">
                    Platform
                    <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-primary transition-all duration-300 group-hover:w-full"></span>
                  </a>
                  <a class="relative text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal group py-2" href="#">
                    Solutions
                    <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-primary transition-all duration-300 group-hover:w-full"></span>
                  </a>
                  <a class="relative text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal group py-2" href="#">
                    Pricing
                    <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-primary transition-all duration-300 group-hover:w-full"></span>
                  </a>
                  <a class="relative text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal group py-2" href="#">
                    Docs
                    <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-primary transition-all duration-300 group-hover:w-full"></span>
                  </a>
                </nav>
                <div class="flex items-center gap-4">
                  <button @click="toggleTheme" class="flex items-center justify-center w-10 h-10 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-primary dark:hover:bg-primary hover:text-white dark:hover:text-white transition-all shadow-sm" title="Toggle Theme">
                    <span class="material-symbols-outlined text-lg" v-if="isDark">light_mode</span>
                    <span class="material-symbols-outlined text-lg" v-else>dark_mode</span>
                  </button>
                  <a href="#" class="text-slate-700 dark:text-slate-200 hover:text-primary dark:hover:text-primary transition-colors text-sm font-bold">Sign In</a>
                  <button class="flex min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-5 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-primary/90 transition-colors shadow-[0_0_15px_rgba(127,19,236,0.5)]">
                    <span class="truncate">Get Started Free</span>
                  </button>
                </div>
              </div>
              <div class="md:hidden flex items-center gap-3">
                <button @click="toggleTheme" class="flex items-center justify-center w-10 h-10 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-primary hover:text-white transition-all shadow-sm" title="Toggle Theme">
                  <span class="material-symbols-outlined text-lg" v-if="isDark">light_mode</span>
                  <span class="material-symbols-outlined text-lg" v-else>dark_mode</span>
                </button>
                <button class="text-slate-900 dark:text-slate-100 flex items-center justify-center">
                  <span class="material-symbols-outlined text-2xl">menu</span>
                </button>
              </div>
            </div>
          </header>
          
          <main class="flex-1 flex flex-col gap-16 pb-16">
            <!-- Hero Section -->
            <section class="@container">
              <div class="flex flex-col gap-10 lg:flex-row lg:items-center px-4">
                <div class="flex flex-col gap-8 lg:w-1/2 lg:pr-8 z-10 animate-fade-in-up">
                  <div class="flex flex-col gap-4 text-left">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/30 w-fit">
                      <span class="material-symbols-outlined text-primary text-sm">visibility</span>
                      <span class="text-primary text-xs font-bold uppercase tracking-wider">Swarm Intelligence</span>
                    </div>
                    <h1 class="text-slate-900 dark:text-white text-5xl font-black leading-tight tracking-[-0.033em] lg:text-6xl">
                      Ghost-test your app <br/><span class="text-transparent bg-clip-text bg-gradient-to-r from-primary to-[#00f0ff]">before hackers do</span>
                    </h1>
                    <h2 class="text-slate-700 dark:text-slate-200 text-lg font-normal leading-relaxed max-w-xl">
                      Use AI swarm intelligence to find logic flaws and security vulnerabilities in your web applications before they are exploited. Stay one step ahead of the unknown.
                    </h2>
                  </div>
                  <div class="flex flex-col gap-6">
                    <div class="flex flex-col sm:flex-row gap-4">
                      <button @click="scrollToBinding" class="flex h-12 items-center justify-center rounded-lg px-8 bg-primary text-white text-base font-bold shadow-[0_0_20px_rgba(127,19,236,0.6)] hover:bg-primary/90 transition-all">
                        Start Testing Now
                      </button>
                      <button class="flex h-12 items-center justify-center rounded-lg px-8 border border-primary/50 text-slate-900 dark:text-white text-base font-bold hover:bg-primary/10 transition-all">
                        <span class="material-symbols-outlined mr-2">play_circle</span>
                        Watch Demo
                      </button>
                    </div>
                    <div class="flex flex-col gap-2">
                      <div class="flex items-center gap-2">
                        <div class="flex -space-x-2">
                          <img class="inline-block h-8 w-8 rounded-full ring-2 ring-background-light dark:ring-background-dark" src="https://i.pravatar.cc/100?img=1" alt=""/>
                          <img class="inline-block h-8 w-8 rounded-full ring-2 ring-background-light dark:ring-background-dark" src="https://i.pravatar.cc/100?img=3" alt=""/>
                          <img class="inline-block h-8 w-8 rounded-full ring-2 ring-background-light dark:ring-background-dark" src="https://i.pravatar.cc/100?img=5" alt=""/>
                          <img class="inline-block h-8 w-8 rounded-full ring-2 ring-background-light dark:ring-background-dark" src="https://i.pravatar.cc/100?img=8" alt=""/>
                        </div>
                        <span class="text-sm text-slate-600 dark:text-slate-400 font-medium ml-2">Trusted by 2,000+ security teams</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="lg:w-1/2 relative w-full aspect-video lg:aspect-square max-h-[500px] flex items-center justify-center animate-fade-in-up animate-delay-200">
                  <div class="absolute inset-0 bg-gradient-to-br from-primary/20 to-transparent rounded-full blur-[100px] -z-10"></div>
                  <div class="w-full h-full rounded-2xl border border-primary/30 bg-slate-900 dark:bg-[#0a0510] relative overflow-hidden shadow-[0_0_40px_rgba(127,19,236,0.2)] flex flex-col font-mono text-xs sm:text-sm">
                    <!-- Window Header -->
                    <div class="flex items-center px-4 py-2 border-b border-primary/20 bg-slate-800 dark:bg-black/40">
                      <div class="flex gap-2">
                        <div class="w-3 h-3 rounded-full bg-red-500"></div>
                        <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                        <div class="w-3 h-3 rounded-full bg-green-500"></div>
                      </div>
                      <div class="mx-auto text-slate-400 font-bold text-xs">specter-swarm-node-01</div>
                    </div>
                    <!-- Terminal Content -->
                    <div class="flex-1 p-4 overflow-y-auto flex flex-col justify-end gap-1" ref="terminalRef">
                      <div v-for="(log, idx) in terminalLogs" :key="idx" class="flex items-start gap-2 animate-fade-in">
                        <span class="text-primary opacity-50 shrink-0">></span>
                        <span :class="[
                          'font-mono break-all',
                          log.type === 'success' ? 'text-green-400' : '',
                          log.type === 'error' ? 'text-red-400' : '',
                          log.type === 'warning' ? 'text-yellow-400' : 'text-slate-300'
                        ]" v-html="log.text"></span>
                      </div>
                      <div class="flex items-center gap-2 mt-2">
                        <span class="text-primary opacity-50">></span>
                        <div class="w-2 h-4 bg-primary animate-pulse"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- How It Works Section -->
            <section id="how-it-works" class="flex flex-col gap-10 px-4 py-16 rounded-2xl bg-white/50 dark:bg-black/20 backdrop-blur-sm border border-primary/10 mt-16 shadow-sm dark:shadow-none animate-fade-in-up animate-delay-300">
              <div class="flex flex-col gap-4 text-center items-center">
                <h2 class="text-primary text-sm font-bold uppercase tracking-widest">How It Works</h2>
                <h3 class="text-slate-900 dark:text-white text-3xl md:text-4xl font-black leading-tight max-w-[720px]">
                  Automated Security Swarms
                </h3>
                <p class="text-slate-700 dark:text-slate-300 text-base font-normal leading-normal max-w-[600px]">
                  Our AI agents work together to simulate complex attacks and uncover deep logic flaws in four simple steps.
                </p>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 pt-8">
                <!-- Step 1 -->
                <div class="flex flex-col gap-4 rounded-xl border border-primary/20 bg-white dark:bg-background-dark/50 p-6 hover:border-primary/80 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(127,19,236,0.3)] relative overflow-hidden group">
                  <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-primary/30 group-hover:blur-3xl transition-all duration-500"></div>
                  <div class="w-12 h-12 rounded-lg bg-primary/10 group-hover:bg-primary/20 flex items-center justify-center text-primary border border-primary/30 z-10 transition-colors">
                    <span class="material-symbols-outlined group-hover:scale-110 transition-transform">link</span>
                  </div>
                  <div class="flex flex-col gap-2 z-10">
                    <h4 class="text-slate-900 dark:text-white text-lg font-bold group-hover:text-primary transition-colors">1. Binding</h4>
                    <p class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">Connect our platform to your application environment securely with a single integration point.</p>
                  </div>
                </div>
                <!-- Step 2 -->
                <div class="flex flex-col gap-4 rounded-xl border border-primary/20 bg-white dark:bg-background-dark/50 p-6 hover:border-primary/80 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(127,19,236,0.3)] relative overflow-hidden group">
                  <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-primary/30 group-hover:blur-3xl transition-all duration-500"></div>
                  <div class="w-12 h-12 rounded-lg bg-primary/10 group-hover:bg-primary/20 flex items-center justify-center text-primary border border-primary/30 z-10 transition-colors">
                    <span class="material-symbols-outlined group-hover:scale-110 transition-transform">memory</span>
                  </div>
                  <div class="flex flex-col gap-2 z-10">
                    <h4 class="text-slate-900 dark:text-white text-lg font-bold group-hover:text-primary transition-colors">2. Spawning</h4>
                    <p class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">Generate a localized swarm of intelligent AI agents specifically tailored to your app's architecture.</p>
                  </div>
                </div>
                <!-- Step 3 -->
                <div class="flex flex-col gap-4 rounded-xl border border-primary/20 bg-white dark:bg-background-dark/50 p-6 hover:border-primary/80 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(127,19,236,0.3)] relative overflow-hidden group">
                  <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-primary/30 group-hover:blur-3xl transition-all duration-500"></div>
                  <div class="w-12 h-12 rounded-lg bg-primary/10 group-hover:bg-primary/20 flex items-center justify-center text-primary border border-primary/30 z-10 transition-colors">
                    <span class="material-symbols-outlined group-hover:scale-110 transition-transform">route</span>
                  </div>
                  <div class="flex flex-col gap-2 z-10">
                    <h4 class="text-slate-900 dark:text-white text-lg font-bold group-hover:text-primary transition-colors">3. Execution</h4>
                    <p class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">Agents autonomously navigate, mutate, and attack your application's logic paths concurrently.</p>
                  </div>
                </div>
                <!-- Step 4 -->
                <div class="flex flex-col gap-4 rounded-xl border border-primary/20 bg-white dark:bg-background-dark/50 p-6 hover:border-primary/80 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_0_30px_rgba(127,19,236,0.3)] relative overflow-hidden group">
                  <div class="absolute top-0 right-0 w-32 h-32 bg-primary/10 rounded-full blur-2xl -mr-10 -mt-10 group-hover:bg-primary/30 group-hover:blur-3xl transition-all duration-500"></div>
                  <div class="w-12 h-12 rounded-lg bg-primary/10 group-hover:bg-primary/20 flex items-center justify-center text-primary border border-primary/30 z-10 transition-colors">
                    <span class="material-symbols-outlined group-hover:scale-110 transition-transform">description</span>
                  </div>
                  <div class="flex flex-col gap-2 z-10">
                    <h4 class="text-slate-900 dark:text-white text-lg font-bold group-hover:text-primary transition-colors">4. Report</h4>
                    <p class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed">Receive detailed vulnerability reports with reproduction steps and actionable remediation advice.</p>
                  </div>
                </div>
              </div>
            </section>

            <!-- Binding Configuration Panel -->
            <section id="binding-configuration" class="mt-16 mb-16 flex flex-col items-center animate-fade-in-up animate-delay-400">
              <div class="glass-panel w-full max-w-2xl p-8 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary to-transparent"></div>
                
                <div class="flex justify-between items-center mb-8 border-b border-primary/20 pb-4">
                  <h2 class="text-2xl font-bold text-slate-900 dark:text-white tracking-wide">Target Binding & Initiation</h2>
                  <div class="w-3 h-3 rounded-full bg-yellow-500 shadow-[0_0_10px_#eab308] animate-pulse"></div>
                </div>

                <div class="mb-8">
                  <label for="target-url" class="block mb-2 text-slate-600 dark:text-slate-400 font-mono text-sm">TARGET_URL</label>
                  <input 
                    id="target-url" 
                    type="url" 
                    class="cyber-input" 
                    placeholder="https://staging.myapp.com"
                    v-model="targetUrl"
                  />
                </div>

                <div class="bg-slate-50 dark:bg-black/20 p-6 rounded border border-dashed border-primary/30 mb-8 grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <h3 class="font-mono text-slate-800 dark:text-white mb-6">> Agent Swarm Configuration</h3>
                    
                    <div class="mb-6">
                      <label class="flex justify-between mb-2 font-mono text-sm text-slate-600 dark:text-slate-300">
                        User Agents: <span class="text-primary font-bold">{{ userAgents }}</span>
                      </label>
                      <input type="range" min="0" max="20" v-model="userAgents" class="w-full h-1 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-primary">
                    </div>
                    
                    <div class="mb-6">
                      <label class="flex justify-between mb-2 font-mono text-sm text-slate-600 dark:text-slate-300">
                        Admin Agents: <span class="text-primary font-bold">{{ adminAgents }}</span>
                      </label>
                      <input type="range" min="0" max="10" v-model="adminAgents" class="w-full h-1 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-primary">
                    </div>
                    
                    <div>
                      <label class="flex justify-between mb-2 font-mono text-sm text-slate-600 dark:text-slate-300">
                        Attacker Agents: <span class="text-red-500 dark:text-red-400 font-bold">{{ attackerAgents }}</span>
                      </label>
                      <input type="range" min="0" max="15" v-model="attackerAgents" class="w-full h-1 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-red-500 dark:accent-red-400">
                    </div>
                  </div>
                  
                  <div class="flex flex-col items-center justify-center bg-white dark:bg-black/40 rounded-lg p-6 border border-primary/10 shadow-inner">
                    <h4 class="text-slate-500 dark:text-slate-400 text-xs font-bold uppercase tracking-widest mb-2">Estimated Attack Power</h4>
                    <div class="flex items-end gap-2 mb-4">
                      <span class="text-5xl font-black" :class="powerColorClass">{{ totalAttackPower }}</span>
                      <span class="text-slate-400 font-mono text-sm pb-1">ops/sec</span>
                    </div>
                    
                    <div class="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-2 mb-2 overflow-hidden">
                      <div class="h-2 rounded-full transition-all duration-300" :class="powerBarColorClass" :style="{ width: Math.min(100, (totalAttackPower / 300) * 100) + '%' }"></div>
                    </div>
                    
                    <div class="flex w-full justify-between text-xs text-slate-500 dark:text-slate-400 font-mono">
                      <span>Low</span>
                      <span>Extreme</span>
                    </div>
                  </div>
                </div>

                <div class="flex justify-end">
                  <button @click="startSimulation" class="cyber-button w-full shadow-[0_0_15px_rgba(127,19,236,0.3)] bg-primary/10 dark:bg-primary/20">
                    Initiate Swarm
                  </button>
                </div>
              </div>
            </section>
          </main>

          <!-- Modern Grid Footer based on reference image -->
          <footer class="mt-auto border-t border-primary/20 bg-slate-50 dark:bg-background-dark relative overflow-hidden">
            <!-- Subtle dot pattern background -->
            <div class="absolute inset-0 opacity-10 dark:opacity-[0.03] z-0" style="background-image: radial-gradient(currentColor 1px, transparent 1px); background-size: 24px 24px;"></div>
            
            <div class="max-w-[1200px] mx-auto px-4 sm:px-10 lg:px-10 py-16 relative z-10 w-full">
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 lg:gap-8">
                <!-- Brand & Description -->
                <div class="lg:col-span-2 flex flex-col gap-6">
                  <div class="flex items-center gap-3">
                    <div class="w-14 h-14 rounded-lg bg-transparent flex items-center justify-center">
                      <img src="/logo.png" alt="SpecterTest Logo" class="h-12 w-auto object-contain drop-shadow-[0_0_8px_rgba(127,19,236,0.8)]">
                    </div>
                    <!-- Footer SpecterTest text removed per user request -->
                  </div>
                  <p class="text-slate-600 dark:text-slate-400 text-sm leading-relaxed max-w-sm">
                    Autonomous AI swarm intelligence for modern web security. Identifying vulnerabilities before they become threats.
                  </p>
                </div>
                
                <!-- Links: PRODUCT -->
                <div class="flex flex-col gap-4">
                  <h3 class="text-slate-900 dark:text-white font-bold text-sm tracking-wider uppercase mb-1">Product</h3>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Features</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Integrations</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Pricing</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Changelog</a>
                </div>

                <!-- Links: RESOURCES -->
                <div class="flex flex-col gap-4">
                  <h3 class="text-slate-900 dark:text-white font-bold text-sm tracking-wider uppercase mb-1">Resources</h3>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Documentation</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Security API</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Status</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Security Policy</a>
                </div>

                <!-- Links: COMPANY -->
                <div class="flex flex-col gap-4">
                  <h3 class="text-slate-900 dark:text-white font-bold text-sm tracking-wider uppercase mb-1">Company</h3>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">About Us</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Privacy</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Terms</a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-primary transition-colors text-sm w-fit">Contact</a>
                </div>
              </div>
              
              <!-- Bottom Bar -->
              <div class="flex flex-col md:flex-row justify-between items-center mt-16 pt-8 border-t border-primary/20 gap-4">
                <p class="text-slate-500 dark:text-slate-500 text-xs font-medium">
                  © 2026 SpecterTest Inc. All rights reserved.
                </p>
                <div class="flex items-center gap-6">
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-white transition-colors">
                    <span class="material-symbols-outlined text-lg">share</span>
                  </a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-white transition-colors">
                    <span class="material-symbols-outlined text-lg">public</span>
                  </a>
                  <a href="#" class="text-slate-600 dark:text-slate-400 hover:text-primary dark:hover:text-white transition-colors">
                    <span class="material-symbols-outlined text-lg">alternate_email</span>
                  </a>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const targetUrl = ref('')
const userAgents = ref(5)
const adminAgents = ref(2)
const attackerAgents = ref(3)
const isDark = ref(true)
const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20
}

// Computed properties for Live Attack Power UI
const totalAttackPower = computed(() => {
  return (userAgents.value * 2) + (adminAgents.value * 5) + (attackerAgents.value * 15);
})

const powerColorClass = computed(() => {
  const power = totalAttackPower.value;
  if (power < 50) return 'text-primary';
  if (power < 150) return 'text-yellow-500';
  return 'text-red-500 shadow-red-500/50 drop-shadow-[0_0_8px_rgba(239,68,68,0.5)]';
})

const powerBarColorClass = computed(() => {
  const power = totalAttackPower.value;
  if (power < 50) return 'bg-primary';
  if (power < 150) return 'bg-yellow-500';
  return 'bg-red-500';
})

// Terminal Simulation State
const terminalLogs = ref([])
const terminalRef = ref(null)
let terminalInterval = null;

const commandPalette = [
  { text: "Initializing Specter Core Engine v2.4.1...", type: "system" },
  { text: "Establishing secure tunnel to target nodes", type: "system" },
  { text: "Swarm deployed. 10 active agents in cluster.", type: "success" },
  { text: "Agent-02: Enumerating endpoints starting at /api/v1", type: "system" },
  { text: "Agent-04: Bypassing WAF heuristics... [OK]", type: "success" },
  { text: "Agent-07: Detected potential IDOR vulnerability at /users/{id}", type: "warning" },
  { text: "Agent-01: Extracting JWT signature secrets...", type: "system" },
  { text: "CRITICAL: Agent-03 successfully elevated privileges to admin", type: "error" },
  { text: "Agent-09: Mapping dependency graph for path traversal", type: "system" },
  { text: "Agent-05: Brute-forcing directory structure [52%]", type: "system" },
  { text: "Warning: Target rate-limiting detected, rotating origin IPs", type: "warning" },
  { text: "Agent-08: Stored XSS payload successfully injected", type: "error" },
];

const addRandomLog = async () => {
  const randomCmd = commandPalette[Math.floor(Math.random() * commandPalette.length)];
  let logText = randomCmd.text;
  
  // Add some dynamic jitter to make it look real
  if (logText.includes(']')) {
    logText = logText.replace(/\[\d+%\]/, `[${Math.floor(Math.random() * 100)}%]`);
  }
  
  // Format current time like [10:42:01.321]
  const now = new Date();
  const timeStr = `[${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')}:${now.getSeconds().toString().padStart(2,'0')}.${now.getMilliseconds().toString().padStart(3,'0')}]`;
  
  terminalLogs.value.push({
    text: `<span class="opacity-50 text-xs mr-2">${timeStr}</span> ${logText}`,
    type: randomCmd.type
  });

  if (terminalLogs.value.length > 15) {
    terminalLogs.value.shift();
  }
  
  // Auto-scroll to bottom
  await nextTick();
  if (terminalRef.value) {
    terminalRef.value.scrollTop = terminalRef.value.scrollHeight;
  }
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.theme = 'dark'
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.theme = 'light'
  }
}

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
  window.addEventListener('scroll', handleScroll)
  
  // Start terminal simulation
  terminalLogs.value.push({ text: "Boot sequence initiated...", type: "system" });
  terminalInterval = setInterval(() => {
    addRandomLog();
  }, 1200 + Math.random() * 2000); // Random interval between 1.2s and 3.2s

  // Theme initialization
  if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDark.value = false
    document.documentElement.classList.remove('dark')
  }

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

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  if (terminalInterval) clearInterval(terminalInterval);
})
</script>

<style scoped>
/* Scoped styles are mostly handled by Tailwind now, keep minimal overrides if needed */
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
