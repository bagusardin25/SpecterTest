<template>
  <div class="app-container">
    <header class="app-header">
      <div class="brand">
        <span class="cyber-icon">👻</span>
        <h1>Specter<span class="highlight">Test</span></h1>
      </div>
      <nav class="app-nav">
        <!-- Optional global navigation can go here later -->
      </nav>
    </header>

    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(13, 9, 20, 0.8);
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand h1 {
  font-size: 1.5rem;
  margin: 0;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.highlight {
  color: var(--primary-color);
  text-shadow: 0 0 10px rgba(159, 122, 234, 0.5);
}

.cyber-icon {
  font-size: 1.75rem;
  display: inline-block;
}

.app-main {
  flex: 1;
  padding: 2rem;
  position: relative;
}

/* Page transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
