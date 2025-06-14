<template>
  <v-app>
    <v-main>
      <v-container>
        <h2 class="text-h5 font-weight-bold mb-4">Uspjeh studenata na ispitima</h2>

        <v-tabs v-model="tab" grow background-color="primary" dark>
          <v-tab>Tablični podaci</v-tab>
          <v-tab>Grafikoni</v-tab>
          <v-tab>Prediktivna analitika</v-tab>
        </v-tabs>

        <v-window v-model="tab">
          <v-window-item :value="0"><DataTableView /></v-window-item>
          <v-window-item :value="1"><ChartsView /></v-window-item>
          <v-window-item :value="2"><PredictionsView /></v-window-item>
        </v-window>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import DataTableView from './components/DataTableView.vue'
import ChartsView from './components/ChartsView.vue'
import PredictionsView from './components/PredictionsView.vue'

const tab = ref(0)
</script>
