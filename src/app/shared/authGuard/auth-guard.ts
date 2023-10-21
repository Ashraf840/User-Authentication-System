import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Injectable } from "@angular/core";
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth/auth.service';
import { TokenModel } from '../models/auth/token-model';
import { JwtHelperService } from '@auth0/angular-jwt';
import { UserProfileModel } from '../models/auth/user-profile-model';


@Injectable()
export class AuthGuard implements CanActivate {

    constructor(
        private authService: AuthService,
        private jwtHelperService: JwtHelperService,
        private router:Router
    ) { }

    canActivate(
        route: ActivatedRouteSnapshot,
        state: RouterStateSnapshot
    ):
        boolean
        | UrlTree
        | Observable<boolean | UrlTree>
        | Promise<boolean | UrlTree> {

        // Fetch the userProfile (BehaviorSubject) data. The data can be null for two reasons: user refreshes the page OR user is not authenticated
        var userProfile = this.authService.userProfile.getValue();
        // user (authenticated/not) refreshed the page
        if (!userProfile) {
            // fetch the token from the localStorage
            var jwtToken = localStorage.getItem('token');
            // user is authencated, since user's jwt token is set to the browser's localStorage
            if (jwtToken) {
                var token = JSON.parse(jwtToken) as TokenModel;
                var userInfo = this.jwtHelperService.decodeToken(token?.access_token) as UserProfileModel;
                this.authService.userProfile.next(userInfo);
                userProfile = userInfo;
            }
        }

        // Check user is authenticated 
        if ((userProfile?.sub ?? 0) > 0) {
            // user is authenticated, but still trying to access into those pages where authentication (being authenticated) is not required
            if (route.data['requiredAuth'] == false) {
                this.router.navigate(['/'])
                return false;
            }
            return true;
        } else {
            // user is not authenticated, but still tryiing to access those pages where being authenticated is required 
            if (route.data['requiredAuth'] == true) {
                this.router.navigate(['/auth/login']);
                return false;
            }
            return true;
        }
    }

}
