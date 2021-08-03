from datetime import datetime
from database import database, feedbacks
from fastapi import FastAPI
from typing import List
import uvicorn
from starlette.responses import RedirectResponse
from schemas import Feedback, FeedbackIn

app = FastAPI(title="Simple Feedback API")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs/")


@app.post("/feedbacks/", response_model=Feedback)
async def create_feedback(feedback: FeedbackIn):
    query = feedbacks.insert().values(service_name=feedback.service_name, tag=feedback.tag, data=feedback.data, created_at=datetime.now())
    last_id = await database.execute(query)
    return {**feedback.dict(), "id": last_id, "created_at": datetime.now()}


@app.get("/feedbacks/", response_model=List[Feedback])
async def get_all_feedbacks(offset: int = 0, limit: int = 20):
    query = feedbacks.select().offset(offset).limit(limit)
    return await database.fetch_all(query)


@app.get("/feedbacks/{feedback_id}/", response_model=Feedback)
async def get_feedback_by_id(feedback_id: int):
    query = feedbacks.select().where(feedbacks.c.id == feedback_id)
    return await database.fetch_one(query)


@app.delete("/feedbacks/{feedback_id}/")
async def delete_feedback(feedback_id: int):
    query = feedbacks.delete().where(feedbacks.c.id == feedback_id)
    await database.execute(query)
    return {"message": f"Note with id: {feedback_id} deleted successfully!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)