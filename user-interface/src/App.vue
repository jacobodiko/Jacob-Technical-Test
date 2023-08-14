<script setup>
import { onMounted, ref } from "vue";
const ip = ref(null);
const loading = ref(false);

async function getIp() {
  ip.value = null;
  loading.value = true;
  await fetch("http://127.0.0.1:5000/gateway-ip")
    .then((response) => response.json())
    .then((data) => {
      ip.value = data.ip;
    })
    .catch((error) => {
      console.log(error);
    });
  loading.value = false;
}

onMounted(async () => {
  await getIp();
})
</script>

<template>
    <div class="container">
      <h1>Gateway IP</h1>
      <p v-if="ip" class="text">{{ ip }}</p>
      <p v-else-if="loading" class="text">Waiting...</p>
      <p v-else class="text">IP not Found</p>
      <button class="button" @click="getIp">Retrieve IP</button>
    </div>
</template>

<style scoped>
header {
  line-height: 1.5;
}
h1 {
  font-size: 4em;
  text-align: center;
  margin: 24px;
  font-weight: bold;
}
.button {
  margin: 16px;
  padding: 16px;
  background: yellow;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
}

.text {
  font-size: 3em;
  text-align: center;
  margin: 24px;
}

.container {
  width: 100%;
  text-align: center;
}
</style>
