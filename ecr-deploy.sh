if [[ $# < 1 ]]
then
    echo "Requires one argument: the name of the environment."
    exit 1
fi

echo "Deploying $1 image to ECR"

pip install awscli

docker build -t 795223264977.dkr.ecr.us-east-2.amazonaws.com/rovercode-web-service:$1 -f ./compose/django/Dockerfile .
docker build -t 795223264977.dkr.ecr.us-east-2.amazonaws.com/rovercode-profanity-check:$1 -f ./compose/profanity/Dockerfile .
eval $(aws ecr get-login --region us-east-2 --no-include-email) # requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY secret environment variable set in Travis
docker push 795223264977.dkr.ecr.us-east-2.amazonaws.com/rovercode-web-service:$1
docker push 795223264977.dkr.ecr.us-east-2.amazonaws.com/rovercode-profanity-check:$1
