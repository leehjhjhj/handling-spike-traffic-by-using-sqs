from pydantic import BaseModel

class TicketRequest(BaseModel):
    user_id: int
    quantity: int
    name: str