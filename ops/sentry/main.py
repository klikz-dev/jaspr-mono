from fabric2 import Connection

ENVS = {
    "production" : "",
    "development" : {
        "host" : "ec2-18-144-2-192.us-west-1.compute.amazonaws.com",
        "domain" : "senty.jaspr-development.com",
        "key" : "/Users/toddcullen/.jaspr/sentry/development.pem"
    }
}

def create_connection(connection, key_filename):
    return Connection(connection, connect_kwargs={"key_filename":key_filename})


def setup_certbot(connection, domain):
    connection.run("sudo add-apt-repository ppa:certbot/certbot")
    connection.run("sudo apt install python-certbot-nginx")
    connection.run(f"sudo certbot --nginx -d {domain}")


def restart_ngnix(connection):
    connection.run('sudo service nginx restart')


def change_nginx_domain(connection):
    # sudo vi /home/ubuntu/.sentry/nginx.conf
    # Change server_name to below
    # server_name "sentry.myapp.com"
    pass

def run_setup(connection):
    pass


if __name__ == "__main__":
    e = ENVS["development"]
    print("creating connection")
    with create_connection(e["host"], e["key"]) as c:
        print("connected")
        print("starting setup")

        print("setup certbot")
        setup_certbot(c, e["domain"])
        print("certbot done")

        print("setup complete")
