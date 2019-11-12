
var app = new Vue({
  delimiters: ['${', '}'],
  el: '#app',
  data: {
    longUrl: '',
    shortUrl:''
  },
  methods: {
    resolveUrl: function (event) {
      //getting the short URL from the server
      axios.get('/resolveShortUrl?longUrl=' + encodeURIComponent(this.longUrl))
            .then((response) => {
              //concating the domain's url to the short URL code
              this.shortUrl = document.location.href + response.data.url;
      });

    }
  }
});
