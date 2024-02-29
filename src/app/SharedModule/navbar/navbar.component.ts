import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/shared/auth/auth.service';
import { UserProfile } from 'src/app/shared/auth/user-profile';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  userProfile?: UserProfile | null; // make the variable or "nullable" since the "BehaviorSubject" is instantiated as of type UserProfile or null.

  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.authService.userProfile.subscribe((data) => {
      this.userProfile = data;
      // console.log("User profile:", this.userProfile);
    });
  }

}
