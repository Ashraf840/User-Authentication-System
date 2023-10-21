import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FavMovieModel } from '../models/fav-movie-model';

@Injectable({
  providedIn: 'root'
})
export class MoviesService {

  constructor(private http:HttpClient) { }

  getFavMovies() {
    return this.http.get<FavMovieModel[]>('http://localhost:3000/user/fav-movies')
  }
}
