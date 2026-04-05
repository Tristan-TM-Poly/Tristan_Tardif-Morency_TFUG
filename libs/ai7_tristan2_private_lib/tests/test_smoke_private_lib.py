from ai7_tristan2_private_lib.actors import ActorProfile, ActorType, is_actor_allowed
from ai7_tristan2_private_lib.governance import evaluate_promotion
from ai7_tristan2_private_lib.parallel_governance import GovernanceMode, ParallelGroup
from ai7_tristan2_private_lib.task_queue import TaskItem
from ai7_tristan2_private_lib.autonomy_governor import AutonomyGovernor


def test_actor_is_allowed() -> None:
    actor = ActorProfile(actor_type=ActorType.TRISTAN, actor_id="t1", display_name="Tristan")
    assert is_actor_allowed(actor) is True


def test_evaluate_promotion() -> None:
    assert evaluate_promotion(8.2).value == "stable"
    assert evaluate_promotion(5.4).value == "crystallizable"
    assert evaluate_promotion(2.5).value == "exploratory"
    assert evaluate_promotion(0.5).value == "quarantine"


def test_parallel_group_governance() -> None:
    group = ParallelGroup(group_id="g1", governance_mode=GovernanceMode.COUPLED_PARALLEL)
    group.add_task(TaskItem(task_id="T1", command="packet.generate"))
    governor = AutonomyGovernor()
    decision = governor.evaluate_group(group)
    assert decision.approved is True
