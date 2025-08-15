import { Component, ElementRef, HostListener, ViewChild } from '@angular/core';
import * as THREE from 'three';
import { Move, RubiksService } from '../../services/rubiks.service';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-rubiks',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './rubiks.component.html',
  styleUrl: './rubiks.component.css',
  host: { 'class': 'flex-1 flex flex-col h-full' }
})
export class RubiksComponent {

  // Three.js components
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;
  private meshGroup!: THREE.Group;

  // All 12 moves for clockwise and counterclockwise
  allMoves = [
    'R', "R'", 'L', "L'", 'U', "U'",
    'D', "D'", 'F', "F'", 'B', "B'"
  ];

  @ViewChild('canvasContainer', { static: true }) canvasContainer!: ElementRef;

  constructor(private rubiksService: RubiksService) {
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera();

    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setSize(window.innerWidth, 500);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
  }

  scrambleCube() {
    this.rubiksService.scrambleCube().subscribe();
  }

  resetCube() {
    this.rubiksService.resetCube();
  }

  predictMove() {
    this.rubiksService.predictMove().subscribe();
  }

  rotateCube(move: any) {
    console.log(move.name);
    this.rubiksService.rotateCube(move).subscribe();
  }

  // Method to get button color class based on face
  getMoveColorClass(move: string): string {
    const face = move.charAt(0); // Get the first character (face letter)

    switch (face) {
      case 'R': return 'btn-blue';
      case 'L': return 'btn-green';
      case 'U': return 'btn-white';
      case 'D': return 'btn-yellow';
      case 'F': return 'btn-orange';
      case 'B': return 'btn-red';
      default: return 'btn-white';
    }
  }

  ngAfterViewInit() {
    const width = this.canvasContainer.nativeElement.clientWidth;
    const height = 500;
    this.renderer.setSize(width, height);

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
    this.camera.position.z = 10; // Set the camera position to see the cube

    // Subscribe to ws messages to update the cube state
    // rubiks refers to the CubeData object that is returned from the rubiksService
    // This will update the cube state whenever a new message is received
    this.rubiksService.getCubeState$().subscribe((rubiks) => {
      if (rubiks) {
        this.redrawCube(rubiks);
      }
    });

  }

  redrawCube(rubiks: number[]) {
    const size = 1.0; // Size of each square on the cube
    const colorToHex: number[] = [
      0xFFFFFF, // White
      0xFFFF00, // Yellow
      0x00FF00, // Green
      0x0000FF, // Blue
      0xFFA500, // Orange
      0xFF0000, // Red
    ];
    // ['U', 'D', 'L', 'R', 'F', 'B']
    // Define positions and rotations for each face
    // These positions are offsets from the center of the cube
    const colorToPosition: THREE.Vector3[] = [
      new THREE.Vector3(0, 1.5, 0),
      new THREE.Vector3(0, -1.5, 0),
      new THREE.Vector3(-1.5, 0, 0),
      new THREE.Vector3(1.5, 0, 0),
      new THREE.Vector3(0, 0, 1.5),
      new THREE.Vector3(0, 0, -1.5),
    ];


    // x axis is red, y axis is green, z axis is blue
    const halfPi = Math.PI / 2;
    const colorToRotation: THREE.Euler[] = [
      new THREE.Euler(-halfPi, 0, 0),
      new THREE.Euler(halfPi, 0, 0),
      new THREE.Euler(0, -halfPi, 0),
      new THREE.Euler(0, halfPi, 0),
      new THREE.Euler(0, 0, 0),
      new THREE.Euler(0, -Math.PI, 0),
    ];

    this.meshGroup = new THREE.Group();
    const n = rubiks.length;
    const faceCount = Math.floor(n / 9);
    for (let i = 0; i < faceCount; i++) {
      const faceIndex = i;
      const faceOriginPosition = colorToPosition[faceIndex];
      const faceRotation = colorToRotation[faceIndex];

      for (let j = 0; j < 9; j++) {
        const squareColor = rubiks[i * 9 + j];
        const squareColorHex = colorToHex[squareColor];
        const row = Math.floor(j / 3);
        const col = j % 3;
        const squarePosition = new THREE.Vector3().copy(faceOriginPosition).add(this.getLocalOffset(row, col).applyEuler(faceRotation));

        const square = this.createSquare(squareColorHex, size - 0.20, squarePosition, faceRotation);
        this.meshGroup.add(square);
      }

    }

    this.scene.add(this.meshGroup);
    this.canvasContainer.nativeElement.appendChild(this.renderer.domElement);

    this.renderer.setAnimationLoop(this.animate.bind(this));
  }

  getLocalOffset(row: number, col: number): THREE.Vector3 {
    const offsetX = (col - 1);
    const offsetY = -(row - 1);
    return new THREE.Vector3(offsetX, offsetY, 0);
  }

  animate() {
    this.controls.update(); // required for damping (if enabled)
    this.renderer.render(this.scene, this.camera);
  }

  createSquare(color: number, size: number, position: THREE.Vector3, rotation: THREE.Euler): THREE.Mesh {
    const geometry = new THREE.BoxGeometry(size, size, 0.1);
    const material = new THREE.MeshBasicMaterial({ color: color });
    const square = new THREE.Mesh(geometry, material);
    square.position.copy(position);
    square.rotation.copy(rotation);
    return square;
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    const width = this.canvasContainer.nativeElement.clientWidth;
    const height = 500;
    this.renderer.setSize(width, height);
    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
  }
}
