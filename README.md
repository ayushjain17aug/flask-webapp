flask-webapp
============

Enviroment

```
$ git clone git@github.com:itdxer/flask-webapp.git
$ cd flask-webapp
$ virtualenv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

Run application
---------------

### Run local server ###

```
python run.py server
```

### Production server on Ubuntu ###

1) Install apps

```
$ sudo apt-get install nginx supervisord
```

2) Configure nginx for static

```
$ sudo nano /etc/nginx/sites-available/watchit.conf
```

Nginx configs file

```
upstream watchit.itdxer.com {
    server localhost:12345 fail_timeout=0;
}

server {
    listen 80;
    client_max_body_size 4G;
    server_name watchit.itdxer.com;
    access_log  /home/superuser/watchit/logs/watchit.access.log;
    keepalive_timeout 5;

    root /home/superuser/watchit/static;
    
    location / {
        proxy_pass http://watchit.itdxer.com;
    }

    location ~ ^/(static)/ {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://watchit.itdxer.com;
            break;
        }
     }
}
```

make symbolic link on this file

```
$ sudo ln -s /etc/nginx/sites-available/watchit.conf /etc/nginx/sites-enabled/
```

Restart nginx 

```
$ sudo service nginx restart
```

3) Gunicorn and supervisord

```
$ sudo nano /etc/supervisor/conf.d/watchit.conf
```

Configaration

```
[program:myproject]
command=/home/superuser/watchit/.env/bin/gunicorn run:app --bind <ipaddr>:80 --workers=3 --log-file /home/superuser/watchit/logs/gunicorn.log
directory=/home/superuser/watchit
umask=022
autostart=true
autorestart=true
startsecs=10
startretries=3
exitcodes=0,2
stopsignal=TERM
stopwaitsecs=10
user=superuser
```

Reload supercisord

```
$ sudo supervisorctl reload
```

4) Open you site in browser
