<template>
  <v-card class="pa-6" elevation="6" rounded>
    <v-card-title class="text-h4 font-weight-bold mb-6 primary--text">
      📊 Pregled studenata
    </v-card-title>
    <v-simple-table class="elevation-1">
      <thead>
        <tr class="blue lighten-5" style="border-bottom: 2px solid #3f51b5;">
          <th class="text-left pa-4">Podatak</th>
          <th
            v-for="(student, index) in students"
            :key="index"
            class="text-center pa-4"
          >
            <v-chip color="indigo lighten-2" text-color="white" class="ma-0 font-weight-semibold">
              Student {{ index + 1 }}
            </v-chip>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(field, idx) in fields"
          :key="idx"
          :class="idx % 2 === 0 ? 'grey lighten-4' : ''"
          class="transition-smooth"
        >
          <td class="font-weight-medium pa-4">{{ field.label }}</td>
          <td
            v-for="(student, sIndex) in students"
            :key="field.key + '-' + sIndex"
            class="text-center pa-4"
          >
            {{ formatValue(student[field.key], field.isPercentage) }}
          </td>
        </tr>
      </tbody>
    </v-simple-table>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const students = ref([]);

const fields = [
  { key: "sex", label: "Spol", isPercentage: false },
  { key: "math percentage", label: "Matematika (%)", isPercentage: true },
  { key: "reading score percentage", label: "Čitanje (%)", isPercentage: true },
  { key: "writing score percentage", label: "Pisanje (%)", isPercentage: true },
];

const formatValue = (value, isPercentage) => {
  if (isPercentage) return (value * 100).toFixed(0) + "%";
  return value;
};

const fetchData = async () => {
  try {
    const response = await axios.get("http://localhost:8000/data/statistics");
    students.value = response.data.students;
  } catch (err) {
    console.error("Greška pri dohvaćanju podataka:", err);
  }
};

onMounted(fetchData);
</script>

<style scoped>
.v-card {
  max-width: 1500px;
  max-height:3000px;
  margin: auto;
  padding: 3px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 80vh;
}

.v-simple-table {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
}
</style>
