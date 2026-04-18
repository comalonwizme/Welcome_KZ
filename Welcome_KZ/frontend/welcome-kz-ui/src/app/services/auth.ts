import { Injectable, inject } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class Auth {
//  private http = inject(HttpClient);
  private api = 'http://localhost:8000';
  constructor(
    private http: HttpClient,
    private router: Router
  ){}

  register(data: any){
    return this.http.post(`${this.api}/register/`, data)
  }

  login(data: any){
    return this.http.post(`${this.api}/login/`, data)
  }

  saveTokens(access: string, refresh: string){
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  isLogged() : boolean{
    return !!localStorage.getItem('access_token')
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.router.navigate(['/login'])
  }

  getRole() : string | null{
    return localStorage.getItem('role');
  }
}
