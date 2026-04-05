from ai7_tristan2_private_lib.autonomy_governor import AutonomyGovernor
from ai7_tristan2_private_lib.batch_executor import execute_parallel_group
from ai7_tristan2_private_lib.parallel_governance import GovernanceMode, ParallelGroup
from ai7_tristan2_private_lib.task_queue import TaskItem


group = ParallelGroup(
    group_id="fractal-loop-parallel-batch",
    governance_mode=GovernanceMode.COUPLED_PARALLEL,
)

group.add_task(TaskItem(task_id="T1", command="packet.generate", priority=5))
group.add_task(TaskItem(task_id="T2", command="synergy.compute", priority=4))
group.add_task(TaskItem(task_id="T3", command="reality.tag", priority=3))

governor = AutonomyGovernor()
decision = governor.evaluate_group(group)
print({"approved": decision.approved, "reason": decision.reason, "next_mode": decision.next_mode.value})

if decision.approved:
    report = execute_parallel_group(group)
    print({"executed": report.executed_tasks, "blocked": report.blocked_tasks})
