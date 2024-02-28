import { Component, OnInit } from '@angular/core';
import { LoginModel } from '../models/login-model';
import { AuthService } from 'src/app/shared/auth/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {

  constructor(private authService: AuthService) { }

  // Require an interface to hold the data sends back from the HTML template
  loginForm: LoginModel = {
    email: '',
    password: '',
  }

  ngOnInit(): void { }

  userLogin() {
    this.authService.userLogin(this.loginForm)
      .subscribe((data) => {
        if (data) {
          alert("success");
        } else {
          alert("failed");
        }
      })
  }

}
