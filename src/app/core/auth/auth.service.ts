import { Injectable, inject } from '@angular/core';
import {
  Auth,
  User,
  authState,
  signInWithEmailAndPassword,
  signOut,
} from '@angular/fire/auth';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly auth = inject(Auth);
  readonly currentUser$ = authState(this.auth);

  async login(email: string, password: string): Promise<User> {
    const credential = await signInWithEmailAndPassword(this.auth, email, password);
    return credential.user;
  }

  logout(): Promise<void> {
    return signOut(this.auth);
  }
}