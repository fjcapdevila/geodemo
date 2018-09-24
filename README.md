# Simple project using Geodjango + Django Rest Framework + PostGIS

This is a simple project for testing purposes, it is not **production-ready** at all.


### Admin

http://18.235.8.240/api/v1/

### API root

http://18.235.8.240/api/v1/


### Create a language

```bash
curl -i -X POST \
   -H "Content-Type:application/json" \
   -H "Authorization:Basic <edited>" \
   -d \
'{
  "name": "French"
}' \
 'http://18.235.8.240/api/v1/languages/'
```


### Create a currency

```bash
curl -i -X POST \
   -H "Content-Type:application/json" \
   -H "Authorization:Basic <edited>" \
   -d \
'{
  "name": "Real"
}' \
 'http://18.235.8.240/api/v1/currencies/'
```


### Create a provider

```bash
curl -i -X POST \
   -H "Content-Type:application/json" \
   -H "Authorization:Basic <edited>" \
   -d \
'{
  "name": "Provider 3",
  "email": "user@provider3.com",
  "phone_number": "+12345667",
  "language": "http://18.235.8.240/api/v1/languages/1/",
  "currency": "http://18.235.8.240/api/v1/currencies/1/",
  "service_areas": []
}' \
 'http://18.235.8.240/api/v1/providers/'
```


### Create a service area

```bash
curl -i -X POST \
   -H "Content-Type:application/json" \
   -H "Authorization:Basic <edited>" \
   -d \
'{
    "id": 4,
    "type": "Feature",
    "geometry": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [
                        -30.0,
                        -30.0
                    ],
                    [
                        -30.0,
                        30.0
                    ],
                    [
                        30.0,
                        30.0
                    ],
                    [
                        30.0,
                        -30.0
                    ],
                    [
                        -30.0,
                        -30.0
                    ]
                ]
            ]
        ]
    },
    "properties": {
        "name": "Medium Centered Square",
        "price": "2.0000",
        "provider": 2
    }
}' \
 'http://18.235.8.240/api/v1/service_areas/'
```

### Get available providers for a location

```bash
curl -i -X GET \
   -H "Authorization:Basic <edited>" \
 'http://18.235.8.240/api/v1/providers_by_location/?lat=1.0&lng=1.0'
```


## Some implementation details

+ It uses an existing Docker image to run PostgreSQL + GIS extensions
+ It can be deployed using an Ansible playbook
+ You can deploy it to a Vagrant machine for local testing
+ It has ~40 test cases
+ Admin interface is enabled for your convenience
+ It uses the reliable **nginx + uwsgi + django + postgresql** stack
+ It was deployed to an EC2 instance (appserver + dbserver)
+ It uses Class Based Views
+ PEP8

- It only uses basic and session authentication backend
- It would be nice to run database on a different host or connect it to a Database as a Service
- Some fields don't have proper validators
- Permissions schema is too basic
- I am not an GIS/GeoJSON expert yet! Practice makes perfect (=



## TODO

- Improve the deployment playbook
- Remove some hardcoded values, specially in the playbook
- Store **sensitive information** using Ansible Vault
- Use environment variables for sensitive data
- Some tests need to be fixed (they are marked as skipped)
- Use better authentication backends (DjangoJWT?)
- Add field validators
- Implement a better permission schema

