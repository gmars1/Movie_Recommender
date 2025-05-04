### все команды выполняются из корня проекта

при изменении models.py нужно создать новый файл миграции:
```commandline
alembic -c FilmsDatabase/alembic.ini revision --autogenerate -m "message"
```

для установки базы в релевантное состояние:
```commandline
alembic -c FilmsDatabase/alembic.ini upgrade head
```

---

### если папки `FilmsDatabase/migrations` и файла `FilmsDatabase/alembic.ini` нет:

1. эта команда выполняется при инициализации alembic'a:

```commandline
cd FilmsDatabase
alembic init -t async migration
```

2. указываем FilmsDatabase/alembic.ini:
```commandline
script_location = migration/FilmsDatabase/
```

3. указываем настройки в `FilmsDatabase/migrations/env.py`:
```commandline
from FilmsDatabase.database import Base, DATABASE_URL

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```

---
