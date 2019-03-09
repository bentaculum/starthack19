import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { RestProvider } from '../../providers/rest/rest';
import { ConfirmPage } from '../confirm/confirm';

/**
 * Generated class for the DriverPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-driver',
  templateUrl: 'driver.html',
})
export class DriverPage {
  is_online: boolean = true;

  constructor(public navCtrl: NavController, public navParams: NavParams, public restProvider: RestProvider) {
    let mode = navParams.get('mode');
    if(mode && mode == "destination_set"){
        this.waitForPassenger();
      }
    else{
        this.waitForDestination();
    }
  }

  waitForDestination(){
    this.restProvider.findDestination().then(
      data => {
        if(data.place){
          this.navCtrl.push(ConfirmPage, {
            'data': data.place,
            'mode': 'destination'
          })
        }
        else{
          console.log("WAIT FOR DESTINATION BEAT");
          setTimeout(() => {
            this.waitForDestination(params);
          }, 2000);
        }
    })
  }

  waitForPassenger(){
    this.restProvider.isPassenger().then(
      data => {
        if(data.success){
          this.navCtrl.push(ConfirmPage, {
            'mode': 'pickup'
          })
        }
        else{
          console.log("WAIT FOR PASSENGER BEAT");
          setTimeout(() => {
            this.waitForDestination(params);
          }, 2000);
        }
    })
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad DriverPage');
  }

}
