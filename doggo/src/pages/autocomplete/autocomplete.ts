import {Component, NgZone} from '@angular/core';
import {ViewController} from 'ionic-angular';
import { IonicPage } from 'ionic-angular';

/**
 * Generated class for the AutocompletePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-autocomplete',
  templateUrl: 'autocomplete.html',
})
export class AutocompletePage {

  autocompleteItems;
  autocomplete;

  latitude: number = 0;
  longitude: number = 0;
  geo: any;

  service = new google.maps.places.AutocompleteService();

  constructor (public viewCtrl: ViewController, private zone: NgZone) {
    this.autocompleteItems = [];
    this.autocomplete = {
      query: ''
    };
  }

  dismiss() {
    this.viewCtrl.dismiss();
  }

  chooseItem(item: any) {
    this.geo = this.geoCode(item);//convert Address to lat and long
    this.viewCtrl.dismiss(this.geo);
  }

  updateSearch() {

    if (this.autocomplete.query == '') {
     this.autocompleteItems = [];
     return;
    }

    let me = this;
    this.service.getPlacePredictions({
    input: this.autocomplete.query,
    // componentRestrictions: {
    //   country: 'de'
    // }
   }, (predictions, status) => {
     me.autocompleteItems = [];

   me.zone.run(() => {
     if (predictions != null) {
        predictions.forEach((prediction) => {
          me.autocompleteItems.push(prediction.description);
        });
       }
     });
   });
  }

  //convert Address string to lat and long
  geoCode(address:any) {
    return {
      "place": address,
      "latitude": "23.2323",
      "longitude": "48.2323"
    }
   //  let geocoder = new google.maps.Geocoder();
   //  geocoder.geocode({ 'address': address }, (results, status) => {
   //
   //  this.latitude = results[0].geometry.location.lat();
   //  this.longitude = results[0].geometry.location.lng();
   //  alert("lat: " + this.latitude + ", long: " + this.longitude);
   // });
 }

}
