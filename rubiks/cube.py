import random
import numpy as np

#        U
#      L F R B
#        D

# If is_row = True, then:
#   index = 0 means top row
#   index = -1 means bottom row
# If is_row = False, then:
#   index = 0 means left column
#   index = -1 means right column

# Format: face: [ (adjacent_face, index, is_row, reverse), ... ]
FACE_EDGE_MAPPINGS = {
    'U': [  # top face
        ('B', 0, True, False),
        ('R', 0, True, False),
        ('F', 0, True, False),
        ('L', 0, True, False),
    ],
    'D': [  # bottom face
        ('F', -1, True, False),
        ('R', -1, True, False),
        ('B', -1, True, False),
        ('L', -1, True, False),
    ],
    'F': [  # front face
        ('U', -1, True, False),
        ('R', 0, False, False),
        ('D', 0, True, True),
        ('L', -1, False, True),
    ],
    'B': [  # back face
        ('U', 0, True, False),
        ('L', 0, False, False),
        ('D', -1, True, True),
        ('R', -1, False, True),
    ],
    'L': [  # left face
        ('U', 0, False, False),
        ('F', 0, False, False),
        ('D', 0, False, False),
        ('B', -1, False, True),
    ],
    'R': [  # right face
        ('U', -1, False, False),
        ('B', 0, False, True),
        ('D', -1, False, False),
        ('F', -1, False, False),
    ],
}

class RubiksCube:
    def __init__(self, size=3):
        self.size = size
        self.state = self._create_solved_state(size)
        self.faces = ['U', 'D', 'L', 'R', 'F', 'B']
        

    def _create_solved_state(self, size):
        # State is a 6 x (size*size) array, each face initialized to a unique integer
        state = np.zeros((6, self.size * self.size), dtype=int)
        for i in range(6):  # 6 faces
            state[i, :] = i
        return state
    
    def rotate_face(self, face, clockwise=True):
        face_idx = self.faces.index(face)
        if clockwise:
            self.state[face_idx] = np.rot90(self.state[face_idx].reshape(self.size, self.size), -1).flatten()
        else:
            self.state[face_idx] = np.rot90(self.state[face_idx].reshape(self.size, self.size), 1).flatten()
        
        # Rotate adjacent faces
        self._rotate_adjacent_faces(face_idx, clockwise)

    def _rotate_adjacent_faces(self, face_idx, clockwise):
        pass
    
    def scramble(self, moves=20, rng=None):
        rng = rng or random
        for _ in range(moves):
            face = rng.choice(self.faces)
            clockwise = rng.choice([True, False])
            self.rotate_face(face, clockwise)
            
    def is_solved(self):
        return all(len(set(face)) == 1 for face in self.state)