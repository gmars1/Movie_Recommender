### все команды выполняются из корня проекта

при изменении models.py нужно создать новый файл миграции:
```commandline
alembic -c FilmsDatabase/alembic.ini revision --autogenerate -m "message"
```

---

### если папки `FilmsDatabase/migration` и файла `FilmsDatabase/alembic.ini` нет:

1. эта команда выполняется при инициализации alembic'a:

```commandline
cd FilmsDatabase
alembic init -t async migration
```

2. указываем настройки в `FilmsDatabase/migration/env.py`:
```commandline

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

#базовый класс
target_metadata = Base.metadata
```

---
