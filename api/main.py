from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import torch, threading
import torch.nn.functional as F
from shared.dqn.model import DQN
from shared.rubiks.cube import RubiksCube
from api.utils.schemas import VALID_MOVES, CubePredictResponse, CubeScrambleRequest, CubeStateRequest, CubeStateResponse, CubeRotateRequest
from api.utils.encoder import encode_facelets

app = FastAPI(title="Rubik's Cube Solver Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"]
)

_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_model_lock = threading.Lock()

def build_model():
    ckpt = torch.load("./artifacts/dqn_rubik_v1.pt", map_location=_device, weights_only=False)
    model = DQN(ckpt["meta"]["input_dim"], ckpt["meta"]["output_dim"])
    model.load_state_dict(ckpt["model_state"])
    model.to(_device).eval()
    return model

_model = build_model()

@app.get("/health")
def health():
    return {"status": "ok", "device": str(_device)}

@app.post("/cube/predict-move", response_model=CubePredictResponse)
def predict(req: CubeStateRequest):
    with _model_lock, torch.no_grad():
        x = encode_facelets(req.state).to(_device)            # (1, 324)
        q_values = _model(x)                                   # (1, 12)

        move_probs = F.softmax(q_values, dim=-1)
        move_idx = int(move_probs.argmax(dim=-1).item())
        move = VALID_MOVES[move_idx]
        confidence = float(move_probs[0, move_idx].item())

        return CubePredictResponse(move=move, confidence=confidence)

@app.post("/cube/rotate", response_model=CubeStateResponse)
def rotate(req: CubeRotateRequest):
    # convert list to numpy array for RubiksCube
    req.state = np.array(req.state, dtype=int)
    cube = RubiksCube(state=req.state)
    cube.rotate_face(req.move[0], clockwise=(len(req.move) == 1))
    return CubeStateResponse(state=cube.state.tolist())

@app.post("/cube/scramble", response_model=CubeStateResponse)
def scramble(req: CubeScrambleRequest):
    cube = RubiksCube()
    cube.scramble(req.moves)
    return CubeStateResponse(state=cube.state.tolist())