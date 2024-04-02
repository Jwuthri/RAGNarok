from pydantic import BaseModel


class ChatModel(BaseModel):
    name: str
    cost_prompt_token: float
    cost_completion_token: float
    context_size: int
    max_output: int
    temperature: float = 0.0
    stop: str = None
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class EmbeddingModel(BaseModel):
    name: str
    cost_token: float
    context_size: int
    dimension: int
    metric: str


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


# ===== EMBEDDING =====


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


class RerankCohereMulti(BaseModel):
    name: str = "rerank-multilingual-v2.0"
    cost_search: float = 0.001


class RerankCohereEnglish(BaseModel):
    name: str = "rerank-english-v2.0"
    cost_search: float = 0.001
