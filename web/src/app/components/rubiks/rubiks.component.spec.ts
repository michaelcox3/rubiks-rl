import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RubiksComponent } from './rubiks.component';

describe('RubixComponent', () => {
  let component: RubiksComponent;
  let fixture: ComponentFixture<RubiksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RubiksComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RubiksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
