if ! [ -d layer ]; then
    pipenv run pip freeze > requirements.txt
    pip3 install -r requirements.txt -t layer/python/lib/python3.12/site-packages
fi

if ! [ -f s3_bucket.txt ]; then
    read -p "s3 bucket (cft templates): " bucket_name
    echo $bucket_name > s3_bucket.txt
fi

read -r S3_BUCKET < s3_bucket.txt

aws s3 sync logs s3://minecraft-world-curran/logs
aws s3 sync server s3://minecraft-world-curran
aws s3 sync scripts s3://minecraft-world-curran/scripts --delete

sam build -t cloudformation.yaml
sam deploy -t cloudformation.yaml \
    --stack-name Minecraft-Server \
    --capabilities CAPABILITY_NAMED_IAM \
    --s3-bucket $S3_BUCKET
