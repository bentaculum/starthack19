import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { PassengerPage } from '../passenger/passenger';
import { DriverPage } from '../driver/driver';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  constructor(public navCtrl: NavController) {
    this.navCtrl = navCtrl;

  }

  openPassengerPage() {
    this.navCtrl.push(PassengerPage)
  }

  openDriverPage() {
    this.navCtrl.push(DriverPage)
  }

}
