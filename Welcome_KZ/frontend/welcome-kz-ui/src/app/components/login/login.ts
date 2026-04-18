import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Auth } from '../../services/auth';
//import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  form = {
    username: '',
    password: ''
  };
  is_load = false;
  errorMessage = '';

  constructor(
    private authService: Auth,
    private router: Router
  ){}

  login(){
    this.is_load = true;
    this.errorMessage = "";
    this.authService.login(this.form).subscribe({
      next: (res: any) => {
        console.log("Ans from django: ", res)
        this.authService.saveTokens(
          res.access,
          res.refresh
        );
        localStorage.setItem('role', res.role);
        localStorage.setItem('username', res.username);
        this.router.navigate(['/']);
      },
      error: () => {
        this.errorMessage = "Неверный логин или пароль";
        this.is_load = false;
      }
    });
  }
}
