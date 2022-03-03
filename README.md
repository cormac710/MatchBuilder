# Why???
The reason for this project is I felt like building a project with flask to brush up on it. 

Im going to deploy to AWS and when, im going to migrate and deploy as lambda functions using API gateway

Why flak? because it`s useful for building python server applications. I know lambdas and serverless has become the buzz word lately so thats why  want to start with flaks and migrate

It should be fun

I am using dynamoDb which is probably the most popular schemaless DB's hosted by AWS.
Really it's between DocumentDb (postgres under the hood to give MongoDb compatibility) and dynamo.
But Dynamo has more cool features, im thinking of adding something fun with dynamo streams later on when the basics are covered.

Essentially this is a backend application for creating matches (im a fan of football), for example people trying to organise astro games during the week.

It's not going to be full of features (at least for now, think of it as basic prototype), my main goal is put together and python application and deploy to AWS.

I think from this approach ill get more benefit that building a load of little perfect features which are similar to code in place. E.x really it should be adding people to teams and adding 2 teams to a match but isnt my goal of this project as I could spend months building features but not learning much.

# Local set up

## Run all in docker
```
# Create directory to mount dynamo 
mkdir docker
docker-compose up -d
```

### Add a Person
Send a POST request to: http://127.0.0.1:5001/api/person/

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
