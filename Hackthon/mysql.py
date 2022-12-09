# Import libraries
from sshtunnel import SSHTunnelForwarder
import pymysql

# SSH (ec2_public_dns, ec2_user, pem_path, remote_bind_address=(rds_instance_access_point, port))
with SSHTunnelForwarder(('ec2-52-202-194-76.public-ec2-instance.amazonaws.com'), ssh_username="ec2-user",
                        ssh_pkey="~/ssh-tunnel-rds.pem", remote_bind_address=(
        'private-rds-instance.ckfkidfytpr4.us-east-1.rds.amazonaws.com', 3306)) as tunnel:
    print("****SSH Tunnel Established****")

    db = pymysql.connect(
        host='127.0.0.1', user="rdsuser", password="rdspassword",
        port=tunnel.local_bind_port, database="dbName"
    )
    # Run sample query in the database to validate connection
    try:
        # Print all the databases
        with db.cursor() as cur:
            # Print all the tables from the database
            cur.execute('SHOW TABLES FROM dbName')
            for r in cur:
                print(r)

            # Print all the data from the table
            cur.execute('SELECT * FROM table_name')
            for r in cur:
                print(r)
    finally:
        db.close()

print("YAYY!!")