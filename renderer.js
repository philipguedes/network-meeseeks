'use-strict'

const zerorpc = require('zerorpc')
var _ = require('lodash')
// var client = new zerorpc.Client()

// client.connect("tcp://127.0.0.1:4242")

// module.exports = client;

class ApiController {

  constructor () {
    this.client = new zerorpc.Client();
    this.client.connect("tcp://127.0.0.1:4242");
    // this.routes = 
  }
  
  updateImage(route) {
    var routes = ['voip', 'gaming', 'dash', 'lstreaming']
    return new Promise ((resolve, reject) => {
      if (_.includes(routes, route)) {
        this.client.invoke(route, (error, res) => {
          if (error) {
            console.log(error);
            reject(error)
          }
          else {
            console.log('new figures omg')
            resolve(res)
          }

        });
      }
      else {
        console.log('invalid route')
        reject('Not a valid route')
      }
    });

    console.log(found)
  }

  getImages() {
    return new Promise ((resolve, reject) => {
      this.client.invoke("get_images", (error, res) => {
        if (error) {
          console.log(error);
          reject(error);
        }
        else {
          console.log('new figures omg')
          // console.log(res);
          resolve(res);
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
