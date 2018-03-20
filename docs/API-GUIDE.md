
# API

## JWT auth token

Post username and password to api/auth/token/ to get the token.

```bash
curl -X POST -d "username=your-username&password=your-pass" https://amfoss.in/api/auth/token/
```

Response is a json object with a token valid for 300 seconds. Use this token to 
make all requests to the server.

```json
{"token":"your_token"}
```

## Status update

Make a request to api/status-report/yyyy-mm-dd/ with your token to get the 
status-report.

```bash
curl -H "Authorization: JWT <your_token>" https://amfoss.in/api/status-report/2018-03-19/
```
