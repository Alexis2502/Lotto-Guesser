<template>
  <div>
    <h3>Występowanie liczb w MiniLotto:</h3>
    <canvas ref="lottoChart"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
  name: 'LottoChart',
  mounted() {
    this.drawChart();
  },
  methods: {
    async drawChart() {
      try {
        const response = await axios.get('http://localhost:5000/lotto-results');
        const data = response.data.minilotto;

        if (!Array.isArray(data) || data.length === 0) {
          throw new Error('No data available');
        }

        const labels = data.map(entry => entry[0]);
        const dataCounts = data.map(entry => entry[1]);

        const canvas = this.$refs.lottoChart;
        const ctx = canvas.getContext('2d');

        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: labels.map(num => `${num}`),
            datasets: [{
              label: 'Occurrences',
              data: dataCounts,
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            }]
          },
          options: {
            indexAxis: 'x',
            scales: {
              x: {
                beginAtZero: true
              }
            }
          }
        });

      } catch (error) {
        console.error('Error fetching or processing data:', error.message);
      }
    }
  }
}
</script>
