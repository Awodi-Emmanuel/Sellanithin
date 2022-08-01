from email.policy import default
from ensurepip import bootstrap
import enum 
import json
from kafka import kafkaProducer

BOOTSTRAP_SERVER=['localhost:9092']

class BaseProducer:
    class ActionTyp(enum.Enum):
        notification = "notification"
        default = "notification"
        
    def __init__(self, req_id: str, stream_id: str, action) -> None:
        self.req_id = req_id
        self.stream_id = stream_id
        self.action = action
        
        
    def event(self):
        event = {
            'req_id': self.req_id,
            'stream_id': self.stream_id,
        }
        return event
    def send_event(self, event):
        producer = kafkaProducer(
            value_serializer=lambda v: json.dump(v).encode("utf-8"),
            bootstrap_server=BOOTSTRAP_SERVER,
        )
        producer.send(ecomtopic=self.action, value=event)