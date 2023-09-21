### I. react-client
```bash
$ cd react-client
$ npm run dev
```

### II. fastapi-server
```bash
$ cd fastapi-server
$ uvicorn main:app --host 0.0.0.0 --realod 
```

### III. (참고) .env
```bash
- COGNITO_REGION : cognito 생성 리전
- COGNITO_USER_POOL_ID : AWS > Cognito > 사용자 풀 > 사용자 풀 개요 > 사용자 풀 ID
- COGNITO_ENDPOINT : AWS > Cognito > 사용자 풀 > 앱 통합 > Cognito 도메인
- COGNITO_CLIENT_ID : AWS > Cognito > 사용자 풀 > 앱 통합 > 앱 클라이언트 목록 > 클라이언트 ID
- AWS_ACCESS_KEY_ID='put your access key' # fastapi-server/.env
- AWS_SECRET_ACCESS_KEY='put your secret access key' # fastapi-server/.env
```
