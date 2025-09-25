"""
Quick AI Fix
This creates a simple AI integration that works immediately
"""
import os
import requests
import json
from typing import Dict, Any, Tuple

class QuickAI:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        
    def generate_text(self, prompt: str, content_type: str = "general", 
                     tone: str = "professional", length: str = "medium") -> Tuple[bool, Any]:
        """Generate text using OpenAI GPT-4o-mini"""
        if not self.api_key:
            return False, {"error": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."}
        
        try:
            # Build system prompt
            system_prompt = f"You are a professional content writer. Create {content_type} content with a {tone} tone. Keep it {length} length."
            
            # Prepare request data
            request_data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result['choices'][0]['message']['content']
                
                return True, {
                    "output_text": generated_text,
                    "model": "gpt-4o-mini"
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
                return False, {"error": error_msg}
                
        except Exception as e:
            return False, {"error": f"Error: {str(e)}"}
    
    def generate_image(self, prompt: str, style: str = "photorealistic", 
                      size: str = "1024x1024", quality: str = "standard") -> Tuple[bool, Any]:
        """Generate image using OpenAI DALL-E"""
        if not self.api_key:
            return False, {"error": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."}
        
        try:
            # Enhance prompt with style
            enhanced_prompt = f"{prompt}, {style} style, high quality"
            
            # Prepare request data
            request_data = {
                "model": "dall-e-3",
                "prompt": enhanced_prompt,
                "n": 1,
                "size": size,
                "quality": quality if quality == "hd" else "standard",
                "response_format": "url"
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=request_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                
                return True, {
                    "image_url": image_url,
                    "model": "dall-e-3"
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', {}).get('message', f"HTTP {response.status_code}")
                return False, {"error": error_msg}
                
        except Exception as e:
            return False, {"error": f"Error: {str(e)}"}

# Global instance
quick_ai = QuickAI()

def test_quick_ai():
    """Test the quick AI service"""
    print("🧪 Testing Quick AI Service...")
    
    # Test text generation
    print("Testing text generation...")
    success, result = quick_ai.generate_text("Write a short product description for wireless headphones")
    if success:
        print(f"✅ Text generated: {result['output_text'][:100]}...")
    else:
        print(f"❌ Text generation failed: {result.get('error', 'Unknown error')}")
    
    # Test image generation
    print("Testing image generation...")
    success, result = quick_ai.generate_image("A beautiful sunset over the ocean")
    if success:
        print(f"✅ Image generated: {result['image_url'][:50]}...")
    else:
        print(f"❌ Image generation failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    test_quick_ai()
