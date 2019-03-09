import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { RestProvider } from '../../providers/rest/rest';

/**
 * Generated class for the InfoPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-info',
  templateUrl: 'info.html',
})
export class InfoPage {

  data: any;
  mode: any;

  constructor(public navCtrl: NavController, public navParams: NavParams, public restProvider: RestProvider) {
    let page = this.navParams.get('page');
    this.mode = page;
    if(page === "find_driver"){
      let params = this.navParams.get('params');
      this.waitForDriver(params);
    }
  }

  waitForDriver(params){
    this.restProvider.findDriver(params.latitude, params.longitude).then(
      data => {
        this.data = data;
        if(data.is_match){
          this.page = "driver_found";
        }
        else{
          console.log("WAIT FOR DRIVER BEAT");
          setTimeout(() => {
            this.waitForDriver(params);
          }, 2000);
        }
    })
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad InfoPage');
  }

}
