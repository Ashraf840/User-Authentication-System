import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';  // Require to import HttpClientModule in the app.module
import { LoginModel } from 'src/app/auth/models/login-model';
import { catchError, map, of } from 'rxjs';
import { TokenModel } from './token-model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  loginURL!: string;

  constructor(private http: HttpClient) { }

  // NB: Consume this method into the login.component file
  userLogin(payload: LoginModel) {
    // Require an interface to hold the data sent back from the API.
    this.loginURL = 'http://127.0.0.1:8080/api/v1/auth/login/';
    return this.http.post(this.loginURL, payload)
      .pipe(
        map(
          (data) => {
            var tokens = data as TokenModel;
            console.log("Login response:", tokens);
            // Store the token-data into browser's local storage
            localStorage.setItem("tokens", JSON.stringify(tokens));
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
