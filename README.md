#ARA Monitoring Tool

## Introduction 
ARA Monitoring Tool 은 ARA의 게시판을 Crawling 하여, Mail 혹은 APNS로 알림을 주는 도구이다. 
자체적으로 Threading을 하여 Daemonize 되어 작동하므로, cron을 이용하지 않아도 된다. 

## Package Dependancies:
requirements.txt 에 명시되어 있다. 권장 설정은 init.py 를 이용하여 설정하는 것이다. 
	
`$ python init.py`
	
init.py 는 virtaulenv 를 설정하고, 의존성 패키지를 설치한다. 또한 필요한 로컬설정파일을 생성한다.

## Initialization 
처음 이 프로그램을 실행시키기 위해 설정해야할 값들이 settings.py 에 모두 있다. 

**DEBUG** : Debug모드를 사용할 것인지 결정한다. Debug모드를 사용하면 log가 모두 화면에 출력되고 log보다 자세한 내용들을 담고 있다. 

**period** : 크롤링을 할 주기이다. 기본은 120초 이다. 

**boardnames** : 크롤링할 보드의 이름들을 적어준다. 되도록 구독하지 않는 보드의 이름은 추가하지 않는 것이 크롤러의 성능과 아라서버의 부하를 줄인다. 

**ara_id** : 크롤링을 위해 아라에 접속할 ID 이다. 

**gmail_user** : 메일을 보내기 위한 SMTP로 GMail 의 SMTP를 사용하고 있으므로, Gmail계정이 필요하다.

**ARA_PASSWORD** : 아라를 크롤링하기 위해 사용할 계정의 비밀번호이다. settings.py 보다는 settings_local.py 에 기록하고 권한을 다르게 설정할 것을 추천한다.

**GMAIL_PASSWORD** : 메일을 보내기위한 Gmail Account의 Password이다. settings.py 보다는 settings_local.py 에 기록하고 권한을 다르게 설정할 것을 추천한다. 

**index_file_name** : 일종의 DB처럼 사용되는 가장 최근에 읽어온 Index가 게시판별로 어디까지 인지 저장한는 파일이다.  IMPORTANT : 현재 이파일을 자동생성해 주는 기능이 없다. 이로 인해서 처음에는 직접 이 파일을 생성해야 한다. 만일 Wanted 게시판의 가장 최신 글이 419900 이라면 다음과 같이 작성하면 된다. 

`419900,Wanted`

이를 작성하지 않고 시작할 경우 어떻게 될지 보장할 수 없다. 	

**log_file_name** : log파일의 이름이다. 

**APNS_pem_name** : APNS 인증서의 이름이다. 

**receivers** : 알림을 받게 될 사람들의 목록이다. 예시와 같이 [(ID,(BOARDS),PUSH)]의 형태로 추가하면 된다. 
	
```
예시)

receivers = [
	('example1@example.org',('ToSysop','BuySell'),False),
	('example2@example.org',('ToSysop','BuySell','Wanted'),True),
	('example3@example.org',('BuySell','Wanted'),False),
	]
```
	
## Run

```./monitor {start|stop|restart}```
	

## Directory 구조 
**src** : 소스코드

**etc** : 설정파일 

**resources** : APNS pem 파일 및 receivers, board_index_file
	
## License 

Copyright 2014 Changje Jeong


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

