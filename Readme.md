This is a case study to evaluate and compare two tables of CI050 and CC050 regularly.
In order to do so, a cron job has been implemented that runs every night at 23:50.
(MarginCheckCronJob in margin_check/cron_jobs.py)

There are two checks that has been implemented:

- Check, if the end-of-day values of the previous day are the same as the first intraday values.
  (margin_check/tasks.py)
  * check_differences_of_cc050_and_ci050_first_intraday

- Check, if the end-of-day values are the same as the last intraday values. (margin_check/tasks.py)
  * check_differences_of_cc050_and_ci050_last_intraday


## Setup Postgresql
On __Ubuntu/Debian__ you need to:
* login as postgres root: `sudo su - postgres`
* run `createuser margin`
* run `createdb -O margin margin`
* run `psql`
* run `ALTER ROLE margin CREATEDB;`
* press twice `CTRL + D` to get back
* edit the file `/etc/postgresql/11.10/main/pg_hba.conf` and  change `md5` to
`trust` for IPv4 local connections:
```
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
```
* you need to restart postgres after this: `systemctl restart postgresql.service`


## How to run application
* `pip install -r requirements_dev.txt`
* `python manage.py migrate`
* `python manage.py runserver`

## How to run pytest

* pytest
