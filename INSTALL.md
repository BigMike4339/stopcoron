# Базовая установка OTP
(По состоянию на 02.12.2020)

Платформа собирается под centos 7.

## Содержание
- [Требуемое ПО](#requiredsoft)
- [Пример установки требуемого ПО](#exampleinstall)
- [Настройка PostgreSQL](#setuppostgresql)
- [Местоположение последней версии OTP](#lastversion)
- [Установка и настройка](#install)
- [Запуск и остановка](#startend)
- [Дополнительно](#add)
- [Документация](#doc)

## Требуемое ПО <a name=requiredsoft></a>
Перед развёртыванием OTP необходимо установить следующее ПО:

- python3
- java8
- nginx (требуется подключение репозитория epel)
- postgresql версии старше 9.6
- ImageMagick-devel


Это ПО указано в этом [документе](https://docs.google.com/document/d/1lc27I0J0vyDnwt-CpaXOJfzXaATdXSPz7_MAQpNu6mU/),
но его необходимость под вопросом:
- perl-Image-ExifTool.noarch
- libreoffice
- poppler-utils

### Пример установки требуемого ПО <a name=exampleinstall></a>
```
yum -y install java-1.8.0-openjdk python3 postgresql-server-9.6.24
```
```
yum install epel-release
yum install nginx
systemctl start nginx
systemctl enable nginx
```

### Настройка PostgreSQL <a name=setuppostgresql></a>
1. Инициализируем базу: `sudo -u postgres postgresql-setup initdb`
2. Указываем права доступа: `vi /var/lib/pgsql/data/pg_hba.conf`
Внимание! Приведённые ниже строки необходимо вставить выше других конфигурационных записей в pg_hba.conf
```
local   dispatcher      dispatcher                              trust
host    dispatcher      dispatcher      127.0.0.1/32            trust  
host    dispatcher      dispatcher      ::1/128                 trust  
local   eva             dispatcher                              trust
host    eva             dispatcher      127.0.0.1/32            trust  
host    eva             dispatcher      ::1/128                 trust  
```
3. Запускаем PostgreSQL и добавляем в автозапуск:
```
systemctl enable postgresql.service
systemctl start postgresql.service
```

## Местоположение последней версии OTP <a name=lastversion></a>
http://storage.dev.isgneuro.com/#browse/browse:components:otp

## Установка и настройка <a name=install></a>
1. Разархивируем полученный otp-YYYY.MM.DD-centos-NN.tar.gz в директорию /opt.
 Далее пути указаны относительно /opt/otp.
2. В папке config/sql выполнить скрипты, создающие пользователя и две базы данных:
```
cd config/sql
chmod +x *.sh
create_user.sh 
create_db_dispatcher.sh
create_db_eva.sh
```
Не должно быть ошибок при выполнении скриптов.
3. Проверить, что базы создались и в них можно войти:
```
psql -U dispatcher dispatcher
psql -U dispatcher eva
```
4. Скопировать содержимое config/nginx в /etc/nginx и перезапустить nginx
```
cp -R config/nginx/* /etc/nginx/ 
systemctl restart nginx
```

## Запуск и остановка <a name=startend></a>
Для запуска выполнить скрипт `/opt/otp/start.sh`.

Так же можно стартовать через systemctl предварительно скопировав 
файл *.service в /etc/systemd.

Для остановки выполнить скрипт `/opt/otp/stop.sh`.

## Дополнительно <a name=add></a>
При проблемах с selinux ввести команду `setsebool -P httpd_can_network_connect 1`.

## Документация <a name=doc></a>
[Команды ОТЛ и общее описание](https://github.com/ISGNeuroTeam/otp)

