import asyncio
from datetime import timedelta
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow, activity

# Activity definition for terminal output
def print_healthcheck(msg: str):
    print(msg)

@activity.defn
async def print_healthcheck_activity(msg: str):
    print_healthcheck(msg)

@workflow.defn
class HealthcheckWorkflow:
    @workflow.run
    async def run(self) -> None:
        while True:
            msg = f"Hello, world! Healthcheck at {workflow.now().isoformat()}"
            await workflow.execute_activity(
                print_healthcheck_activity,
                msg,
                schedule_to_close_timeout=timedelta(seconds=5),
            )
            await asyncio.sleep(5)

async def main():
    # Connect to Temporal server (default localhost:7233)
    client = await Client.connect("localhost:7233")

    # Start a worker for the healthcheck task queue
    async with Worker(
        client,
        task_queue="healthcheck-task-queue",
        workflows=[HealthcheckWorkflow],
        activities=[print_healthcheck_activity],
    ):
        # Start the workflow if not already running
        try:
            await client.start_workflow(
                HealthcheckWorkflow.run,
                id="healthcheck-workflow",
                task_queue="healthcheck-task-queue",
                execution_timeout=None,
            )
        except Exception:
            print("Workflow may already be running or another error occurred.")
        print("Healthcheck workflow started. Press Ctrl+C to exit.")
        while True:
            await asyncio.sleep(2)

if __name__ == "__main__":
    # NOTE: For best compatibility, use Python 3.8–3.11 with Temporal Python SDK.
    asyncio.run(main())