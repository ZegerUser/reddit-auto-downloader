<script>
import headerBar from '../components/headerBar.vue'
import config from '../components/config.vue'
export default {
  components: {
    headerBar,
    config
  }
}
</script>

<template>
    <headerBar />
    <Suspense>
        <config />
    </Suspense>
</template>