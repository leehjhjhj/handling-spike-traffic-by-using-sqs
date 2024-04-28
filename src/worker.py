import time, json, os, boto3, asyncio
from common.errors.exception import TimeoutException

class SimpleSQSTicketWorker:
    def __init__(self):
        self._sqs = boto3.client('sqs', region_name='ap-northeast-2', aws_access_key_id=os.environ['AWS_ACCESS_KEY'], aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
        self._queue_url = os.environ['SQS_QUEUE_URL']

    def process_message(self, message):
        body = json.loads(message['Body'])
        print(f"Processing message: {body}")

    def poll_sqs_messages(self):
        while True:
            response = self._sqs.receive_message(
                QueueUrl=self._queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20
            )
            messages = response.get('Messages', [])
            for message in messages:
                try:
                    self.process_message(message) # with_timeout 추가해야함
                    self._sqs.delete_message(
                        QueueUrl=self._queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                except TimeoutException:
                    print("Processing time out")
                    continue
                except Exception as e:
                    print("Error processing message:", e)
                    self._sqs.change_message_visibility(
                        QueueUrl=self._queue_url,
                        ReceiptHandle=message['ReceiptHandle'],
                        VisibilityTimeout=0  # 0으로 설정하면 즉시 다른 컨슈머가 메시지를 받을 수 있음
                    )