<template>
  <v-card class="pa-4 full-width-card">
    <v-card-title>Predikcije prolaznosti za 10 studenata</v-card-title>

    <div class="content-wrapper">
      <div class="table-wrapper">
        <v-simple-table>
          <thead>
            <tr>
              <th></th>
              <th>Parental Level of Education | </th>
              <th>RF Predikcija (%) | </th>
              <th>DL Predikcija (%) | </th>
              <th>DL Vjerojatnost (%) </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(student, index) in studentsWithPredictions" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ student.parental_level_of_education }}</td>
              <td>{{ (student.random_forest_prediction * 100).toFixed(0) }}</td>
              <td>{{ (student.deep_learning_prediction * 100).toFixed(0) }}</td>
              <td>{{ (student.deep_learning_probability * 100).toFixed(1) }}</td>
            </tr>
          </tbody>
        </v-simple-table>
      </div>

      <div class="chart-wrapper">
        <canvas ref="predictionChart" style="max-height: 350px; width: 100%;"></canvas>
      </div>
    </div>

    <!-- Opis i statistika -->
    <p class="description mt-6">
      Ova analiza prikazuje predikcije prolaznosti studenata koristeći dva modela: Random Forest (RF) i Deep Learning (DL). 
      Vrijednosti su izražene u postotcima. DL vjerojatnost predstavlja pouzdanost DL modela u toj predikciji.
      Najviša DL vjerojatnost prolaznosti među prikazanim studentima je <strong>{{ maxProbability }}%</strong>, 
      a najniža je <strong>{{ minProbability }}%</strong>.
    </p>

    <!-- Loading indikator -->
    <div v-if="loading" class="loading-overlay">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>
  </v-card>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

const students = ref([])
const studentsWithPredictions = ref([])
const loading = ref(false)

const predictionChart = ref(null)
let chartInstance = null

const maxProbability = ref(0)
const minProbability = ref(100)

const fetchStudents = async () => {
  try {
    const response = await axios.get('http://localhost:8000/data/data-summary')
    students.value = response.data.sample.slice(0, 10)
  } catch (e) {
    console.error('Greška kod dohvaćanja studenata:', e)
  }
}

const fetchPredictionForStudent = async (student) => {
  try {
    const payload = {
      sex: student.sex,
      race_ethnicity: student["race/ethnicity"],
      parental_level_of_education: student["parental level of education"],
      lunch: student.lunch,
      test_preparation_course: student["test preparation course"],
      math_percentage: student["math percentage"],
      reading_score_percentage: student["reading score percentage"],
      writing_score_percentage: student["writing score percentage"]
    }
    const response = await axios.post('http://localhost:8000/predict/predict', payload)
    return { ...student, ...response.data }
  } catch (e) {
    console.error('Greška kod predikcije:', e)
    return { ...student }
  }
}

const fetchAllPredictions = async () => {
  loading.value = true
  await fetchStudents()
  const promises = students.value.map(student => fetchPredictionForStudent(student))
  studentsWithPredictions.value = await Promise.all(promises)
  loading.value = false
}

watch(studentsWithPredictions, (newVal) => {
  if (newVal.length) {
    maxProbability.value = Math.max(...newVal.map(s => s.deep_learning_probability * 100)).toFixed(1)
    minProbability.value = Math.min(...newVal.map(s => s.deep_learning_probability * 100)).toFixed(1)
    renderChart()
  }
})

function renderChart() {
  if (!predictionChart.value) return
  if (chartInstance) chartInstance.destroy()

  const ctx = predictionChart.value.getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: studentsWithPredictions.value.map((_, i) => `Student ${i + 1}`),
      datasets: [
        {
          label: 'Random Forest Predikcija (%)',
          data: studentsWithPredictions.value.map(s => (s.random_forest_prediction || 0) * 100),
          backgroundColor: '#3f51b5'
        },
        {
          label: 'Deep Learning Predikcija (%)',
          data: studentsWithPredictions.value.map(s => (s.deep_learning_prediction || 0) * 100),
          backgroundColor: '#e91e63'
        }
      ]
    },
    options: {
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: ctx => ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(1) + '%'
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: val => val + '%'
          }
        }
      }
    }
  })
}

onMounted(fetchAllPredictions)
</script>

<style scoped>
.full-width-card {
  max-width: 95vw;
  margin: 2rem auto;
  padding: 2rem 2rem;
  box-sizing: border-box;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(63, 81, 181, 0.12);
  position: relative;
  transition: box-shadow 0.3s ease;
}

.full-width-card:hover {
  box-shadow: 0 12px 32px rgba(63, 81, 181, 0.2);
}

.v-card-title {
  font-size: 2rem;
  font-weight: 700;
  color: #3f51b5;
  text-align: center;
  margin-bottom: 2rem;
  letter-spacing: 0.03em;
}

.content-wrapper {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
}

.table-wrapper {
  flex: 1 1 55%;
  min-width: 320px;
  max-height: 500px;
  overflow-y: auto;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(63, 81, 181, 0.12);
  background: #fafafa;
  padding: 1rem;
}

.chart-wrapper {
  flex: 1 1 40%;
  min-width: 300px;
  background: #fff;
  padding: 1rem;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(233, 30, 99, 0.12);
  display: flex;
  justify-content: center;
  align-items: center;
}

.v-simple-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 10px;
}

.v-simple-table thead tr {
  background-color: #e8eaf6;
  border-bottom: 3px solid #3f51b5;
  border-radius: 12px;
}

.v-simple-table thead th {
  padding: 14px 12px;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 1rem;
  color: #3f51b5;
  text-align: center;
  letter-spacing: 0.05em;
}

.v-simple-table tbody tr {
  background-color: #fafafa;
  transition: background-color 0.3s ease;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.v-simple-table tbody tr:hover {
  background-color: #dde3f8;
  box-shadow: 0 4px 12px rgba(63, 81, 181, 0.15);
}

.v-simple-table tbody td {
  padding: 12px 10px;
  text-align: center;
  font-size: 1rem;
  color: #424242;
}

.v-simple-table tbody td:first-child {
  font-weight: 700;
  color: #1a237e;
  text-align: left;
  padding-left: 20px;
}

.description {
  font-size: 1rem;
  color: #3f51b5;
  max-width: 100%;
  margin: 2rem auto 0;
  text-align: center;
  font-weight: 500;
  line-height: 1.4;
  padding: 0 1rem;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  z-index: 10;
}

/* Scrollbar stil (opcionalno) */
.table-wrapper::-webkit-scrollbar {
  width: 8px;
}
.table-wrapper::-webkit-scrollbar-thumb {
  background-color: rgba(63, 81, 181, 0.4);
  border-radius: 4px;
}
</style>
