"""
요구사항 개선 로직
"""
from typing import Dict, List
from .ai_client import AIClient


class RequirementImprover:
 
    
    def __init__(self, ai_client: AIClient, quality_prompt: str):

        self.ai_client = ai_client
        self.quality_prompt = quality_prompt
    
    def improve(
        self,
        original_text: str,
        subject: str,
        system: str,
        receiver: str
    ) -> Dict:

        # AI에게 요구사항 개선 요청
        improved_text = self.ai_client.improve_requirement(
            quality_prompt=self.quality_prompt,
            original_text=original_text,
            subject=subject,
            system=system,
            receiver=receiver
        )
        
        return {
            "original": original_text,
            "improved": improved_text,
            "subject": subject,
            "system": system,
            "receiver": receiver
        }
    
    def parse_improved_requirements(self, improved_text: str) -> List[Dict]:

        requirements = []
        
        # "요구사항 1:", "요구사항 2:" 등으로 분리
        lines = improved_text.split('\n')
        current_req = None
        
        for line in lines:
            if line.strip().startswith('요구사항'):
                if current_req:
                    requirements.append(current_req)
                current_req = {
                    'number': len(requirements) + 1,
                    'text': '',
                    'pattern': 'Ubiquitous'  # 기본값
                }
            elif current_req and line.strip():
                current_req['text'] += line.strip() + ' '
        
        if current_req:
            requirements.append(current_req)
        
        return requirements