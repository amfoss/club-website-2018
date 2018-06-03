### Status update

#### Update database

```bash
python manage.py update_status --date 02-06-2018
```

This command will only update the status report in the group.

##### With option

This will send status report message to telegram group, mailing list and create a new thread for the next day.

```bash
python3 /home/ubuntu/fosswebsite/manage.py update_status --telegram --create-thread --mail --date 02-06-2018 
```

#### Update GMail api token

```bash
python3 create-gmail-token.py --noauth_local_webserver
```
