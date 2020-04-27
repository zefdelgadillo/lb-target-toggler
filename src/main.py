from googleapiclient.discovery import build
import uuid
import os

LOAD_BALANCER = os.environ.get('LOAD_BALANCER')
BACKEND_BUCKET = os.environ.get('BACKEND_BUCKET')
PROJECT = os.environ.get('GCP_PROJECT')

compute = build('compute', 'v1')

def main(event, context):
  print('Event: ' + str(event))
  print('Context: ' + str(context))
  update_url_map()

def update_url_map():
  target_service = f'https://www.googleapis.com/compute/v1/projects/{PROJECT}/global/backendBuckets/{BACKEND_BUCKET}'
  body = {
    'defaultService': target_service
  }
  try:
    request = compute.urlMaps().patch(project=PROJECT, urlMap=LOAD_BALANCER, body=body, requestId=uuid.uuid4())
    response = request.execute()
    print(response)
    return response
  except Exception as e:
    print(e)
