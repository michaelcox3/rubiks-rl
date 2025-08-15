// src/app/services/post.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, map, Observable } from 'rxjs';

export type Move = 'U' | 'U\'' | 'D' | 'D\'' | 'L' | 'L\'' | 'R' | 'R\'' | 'F' | 'F\'' | 'B' | 'B\'';

export interface CubeState {
    state: number[];
}

export interface CubePredictResponse {
    move: Move;
    confidence: number | null;
}

@Injectable({
    providedIn: 'root',
})
export class RubiksService {
    private apiUrl = 'http://localhost:8000';

    // BehaviorSubject to hold the cube state
    private cubeStateSubject = new BehaviorSubject<number[] | null>(null);
    private cubeMoveLog: Move[] = [];

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

    scrambleCube(): Observable<CubeState> {
        return this.http.post<CubeState>(`${this.apiUrl}/cube/scramble`, { moves: 1 }).pipe(
            map((data: CubeState) => {
                this.setCubeState(data.state);
                return data;
            })
        );
    }

    rotateCube(move: Move): Observable<CubeState> {
        return this.http.post<CubeState>(`${this.apiUrl}/cube/rotate`, { state: this.currentCubeState, move }).pipe(
            map((data: CubeState) => {
                this.setCubeState(data.state);
                this.cubeMoveLog.push(move); // Log the move
                return data;
            })
        );
    }

    predictMove(): Observable<CubePredictResponse> {
        return this.http.post<CubePredictResponse>(`${this.apiUrl}/cube/predict-move`, { state: this.currentCubeState }).pipe(
            map((data: CubePredictResponse) => {
                this.rotateCube(data.move).subscribe();
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
