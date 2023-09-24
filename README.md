# apartment_scraper
This is a project used to get information about apartments available to rent or buy from Willhaben.at, on the biggest platforms available in Austria. You can select yourself what areas of Austria you are interested in, as well as if it is for buying or renting. The data will then be saved in a local database that easily can be used to get a good overview of the market.

## Possible improvements
- Currently it only stores data in the database. It would be nice with some kind of export to for example .csv or excel files.
- Currently only supports Willhaben.at. Might be of interest to add other platforms as well.

## How to use
Checkout out the repo from Github:
```bash
git clone https://github.com/golgor/apartment_scraper.git
```
Then install it as editable install using pip:
```
pip install -e .
```
Customize __main__.py accordingly, execute it, and you will then find the database in the folder of the package, typically `apartment_scraper/apartment_scraper/test.db`.

### Use API
To use the API, build the image using docker. While in the main directory, execute:
```bash
> docker build -t apartment-api .
```
To start the image in a detached state, execute:
```bash
> docker run -d -p 8080:80 apartment-api:latest
```

## Deployment
### Deployment files
You can use the [kompose](https://github.com/kubernetes/kompose) to generate Kubernetes deployment files from the docker-compose.yaml. Note the added label for the web service, this is used by kompose to also generate a load balancer so the pod is reachable externally. Also, it seems to not work when using profiles in the docker-compose.yaml. These have to be commented out when using `kompose`. To generate the files the command `kompose convert` was used.

### Minikube
[Minikube](https://github.com/kubernetes/minikube) is used to deploy the app locally for this testing purposes. To deploy the app locally, the steps below is necessary:
1. Start the minikube `minikube start`.
2. Verify that the correct context is selected `kubectl config current-context`. It should be `minikube`
3. Being in the same folder as the generated files, run `kubectl apply -f database-deployment.yaml,database-service.yaml,postgres-data-persistentvolumeclaim.yaml,web-deployment.yaml,web-service.yaml,web-tcp-service.yaml`
4. Running `kubectl get pods` should show two pods that are either running or starting up.
5. We need to initialize the database
    1. Login into the shell of the database pod. `kubectl exec --stdin --tty database-db897986c-qkdqs -- /bin/bash`. The exact name of the database pod is available using `kubectl get pods`
    2. Run the command `createdb -h localhost -U postgres` apartments
    3. (Optional) Verify everything by running `psql -h localhost -U postgres` and then run `\l` to list all the databases. One of the rows returned should be apartments.
6. Get the external url for the load balancer using `minikube service web-tcp --url`. This typically returns something like `http://192.168.49.2:31717`.
7. Open the url from above in a browser should return `{"Hello":"World"}`.