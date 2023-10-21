import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { AuthGuard } from 'src/app/shared/authGuard/auth-guard';

const routes: Routes = [
  {
    path:'login',
    component:LoginComponent,
    data: {
      requiredAuth: false
    },
    canActivate:[AuthGuard]
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthRoutingModule { }
