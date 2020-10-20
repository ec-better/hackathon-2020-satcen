# satcen-better-hackathon-2020

## Run the notebook on Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ec-better/hackathon-2020-satcen/master?urlpath=lab)

## Run the notebook locally using docker

Clone this repository with:

```bash
git clone https://github.com/ec-better/hackathon-2020-satcen.git
```

Go to the directory containing the cloned repository:

```bash
cd hackathon-2020-satcen
```

Use docker compose to build the docker image:

```bash
docker-compose build
```

This step can take a few minutes...

Finally run the docker with:

```
docker-compose up
```

Open a browser window at the address http://0.0.0.0:9005 or http://127.0.0.1:9005 and run the notebook

## About the hackathon

 ### Description: 
 The goal is to identify changes in Sentinel-1 (SAR) imagery. 
 The complexity of the exercises will depend on the audience skills.
 
 ### Tentative Agenda:
     
* 1.[Introduction](./introduction.ipynb)
     
* 2.[Introduction to SAR image formation and differences with Optical Data](./introductionSAR.ipynb)
     
* 3.[Change Detection with SAR imagery](./acd.ipynb)

* 4.[Thresholding techniques](./thresholding.ipynb)
     
* 5.[Postprocessing](./postprocessing.ipynb)
     
* 6.[Series of data](./series.ipynb)
 
 
 ### Requirements: 
 This [Binder](https://mybinder.readthedocs.io/en/latest/introduction.html#what-is-a-binder) repository was set up so that you can participate with no pre-requirement to be installed on your side.
 However, the notebook must target a computing environment with 2 GB of RAM. After some inactivity, the docker container is culled. Access to a web browser should be enough for your successful participation.
 
 ### Target Participants: 
 Students, Software developers, Data scientists, EO-developers, anyone with an interest in the topic.
 
 ### Time requirements: 
 
 Half day (4 hours)
