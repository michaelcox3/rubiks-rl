
# Rubiks-RL

Rubiks-RL is a reinforcement learning project to solve a Rubik's Cube using Deep Q-Networks (DQN). It includes a Python API, a web-based Angular frontend, and training scripts/notebooks for model development.

## Features
- Rubik's Cube environment and DQN agent implementation
- Jupyter notebook for training and experimentation
- REST API for cube manipulation and model inference
- Angular web interface for interactive visualization

---

## Getting Started

### 1. Install Dependencies

Create a Python virtual environment and install required packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
*Install the correct version of PyTorch based on your hardware: https://pytorch.org/

For the web frontend:

```powershell
cd web
npm install
```

---

### 2. Train a Model in the Notebook

Open `training.ipynb` in VS Code or Jupyter Lab. The notebook contains several DQN training variants:

- **DQN without Replay Buffer or Target Net**
- **DQN with Replay Buffer**
- **DQN with Replay Buffer & Target Net**

To train a model:
1. Run all cells in the notebook sequentially.
2. Adjust hyperparameters as needed.
3. The current trained model can be saved to `artifacts/dqn_rubik_v1.pt` in the last code block

---

### 3. Start the API Server

Run the FastAPI server (from the repo root):

```powershell
uvicorn api.main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

### 4. Start the Web Server

From the `web` directory:

```powershell
ng serve
```

The Angular app will be available at [http://localhost:4200](http://localhost:4200).

---

## Sources
- [PyTorch DQN Tutorial](https://docs.pytorch.org/tutorials/intermediate/reinforcement_q_learning.html)