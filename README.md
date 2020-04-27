# Load Balancer Target Toggler

Use a Cloud Function on a schedule to toggle between multiple different backend services. Useful if you need to turn on and off a website on a schedule for some reason.

## Example deployment:
1. Deploy static sites into 2 separate publicly available buckets. See `site-off/` and `site-on/` for examples.
2. Create backend bucket resources for each site. Note the name of the backend bucket resource, example below is using `site-on` and `site-off`.
```
# Create some names that we'll re-use for the resources
SITE_1=site-on
SITE_2=site-off

SITE_1_BUCKET=<Bucket for site 1>
SITE_2_BUCKET=<Bucket for site 2>

gcloud compute backend-buckets create $SITE_1 --gcs-bucket-name $SITE_1_BUCKET
gcloud compute backend-buckets create $SITE_2 --gcs-bucket-name $SITE_2_BUCKET
```
3. Create PubSub topics that each of your Cloud Functions will use for the trigger.
```
gcloud pubsub topics create ${SITE_1}-topic
gcloud pubsub topics create ${SITE_2}-topic
```
4. Create Cloud Function for each site, setting the Load Balancer name and using the backend bucket resources created in Step 2.
```
LOAD_BALANCER=<Load balancer name>

gcloud functions deploy toggle-${SITE_1} \
    --source=./src/ \
    --entry-point main \
    --runtime python37 \
    --trigger-topic ${SITE_1}-topic \
    --set-env-vars LOAD_BALANCER=$LOAD_BALANCER,BACKEND_BUCKET=$SITE_1

gcloud functions deploy toggle-${SITE_2} \
    --source=./src/ \
    --entry-point main \
    --runtime python37 \
    --trigger-topic ${SITE_2}-topic \
    --set-env-vars LOAD_BALANCER=$LOAD_BALANCER,BACKEND_BUCKET=$SITE_2
```
