# Pull Request analizer

## How to run

### Get Bitbucket token bearer

- Go to http://wzgdcvaleja01pr:7990/plugins/servlet/access-tokens/manage
- Click `Create a token`
- Choose a name fot the credentials, give read permissiones and click `Create`

### Run app

```shell
python3 pull-requests-analizer.py your-bitbucket-token your-pivotal-token
```
