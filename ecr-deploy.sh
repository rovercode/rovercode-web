if [[ $# < 1 ]]
then
    echo "Requires one argument: the name of the environment."
    exit 1
fi

echo "Deploying $1 image to ECR"

pip install --user awscli
export PATH=$PATH:$HOME/.local/bin

cp ./compose/django/Dockerfile .
docker build -t 795223264977.dkr.ecr.us-east-2.amazonaws.com/rovercode:$1 .
eval $(aws ecr get-login --region us-east-2 --no-include-email) # requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY secret environment variable set in Travis
docker push 795223264977.dkr.ecr.us-east-2.amazonaws.com/rovercode:$1
