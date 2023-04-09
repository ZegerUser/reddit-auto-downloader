<script>
import axios from "axios"
export default{
       props: ["name"],
       methods: {
        async removeSub(subString) {
            const res = await axios.delete("http://localhost:3000/config/remove", { data: {"sub": subString} })
            window.location.reload()
        }
  }
} 
</script>

<template>
    <li>{{ name }} <button @click="removeSub(name)">X</button></li>
</template>