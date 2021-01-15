from typing import List, Tuple
import gym
import tqdm
import pyautogui
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from env import Env


# env = gym.make("CartPole-v0")
env = Env()
seed = 42
# env.seed(seed=seed)
tf.random.set_seed(42)
np.random.seed(seed)

eps = np.finfo(np.float).eps.item()

class ActorCritic(tf.keras.Model):

    def __init__(self, num_actions, num_hidden_units) -> None:
        super().__init__()

        self.conv1 = layers.Conv2D(8, (3, 3), activation='relu')
        self.maxpool1 = layers.MaxPooling2D((2, 2))
        self.conv2 = layers.Conv2D(16, (3, 3), activation='relu')
        self.maxpool2 = layers.MaxPooling2D((2, 2))
        self.flatten = layers.Flatten()
        self.dense1 = layers.Dense(num_hidden_units, activation='relu')
        self.actor = layers.Dense(num_actions)
        self.critic = layers.Dense(1)

    def call(self, inputs: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        x = self.conv1(inputs)
        x = self.maxpool1(x)
        x = self.conv2(x)
        x = self.maxpool2(x)
        x = self.flatten(x)
        x = self.dense1(x)
        return self.actor(x), self.critic(x)

num_actions = len(env.action_space)
num_hidden_units = 128

model = ActorCritic(num_actions, num_hidden_units)

def env_step(action: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

    state, reward, done, _ = env.step(action)
    return(state.astype(np.float32), np.array(reward, np.int32), np.array(done, np.int32))


def tf_env_step(action: tf.Tensor) -> List[tf.Tensor]:
    return tf.numpy_function(env_step, [action], [tf.float32, tf.int32, tf.int32])


def run_episode(initial_state: tf.Tensor, model: tf.keras.Model, max_steps: int) -> List[tf.Tensor]:
    action_probs = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
    values = tf.TensorArray(dtype=tf.float32, size=0, dynamic_size=True)
    rewards = tf.TensorArray(dtype=tf.int32, size=0, dynamic_size=True)

    initial_state_shape = initial_state.shape
    state = initial_state

    for t in tf.range(max_steps):
        state = tf.expand_dims(state, 0)
        action_logits_t, value = model(state)
        action = tf.random.categorical(action_logits_t, 1)[0, 0]
        action_probs_t = tf.nn.softmax(action_logits_t)

        values = values.write(t, tf.squeeze(value))
        action_probs = action_probs.write(t, action_probs_t[0, action])
        
        state, reward, done = tf_env_step(action)
        state.set_shape(initial_state_shape)

        rewards = rewards.write(t, reward)

        if tf.cast(done, tf.bool):
            break
    
    action_probs = action_probs.stack()
    values = values.stack()
    rewards = rewards.stack()

    return action_probs, values, rewards

    
def get_expected_return(rewards: tf.Tensor, gamma: float, standardize: bool = True) -> tf.Tensor:
    n = tf.shape(rewards)[0]
    returns = tf.TensorArray(dtype=tf.float32, size=n)

    rewards = tf.cast(rewards[::-1], dtype=tf.float32)
    discounted_sum = tf.constant(0.0)
    discounted_sum_shape = discounted_sum.shape
    for i in tf.range(n):
        reward = rewards[i]
        discounted_sum = reward + gamma * discounted_sum
        discounted_sum.set_shape(discounted_sum_shape)
        returns = returns.write(i, discounted_sum)
    returns = returns.stack()[::-1]

    if standardize:
        returns =((returns - tf.math.reduce_mean(returns)) / (tf.math.reduce_std(returns) + eps))

    return returns
    
huber_loss = tf.keras.losses.Huber(reduction=tf.keras.losses.Reduction.SUM)


def compute_loss(action_probs: tf.Tensor, values: tf.Tensor, returns: tf.Tensor) -> tf.Tensor:
    advantage = returns - values

    action_log_probs = tf.math.log(action_probs)
    actor_loss = -tf.math.reduce_sum(action_log_probs * advantage)

    critic_loss = huber_loss(values, returns)

    return actor_loss + critic_loss


optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)


@tf.function
def train_step(initial_state: tf.Tensor, model: tf.keras.Model, optimizer: tf.keras.optimizers.Optimizer, gamma: float, max_steps_per_episode: int) -> tf.Tensor:
    with tf.GradientTape() as tape:
        action_probs, values, rewards = run_episode(initial_state, model, max_steps_per_episode)
        returns = get_expected_return(rewards, gamma)

        action_probs, values, returns = [tf.expand_dims(x, 1) for x in [action_probs, values, returns]]
        
        loss = compute_loss(action_probs, values, returns)
    
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))

    episode_reward = tf.math.reduce_sum(rewards)

    return episode_reward


max_episodes = 10
max_steps_per_episode = 10

reward_threshold = 0
running_reward = 0

gamma = 0.99
pyautogui.hotkey('alt', 'tab')
pyautogui.sleep(0.5)

with tqdm.trange(max_episodes) as t:
    for i in t:
        initial_state = tf.constant(env.reset(), dtype=tf.float32)
        episode_reward = int(train_step(initial_state, model, optimizer, gamma, max_steps_per_episode))
    
        running_reward = episode_reward * 0.01 + running_reward * 0.99

        t.set_description(f'Episode {i}')
        t.set_postfix(episode_reward=episode_reward, running_reward=running_reward)
    
        if i % 10 == 0:
            pass
        
        if running_reward > reward_threshold:
            break
print(f'\nSolved at episode {i}: average reward: {running_reward:.2f}!')
