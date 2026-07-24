/**
 * @fileoverview Configuración global de la aplicación Angular.
 * Registra los proveedores globales como HttpClient y los escuchadores de errores del navegador.
 */

import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';

/** Configuración raíz de Angular pasable a `bootstrapApplication` */
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(), 
    provideHttpClient() // Habilita el cliente HTTP de Angular para llamadas a la API REST de Flask
  ],
};

