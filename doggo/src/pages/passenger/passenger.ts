import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams, ModalController } from 'ionic-angular';
import {AutocompletePage} from '../autocomplete/autocomplete';
import { InfoPage } from '../info/info';

/**
 * Generated class for the PassengerPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-passenger',
  templateUrl: 'passenger.html',
})
export class PassengerPage {
  address;
  show_button: boolean = false;

  constructor(public navCtrl: NavController, public navParams: NavParams, private modalCtrl:ModalController) {
    this.address = {
      place: ''
    };
  }

  showAddressModal(){
    let modal = this.modalCtrl.create(AutocompletePage);
    modal.onDidDismiss(data => {
      if(data && 'place' in data){
        this.address = data;
        this.show_button = true;
      }
    });
    modal.present();
  }

  findingRider() {
    this.navCtrl.push(InfoPage, {
      'page': 'find_driver',
      'params': this.address
    })
  }

}
