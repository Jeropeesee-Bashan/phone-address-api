# Тестовое задание AVE Technologies

## Адресный сервис
Сервис представляет из себя веб-приложение, написанное на Python при помощи
FastAPI. С помощью него можно сохранять данные некоторых лиц
(номер телефона и адрес) в базу данных Redis.

Зависимости:
- fastapi
- pydantic-extra-types
- pydantic-settings
- phonenumbers
- redis
- uvicorn

## Развёртывание в Docker
Приложение можно развернуть как Docker-контейнер. Достаточно лишь его собрать:
```sh
docker build -t phone-address-api:latest .
```

Предполагается, что адресный сервис работает как микросервис, поэтому запуск
в Docker производится через штатную точку входа `fastapi`, запускаясь, как один
поток в одном процессе, что весьма предпочтительно для кластеров Kubernetes.

## Тестирование
Чтобы быстро протестировать сервис, можно воспользоваться pytest и
Docker Compose:
```sh
# pip install pytest httpx

docker-compose up --build -d
pytest ./tests/phonenumbers.py
docker-compose down
```

## Описание
Были реализованы четыре обработчика по пути `/address` с методами:
- GET
- POST
- PUT
- DELETE

По ним можно либо получить адрес по известному номеру телефона, либо удалить
или записать.

На мой личный взгляд, `/address` - отличное название для пути ресурса, так как
оно лучше всего даёт понять о тех данных, с которыми мы работаем. `/check_data`
и `/write_data` плохо соответствуют принципам REST.

Дополнительные методы PUT и DELETE были добавлены, потому что загрузка новых
данных и обновление существующих по отдельности дают больше контроля при
разработке использовании сервиса и могут применяться в разных use-кейсах. Также
всегда стоит предусматривать случаи, когда может потребоваться удалить данные
из хранилища.

### Архитектура
Хоть сервис и не такой уж и большой, я разделил его исходный код на несколько
файлов. Каждый из них представляет из себя рабочую часть сервиса.

#### app.py
Определение FastAPI-приложения и реализация обработчиков.

#### keyval.py
Определение интерфейса key-value хранилища, с помощью которого осуществляется
доступ к номерам телефонов и адресам. Здесь также есть реализация этого
интерфейса для взаимодействия с Redis.

#### storage.py
Реализация доступа к хранилищу во время работы приложения. Во время старта
приложения присваевает переменной `storage` значение типа KeyVal при помощи
фабричного метода, определённого в настройках.

#### schema.py
Описание модели данных, с которыми работает FastAPI. Здесь я использую
валидацию номеров телефонов, определённых в
`pydantic_extra_types.phone_numbers`.

Единственный нюанс, который стоит упомянуть - это то, что вводимые российские
номера должны начинаться либо с +7, либо без какого-либо префикса. То есть,
номера не начинаются с 8. Так работает `phonenumbers`. Пользователям сервиса
стоит учесть этот нюанс и при возможности преобразовывать номера телефонов
самостоятельно, если требуется.

Сервис сохраняет каждый номер телефона в формате виде типа "+79001111111",
что является самой универсальной и краткой записью номера телефона, которую
можно использовать как ключ.

#### config.py
Определение доступных настроек приложения. Во время старта сервиса
автоматически подхватываются переменные окружения, которые можно
переопределять:
- PHONEADDRESS_HOST
- PHONEADDRESS_PORT
- PHONEADDRESS_REDIS_URL

## Второе теоретическое задание
Со вторым тестовым заданием можно ознакомиться в этом репозитории в файле
`Second_Task.md`.
