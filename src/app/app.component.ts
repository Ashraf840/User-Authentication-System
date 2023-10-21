import { AuthService } from './shared/services/auth/auth.service';
import { Component, OnInit } from '@angular/core';
import { UserProfileModel } from './shared/models/auth/user-profile-model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  constructor(
    private authService:AuthService,
    private router:Router) {}
  title = 'jwt-auth';
  
  userProfile?:UserProfileModel | null;

  ngOnInit(): void {
    // Listen to the authService's userProfile attr.
    this.authService.userProfile.subscribe((data) => {
      this.userProfile = data;
    })
  }

  userLogout() {
    // console.log(`User logout method is called!`);
    // check if ther is any object called "token"
    if (localStorage.getItem('token') !== null) {
      // console.log(`Remove token`);
      this.authService.userProfile.next(null);
      // console.log(`User profile:`, this.authService.userProfile);
      localStorage.removeItem('token');
      this.router.navigate(['/auth/login']);
    }
  }
}
