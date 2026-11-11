import { Routes } from '@angular/router';

export const routes: Routes = [
	{
		path: '',
		loadComponent: () => import('./shared/layout/app-layout.component').then((module) => module.AppLayoutComponent),
		children: [
			{
				path: '',
				pathMatch: 'full',
				loadComponent: () => import('./features/tests/pages/test-library.component').then((module) => module.TestLibraryComponent),
			},
			{
				path: 'test',
				loadComponent: () => import('./features/tests/pages/test-player.component').then((module) => module.TestPlayerComponent),
			},
			{
				path: 'login',
				loadComponent: () => import('./features/auth/pages/login.component').then((module) => module.LoginComponent),
			},
		],
	},
	{ path: '**', redirectTo: '' },
];
