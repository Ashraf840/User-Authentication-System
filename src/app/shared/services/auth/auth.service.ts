import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LoginModel } from 'src/app/modules/auth/models/login-model';
import { TokenModel } from '../../models/auth/token-model';
import { BehaviorSubject, catchError, map, of } from 'rxjs';
import { JwtHelperService } from '@auth0/angular-jwt';
import { UserProfileModel } from '../../models/auth/user-profile-model';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }
  jwtHelper = new JwtHelperService();
  userProfile = new BehaviorSubject<UserProfileModel | null>(null);

  // Method to acquire access token as an output
  getAccessToekn() {
    var localSAtorageToken = localStorage.getItem('token');
    if (localSAtorageToken) {
      var token = JSON.parse(localSAtorageToken) as TokenModel;
      var isTokenExpired = this.jwtHelper.isTokenExpired(token.access_token);
      // Token is expired/invalid
      if (isTokenExpired) {
        this.userProfile.next(null);
        return '';
      }
      // Token is valid
      var userInfo = this.jwtHelper.decodeToken(token?.access_token) as UserProfileModel;
      this.userProfile.next(userInfo);
      return token?.access_token;
    }
    return '';
  }

  userLogin(payload: LoginModel) {
    return this.http.post('http://localhost:3000/auth/login', payload)
      .pipe(
        map((data) => {
          var token = data as TokenModel;
          localStorage.setItem('token', JSON.stringify(token));

          console.log(`Decoded JWT Token:`, this.jwtHelper.decodeToken(token?.access_token));
          var userData = this.jwtHelper.decodeToken(token?.access_token) as UserProfileModel;
          this.userProfile.next(userData);

          return true;
        }),
        catchError((error) => {
          return of(false)
        })
      );
  }

  // Refresh Token; send expired access & refresh token as payload to acquire new tokens
  refreshToken(payload: TokenModel) {
    // Send data of type type TokenModel, which in return will provide a response of type TokenModel. Thus we define the type in "<TokenModel>" after the post method. 
    return this.http.post<TokenModel>('http://localhost:3000/auth/refreshtoken', payload)
  }
}
