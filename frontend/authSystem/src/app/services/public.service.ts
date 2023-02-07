import { Injectable } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
// This can fetch data from backend server using HttpClient.get method
export class PublicService {
  api_url = 'http://127.0.0.1:8080/';
  constructor(private http: HttpClient) { }

  // fetch data with this method using the get-fetch methodology
  getMessage() {
    return this.http.get(this.api_url);
  }
}
