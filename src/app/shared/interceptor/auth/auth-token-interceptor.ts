import { AuthService } from './../../services/auth/auth.service';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, catchError, switchMap, throwError } from "rxjs";
import { TokenModel } from "../../models/auth/token-model";
import { JwtHelperService } from "@auth0/angular-jwt";
import { UserProfileModel } from '../../models/auth/user-profile-model';
import { Router } from '@angular/router';

@Injectable()
export class AuthTokenInterceptor implements HttpInterceptor {
    constructor(
        private jwtHelperService: JwtHelperService,
        private authService: AuthService,
        private router: Router
    ) { }

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

        if (req.url.includes('login') || req.url.includes('refreshtoken')) {
          return next.handle(req);
        }
      
        const localStorageToken = localStorage.getItem('token');
        var token: TokenModel;
      
        if (localStorageToken) {
          token = JSON.parse(localStorageToken) as TokenModel;
          var isTokenExpired = this.jwtHelperService.isTokenExpired(token?.access_token);
      
          if (!isTokenExpired) {
            return next.handle(req);
          } else {
            return this.authService.refreshToken(token)
              .pipe(
                switchMap((newTokens: TokenModel) => {
                  localStorage.setItem('token', JSON.stringify(newTokens));
                  // Update userProfile data based on newly updated access token
                  var userInfo = this.jwtHelperService.decodeToken(newTokens?.access_token) as UserProfileModel;
                  this.authService.userProfile.next(userInfo);
                  // Auth token interceptor doesn't automatically add authorization header, thus we need to manually add the authorization header
                  const tranformReq = req.clone({
                    headers: req.headers.set('Authorization', `Bearer ${newTokens?.access_token}`)
                  });
                  return next.handle(tranformReq);
                }),
                catchError((error) => {
                  localStorage.removeItem('token');
                  this.authService.userProfile.next(null);
                  this.router.navigate(['/']);
                  return throwError('Invalid call');
                })
              );
          }
        }
        return throwError('Invalid call');
      }

}
