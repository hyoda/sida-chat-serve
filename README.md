# chatbot


## 필요사항
### 환경변수 셋팅
.streamlit 폴더 내 secrets.toml 파일에 "pass" 키(openai.api_key 에 할당할 OPEN AI API KEY)를 셋팅하고 테스트 하시면 됩니다.
### 패키지 인스톨
```
pip install -r requirements.txt
```

### 실행
```
streamlit run sida-chat-with-st-chat-message.py
```

### 이슈 

#### 23년 8월 17일 기준
- 스트림릿에서 제공하는 chat_input 엘리먼트에서 한글 등 다국어 입력시. 마침표 등의 등호를 포함시키지 않으면 온전한 문장이 프롬프트로 전달되지 않는 이슈가 있음.
  1.26.0 버전에서 해결될 것으로 예상되나, 현재까지 릴리즈 되지 않은 상태임.
  
