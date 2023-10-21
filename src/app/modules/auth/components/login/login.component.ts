import { AuthService } from './../../../../shared/services/auth/auth.service';
import { Component, OnInit } from '@angular/core';
import { LoginModel } from '../../models/login-model';
import { Router } from '@angular/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  constructor(
    private authService:AuthService,
    private router:Router
  ) {}

  ngOnInit(): void {}

  loginForm:LoginModel = {
    username:'',
    password:'',
  }

  userLogin() {
    console.log(`Login method is invoked!`);
    console.log(`Login-form username:`, this.loginForm.username);
    console.log(`Login-form password:`, this.loginForm.password);
    console.log(`Loginform:`, this.loginForm);
    
    
    this.authService.userLogin(this.loginForm)
    .subscribe((data) => {
      if(data) {
        this.router.navigate(['/']);
      } else{
        console.log(`failed!`);
      }
    })
  }
}
