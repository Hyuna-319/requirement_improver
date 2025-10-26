"""
AI API 클라이언트
"""
import anthropic
from pathlib import Path
from typing import Dict, Any
import json


class AIClient:
    
    
    def __init__(self, api_key: str, model: str, max_tokens: int):
        """
        Args:
            api_key: Anthropic API 키
            model: 사용할 모델 이름
            max_tokens: 최대 토큰 수
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        
    def load_prompt(self, file_path: Path) -> str:
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def call_api(self, system_prompt: str, user_message: str) -> str:

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": user_message
                }]
            )
            return message.content[0].text
        except Exception as e:
            raise Exception(f"AI API 호출 실패: {str(e)}")
    
    def improve_requirement(
        self,
        quality_prompt: str,
        original_text: str,
        subject: str,
        system: str,
        receiver: str
    ) -> str:

        user_message = f
        
        return self.call_api(quality_prompt, user_message)
    
    def evaluate_requirement(
        self,
        scoring_prompt: str,
        text: str
    ) -> Dict[str, Any]:

        user_message = f
        
        full_prompt = scoring_prompt + "\n\n" + user_message
        response = self.call_api(scoring_prompt, user_message)
        
        
        try:
            
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("JSON 형식을 찾을 수 없습니다")
        except Exception as e:
            raise Exception(f"점수 평가 결과 파싱 실패: {str(e)}\n응답: {response}")