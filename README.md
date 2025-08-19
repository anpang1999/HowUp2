# HowUp 🚀

**어떻게(How) 스타트업(Start-up) 아이디어를 성장(Up)시키고 성공으로 이끌지 통찰을 제공하는 AI 챗봇 서비스**

---

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [사용 기술 및 데이터](#사용-기술-및-데이터)
- [프로젝트 구조](#프로젝트-구조)
- [환경 설정](#환경-설정)
- [설치 및 실행](#설치-및-실행)
- [사용 방법](#사용-방법)

---

## 프로젝트 개요

**HowUp**은 사용자가 제안한 소프트웨어 아이디어를 분석하고, 기존 특허 및 유사 서비스와의 차이점 및 상업성을 평가하여 창업 성공 가능성을 높이는 AI 기반 챗봇 서비스입니다.

### 주요 기능

1. **아이디어 분석**
   - 사용자가 입력한 소프트웨어 아이디어를 자연어 처리 기술로 분해 및 분석하여 주요 구성 요소를 도출.
2. **기존 특허 및 서비스 검색**
   - KIPRISPlus Open API 및 SERPER API를 사용하여 관련 특허 및 유사 서비스 정보를 검색하고 차별점 및 중복 가능성을 분석.
3. **산업 동향 및 사업성 평가**
   - DB의 시장 데이터 및 산업 현황을 분석하여 아이디어의 상업적 성공 가능성을 예측.
4. **차별화 전략 등 카운셀링**
   - 기술적 조언, 시장 진입 전략, 차별화 방안 등 사용자 맞춤형 창업 전략을 제시.

---

## 사용 기술 및 데이터

- **OpenAI API**
  - LLM 답변 생성 및 아이디어 분석.
- **FAISS (Facebook AI Similarity Search)**
  - 문서의 임베딩 벡터를 저장하고 유사도 검색을 수행하는 벡터 데이터베이스
  - 내장된 지식베이스에서 비즈니스 아이디어, 산업 동향, 시장 분석 정보 검색

### **외부 API 연동**

- **SERPER API**
  - 실시간 시장 동향, 최신 뉴스, 경쟁사 정보, 현재 트렌드 등 최신 정보 검색
- **KIPRISPlus Open API**
  - 특허, 실용신안, 디자인, 상표 등의 지식재산 데이터 연동
  - 기존 기술 조사 및 특허 침해 가능성 확인

### **사용자 인터페이스**

- **Streamlit**
  - 직관적이고 반응형 웹 인터페이스 제공
  - 실시간 AI 분석 결과 시각화

---

## 프로젝트 구조

```
HowUp2/
├── backend/                 # 백엔드 핵심 로직
│   ├── agent.py           # AI 에이전트 구현
│   ├── llm_model.py       # LLM 모델 관리
│   ├── react_prompt.py    # ReAct 프롬프트 템플릿
│   └── tools.py           # 도구 및 유틸리티
├── frontend/               # 프론트엔드 애플리케이션
│   ├── app.py             # Streamlit 메인 앱
│   ├── models/            # 데이터 모델
│   └── ui/                # 사용자 인터페이스 컴포넌트
├── processing/             # 데이터 처리 및 분석
│   ├── embeddings/        # 문서 임베딩 생성
│   ├── faiss_storage/     # FAISS 벡터 데이터베이스
│   ├── ragas_pipeline/    # RAG 시스템 성능 평가 파이프라인
│   └── run_all_RAG.py     # 전체 RAG 파이프라인 실행 스크립트
├── utils/                  # 유틸리티 함수
│   ├── cache_manager.py   # 캐시 관리
│   ├── fetch_patent_info.py # 특허 정보 조회
│   ├── google_serper.py   # SERPER API 연동
│   └── retriever_faiss.py # FAISS 검색기
├── db/                     # 데이터베이스 파일
├── pdfs/                   # PDF 문서 저장소
├── response_cache/         # 응답 캐시
└── vector_construction.ipynb # 벡터 구축
```

---

## 환경 설정

### 필요한 API 키

1. **OpenAI API Key**: [OpenAI Platform](https://platform.openai.com/)에서 발급
2. **SERPER API Key**: [Serper.dev](https://serper.dev/)에서 발급
3. **KIPRISPlus API Key**: [KIPRIS](https://www.kipris.or.kr/)에서 발급

### 시스템 요구사항

- Python 3.11.10
- 8GB RAM 이상
- 인터넷 연결

---

## 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/anpang1999/HowUp2.git
cd HowUp2
```

### 2. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 필요한 API 키를 설정하세요:

```env
# 필수 API 키
OPENAI_API_KEY=your_openai_api_key
KIPRIS_REST_KEY=your_kipris_api_key
SERPER_API_KEY=your_serper_api_key

# 선택사항 (LangChain 추적용)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=your_langchain_endpoint
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT=your_project_name
```

### 5. 애플리케이션 실행

```bash
streamlit run frontend/app.py
```

---

## 사용 방법

### 1. 웹 인터페이스 접속

브라우저에서 `http://localhost:8501`로 접속

### 2. 질문 입력 및 AI 분석

- **창업 아이디어 분석**: 소프트웨어 아이디어에 대한 구체적인 질문 입력
- **특허 검색**: 유사 특허 존재 여부 및 특허 번호 확인
- **경쟁사 분석**: 기존 서비스 운영 현황 및 시장 상황 파악
- **시장 전망**: 타겟 시장 및 사업 전망에 대한 인사이트 요청
- **차별화 전략**: 경쟁 앱과의 차별화 방안 구조화된 분석 요청

### 3. AI의 지능형 도구 활용

HowUp은 사용자 질문에 따라 **자동으로 적절한 도구를 선택**하여 답변합니다:

- **내장 지식베이스 검색**: FAISS를 통한 비즈니스 통찰 및 창업 전략 정보
- **실시간 인터넷 검색**: SERPER API를 통한 최신 시장 동향 및 경쟁사 정보
- **특허 정보 검색**: KIPRISPlus API를 통한 기존 기술 조사 및 특허 분석

### 사용 예시

#### **예시 1: 특허 검색**

```
사용자: "개인 맞춤형 운동 루틴을 추천하는 앱에 대한 유사특허가 있다면
       특허 번호를 포함해서 알려주세요."

AI 응답: 특허 번호 1020250034335 등 유사 특허 정보 제공
```

#### **예시 2: 경쟁사 분석**

```
사용자: "오늘 기준으로 이와 비슷한 기존 서비스가 운영되고 있는지,
       검색해서 자세히 알려주세요."

AI 응답: 플랜핏, Hevy, Nike Training Club 등 경쟁 앱 상세 분석
```

#### **예시 3: 시장 전망**

```
사용자: "개인화 운동 추천 앱이 타겟으로 하는 주요 시장은 어디인지
       사업 전망에 대한 인사이트를 주세요."

AI 응답: 타겟 시장 분석 및 AI/웨어러블 기술 발전에 따른 성장 전망 제시
```

#### **예시 4: 차별화 전략**

```
사용자: "경쟁 앱과 차별화하기 위한 중요한 전략은 무엇일지
       구조화된 분석을 해주세요."

AI 응답: 사용자 경험, AI 기반 맞춤형 추천, 커뮤니티 기능,
        웨어러블 연동성 등 차별화 전략 구조화
```

---

## 문의 및 지원

- **이슈 리포트**: [GitHub Issues](https://github.com/anpang1999/HowUp2/issues)
- **이메일**: nbhdqxt@gmail.com
- **프로젝트 홈페이지**: [HowUp2](https://github.com/anpang1999/HowUp2)
