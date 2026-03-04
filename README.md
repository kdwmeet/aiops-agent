# AIOps Log Analyzer (서버 장애 예측 및 로그 분석기)

## 1. 프로젝트 개요

AIOps Log Analyzer는 방대한 서버 로그를 AI가 자동으로 분석하여 장애의 전조 증상을 탐지하고 근본 원인(Root Cause)을 규명하는 운영 자동화 도구입니다.

숙련된 엔지니어가 로그를 한 줄씩 분석하는 데 걸리는 시간을 획기적으로 단축시키며, 단순한 정규표현식(Regex) 기반 검색으로는 찾아내기 힘든 '맥락적 이상 징후(Contextual Anomaly)'를 파악합니다.

### 주요 기능
* **Semantic Log Parsing:** 비정형 로그 텍스트를 분석하여 '메모리 누수', 'DB 락(Lock)', '네트워크 지연' 등의 의미론적 패턴 도출.
* **Anomaly Detection:** 타임스탬프를 기반으로 시스템 성능 저하와 에러 발생 간의 인과관계 추적.
* **Root Cause Analysis (RCA):** 장애의 직접적인 원인(예: 특정 배포 버전, 특정 API 호출)을 추론.
* **Actionable Insight:** 롤백, 설정 변경, 핫픽스 등 즉시 실행 가능한 구체적인 해결책 제안.

## 2. 시스템 아키텍처

1.  **Log Ingestion:** 사용자가 `.log` 또는 `.txt` 포맷의 서버 로그 파일을 업로드.
2.  **Preprocessing:** 대용량 로그의 경우 분석 효율을 위해 핵심 구간(Tail) 추출 및 전처리.
3.  **LLM Inference:** **gpt-5-mini** 모델에 'SRE 엔지니어' 페르소나를 적용하여 로그 컨텍스트 분석.
4.  **Reporting:** 분석 결과를 심각도(Critical/Warning/Healthy)에 따라 분류하고 대시보드에 시각화.

## 3. 기술 스택

* **Language:** Python 3.10+
* **Package Manager:** uv
* **LLM:** OpenAI **gpt-5-mini**
* **Framework:** Streamlit
* **Log Processing:** Pandas (Optional)

## 4. 프로젝트 구조

```text
aiops-agent/
├── .env                  # API Key 설정
├── requirements.txt      # 의존성 패키지 목록
├── main.py               # 로그 업로드 및 분석 대시보드 UI
├── sample_logs/          # 테스트용 샘플 로그 파일
└── app/
    ├── __init__.py
    ├── config.py         # SRE 페르소나 및 분석 프롬프트
    └── analyzer.py       # 로그 파싱 및 이상 탐지 엔진
```

## 5. 설치 및 실행 가이드 (uv 기준)
### 5.1. 사전 준비
```Bash
git clone [레포지토리 주소]
cd aiops-agent
```
### 5.2. 환경 변수 설정
.env 파일에 API 키를 입력합니다.

```Ini, TOML
OPENAI_API_KEY=sk-your-api-key-here
```
### 5.3. 가상환경 및 패키지 설치
```Bash
uv venv
uv pip install -r requirements.txt
```
### 5.4. 실행
```Bash
uv run streamlit run main.py
```
## 6. 출력 데이터 예시
```JSON
{
  "status": "Critical",
  "summary": "배치 작업 실행 직후 메모리 사용량 급증으로 인한 OOM(Out of Memory) 발생",
  "root_cause": "heavy_image_processing 작업이 가용 메모리를 초과하여 OOM Killer 동작",
  "recommendation": "해당 배치 작업의 동시 처리량을 제한하거나 워커 노드의 메모리 증설 필요."
}
```
## 7. 실행 화면
<img width="1405" height="683" alt="스크린샷 2026-03-04 130614" src="https://github.com/user-attachments/assets/137ca3f5-5115-4bfa-a101-e7fdb4294ec0" />


## 8. 주의 사항
프로덕션 환경에서는 민감한 개인정보(PII)가 로그에 포함되지 않도록 마스킹(Masking) 처리가 선행되어야 합니다.

매우 큰 로그 파일(수 GB 이상)은 전체 분석 시 API 비용이 과다할 수 있으므로, 에러 발생 시점 전후의 로그만 추출하여 분석하는 것을 권장합니다.
