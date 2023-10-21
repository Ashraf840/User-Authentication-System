import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MoviesRoutingModule } from './movies-routing.module';
import { FavMoviesComponent } from './components/fav-movies/fav-movies.component';


@NgModule({
  declarations: [
    FavMoviesComponent
  ],
  imports: [
    CommonModule,
    MoviesRoutingModule
  ]
})
export class MoviesModule { }
