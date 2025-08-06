from bimanual import SingleArm
from typing import Dict, Any

def test_follower(single_arm: SingleArm):
    initial_position = single_arm.get_joint_positions()
    while(1):
        single_arm.set_joint_positions(positions=initial_position)

if __name__ == "__main__":
    arm_config: Dict[str, Any] = {
        "can_port": "can1",
        "type": 0,
    }
    single_arm = SingleArm(arm_config)
    test_follower(single_arm)