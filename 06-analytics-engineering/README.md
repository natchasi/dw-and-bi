Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

# Analytics Engineer using dbt

## Create virtual env
``` 
python -m venv ENV
```
```
# activate ENV
source ENV/bin/activate
```

## Install packages from requirement.txt
```
pip install -r requirement.txt (already created all updated package version)
```

## initiate project
```
dbt init
```
### Setup project
```
name project -ds525
```

> setup profile for collect information to connect to data warehouse
show information

```
code | profile directory
```
> create profile.yml to collect all information

## Check connection
```
dbt debug
```
All checks passed!

## read all models and show in destination

- create model 

> run automate test
```
dbt test
```

- create layer
> staging
create model in staging

> marts

- materization
> by staging and marts
