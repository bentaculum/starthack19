import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { PassengerPage } from '../passenger/passenger';

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

}
