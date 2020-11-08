<template>
  <div class="hello">

    <h3>Get currency dynamic</h3>
    <div>
      <label>Choose a currency:</label>
      <b-form-select :options="currencies" v-model="currency" required></b-form-select>
      <br>
      <label>and dates to compare: </label>
      <b-form-datepicker id="example-datepicker" v-model="start_date" placeholder="Choose first date" class="mb-2"></b-form-datepicker>
      <br>
      <b-form-datepicker id="example-datepicker" v-model="end_date" placeholder="Choose second date" class="mb-2"></b-form-datepicker>
      <b-btn @click="getValues">Get results!</b-btn>
    </div>
    <div v-if="result">
      <br>
      {{this.currency}} rate at {{this.start_date + ": " + this.result.start_rate}}
      <br>
      {{this.currency}} rate at {{this.end_date + ": " + this.result.end_rate}}
      <br>
      difference is {{this.result.rate_difference}}
    </div>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

export default {
  name: 'CurrencyInspector',
  props: {
    currencies: [],
    currency: null,
    end_date: null,
    start_date: null,
    result: Object
  },
  mounted () {
    this.getList()
  },
  computed: {
  },
  methods: {
    setCurrencyOptions (curr) {
      var result = []
      curr.forEach((item) => {
        result.push(
          { 'value': item.code,
            'text': item.name + ', ' + item.code }
        )
      })
      return result
    },
    getList () {
      console.log('fetching')
      fetch('http://localhost:5000/list')
        .then(res => res.json())
        .then(data => {
          this.currencies = this.setCurrencyOptions(data.currencies)
        })
    },
    getValues () {
      var url = new URL('http://localhost:5000/difference')
      var params = {
        'start_date': this.start_date,
        'end_date': this.end_date,
        'currency': this.currency
      }
      url.search = new URLSearchParams(params).toString()
      fetch(url)
        .then(res => res.json())
        .then(res => {
          this.result = res
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
