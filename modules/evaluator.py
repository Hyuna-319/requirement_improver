"""
점수 평가 로직
"""
from typing import Dict, List
from .ai_client import AIClient


class RequirementEvaluator:
    
    
    def __init__(self, ai_client: AIClient, scoring_prompt: str):

        self.ai_client = ai_client
        self.scoring_prompt = scoring_prompt
        
        # 규칙 목록 (64개)
        self.all_rules = [
            # Pattern Rules
            "P1", "P2", "P3", "P4", "P5", "P6", "P7",
            # Characteristics - Individual
            "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9",
            # Characteristics - Set
            "C10", "C11", "C12", "C13", "C14", "C15",
            # Writing Rules
            "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9",
            "R10", "R11",
            "R12", "R13", "R14", "R15", "R16", "R17",
            "R18", "R19", "R20", "R21", "R22", "R23",
            "R24", "R25",
            "R26",
            "R27", "R28",
            "R29", "R30",
            "R31",
            "R32",
            "R33",
            "R34", "R35",
            "R37", "R38", "R39", "R40",
            "R41", "R42"
        ]
    
    def evaluate(self, text: str) -> Dict:

        try:
            scores = self.ai_client.evaluate_requirement(
                scoring_prompt=self.scoring_prompt,
                text=text
            )
            return self._process_scores(scores)
        except Exception as e:
            # 오류 발생 시 기본 점수 반환
            return self._get_default_scores()
    
    def _process_scores(self, scores: Dict) -> Dict:
        """점수 처리 및 집계"""
        total_score = 0
        max_score = 0
        
        for rule in self.all_rules:
            if rule in scores:
                score = scores[rule].get('score', 0)
                if score > 0:  # N/A가 아닌 경우만
                    total_score += score
                    max_score += 5
        
        # 카테고리별 점수 계산
        categories = self._calculate_category_scores(scores)
        
        return {
            "total": total_score,
            "max": max_score if max_score > 0 else 320,
            "percentage": round((total_score / max_score * 100), 1) if max_score > 0 else 0,
            "scores": scores,
            "categories": categories
        }
    
    def _calculate_category_scores(self, scores: Dict) -> Dict:
   
        categories = {
            "패턴 규칙 (P1-P7)": {"rules": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"], "score": 0, "max": 35},
            "개별 특성 (C1-C9)": {"rules": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"], "score": 0, "max": 45},
            "집합 특성 (C10-C15)": {"rules": ["C10", "C11", "C12", "C13", "C14", "C15"], "score": 0, "max": 30},
            "정확성 (R1-R9)": {"rules": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9"], "score": 0, "max": 45},
            "기타 규칙": {"rules": [r for r in self.all_rules if r.startswith('R') and int(r[1:]) >= 10], "score": 0, "max": 165}
        }
        
        for cat_name, cat_data in categories.items():
            for rule in cat_data["rules"]:
                if rule in scores:
                    score = scores[rule].get('score', 0)
                    if score > 0:
                        cat_data["score"] += score
        
        return categories
    
    def _get_default_scores(self) -> Dict:
  
        return {
            "total": 0,
            "max": 320,
            "percentage": 0,
            "scores": {},
            "categories": {}
        }
    
    def compare_scores(self, original_scores: Dict, improved_scores: Dict) -> Dict:

        changes = {}
        
        for rule in self.all_rules:
            orig = original_scores.get("scores", {}).get(rule, {}).get("score", 0)
            impr = improved_scores.get("scores", {}).get(rule, {}).get("score", 0)
            
            if orig > 0 or impr > 0:  # N/A가 아닌 경우만
                changes[rule] = {
                    "original": orig,
                    "improved": impr,
                    "change": impr - orig
                }
        
        return {
            "original": original_scores,
            "improved": improved_scores,
            "changes": changes,
            "total_improvement": improved_scores.get("total", 0) - original_scores.get("total", 0)
        }