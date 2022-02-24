# The name of our algorithm
algorithm_name=training-gpu
aws_algorithm_name=training-gpu
aws_account_id=012345678901
account=$(aws sts get-caller-identity --query Account --output text)
# Get the region defined in the current configuration (default to us-west-2 if none defined)
region=$(aws configure get region)
region=${region:-us-west-2}
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${aws_algorithm_name}:latest"
# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${aws_algorithm_name}" > /dev/null 2>&1
if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${aws_algorithm_name}" > /dev/null
fi
# Get the login command from ECR and execute it directly
docker login -u AWS -p $(aws ecr get-login-password --region us-east-2) ${aws_account_id}.dkr.ecr.us-east-2.amazonaws.com
# Build the docker image locally with the image name and then push it to ECR
# with the full name.
docker build -q -t ${algorithm_name} .
docker tag ${algorithm_name} ${fullname}
docker push ${fullname}