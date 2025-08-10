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
            self.state[face_idx] = np.rot90(self._get_face_as_matrix(face_idx), -1).flatten()
        else:
            self.state[face_idx] = np.rot90(self._get_face_as_matrix(face_idx), 1).flatten()
        
        # Rotate adjacent faces
        self._rotate_adjacent_faces(face_idx, clockwise)

            

    def _rotate_adjacent_faces(self, face_idx, clockwise):
        if clockwise:
            mappings = FACE_EDGE_MAPPINGS[self.faces[face_idx]]
        else:
            mappings = FACE_EDGE_MAPPINGS[self.faces[face_idx]][::-1]

        # Cache the first slice's values before overwriting
        first_face, first_idx, first_is_row, first_reverse = mappings[0]

        if first_is_row:
            temp_values = self._get_row_in_face(first_face, first_idx)
        else:
            temp_values = self._get_col_in_face(first_face, first_idx)
            
        # Iterate through mappings and shift values left
        for i in range(len(mappings) - 1):
            src_face, src_idx, src_is_row, src_reverse = mappings[i + 1]
            dst_face, dst_idx, dst_is_row, dst_reverse = mappings[i]
            
            # Get the row/col of source to set in the previous face going counter clockwise (dest)
            if src_is_row:
                new_vector = self._get_row_in_face(src_face, src_idx)
            else:
                new_vector = self._get_col_in_face(src_face, src_idx)
                
            
            # Set dest row/col
            if dst_is_row:
                self._set_row_in_face(dst_face, dst_idx, new_vector[::-1] if dst_reverse else new_vector)
            else:
                self._set_col_in_face(dst_face, dst_idx, new_vector[::-1] if dst_reverse else new_vector)
            
        # Set last mapping to the cached first slice
        last_face, last_idx, last_is_row, last_reverse = mappings[-1]
        if last_is_row:
            self._set_row_in_face(last_face, last_idx,
                                temp_values[::-1] if last_reverse else temp_values)
        else:
            self._set_col_in_face(last_face, last_idx,
                                temp_values[::-1] if last_reverse else temp_values)
        
        
    def _get_face_as_matrix(self, face_idx):
        return self.state[face_idx].reshape(self.size, self.size)
    
    def _get_row_in_face(self, face, index):
        face_idx = self.faces.index(face)
        matrix = self._get_face_as_matrix(face_idx)
        return matrix[index, :].copy()
    
    def _set_row_in_face(self, face, index, new_row):
        face_idx = self.faces.index(face)
        matrix = self._get_face_as_matrix(face_idx)
        matrix[index, :] = new_row
        self.state[face_idx] = matrix.flatten()
        
    def _get_col_in_face(self, face, index):
        face_idx = self.faces.index(face)
        matrix = self._get_face_as_matrix(face_idx)
        return matrix[:, index].copy()
    
    def _set_col_in_face(self, face, index, new_col):
        face_idx = self.faces.index(face)
        matrix = self._get_face_as_matrix(face_idx)
        matrix[:, index] = new_col
        self.state[face_idx] = matrix.flatten()
    
    def scramble(self, moves=20, rng=None):
        rng = rng or random
        for _ in range(moves):
            face = rng.choice(self.faces)
            clockwise = rng.choice([True, False])
            self.rotate_face(face, clockwise)
            
    def is_solved(self):
        return all(len(set(face)) == 1 for face in self.state)