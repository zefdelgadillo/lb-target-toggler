upload: 
	gsutil -m -h "Cache-Control:no-cache,max-age=0" \
		cp -r static/* gs://${TARGET_BUCKET}/
	gsutil web set -m index.html -e 404.html gs://${TARGET_BUCKET}/ 

deploy: build upload
