<template>
  <Login v-if="!session.logged" />
  <router-view v-else />
</template>

<script setup>
import { useSession } from './stores/session.js'
import Login from './views/Login.vue'

const session = useSession()
</script>
