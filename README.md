ARA Monitoring Tool

Author : Changje Jeong<rodumani@sparcs.org>
Version : 1.0 

1.Introduction 
	ARA Monitoring Tool 은 ARA의 게시판을 Crawling 하여, Mail 혹은 APNS로 알림을 주는 도구이다. 
	자체적으로 Threading을 하여 Daemonize 되어 작동하므로, cron을 이용하지 않아도 된다. 

2.Package Dependancies:
	pyapns 
	BeautifulSoap

3.Initialization 
	처음 이 프로그램을 실행시키기 위해 설정해야할 값들이 settings.py 에 모두 있다. 

	DEBUG : Debug모드를 사용할 것인지 결정한다. Debug모드를 사용하면 log가 모두 화면에 출력되고 log보다 자세한 내용들을 담고 있다.  

	period : 크롤링을 할 주기이다. 기본은 60초 이다. 
	
	boardnames : 크롤링할 보드의 이름들을 적어준다. 되도록 구독하지 않는 보드의 이름은 추가하지 않는 것이 크롤러의 성능과 아라서버의 부하를 줄인다. 
	
	ara_id : 크롤링을 위해 아라에 접속할 ID 이다. 
	gmail_user : 메일을 보내기 위한 SMTP로 GMail 의 SMTP를 사용하고 있으므로, Gmail계정이 필요하다. 
	
	password_file_name : 앞서 적은 ara_id에 대응하는 Password를 적어놓은 파일의 경로이다. 다른 사람이 읽지 못하도록하기 위해서 파일을 분리하였다. 
	index_file_name : 일종의 DB처럼 사용되는 가장 최근에 읽어온 Index가 게시판별로 어디까지 인지 저장한는 파일이다.  IMPORTANT : 현재 이파일을 자동생성해 주는 기능이 없다. 이로 인해서 처음에는 직접 이 파일을 생성해야 한다. 만일 Wanted 게시판의 가장 최신 글이 419900 이라면 다음과 같이 작성하면 된다. 

		419900,Wanted 

	이를 작성하지 않고 시작할 경우 어떻게 될지 보장할 수 없다. 	
	
	gmail_password_file_name : 앞서 적은 gmail_user에 대응하는 Password를 적어놓은 파일의 경로이다. 역시나 다른 사람들이 읽지 못하도록 하기 위해서 파일을 분리하였다. $ chown 600 명령을 통해 반듯이 자신만 읽을 수 있도록 하기 바란다. 
	log_file_name : log파일의 경로이다. 
	
	APNS_pem_name : APNS 인증서의 경로이다. 

	tokens : Push알림을 받게될 iOS APNS token들의 Dictionary이다. Mail Receiver의 ID를 Key로 하여 APNS Token을 Value로 적으면 된다. 

	receivers : 알림을 받게 될 사람들의 목록이다. 예시와 같이 [(ID,(BOARDS),PUSH)]의 형태로 추가하면 된다. 
		예시) 
		receivers = [
				('changjej@gmail.com',('ToSysop','BuySell','Wanted'),True),
				('zzongaly@sparcs.org',('ToSysop','BuySell'),False),
				('apple@sparcs.org',('BuySell','Wanted'),False),
					]

4. License 
	딱히 생각이 없다. 

