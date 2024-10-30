<template>
  <div id="app">
    <div class="tabs">
      <button v-for="game in games" :key="game" @click="selectedGame = game" :class="{ active: selectedGame === game }">{{ game }}</button>
    </div>
    <div class="content">
      <div v-if="selectedGame === 'Lotto'">
        <h2>Lotto</h2>
        <lotto-chart />
      </div>
      <div v-else-if="selectedGame === 'MiniLotto'">
        <h2>MiniLotto</h2>
        <mini-lotto-chart />
      </div>
      <div v-else-if="selectedGame === 'EuroJackpot'">
        <h2>EuroJackpot</h2>
        <EuroJackpotChart />
      </div>
    </div>
  </div>
</template>


<script>
import LottoChart from './components/LottoChart.vue';
import MiniLottoChart from './components/MiniLottoChart.vue';
import EuroJackpotChart from './components/EuroJackpotChart.vue';

export default {
  name: 'App',
  data() {
    return {
      games: ['Lotto', 'MiniLotto', 'EuroJackpot'],
      selectedGame: 'Lotto'
    }
  },
  components: {
    LottoChart,
    MiniLottoChart,
    EuroJackpotChart
  }
}
</script>

<style>
.tabs {
  display: flex;
}

.tabs button {
  background-color: #f1f1f1;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 10px 20px;
  transition: background-color 0.3s;
}

.tabs button.active {
  background-color: #ddd;
}

.content {
  margin-top: 20px;
}
</style>
