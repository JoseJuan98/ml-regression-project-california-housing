# Microservice Development

#### Deploying the API Locally

1. Clone the repository from GitHub:

```shell
git clone https://github.com/yourusername/your-repository.git
```

2. Install the required dependencies using pip:

```shell
cd your-repository pip install -r requirements.txt
```

3. Start the Flask server:

```shell
python app.py
```

4. The API should now be available at `http://localhost:5000/`.

#### Deploying the API to a Server

1. Ensure that you have Docker installed on the server.
2. Clone the repository from GitHub:

```shell
git clone https://github.com/yourusername/your-repository.git
```

3. Build the Docker image:

```shell
cd your-repository docker build -t your-image-name .
```

4. Run the Docker container:

```shell
docker run -p 5000:5000 -it your-image-name
```

5. The API should now be available at `http://your-server-ip-address:5000/`.

Note: You may need to configure your firewall to allow incoming connections on port 5000.

#### Using the API

The API supports a `POST` request to the `/predict` endpoint with a JSON payload containing the features for the
prediction. The expected features
are `longitude`, `latitude`, `housing_median_age`, `total_rooms`, `total_bedrooms`, `population`, `households`,
and `median_income`.

Here's an example request using `curl`:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"longitude":-122.23,"latitude":37.88,"housing_median_age":41,"total_rooms":880,"total_bedrooms":129,"population":322,"households":126,"median_income":8.3252}' http://localhost:5000/predict
```

The response will be a JSON object containing the predicted value for `median_house_value`.