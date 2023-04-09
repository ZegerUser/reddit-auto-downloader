<script>
import axios from "axios"
export default {
  methods: {
    async addSub(subString) {
        const res = await axios.put("http://localhost:3000/config/add", {"sub": subString})
        window.location.reload()
    }
  }
}
</script>

<template>
    <textarea v-model="subString"></textarea>
    <button @click="addSub(subString)">add</button>
</template>