# Why???
The reason for this project is I felt like building a project with flask to brush up on it. 

Im going to deploy to AWS using ECS and EC2 when thats done, im going to migrate and deploy as lambda functions using API gateway

Why flak? because it`s useful for building python server applications. I know lambdas and serverless has become the buzz word lately so thats why  want to start with flask and migrate

It should be fun

I am using dynamoDb which is probably the most popular schemaless DB's hosted by AWS.
Really it's between DocumentDb (postgres under the hood to give MongoDb compatibility) and dynamo.
But Dynamo has more cool features, im thinking of adding something fun with dynamo streams later on when the basics are covered.

Essentially this is a backend application for creating matches (im a fan of football), for example players trying to organise astro games during the week.

It's not going to be full of features (at least for now, think of it as basic prototype), my main goal is put together a super basic python application and deploy to AWS.

I think from this approach ill get more benefit that building a load of little perfect features for a real life app which are similar to code in place. E.x really it should be adding players to teams and adding 2 teams to a match but isnt my goal of this project as I could spend months building features but not learning much.

I will be looking into improving and scaling the dynamoDb so features may be edited to work with this in the future

# Local set up

## Run all in docker
Do to the docker-compose and make sure `IS_DEV=True` is set in the flask configuration.
```
# Create directory to mount dynamo 
mkdir docker
docker-compose up -d
```

### Add a player
Send a POST request to: http://127.0.0.1:5001/api/player/

You can use the following body (at least until swagger is up and running)
```
{
    "email": "cormac@email.com",
    "first_name": "cormac",
    "age": 22
}
```

Note: ive set it up using 5001 for local dev reasons on my own machine instead of the default 5000

## Run as application 

### Dynamo (still using dynamo docker container)
Comment out the "backend" configuration in docker-compose.yaml
```
# Create directory to mount dynamo 
mkdir docker
docker-compose up -d
```

### Flask

Python 3.8.9
#### Create virtual env
```
virtualenv venv
source venv/bin/activate
pip install -r src/requirements.txt
python -m src.app
```

# Deploy to AWS 
To deploy you must set up and AWS and get your secret and access keys and export and environment variables

Also note, only available to deploy in eu-west-1 region (Ireland). Deploying to other regions is in the TODO column. 
I am more interested in getting a basic working app and deploying up and running at the minute
```
export AWS_ACCESS_KEY=<yur_access_key>
export AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
export AWS_DEFAULT_REGION=<your_region>
```

Run "deploy/deploy_main.py" to deploy services to AWS (still in being developed and improved).

Some new requirements are needed for this, at the minute installing them into the existing venv but in the future I plan
to deploy via docker so this is only a temporary measure until I get the basics working.

Currently it deploys all services and if one fails, all are rolled. In a microservies architecture, services should be able to be upgraded independently but dont worry Ill get there :) 

```commandline
MatchBuilder % pip3 install -r deploy/deploy_requirements.txt
MatchBuilder % python -m deploy.deploy_main
```

## Deploy Backend using Flask and ECS, WHY?
This is phase one, EC2 to being phased out by serverless architectures or using Fargate.

I started with this because its very popular and is still used a lot and practice migrating to serverless.

Why EC2 over Fargate, because EC2 is harder to deploy than Fargate. If you can deploy using EC2 you can do Fargate.

## Deploy Backend using lambda
Because serverless!!! 

TODO
