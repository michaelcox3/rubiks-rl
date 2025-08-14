import os
from fastapi import FastAPI
import torch, threading
import torch.nn.functional as F
from shared.dqn import DQN
from shared.utils.schemas import VALID_MOVES, CubePredictResponse, CubeStateRequest, CubeStateResponse, CubeRotateRequest
from shared.utils.encoder import encode_facelets
from shared.rubiks.cube import RubiksCube
import numpy as np

app = FastAPI(title="Rubik's Cube Solver Service")

_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_model_lock = threading.Lock()

def build_model():
    ckpt = torch.load("../shared/artifacts/dqn_rubik_v1.pt", map_location=_device, weights_only=False)
    model = DQN(ckpt["meta"]["input_dim"], ckpt["meta"]["output_dim"])
    model.load_state_dict(ckpt["model_state"])
    model.to(_device).eval()
    return model

_model = build_model()

@app.get("/health")
def health():
    return {"status": "ok", "device": str(_device)}

@app.post("/predict", response_model=CubePredictResponse)
def predict(req: CubeStateRequest):
    with _model_lock, torch.no_grad():
        x = encode_facelets(req.state).to(_device)            # (1, 324)
        q_values = _model(x)                                   # (1, 12)

        move_probs = F.softmax(q_values, dim=-1)
        move_idx = int(move_probs.argmax(dim=-1).item())
        move = VALID_MOVES[move_idx]
        confidence = float(move_probs[0, move_idx].item())

        return CubePredictResponse(move=move, confidence=confidence)
    

@app.post("/rotate", response_model=CubeStateResponse)
def rotate(req: CubeRotateRequest):
    # convert list to numpy array for RubiksCube
    req.state = np.array(req.state, dtype=int)
    cube = RubiksCube(state=req.state)
    cube.rotate_face(req.move[0], clockwise=(len(req.move) == 1))
    new_state = cube.state.flatten().tolist()
    return CubeStateResponse(state=new_state)