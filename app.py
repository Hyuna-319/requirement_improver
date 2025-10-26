"""
요구사항 개선 도구 - Streamlit App
INCOSE 표준 기반 자동 요구사항 품질 향상 시스템
"""
import streamlit as st
import json
from pathlib import Path
from modules import AIClient, RequirementImprover, RequirementEvaluator
import config

# 페이지 설정
st.set_page_config(
    page_title="요구사항 개선",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 메인 컨텐츠 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* 섹션 스타일 */
    .stMarkdown {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 3rem;
        font-size: 16px;
        font-weight: 600;
        width: auto;
        margin: 0 auto;
        display: block;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 입력 필드 */
    .stTextInput input, .stTextArea textarea {
        border: 2px solid #e0e0e0;
        border-radius: 5px;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #667eea;
    }
    
    /* 헤더 */
    h1 {
        color: white;
        text-align: center;
        padding: 2rem;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* 섹션 타이틀 */
    h2 {
        color: #333;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# API 키 저장 경로
CONFIG_DIR = Path.home() / ".requirement_improver"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_api_key():
    """저장된 API 키 불러오기"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
                return config_data.get('api_key', '')
        except:
            return ''
    return ''

def save_api_key(api_key):
    """API 키 저장"""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'api_key': api_key}, f)

def delete_api_key():
    """API 키 삭제"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()

# 세션 스테이트 초기화
if 'api_key' not in st.session_state:
    st.session_state.api_key = load_api_key()

if 'improved_result' not in st.session_state:
    st.session_state.improved_result = None

if 'original_scores' not in st.session_state:
    st.session_state.original_scores = None

if 'improved_scores' not in st.session_state:
    st.session_state.improved_scores = None

# 헤더
st.markdown("# 🔧 요구사항 개선 도구")
st.markdown("""
<div style='text-align: center; color: white; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
     padding: 1rem; border-radius: 10px; margin-bottom: 2rem;'>
    INCOSE 표준 기반 자동 요구사항 품질 향상 시스템
</div>
""", unsafe_allow_html=True)

# 1. API 설정 섹션
st.markdown("## 🔑 API 설정")

col1, col2 = st.columns([3, 1])

with col1:
    api_key_input = st.text_input(
        "Anthropic API 키",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-api03-xxxxx...",
        help="API 키가 저장됩니다."
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_save, col_delete = st.columns(2)
    
    with col_save:
        if st.button("저장"):
            if api_key_input:
                save_api_key(api_key_input)
                st.session_state.api_key = api_key_input
                st.success("API 키가 저장되었습니다!")
            else:
                st.error("API 키를 입력해주세요")
    
    with col_delete:
        if st.button("삭제"):
            delete_api_key()
            st.session_state.api_key = ''
            st.info("API 키가 삭제되었습니다")
            st.rerun()

# API 키 상태 표시
if st.session_state.api_key:
    st.success("저장된 API 키가 로드되었습니다")
else:
    st.info("API 키를 입력하고 저장해주세요")

st.markdown("---")

# 2. 프로젝트 설정 섹션
st.markdown("## ⚙️ 프로젝트 설정")

st.info("💡 **안내:** 원본 요구사항에 주체, 대상 시스템, 수신자가 누락된 경우 아래 설정값이 자동으로 적용됩니다.")

col1, col2, col3 = st.columns(3)

with col1:
    subject = st.text_input(
        "시스템 주체",
        value=config.DEFAULT_SUBJECT,
        help="요구사항을 수행하는 주체"
    )

with col2:
    system = st.text_input(
        "대상 시스템",
        value=config.DEFAULT_SYSTEM,
        help="요구사항이 적용되는 시스템"
    )

with col3:
    receiver = st.text_input(
        "수신자/협의 대상",
        value=config.DEFAULT_RECEIVER,
        help="문서 제출처 또는 협의 상대"
    )

st.markdown("---")

# 3. 요구사항 입력 섹션
st.markdown("## 📝 요구사항 입력")

requirement_text = st.text_area(
    "개선할 요구사항 텍스트",
    height=150,
    placeholder="예: CANFD 통신 표준 사양을 만족해야 한다.",
    help="개선할 요구사항을 입력하세요"
)

# 개선하기 버튼
if st.button("✨ 요구사항 개선하기", disabled=(not st.session_state.api_key or not requirement_text)):
    if not st.session_state.api_key:
        st.error("API 키를 먼저 설정해주세요")
    elif not requirement_text:
        st.error("요구사항을 입력해주세요")
    else:
        with st.spinner("🔄 요구사항을 분석하고 개선하는 중입니다..."):
            try:
                # AI 클라이언트 초기화
                ai_client = AIClient(
                    api_key=st.session_state.api_key,
                    model=config.AI_MODEL,
                    max_tokens=config.MAX_TOKENS
                )
                
                # 프롬프트 로드
                quality_prompt = ai_client.load_prompt(config.PROMPT_FILE)
                scoring_prompt_file = config.SCORING_PROMPT_FILE
                scoring_prompt = ai_client.load_prompt(scoring_prompt_file)
                
                # 개선기 및 평가기 초기화
                improver = RequirementImprover(ai_client, quality_prompt)
                evaluator = RequirementEvaluator(ai_client, scoring_prompt)
                
                # 1. 원본 평가
                st.session_state.original_scores = evaluator.evaluate(requirement_text)
                
                # 2. 요구사항 개선
                improved_result = improver.improve(
                    original_text=requirement_text,
                    subject=subject,
                    system=system,
                    receiver=receiver
                )
                st.session_state.improved_result = improved_result
                
                # 3. 개선된 요구사항 평가
                st.session_state.improved_scores = evaluator.evaluate(improved_result['improved'])
                
                st.success("개선 완료!")
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
                st.info("API 키가 올바른지, 인터넷 연결이 정상인지 확인해주세요.")

st.markdown("---")

# 4. 품질 점수 비교 (결과가 있을 때만 표시)
if st.session_state.original_scores and st.session_state.improved_scores:
    st.markdown("## 📊 품질 점수 비교")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📉 원본 요구사항")
        
        orig = st.session_state.original_scores
        st.metric(
            "총점",
            f"{orig['total']} / {orig['max']}",
            delta=None
        )
        st.metric(
            "만족률",
            f"{orig['percentage']}%",
            delta=None
        )
        
        # 카테고리별 점수
        if 'categories' in orig and orig['categories']:
            st.markdown("**카테고리별 점수**")
            for cat_name, cat_data in orig['categories'].items():
                score = cat_data['score']
                max_score = cat_data['max']
                percentage = round((score / max_score * 100), 1) if max_score > 0 else 0
                st.text(f"{cat_name}: {score}/{max_score} ({percentage}%)")
                st.progress(percentage / 100)
    
    with col2:
        st.markdown("### 📈 개선된 요구사항")
        
        impr = st.session_state.improved_scores
        delta = impr['total'] - orig['total']
        delta_pct = impr['percentage'] - orig['percentage']
        
        st.metric(
            "총점",
            f"{impr['total']} / {impr['max']}",
            delta=f"+{delta}점"
        )
        st.metric(
            "만족률",
            f"{impr['percentage']}%",
            delta=f"+{delta_pct:.1f}%"
        )
        
        # 카테고리별 점수
        if 'categories' in impr and impr['categories']:
            st.markdown("**카테고리별 점수**")
            for cat_name, cat_data in impr['categories'].items():
                score = cat_data['score']
                max_score = cat_data['max']
                percentage = round((score / max_score * 100), 1) if max_score > 0 else 0
                st.text(f"{cat_name}: {score}/{max_score} ({percentage}%)")
                st.progress(percentage / 100)
    
    st.markdown("---")
    
    # 5. 상세 점수 비교
    st.markdown("## 📋 상세 점수 비교")
    
    # 점수 변화 테이블
    evaluator = RequirementEvaluator(None, "")
    comparison = evaluator.compare_scores(orig, impr)
    
    if comparison['changes']:
        # 데이터프레임으로 표시
        import pandas as pd
        
        data = []
        for rule, change_data in comparison['changes'].items():
            # 규칙 이름 매핑 (간단히)
            rule_names = {
                "P1": "Subject (주어)",
                "P2": "Modal Verb (의무형 동사)",
                "P3": "Action (행동)",
                "P4": "Object (객체)",
                "P5": "Performance Measure (성능 측정)",
                "C5": "Singular (단일성)",
                "R7": "Vague Terms (모호한 용어)",
                # ... 나머지는 기본으로
            }
            
            rule_name = rule_names.get(rule, rule)
            
            data.append({
                "규칙": f"{rule} - {rule_name}",
                "원본": change_data['original'],
                "개선": change_data['improved'],
                "변화": f"+{change_data['change']}" if change_data['change'] > 0 else str(change_data['change'])
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # 6. 개선된 요구사항
    st.markdown("## ✅ 개선된 요구사항")
    
    if st.session_state.improved_result:
        improved_text = st.session_state.improved_result['improved']
        
        # 간단한 파싱으로 요구사항 표시
        st.markdown("### 개선된 텍스트")
        st.text_area(
            "개선 결과",
            value=improved_text,
            height=200,
            disabled=True
        )
        
        # 주요 개선 사항
        st.markdown("### 🎯 주요 개선 사항")
        
        improvements = []
        if delta > 0:
            improvements.append(f"✓ **총점 향상**: {orig['total']}점 → {impr['total']}점 (+{delta}점)")
            improvements.append(f"✓ **만족률 향상**: {orig['percentage']}% → {impr['percentage']}% (+{delta_pct:.1f}%)")
        
        # 가장 많이 개선된 규칙 찾기
        if comparison['changes']:
            top_improvements = sorted(
                comparison['changes'].items(),
                key=lambda x: x[1]['change'],
                reverse=True
            )[:3]
            
            for rule, change_data in top_improvements:
                if change_data['change'] > 0:
                    improvements.append(f"✓ **{rule} 개선**: {change_data['original']}점 → {change_data['improved']}점 (+{change_data['change']}점)")
        
        for improvement in improvements:
            st.markdown(improvement)
        
        # 다운로드 버튼
        st.download_button(
            label="📥 개선된 요구사항 다운로드",
            data=improved_text,
            file_name="improved_requirement.txt",
            mime="text/plain"
        )