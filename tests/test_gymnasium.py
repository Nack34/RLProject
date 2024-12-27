import gymnasium as gym

env = gym.make("CartPole-v1")
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()  # Acción aleatoria
    observation, reward, done, truncated, info = env.step(action)
    if done or truncated:
        observation, info = env.reset()

env.close()
