import random
import numpy as np

from env.network_simulator import NetworkSimulator
from env.network_env import NetworkEnv

from metrics.metrics import MetricsEngine
from llm.policy_interpreter import PolicyInterpreter
from trust.trust_engine import TrustEngine
from adversarial.jammer_predictor import JammerPredictor
from reward.reward_fusion import RewardFusion
from blockchain.blockchain import BlockchainLogger
from federated.federated_buffer import FederatedBuffer
from multi_agent.agent_pool import AgentPool
from meta.meta_optimizer import MetaOptimizer
from digital_twin.world import DigitalTwin

from rl.dqn import DQNAgent


# =========================
# INIT SYSTEM
# =========================

sim = NetworkSimulator()
env = NetworkEnv(sim)

metrics = MetricsEngine()
llm = PolicyInterpreter()
trust = TrustEngine()
jammer = JammerPredictor()
fusion = RewardFusion()

chain = BlockchainLogger()
memory = FederatedBuffer()

agents = AgentPool()
meta = MetaOptimizer()
twin = DigitalTwin()


# =========================
# DQN CONFIG
# =========================

STATE_DIM = 4
ACTION_DIM = 20

dqn = DQNAgent(STATE_DIM, ACTION_DIM)

EPISODES = 500

# initial state
state = env.reset()


# =========================
# TRAINING LOOP
# =========================

for ep in range(EPISODES):

    # -------------------------
    # MULTI-AGENT PROPOSAL
    # -------------------------
    proposals = agents.propose()
    flat_actions = [a for sub in proposals for a in sub]

    safe_actions, _ = llm.filter(flat_actions)

    if len(safe_actions) == 0:
        safe_actions = [0]

    ranked = trust.score(safe_actions)

    scored = []
    for action, trust_score in ranked:

        threat = jammer.predict(action)
        attack = twin.simulate_attack(action)

        final_score = trust_score - threat - attack

        scored.append((action, final_score, trust_score, threat))

    scored.sort(key=lambda x: x[1], reverse=True)

    # -------------------------
    # DQN ACTION
    # -------------------------
    dqn_action = dqn.act(state)

    # hybrid policy (exploration + safety)
    best_action = (
        scored[0][0] if random.random() < 0.3 else dqn_action
    )

    jammer_power = random.uniform(0.1, 1.0)

    # -------------------------
    # ENV STEP
    # -------------------------
    next_state, base_reward, result = env.step(best_action, jammer_power)

    # -------------------------
    # REWARD FUSION
    # -------------------------
    final_reward = fusion.compute(
        base_reward,
        scored[0][2],
        scored[0][3]
    )

    done = False

    # -------------------------
    # DQN TRAIN
    # -------------------------
    dqn.remember(state, best_action, final_reward, next_state, done)
    dqn.replay(32)

    state = next_state

    if ep % 10 == 0:
        dqn.update_target()

    # -------------------------
    # MEMORY STORE
    # -------------------------
    memory.store({
        "state": state.tolist() if hasattr(state, "tolist") else state,
        "action": int(best_action),
        "reward": float(final_reward)
    })

    # -------------------------
    # BLOCKCHAIN LOG
    # -------------------------
    chain.add_block({
        "episode": ep,
        "state": state.tolist() if hasattr(state, "tolist") else state,
        "action": int(best_action),
        "reward": float(final_reward),
        "trust": float(scored[0][2]),
        "threat": float(scored[0][3]),
        "epsilon": float(dqn.epsilon),
        "alpha": float(meta.alpha)
    })

    # -------------------------
    # METRICS
    # -------------------------
    metrics.log(result)

    # -------------------------
    # META UPDATE
    # -------------------------
    alpha = meta.update(final_reward)

    # -------------------------
    # OUTPUT
    # -------------------------
    print(f"\nEpisode {ep}")
    print("Action:", best_action)
    print("Reward:", round(final_reward, 3))
    print("Epsilon:", round(dqn.epsilon, 3))
    print("Alpha:", round(alpha, 3))
    print("Memory:", len(memory.buffer))


# =========================
# VISUALIZATION (AFTER TRAIN)
# =========================

from blockchain.visualize_blockchain import visualize_real_chain

visualize_real_chain(chain)