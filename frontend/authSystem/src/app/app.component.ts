import { Component } from '@angular/core';
import { PublicService } from './services/public.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Django & Angular Auth System';
  msg: any;

  constructor(private pServices:PublicService) {}
  ngOnInit(): void {
    this.showMessage();
  }

  // method to show msg fetched from backend-API.
  showMessage() {
    this.pServices.getMessage().subscribe(data=>{
      this.msg = data;
      console.log("Message: ", this.msg);
    });
  }
}
