import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FavMoviesComponent } from './components/fav-movies/fav-movies.component';
import { AuthGuard } from 'src/app/shared/authGuard/auth-guard';

const routes: Routes = [
  {
    path:'fav-movies',
    component:FavMoviesComponent,
    data: {
      requiredAuth: true
    },
    canActivate:[AuthGuard]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MoviesRoutingModule { }
