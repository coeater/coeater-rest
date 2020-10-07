# coeater-rest

- [coeater-rest](#coeater-rest)
  - [파일 구조](#파일-구조)
  - [사용 방법](#사용-방법)
      - [설치하기](#설치-하기)
      - [서버 실행하기](#서버-실행하기)
  - [DB 구조](#db-구조)
      - [User](#user)
      - [Friend](#friend)
      - [History](#history)

## 파일 구조

다양한 파일이 있지만, 읽어볼만한 파일들만 적습니다.

&nbsp;backend/

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;settings.py						-> Django에 추가한 api와 기본 설정들

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;urls.py								-> Request가 가능한 url 모음

&nbsp;users/

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;models.py						-> DB구조 정의			

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;serializers.py					-> Serialization을 위한 serializer클래스 정의

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;views.py							-> REST API 실제 구현 코드, **현재 미구현**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;urls.py								-> backend/urls.py에 정의된 url 중 users로 이어지는 url들 세부 분류, **현재 미구현**

​	

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



## DB 구조

#### User

 - id : Number

   ​	-> 식별자의 역할입니다. 코드 상에는 없지만, 자동으로 추가되는 필드입니다.

 - created : Date

   ​	-> 가입날짜입니다. 자동으로 현재시간으로 생성됩니다.

 - phone : PhoneNumber

   ​	-> 로그인할 때 쓰이는 데이터입니다. 편의상 전화번호로 했고, 추후 수정 가능합니다.

 - nickname : Char[20]

   ​	-> 사용자의 별명입니다. 20글자 제한입니다.

 - is\_active, is\_admin, is\_superuser, is\_staff : Boolean

   ​	-> Django 내부적으로 쓰이는 필드입니다.

#### Friend

friend 테이블은 유저와 유저를 1:1로 연결합니다.

User A와 B가 있을 때, {owner: A, friend: B}는 DB에 있지만 {owner: B, friend: A}는 없는 경우 친구 승락 대기 중으로 판단할 수 있습니다.

- id : Number

  ​	-> 식별자의 역할입니다. 코드 상에는 없지만, 자동으로 추가되는 필드입니다.

- created : Date

  ​	-> 생성날짜입니다. 자동으로 현재시간으로 생성됩니다.

- owner : User

  ​	-> 친구를 신청한 유저입니다.

- friend : User

  ​	-> 친구를 신청받은 유저입니다.

#### History

history 테이블은 유저와 유저를 1:1로 연결합니다.

User A와 B에 대한 새로운 History tuple을 생성 시 {owner: A, target: B}와 {owner:B, target: A}를 동시에 생성하는 것을 원칙으로 합니다.

이는 A가 B에 대한 history를 삭제해도 B의 A에 대한 history가 남아있게 하기 위해서입니다.

**각 Attribute에 대한 내용은 Friend와 유사하므로 생략합니다.**

- id : Number
- created : Date
- owner : User
- target: User