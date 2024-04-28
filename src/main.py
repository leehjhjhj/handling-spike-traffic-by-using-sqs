from fastapi import FastAPI, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from schema import TicketRequest
from worker import SimpleSQSTicketWorker

app = FastAPI()

load_dotenv()

@app.get("/start-polling")
async def start_polling(background_tasks: BackgroundTasks):
    worker = SimpleSQSTicketWorker()
    background_tasks.add_task(worker.poll_sqs_messages)
    return {"message": "Started polling SQS messages in the background"}

@app.post("/tickets/purchase")
def purchase_ticket(ticket_request: TicketRequest):
    print(f"Processing message: {ticket_request}")
    return ticket_request