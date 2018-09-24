# Setup instructions

## Install requirements:

`pip install ansible`

## Update configuration files

Edit inventory file and update variables

## To deploy geodemo to EC2 instance:

`ansible-playbook -i inventories/prod install.yml`

## Create a superuser account

Login to the server using SSH and run:

```bash
$ cd /opt/geodemo
$ source venv/bin/activate
$ cd geodemo
$ python manage.py createsuperuser
```

## Profit!

Use you new superuser account to login and have fun!
