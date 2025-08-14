import torch

def encode_facelets(state: list[int]) -> torch.Tensor:
    return torch.tensor(state, dtype=torch.float32).unsqueeze(0)  # shape (1, 54)
