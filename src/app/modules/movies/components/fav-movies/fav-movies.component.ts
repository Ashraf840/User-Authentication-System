import { FavMovieModel } from '../../models/fav-movie-model';
import { MoviesService } from './../../services/movies.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-fav-movies',
  templateUrl: './fav-movies.component.html',
  styleUrls: ['./fav-movies.component.css']
})
export class FavMoviesComponent implements OnInit{
  constructor(private moviesService:MoviesService) {}

  favMovies:FavMovieModel[] = [];

  ngOnInit(): void {
    this.moviesService.getFavMovies().subscribe((data) => {
      this.favMovies = data;
    })
  }
}
