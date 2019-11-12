Vue.use(VueCharts);
var app = new Vue({
  delimiters: ['${', '}'],
  el: '#statisticsApp',
  data() {
    return {
      dataentry: null,
      datalabel: null,

      redirectionsCount:0,

      /*good requests */
      lastDayGoodLabels: [],
      lastDayGoodDataset: [],

      lastHourGoodLabels: [],
      lastHourGoodDataset: [],

      lastMinuteGoodLabels: [],
      lastMinuteGoodDataset: [],
      /*bad requests */
      lastDayBadLabels: [],
      lastDayBadDataset: [],

      lastHourBadLabels: [],
      lastHourBadDataset: [],

      lastMinuteBadLabels: [],
      lastMinuteBadDataset: []

    }
  },
  mounted: function () {
    this.getStatistics()
  },
  methods: {
    getStatistics: function (event) {
      //getting the statistics from the server
      axios.get('/getStatistics')
            .then((response) => {
              this.redirectionsCount = response.data["redirectionsCount"];
              /*good requests */
              lastDayRequestsGood = response.data["lastDayRequestsGood"];
              for (const item of lastDayRequestsGood) {
                this.lastDayGoodLabels.push(item[0]);
                this.lastDayGoodDataset.push(item[1]);
              }

              lastHourRequestsGood = response.data["lastHourRequestsGood"];
              for (const item of lastHourRequestsGood) {
                this.lastHourGoodLabels.push(item[0]);
                this.lastHourGoodDataset.push(item[1]);
              }

              lastMinuteRequestsGood = response.data["lastMinuteRequestsGood"];
              for (const item of lastMinuteRequestsGood) {
                this.lastMinuteGoodLabels.push(item[0]);
                this.lastMinuteGoodDataset.push(item[1]);
              }
              /*bad requests */
              lastDayRequestsBad = response.data["lastDayRequestsBad"];
              for (const item of lastDayRequestsBad) {
                this.lastDayBadLabels.push(item[0]);
                this.lastDayBadDataset.push(item[1]);
              }

              lastHourRequestsBad = response.data["lastHourRequestsBad"];
              for (const item of lastHourRequestsBad) {
                this.lastHourBadLabels.push(item[0]);
                this.lastHourBadDataset.push(item[1]);
              }

              lastMinuteRequestsBad = response.data["lastMinuteRequestsBad"];
              for (const item of lastMinuteRequestsBad) {
                this.lastMinuteBadLabels.push(item[0]);
                this.lastMinuteBadDataset.push(item[1]);
              }
              
      });

    }
  }
});

