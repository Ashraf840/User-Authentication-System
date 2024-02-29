import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';  // Require to import HttpClientModule in the app.module
import { LoginModel } from 'src/app/auth/models/login-model';
import { BehaviorSubject, catchError, map, of } from 'rxjs';
import { TokenModel } from './token-model';
import { JwtHelperService } from '@auth0/angular-jwt';
import { UserProfile } from './user-profile';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  loginURL!: string;

  constructor(private http: HttpClient) { }

  // Install "@autho0/anguler-jwt" package to decode jwt tokens;  Link - https://www.npmjs.com/package/@auth0/angular-jwt
  jwtHelper = new JwtHelperService();
  userProfile = new BehaviorSubject<UserProfile | null>(null);

  // NB: Consume this method into the login.component file
  userLogin(payload: LoginModel) {
    // Require an interface to hold the data sent back from the API.
    this.loginURL = 'http://127.0.0.1:8080/api/v1/auth/login/';
    return this.http.post(this.loginURL, payload)
      .pipe(
        map(
          (data) => {
            var tokens = data as TokenModel;

            // Store the token-data into browser's local storage
            localStorage.setItem("tokens", JSON.stringify(tokens));

            // console.log("Login response:", tokens);
            // console.log("Decoded token:", this.jwtHelper.decodeToken(tokens?.access_token));

            var userData = this.jwtHelper.decodeToken(tokens?.access_token) as UserProfile;
            userData['email'] = tokens?.email;
            userData['full_name'] = tokens?.full_name;

            // console.log("User Profile data:", userData);

            this.userProfile.next(userData);

            return true;
          }
        ),
        catchError(
          (error) => {
            console.log(error);
            return of(false);
          }
        )
      )
  }
}
