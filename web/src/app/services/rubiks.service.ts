// src/app/services/post.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, map, Observable } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class RubiksService {
    private apiUrl = 'http://localhost:8000/';

    // BehaviorSubject to hold the cube state
    private cubeStateSubject = new BehaviorSubject<number[] | null>(null);

    constructor(private http: HttpClient) {
        // Initialize the cube state
        this.setCubeState(this.getSolvedCube());
    }

    get currentCubeState(): number[] | null {
        return this.cubeStateSubject.value;
    }

    getCubeState$(): Observable<number[] | null> {
        return this.cubeStateSubject.asObservable(); // keeps it readonly from outside
    }

    setCubeState(cubeState: number[]): void {
        this.cubeStateSubject.next(cubeState); // make it reactive
    }

    scrambleCube(): Observable<number[]> {
        return this.http.post<number[]>(`${this.apiUrl}/scramble`, {}).pipe(
            map((data: number[]) => {
                this.setCubeState(data);
                return data;
            })
        );
    }

    rotateCube(): Observable<number[]> {
        return this.http.post<number[]>(`${this.apiUrl}/rotate`, {}).pipe(
            map((data: number[]) => {
                this.setCubeState(data);
                return data;
            })
        );
    }

    getSolution(): Observable<number[]> {
        return this.http.get<number[]>(`${this.apiUrl}/solution`).pipe(
            map((data: number[]) => {
                this.setCubeState(data);
                return data;
            })
        );
    }

    resetCube() {
        this.setCubeState(this.getSolvedCube());
    }

    private getSolvedCube(): number[] {
        return [
            0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 1, 1, 1, 1, 1, 1,
            2, 2, 2, 2, 2, 2, 2, 2, 2,
            3, 3, 3, 3, 3, 3, 3, 3, 3,
            4, 4, 4, 4, 4, 4, 4, 4, 4,
            5, 5, 5, 5, 5, 5, 5, 5, 5
        ];
    }
}
