# coeater-rest

## 사용 방법

#### 설치하기

1. python3를 설치합니다.

   ```
   apt-get install python3
   ```

2. pip를 설치합니다.

   ```
   apt-get install python3-pip
   ```

3. requirements를 설치합니다.

   ```
   pip3 install requirements.txt
   ```

#### 서버 실행하기

​	Django는 manage.py로 모든 것을 관리합니다.

​	migration을 해주는 이유는, models에 코드로 정의되어있는 db struct를 실제 db로 만들기 위해서입니다.

1. migration파일을 만들어줍니다.

   ```
   python3 ./manage.py makemigrations
   ```

2. migrate를 해줍니다.

   ```
   python3 ./manage.py migrate
   ```

3. 서버를 돌려줍니다. $port는 원하는 포트 번호로 입력해줍니다.

   ```
   python3 ./manage.py runserver $port
   ```

#### 슈퍼 유저 만들기

​	Django에서 자동으로 만들어주는 admin site에 접속하기 위한 슈퍼 유저 만드는 법입니다.

```
python3 ./manage.py createsuperuser
```

#### Admin site 들어가기

서버 실행하기 이후, `http:://YOUR-URL/admin`에 접속하여 슈퍼 유저로 로그인해줍니다.

UID와 password를 이용해 로그인 가능하고, DB 수정 및 조회가 가능합니다.

