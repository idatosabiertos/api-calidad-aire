# API Calidad del Aire / Air Quality API [![Build Status](https://travis-ci.org/idatosabiertos/api-calidad-aire.svg?branch=develop)](https://travis-ci.org/idatosabiertos/api-calidad-aire)
API rest para [aplicación web Calidad del Aire](https://github.com/idatosabiertos/calidad-del-aire-webapp), construido a partir de un framework que utiliza MongoEngine.  
A Restful API for [Air quality web app](https://github.com/idatosabiertos/calidad-del-aire-webapp), built from framework wrapped around MongoEngine.

## REQUERIMIENTOS / REQUIREMENTS
1. **Mongo DB**	 
	 - [Instalación / Installation](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-mongodb-on-ubuntu-16-04) 
2. **Python && pip**
	 - $`sudo apt-get install -y python-pip python-dev build-essential python-blinker`
	 - $`sudo pip install --upgrade pip`	 

3. **Twitter Keys and Access Tokens**
	 - [Crear app en twitter/Create twitter app](https://apps.twitter.com)

## INSTALACIÓN / INSTALATION
- $`git clone https://github.com/idatosabiertos/api-calidad-aire`
- $`pip install -r requirements.txt`
- $`export con_secret= your_twitter_consumer`
- $`export con_secret_key=your_twitter_consumer_secret`
- $`export token=your_twitter_token`
- $`export token_key=your_twitter_token_secret`
- $`export rollbar_key=your_rollbar_key`
- $`export rollbar_environment=your_environment`
- $`python run.py`