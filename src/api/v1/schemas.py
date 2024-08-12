import time
from pydantic import BaseModel, model_validator

class Body(BaseModel):
    message: str

class Response(BaseModel):
    timestamp: str = ""
    redirect_uri: str = ""
    meta: dict = None
    event: dict = None

    class Config:
        validate_assignment = True

    @model_validator(mode='after')
    def test_validate(self):
        if not self.timestamp or self.timestamp == "":
            self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S%z")
        return self
        

class Payload(BaseModel):
    message: str = ""
    
class MetaData(BaseModel):
    id: str = ""
    trace_id: str = ""
    created_at: str = ""
    updated_at: str = ""
    is_async: bool = False
    state: str = "COMPLETED"

    class Config:
        validate_assignment = True
    
    @model_validator(mode='after')
    def set_default_timestamps(self):
        dt = time.strftime("%Y-%m-%d %H:%M:%S%z")
        
        if self.created_at == "":
            self.created_at = dt
        if self.updated_at == "":
            self.updated_at = dt
        return self
    


    