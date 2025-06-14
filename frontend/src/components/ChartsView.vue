<template>
  <v-card class="pa-4">
    <v-card-title>Grafički prikaz rezultata</v-card-title>
    <canvas ref="chartCanvas"></canvas>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios'

const chartCanvas = ref(null)

const fetchChartData = async () => {
  try {
    const response = await axios.get('http://localhost:8000/data/data-summary')
    const data = response.data.sample

    console.log('Sample data:', data)  // Provjeri točne nazive polja u konzoli

    // Koristi parental level of education za x-osi:
    const labels = data.map(s => s['parental level of education'] || 'Nepoznato')

    const mathScores = data.map(s => s['math percentage'] || 0)
    const readingScores = data.map(s => s['reading score percentage'] || 0)
    const writingScores = data.map(s => s['writing score percentage'] || 0)

    const ctx = chartCanvas.value.getContext('2d')

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Matematika',
            data: mathScores,
            backgroundColor: '#3f51b5',
          },
          {
            label: 'Čitanje',
            data: readingScores,
            backgroundColor: '#e91e63',
          },
          {
            label: 'Pisanje',
            data: writingScores,
            backgroundColor: '#009688',
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 1,
            ticks: {
              callback: val => (val * 100).toFixed(0) + '%'
            }
          }
        }
      },
    })
  } catch (err) {
    console.error('Greška pri dohvaćanju podataka za graf:', err)
  }
}

onMounted(fetchChartData)
</script>

<style scoped>
.v-card {
  max-width: 1500px;
  max-height: 600px;
  margin: auto;
  background-color: #ffffff !important;
  border-radius: 16px !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.v-card canvas {
  width: 100% !important;
  height: auto !important;
  max-height: 400px;
  display: block;
}

@media (max-width: 768px) {
  .v-card {
    padding: 3rem;
    max-width: 100%;
  }
  .v-card canvas {
    max-height: 300px;
  }
}

@media (max-width: 480px) {
  .v-card {
    padding: 1rem;
  }
  .v-card canvas {
    max-height: 250px;
  }
}
</style>
