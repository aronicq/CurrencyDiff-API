<template>
  <div id="app">
    <CurrencyInspector/>
  </div>
</template>

<script>
import CurrencyInspector from './components/CurrencyInspector'

export default {
  name: 'App',
  components: {CurrencyInspector}
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
