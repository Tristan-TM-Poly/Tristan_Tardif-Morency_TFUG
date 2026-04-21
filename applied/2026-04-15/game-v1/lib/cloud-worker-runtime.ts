export type WorkerTask = {
  id: string;
  type: string;
  payload: any;
};

export function runWorker(task: WorkerTask) {
  return {
    task_id: task.id,
    result: `executed ${task.type}`,
    status: 'completed',
    timestamp: Date.now(),
  };
}

export function runQueue(tasks: WorkerTask[]) {
  return tasks.map(runWorker);
}
