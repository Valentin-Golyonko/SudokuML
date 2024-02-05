
black
```shell
black .
```

migration
```shell
python manage.py makemigrations && python manage.py migrate
```

Backup INITIAL and TEST DATA:
```shell
python manage.py dumpdata core solver -o db_backup/initial_data.json.xz
python manage.py dumpdata core solver -o db_backup/test_data.json.xz
```

```shell
pip install -U pip setuptools wheel pip-tools --timeout 60
pip-compile --upgrade requirements.in -o requirements.txt
pip-compile --upgrade requirements_dev.in -o requirements_dev.txt -c requirements.txt
pip-sync requirements.txt requirements_dev.txt --pip-args "--retries 10 --timeout 60"
```

```shell

```
