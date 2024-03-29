# Stock Visualization Container on AWS 
This project creates and deploys a Docker container on AWS which can do stock visualization. This project is easily scalable to do financial analysis and machine learning prediction.

**Demo Video:**

https://youtu.be/za1JScC2QmQ

# Usage
Through Docker Hub, the project can be easily run anywhere in a form of a container on your local machine.

## Pull the docker repository
```
docker pull yzjshz1998/project2
```

## Run the image
```
docker run -it yzjshz1998/project2 python -W ignore stock.py
```

Then the stock price of AMZN has been crawled and visualized, then saved as an png image.
