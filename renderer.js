'use-strict'

const zerorpc = require('zerorpc')
// var client = new zerorpc.Client()

// client.connect("tcp://127.0.0.1:4242")

// module.exports = client;

class ApiController {

  constructor () {
    this.client = new zerorpc.Client();
    this.apiRoute = 
    this.client.connect("tcp://127.0.0.1:4242");
  }

  getImages() {
    return new Promise ((resolve, reject) => {
      this.client.invoke("voip", (error, res) => {
        if (error) {
          console.log(error);
        }
        else {
          console.log('heeeeey')
          console.log(res);
        }

      });
    
    });
  }

  loadStatistics() {
    // var data = {}
    // var data = 
    return new Promise((resolve, reject) => {
      this.client.invoke("recent_data", (error, res) => {
      if (error) {
        console.log(error)
        return reject({name: 'test'})
      }
      else {
        var data = {}
        data['last_update'] = res['last_update'];
        data['voip'] = res['voip'];
        data['gaming'] = res['gaming'];
        data['dash'] = res['dash'];
        data['lstreaming'] = res['lstreaming'];
        return resolve(data)
      }
    })
  });
    // return data;
  }

  getGraphData() {}


}

var api = new ApiController()

module.exports = api;
