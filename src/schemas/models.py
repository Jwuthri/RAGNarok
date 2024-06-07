from typing import Optional, Literal
from pydantic import BaseModel


class ChatModel(BaseModel):
    name: str
    max_output: int
    context_size: int
    cost_prompt_token: float
    stop: Optional[str] = None
    cost_completion_token: float
    temperature: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0


class EmbeddingModel(BaseModel):
    context_size: int
    cost_token: float
    dimension: int
    metric: str
    name: str


class TTSModel(BaseModel):
    cost_char: float
    name: str
    voice: str = Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


class RerankModel(BaseModel):
    name: str
    cost_search: float


# ===== CHAT =====


class ChatCohereCommandR(ChatModel):
    name: str = "command-r"
    cost_prompt_token: float = 0.0000005
    cost_completion_token: float = 0.0000015
    context_size: int = 128_000
    max_output: int = 4096


class ChatCohereCommand(ChatModel):
    name: str = "command"
    cost_prompt_token: float = 0.0000005
    cost_completion_token: float = 0.0000015
    context_size: int = 4096
    max_output: int = 1024


class ChatCohereCommandLight(ChatModel):
    name: str = "command-light"
    cost_prompt_token: float = 0.0000003
    cost_completion_token: float = 0.0000006
    context_size: int = 4096
    max_output: int = 1024


class ChatCohereCommandNightly(ChatModel):
    name: str = "command-nightly"
    cost_prompt_token: float = 0.0000003
    cost_completion_token: float = 0.0000006
    context_size: int = 8192
    max_output: int = 1024


class ChatCohereCommandLightNightly(ChatModel):
    name: str = "command-light-nightly"
    cost_prompt_token: float = 0.0000003
    cost_completion_token: float = 0.000006
    context_size: int = 8192
    max_output: int = 1024


class ChatOpenaiGpt4Turbo(ChatModel):
    name: str = "gpt-4-turbo"
    cost_prompt_token: float = 0.00001
    cost_completion_token: float = 0.00003
    context_size: int = 128_000
    max_output: int = 4096


class ChatOpenaiGpt4o(ChatModel):
    name: str = "gpt-4o"
    cost_prompt_token: float = 0.00001
    cost_completion_token: float = 0.00003
    context_size: int = 128_000
    max_output: int = 4096


class ChatOpenaiGpt4(ChatModel):
    name: str = "gpt-4"
    cost_prompt_token: float = 0.00003
    cost_completion_token: float = 0.00006
    context_size: int = 8192
    max_output: int = 1024


class ChatOpenaiGpt35(ChatModel):
    name: str = "gpt-3.5-turbo"
    cost_prompt_token: float = 0.0000005
    cost_completion_token: float = 0.0000015
    context_size: int = 16_000
    max_output: int = 1024


class ChatAnthropicClaude21(ChatModel):
    name: str = "claude-2.1"
    cost_prompt_token: float = 0.000008
    cost_completion_token: float = 0.000024
    context_size: int = 200_000
    max_output: int = 1024


class ChatAnthropicClaude2(ChatModel):
    name: str = "claude-2"
    cost_prompt_token: float = 0.000008
    cost_completion_token: float = 0.000024
    context_size: int = 100_000
    max_output: int = 1024


class ChatAnthropicClaude12(ChatModel):
    name: str = "claude-instant-1.2"
    cost_prompt_token: float = 0.0000008
    cost_completion_token: float = 0.0000024
    context_size: int = 100_000
    max_output: int = 1024


class ChatAnthropicClaude3Opus(ChatModel):
    name: str = "claude-3-opus-20240229"
    cost_prompt_token: float = 0.000015
    cost_completion_token: float = 0.000075
    context_size: int = 200_000
    max_output: int = 4096


class ChatAnthropicClaude3Sonnet(ChatModel):
    name: str = "claude-3-sonnet-20240229"
    cost_prompt_token: float = 0.000003
    cost_completion_token: float = 0.000015
    context_size: int = 200_000
    max_output: int = 1024


class ChatAnthropicClaude3Haiku(ChatModel):
    name: str = "claude-3-haiku-20240307"
    cost_prompt_token: float = 0.00000025
    cost_completion_token: float = 0.0000015
    context_size: int = 200_000
    max_output: int = 1024


class ChatGoogleGeminiPro1(ChatModel):
    name: str = "gemini-pro"
    cost_prompt_token: float = 0.00000005
    cost_completion_token: float = 0.00000005
    context_size: int = 32_000
    max_output: int = 1024


class ChatGoogleGeminiPro15(ChatModel):
    name: str = "gemini-pro-1.5"
    cost_prompt_token: float = 0.00003
    cost_completion_token: float = 0.00009
    context_size: int = 128_000
    max_output: int = 4096


class ChatGoogleGeminiProVision1(ChatModel):
    name: str = "gemini-pro-vision"
    cost_prompt_token: float = 0.00000005
    cost_completion_token: float = 0.00000005
    context_size: int = 32_000
    max_output: int = 1024


# ===== EMBEDDING =====


class MSMarcoMiniLML6v2(EmbeddingModel):
    name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    cost_token: float = 0.0000001
    context_size: int = 512
    dimension: int = 384
    metric: str = "Sigmoid"


class MiniLML6v2(EmbeddingModel):
    name: str = "all-MiniLM-L6-v2"
    cost_token: float = 0.0000001
    context_size: int = 512
    dimension: int = 384
    metric: str = "Cosine"


class EmbeddingAnthropicVoyage2(EmbeddingModel):
    name: str = "voyage-2"
    cost_token: float = 0.00000002
    context_size: int = 4000
    dimension: int = 1024
    metric: str = "Cosine"


class EmbeddingAnthropicVoyageLarge2(EmbeddingModel):
    name: str = "voyage-large-2"
    cost_token: float = 0.00000002
    context_size: int = 16000
    dimension: int = 1536
    metric: str = "Cosine"


class EmbeddingAnthropicVoyageCode2(EmbeddingModel):
    name: str = "voyage-code-2"
    cost_token: float = 0.00000002
    context_size: int = 16000
    dimension: int = 1536
    metric: str = "Cosine"


class EmbeddingOpenaiSmall3(EmbeddingModel):
    name: str = "text-embedding-3-small"
    cost_token: float = 0.00000002
    context_size: int = 8191
    dimension: int = 1536
    metric: str = "Cosine"


class EmbeddingOpenaiLarge3(EmbeddingModel):
    name: str = "text-embedding-3-large"
    cost_token: float = 0.00000013
    context_size: int = 8191
    dimension: int = 3072
    metric: str = "Cosine"


class EmbeddingOpenaiAda2(EmbeddingModel):
    name: str = "text-embedding-ada-002"
    cost_token: float = 0.00000010
    context_size: int = 8191
    dimension: int = 1536
    metric: str = "Cosine"


class EmbeddingCohereEnglishV3(EmbeddingModel):
    name: str = "embed-english-v3.0"
    cost_token: float = 0.0000001
    context_size: int = 512
    dimension: int = 1024
    metric: str = "Cosine"


class EmbeddingCohereEnglishLightV3(EmbeddingModel):
    name: str = "embed-english-light-v3.0"
    cost_token: float = 0.0000001
    context_size: int = 512
    dimension: int = 384
    metric: str = "Cosine"


class EmbeddingCohereEnglishV2(EmbeddingModel):
    name: str = "embed-english-v2.0"
    cost_token: float = 0.0000001
    context_size: int = 512
    dimension: int = 4096
    metric: str = "Cosine"


class EmbeddingCohereEnglishLightV2(EmbeddingModel):
    name: str = "embed-english-light-v2.0"
    cost_token: float = 0.0000001
    context_size: int = 512
    dimension: int = 1024
    metric: str = "Cosine"


class EmbeddingCohereMultiV3(EmbeddingModel):
    name: str = "embed-multilingual-v3.0"
    cost_token: float = 0.0000001
    context_size: int = 512
    dimension: int = 1024
    metric: str = "Cosine"


class EmbeddingCohereMultiLightV3(EmbeddingModel):
    name: str = "embed-multilingual-light-v3.0"
    cost_token: float = 0.0000001
    context_size: int = 512
    dimension: int = 384
    metric: str = "Cosine"


class EmbeddingCohereMultiV2(EmbeddingModel):
    name: str = "embed-multilingual-v2.0"
    cost_token: float = 0.0000001
    context_size: int = 256
    dimension: int = 768
    metric: str = "Dot-Product"


# ===== RERANK =====


class RerankCohereMultiV2(RerankModel):
    name: str = "rerank-multilingual-v2.0"
    cost_search: float = 0.001


class RerankCohereEnglishV2(RerankModel):
    name: str = "rerank-english-v2.0"
    cost_search: float = 0.001


class RerankCohereMultiV3(RerankModel):
    name: str = "rerank-multilingual-v3.0"
    cost_search: float = 0.001


class RerankCohereEnglishV3(RerankModel):
    name: str = "rerank-english-v3.0"
    cost_search: float = 0.001


# ===== TTS =====


class TTSOpenai1(TTSModel):
    cost_char: float = 1.5e-5
    name: str = "tts-1"
    voice: str


class TTSOpenai1HD(TTSModel):
    cost_char: float = 3e-5
    name: str = "tts-1-hd"
    voice: str
