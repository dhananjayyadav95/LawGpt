"""
AI Provider Abstraction Layer
Supports multiple AI providers: OpenAI, Anthropic, Google Gemini, Emergent LLM
"""

import os
import asyncio
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AIProvider:
    """Base class for AI providers"""
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.model = model
    
    async def generate_response(self, system_message: str, user_message: str) -> str:
        """Generate AI response - to be implemented by subclasses"""
        raise NotImplementedError

class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    async def generate_response(self, system_message: str, user_message: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=4000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

class AnthropicProvider(AIProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        super().__init__(api_key, model)
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
    
    async def generate_response(self, system_message: str, user_message: str) -> str:
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                system=system_message,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

class GoogleGeminiProvider(AIProvider):
    """Google Gemini provider"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        super().__init__(api_key, model)
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model_instance = genai.GenerativeModel(model)
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
    
    async def generate_response(self, system_message: str, user_message: str) -> str:
        try:
            # Combine system and user messages for Gemini
            combined_prompt = f"{system_message}\n\nUser Query: {user_message}"
            
            # Run in thread pool since Gemini doesn't have async support
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                self.model_instance.generate_content, 
                combined_prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            raise

class EmergentLLMProvider(AIProvider):
    """Emergent LLM provider (optional)"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-pro"):
        super().__init__(api_key, model)
        try:
            from emergentintegrations.llm.chat import LlmChat, UserMessage
            self.LlmChat = LlmChat
            self.UserMessage = UserMessage
        except ImportError:
            raise ImportError(
                "Emergent integrations package not installed. "
                "Install with: pip install emergentintegrations"
            )
    
    async def generate_response(self, system_message: str, user_message: str) -> str:
        try:
            chat = self.LlmChat(
                api_key=self.api_key,
                session_id=f"session-{hash(user_message) % 10000}",
                system_message=system_message
            ).with_model("gemini", self.model)
            
            user_msg = self.UserMessage(text=user_message)
            response = await chat.send_message(user_msg)
            return str(response)
        except Exception as e:
            logger.error(f"Emergent LLM API error: {e}")
            raise

class AIProviderFactory:
    """Factory to create AI providers based on configuration"""
    
    @staticmethod
    def create_provider(provider_type: str, api_key: str, model: Optional[str] = None) -> AIProvider:
        """Create AI provider instance"""
        
        provider_type = provider_type.lower()
        
        if provider_type == "openai":
            default_model = "gpt-3.5-turbo" if not model else model
            return OpenAIProvider(api_key, default_model)
        
        elif provider_type == "anthropic":
            default_model = "claude-3-sonnet-20240229" if not model else model
            return AnthropicProvider(api_key, default_model)
        
        elif provider_type == "google" or provider_type == "gemini":
            default_model = "gemini-pro" if not model else model
            return GoogleGeminiProvider(api_key, default_model)
        
        elif provider_type == "emergent":
            try:
                default_model = "gemini-2.5-pro" if not model else model
                return EmergentLLMProvider(api_key, default_model)
            except ImportError as e:
                raise ImportError(
                    f"Emergent LLM provider requires emergentintegrations package. "
                    f"Install with: pip install emergentintegrations, or use another provider like 'openai'"
                )
        
        else:
            raise ValueError(f"Unsupported AI provider: {provider_type}. Choose from: openai, anthropic, google, emergent")

def get_ai_provider() -> AIProvider:
    """Get configured AI provider from environment variables"""
    
    # Check environment variables for AI configuration
    ai_provider = os.environ.get('AI_PROVIDER', 'openai').lower()
    ai_model = os.environ.get('AI_MODEL', None)
    
    # Try different API key environment variables
    api_key = None
    
    if ai_provider == "openai":
        api_key = os.environ.get('OPENAI_API_KEY') or os.environ.get('AI_API_KEY')
    elif ai_provider == "anthropic":
        api_key = os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('AI_API_KEY')
    elif ai_provider in ["google", "gemini"]:
        api_key = os.environ.get('GOOGLE_API_KEY') or os.environ.get('AI_API_KEY')
    elif ai_provider == "emergent":
        api_key = os.environ.get('EMERGENT_LLM_KEY') or os.environ.get('AI_API_KEY')
    
    if not api_key:
        # Fallback to generic API key
        api_key = os.environ.get('AI_API_KEY')
    
    if not api_key or 'your_' in api_key.lower():
        raise ValueError(f"No valid API key found for {ai_provider}. Please set a real API key in backend/.env file.")
    
    try:
        provider = AIProviderFactory.create_provider(ai_provider, api_key, ai_model)
        logger.info(f"Using AI provider: {ai_provider} with model: {provider.model}")
        return provider
    except Exception as e:
        logger.error(f"Failed to create AI provider {ai_provider}: {e}")
        # Fallback to OpenAI if available
        openai_key = os.environ.get('OPENAI_API_KEY')
        if ai_provider != "openai" and openai_key and 'your_' not in openai_key.lower():
            logger.info("Falling back to OpenAI provider")
            return OpenAIProvider(openai_key, "gpt-3.5-turbo")
        raise

# Convenience function for backward compatibility
async def generate_ai_response(system_message: str, user_message: str) -> str:
    """Generate AI response using configured provider"""
    provider = get_ai_provider()
    return await provider.generate_response(system_message, user_message)