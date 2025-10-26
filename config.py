"""
설정 파일
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).parent

# 프롬프트 파일 경로
PROMPT_FILE = BASE_DIR / "prompts" / "Quality.md"

# AI 모델 설정
AI_MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 8000

# 기본값 설정
DEFAULT_SUBJECT = "Supplier"
DEFAULT_SYSTEM = "IRCU 시스템"
DEFAULT_RECEIVER = "HKMC"

# 점수 관련 설정
MAX_SCORE = 320  # 64개 규칙 × 5점
RULES_COUNT = {
    "P1-P7": 7,      # 패턴 규칙
    "C1-C9": 9,      # 개별 특성
    "C10-C15": 6,    # 집합 특성
    "R1-R9": 9,      # 정확성
    "R10-R11": 2,    # 간결성
    "R12-R17": 6,    # 비모호성
    "R18-R23": 6,    # 단일성
    "R24-R25": 2,    # 완전성
    "R26": 1,        # 현실성
    "R27-R28": 2,    # 조건
    "R29-R30": 2,    # 유일성
    "R31": 1,        # 추상화
    "R32": 1,        # 양화사
    "R33": 1,        # 허용오차
    "R34-R35": 2,    # 정량화
    "R37-R40": 4,    # 균일성
    "R41-R42": 2     # 모듈성
}


def get_api_key():
    """환경 변수에서 API 키 가져오기"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "환경 변수가 설정되지 않았습니다.\n"
            ".env 파일을 생성하거나 환경 변수를 설정해주세요."
        )
    return api_key