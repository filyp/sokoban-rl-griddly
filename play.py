import gym
from gym.utils.play import play

from griddly import GymWrapperFactory, gd
from griddly.RenderTools import VideoRecorder


def callback(env):

    initial_global_obs = env.render(observer="global", mode="rgb_array")
    observation_shape = initial_global_obs.shape

    recorder = VideoRecorder()
    recorder.start("human_player_video_test.mp4", observation_shape)

    def _callback(prev_obs, obs, action, rew, env_done, info):

        # env.render(observer="global")
        global_obs = env.render(observer="global", mode="rgb_array")
        recorder.add_frame(global_obs)
        if rew != 0:
            print(f"\nReward: {rew}")
        if env_done:
            print(f"Done!")

        if len(info) > 0:
            print(info)

    return _callback


if __name__ == "__main__":
    wrapper = GymWrapperFactory()

    environment_name = "TestEnv"

    level = 0

    wrapper.build_gym_from_yaml(
        environment_name,
        yaml_file="gridman/gridman.yaml",
        player_observer_type="HumanPlayerBlockObserver",
        global_observer_type="GlobalSpriteObserver",
        level=level,
    )
    env = gym.make(f"GDY-{environment_name}-v0")
    # env.enable_history(True)
    env.reset()
    play(env, callback=callback(env), fps=10, zoom=3)


