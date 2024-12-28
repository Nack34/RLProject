import gymnasium as gym

env = gym.make("CartPole-v1")
state, _ = env.reset()

for _ in range(1000):
    state, _ = env.reset()
    while not done or truncated:
        action = env.action_space.sample()  # Acción aleatoria
        state, reward, done, truncated, _ = env.step(action)

env.close()
