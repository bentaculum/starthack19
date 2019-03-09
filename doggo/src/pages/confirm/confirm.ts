import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { RestProvider } from '../../providers/rest/rest';
import { InfoPage } from '../info/info';
import { DriverPage } from '../driver/driver';

/**
 * Generated class for the ConfirmPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-confirm',
  templateUrl: 'confirm.html',
})
export class ConfirmPage {
  data: any;
  mode: any;

  constructor(public navCtrl: NavController, public navParams: NavParams, public restProvider: RestProvider) {
    this.data = navParams.get('data');
    this.mode = navParams.get('mode');
  }

  confirmPassenger(){
    this.restProvider.replyToPassenger('yes').then(
      data => {
        this.navCtrl.push(InfoPage, {
          'mode': 'pickup'
        })
    });
  }

  setDestination(){
    this.navCtrl.push(DriverPage, {
      'mode': 'destination_set'
    })
  }

}
