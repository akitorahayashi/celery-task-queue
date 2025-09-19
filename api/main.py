from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult

from .tasks import add
from celery_app.app import app as celery_app

app = FastAPI(title="Async Task Queue Sample")


@app.get("/add")
def enqueue_add(x: int, y: int):
    try:
        res = add.delay(x, y)
        return {"task_id": res.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_id}")
def get_task_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        return {"status": "PENDING"}
    elif result.state == "SUCCESS":
        return {"status": "SUCCESS", "result": result.result}
    else:
        return {"status": result.state, "info": str(result.info)}
