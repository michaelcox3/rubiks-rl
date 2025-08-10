import gymnasium as gym
from dqn.model import QNetwork
from rubiks.env import RubiksCubeEnv
import torch
import torch.nn as nn
import torch.optim as optim

def train():
    env = RubiksCubeEnv(size=3, scramble_moves=1)
    input_dim = env.observation_space.shape[0]  # 6 * size^2
    output_dim = env.action_space.n  # 12 (6 faces * 2 rotations)

    model = QNetwork(input_dim, output_dim)  # Initialize with random weights and biases
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    num_episodes = 2000
    max_steps = 10
    gamma = 0.99

    epsilon = 1.0 # Initial exploration rate, 1.0 means 100% exploration, 0.0 means 100% exploitation
    min_epsilon = 0.01
    epsilon_decay = 0.0003

    for episode in range(num_episodes):
        # Reset the game state for each episode
        state, _ = env.reset()
        total_reward = 0
        
        for step in range(max_steps):
            # Convert state to tensor
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            
            # 1. Choose action (e-greedy)
            random = torch.rand(1).item() # random float between 0 and 1
            if random < epsilon:
                action = env.action_space.sample()  # explore
            else:
                q_values = model(state_tensor)
                action = q_values.argmax().item()  # exploit
                
            # 2. Perform action
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            total_reward += reward
            
            # 3. Update weights
            # Convert next state to tensor
            next_state_tensor = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0)
            
            # Calculate target Q-value (the temporal difference target)
            with torch.no_grad():
                max_next_q = model(next_state_tensor).max().item()
                target_q = reward if done else reward + gamma * max_next_q
            
            # Get predicted Q-value for the current state-action pair
            predicted_q = model(state_tensor)[0, action] # [0, action] to get the scalar value
            
            # Calculate loss
            loss = loss_fn(predicted_q, torch.tensor(target_q, dtype=torch.float32))
            
            optimizer.zero_grad() # Clear gradients
            loss.backward() # Backpropagation, this computes gradients
            optimizer.step() # Update weights
            
            # 4. Move to next state
            state = next_state
            
            if done:
                break
            
        # 5 Decay epsilon (less exploration over time)
        epsilon = max(min_epsilon, epsilon - epsilon_decay)

        print(f"Episode {episode+1}, Total Reward: {total_reward:.1f}, Epsilon: {epsilon:.3f}")


if __name__ == "__main__":
    train()
