import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

/*
  Generated class for the RestProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class RestProvider {

  base_api_url = 'http://localhost:5000';

  constructor(public http: HttpClient) {
    console.log('Hello RestProvider Provider');
  }

  findDriver(lat, lng) {
    return new Promise(resolve => {
      this.http.get(this.base_api_url+'/find_driver?lat='+lat+'&lng='+lng).subscribe(data => {
        resolve(data);
      },
      err => {
        console.log(err);
      });
    });
  }

  isPassenger() {
    return new Promise(resolve => {
      this.http.get(this.base_api_url+'/is_passenger').subscribe(data => {
        resolve(data);
      },
      err => {
        console.log(err);
      });
    });
  }

  findDestination() {
    return new Promise(resolve => {
      this.http.get(this.base_api_url+'/wait_for_destination').subscribe(data => {
        resolve(data);
      },
      err => {
        console.log(err);
      });
    });
  }

  replyToPassenger(reply){
    return new Promise(resolve => {
      this.http.get(this.base_api_url+'/reply_to_passenger?reply='+reply).subscribe(data => {
        resolve(data);
      },
      err => {
        console.log(err);
      });
    });
  }

}
