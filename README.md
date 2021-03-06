# API Calidad del Aire / Air Quality API [![Build Status](https://travis-ci.org/idatosabiertos/api-calidad-aire.svg?branch=master)](https://travis-ci.org/idatosabiertos/api-calidad-aire)
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
4. **API JOB**
	- [API JOB](https://github.com/idatosabiertos/calidad-aire-cdmx-latam) levantada y corriendo / up and running

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

### Vagrant  [/vagrant](https://github.com/idatosabiertos/api-calidad-aire/tree/master/Vagrant)
**Requerimientos / Requirements**
 - [Vagrant](https://www.vagrantup.com/downloads.html)
 - [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
**Pasos / Steps:**
1. `git clone https://github.com/idatosabiertos/api-calidad-aire`
2. `cd api-calidad-aire/Vagrant`
3. `vagrant up` 
4. Navegar a / Navigate to `http://localhost:8000` en la maquina host / on host machine.


## DATOS / DATA
Los datos son cargados por un [trabajo programado](https://github.com/idatosabiertos/calidad-aire-cdmx-latam) que corre periódicamente, donde consulta la [API](http://148.243.232.113/calidadaire/xml/simat.json) de Secretaría de Medio Ambiente de la Ciudad de México y actualiza la base de datos.

The data is uploaded by a [scheduled work](https://github.com/adatosabiertos/calidad-aire-cdmx-latam) that runs periodically, where it queries the [API](http://148.243.232.113/calidadaire/xml/simat.json) from Secretary of the Environment of Mexico City and updates the database.

Los datos son almacenados en una base de datos NO relacional, compuesta de la siguiente forma:  
The data is stored in a NON-relational database, composed as follows:

![alt text](https://github.com/idatosabiertos/api-calidad-aire/blob/master/documentation/database.jpg "database")