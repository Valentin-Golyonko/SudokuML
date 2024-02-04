
black
```shell
black .
```

migration
```shell
python manage.py makemigrations && python manage.py migrate
```

INITIAL DATA:
```shell
python manage.py dumpdata core solver -o db_backup/initial_data.json.xz
```

TEST DATA:
```shell
python manage.py dumpdata core solver -o db_backup/test_data.json.xz
```

```shell

```
