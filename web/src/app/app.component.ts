import { Component } from '@angular/core';
import { RubiksComponent } from './components/rubiks/rubiks.component';

@Component({
  selector: 'app-root',
  imports: [RubiksComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'web';
}
