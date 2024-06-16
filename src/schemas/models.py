from typing import Optional, Literal
from pydantic import BaseModel

from rich.table import Table


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


class STTModel(BaseModel):
    cost_char: float
    name: str


# ===== CHAT =====


class ChatCohereCommandRPlus(ChatModel):
    name: str = "command-r-plus"
    cost_prompt_token: float = 0.0000005
    cost_completion_token: float = 0.0000015
    context_size: int = 128_000
    max_output: int = 4096


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


# ----- #

anthropic_table = Table(show_header=True, header_style="bold magenta")
anthropic_table.add_column("Model Name", justify="left")
anthropic_table.add_column("Description", justify="left")
anthropic_table.add_column("Context Length", justify="right")
anthropic_table.add_column("Rate Limit", justify="left")
anthropic_table.add_column("Pricing for 1 Million Tokens", justify="left")

anthropic_table.add_row(
    "Claude 3 Opus", "Most powerful model for highly complex tasks", "200_000 tokens", "N/A", "$15.00 / $75.00"
)
anthropic_table.add_row(
    "Claude 3 Sonnet",
    "Ideal balance of intelligence and speed for enterprise workloads",
    "200_000 tokens",
    "N/A",
    "$3.00 / $15.00",
)
anthropic_table.add_row(
    "Claude 3 Haiku",
    "Fastest and most compact model for near-instant responsiveness",
    "200_000 tokens",
    "N/A",
    "$0.25 / $1.25",
)
anthropic_table.add_row(
    "Claude 2.1", "Updated version of Claude 2 with improved accuracy", "128_000 tokens", "N/A", "$8.00 / $24.00"
)
anthropic_table.add_row(
    "Claude 2",
    "Predecessor to Claude 3, offering strong all-round performance",
    "128_000 tokens",
    "N/A",
    "$8.00 / $24.00",
)
anthropic_table.add_row(
    "Claude Instant 1.2",
    "Our cheapest small and fast model, a predecessor of Claude Haiku.",
    "128_000 tokens",
    "N/A",
    "$0.80 / $2.40",
)

# ----- #

cohere_table = Table(show_header=True, header_style="bold magenta")
cohere_table.add_column("Model Name", justify="left")
cohere_table.add_column("Description", justify="left")
cohere_table.add_column("Context Length", justify="right")
cohere_table.add_column("Rate Limit", justify="left")
cohere_table.add_column("Pricing for 1 Million Tokens", justify="left")

cohere_table.add_row(
    "command",
    "An instruction-following conversational model that performs language tasks with high quality, more reliably and with a longer context than our base gen",
    "4096 tokens",
    "N/A",
    "$0.50 / $1.50",
)
cohere_table.add_row(
    "command-light",
    "A smaller, faster version of command. Almost as capable, but a lot faster.",
    "4096 tokens",
    "N/A",
    "$0.50 / $1.50",
)
cohere_table.add_row(
    "command-nightly",
    "To reduce the time between major releases, we put out nightly versions of command models. For command, that is command-nightly.",
    "128_000 tokens",
    "N/A",
    "$0.50 / $1.50",
)
cohere_table.add_row(
    "command-light-nightly",
    "To reduce the time between major releases, we put out nightly versions of command models. For command-light, that is command-light-nightly.",
    "128_000 tokens",
    "N/A",
    "$0.50 / $1.50",
)
cohere_table.add_row(
    "command-r",
    "Command R is an instruction-following conversational model that performs language tasks at a higher quality, more reliably,",
    "128_000 tokens",
    "N/A",
    "$0.50 / $1.50",
)
cohere_table.add_row(
    "command-r+",
    "Command R is an instruction-following conversational model that performs language tasks at a higher quality, more reliably,",
    "128_000 tokens",
    "N/A",
    "$3.00 / $15.00",
)

# ----- #

google_table = Table(show_header=True, header_style="bold magenta")
google_table.add_column("Model Name", justify="left")
google_table.add_column("Description", justify="left")
google_table.add_column("Context Length", justify="right")
google_table.add_column("Rate Limit", justify="left")
google_table.add_column("Pricing for 1 Million Tokens", justify="left")

google_table.add_row(
    "Gemini-Pro 1.0", "Gemini-Pro model", "100_000", "360 RPM, 120,000 TPM, 30,000 RPD", "$0.50 / $1.50"
)
google_table.add_row(
    "Gemini-Pro Vision 1.0", "Gemini-Pro Vision model", "100_000", "360 RPM, 120,000 TPM, 30,000 RPD", "$0.50 / $1.50"
)
google_table.add_row(
    "Gemini-Pro 1.5", "Gemini-Pro 1.5 model", "1_000_0000", "5 RPM, 10 million TPM, 2,000 RPD", "$7 / $21"
)

# ----- #

openai_table = Table(show_header=True, header_style="bold magenta")
openai_table.add_column("Model Name", justify="left")
openai_table.add_column("Description", justify="left")
openai_table.add_column("Context Length", justify="right")
openai_table.add_column("Rate Limit", justify="left")
openai_table.add_column("Pricing for 1 Million Tokens", justify="left")

openai_table.add_row(
    "gpt-4-0125-preview", "New GPT-4 Turbo intended to reduce 'laziness'.", "128,000 tokens", "N/A", "$10.00 / $30.00"
)
openai_table.add_row("gpt-4-turbo-preview", "Points to gpt-4-0125-preview.", "128,000 tokens", "N/A", "$10.00 / $30.00")
openai_table.add_row(
    "gpt-4-1106-preview",
    "Features improved instruction following, JSON mode, and more.",
    "128,000 tokens",
    "N/A",
    "$10.00 / $30.00",
)
openai_table.add_row(
    "gpt-4-vision-preview", "GPT-4 with image understanding capabilities.", "128,000 tokens", "N/A", "$10.00 / $30.00"
)
openai_table.add_row("gpt-4", "Currently points to gpt-4-0613.", "8,192 tokens", "N/A", "$30.00 / $60.00")
openai_table.add_row(
    "gpt-3.5-turbo-0125", "Latest GPT-3.5 Turbo model with higher accuracy.", "16,385 tokens", "N/A", "$1.50 / $2.00"
)
openai_table.add_row("gpt-3.5-turbo", "Points to gpt-3.5-turbo-0125.", "16,385 tokens", "N/A", "$1.50 / $2.00")
openai_table.add_row(
    "gpt-3.5-turbo-instruct",
    "Similar capabilities as GPT-3 models, for legacy endpoints.",
    "4,096 tokens",
    "N/A",
    "$1.50 / $2.00",
)
openai_table.add_row(
    "gpt-4o",
    "Fastest and most affordable flagship model with multimodal capabilities.",
    "128,000 tokens",
    "N/A",
    "$5.00 / $15.00",
)

# ===== EMBEDDING =====


class EmbeddingGoogle4(EmbeddingModel):
    name: str = "text-embedding-004"
    cost_token: float = 0.0000001
    context_size: int = 2048
    dimension: int = 768
    metric: str = "Cosine"


class EmbeddingGoogle4(EmbeddingModel):
    name: str = "text-multilingual-embedding-002"
    cost_token: float = 0.0000001
    context_size: int = 2048
    dimension: int = 768
    metric: str = "Cosine"


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


# Google Models
google_embedding_table = Table(show_header=True, header_style="bold magenta")
google_embedding_table.add_column("Model Name", justify="left")
google_embedding_table.add_column("Dimensions", justify="right")
google_embedding_table.add_column("Context Length", justify="right")
google_embedding_table.add_column("Price per 1 Million Tokens", justify="left")

google_embedding_table.add_row("text-embedding-004", "768", "2048 tokens", "$0.0004")
google_embedding_table.add_row("text-multilingual-embedding-002", "768", "2048 tokens", "$0.0012")

# OpenAI Models
openai_embedding_table = Table(show_header=True, header_style="bold magenta")
openai_embedding_table.add_column("Model Name", justify="left")
openai_embedding_table.add_column("Dimensions", justify="right")
openai_embedding_table.add_column("Context Length", justify="right")
openai_embedding_table.add_column("Price per 1 Million Tokens", justify="left")

openai_embedding_table.add_row("text-embedding-ada-002", "1536", "8192 tokens", "$0.0004")
openai_embedding_table.add_row("text-embedding-3-small", "768", "8192 tokens", "$0.0012")
openai_embedding_table.add_row("text-embedding-3-large", "1536", "8192 tokens", "$0.0012")

# VoyageAI Models
anthropic_embedding_table = Table(show_header=True, header_style="bold magenta")
anthropic_embedding_table.add_column("Model Name", justify="left")
anthropic_embedding_table.add_column("Dimensions", justify="right")
anthropic_embedding_table.add_column("Context Length", justify="right")
anthropic_embedding_table.add_column("Price per 1 Million Tokens", justify="left")

anthropic_embedding_table.add_row("voyage-large-2-instruct", "3072", "120K tokens", "$0.12")
anthropic_embedding_table.add_row("voyage-code-2", "1536", "120K tokens", "$0.12")
anthropic_embedding_table.add_row("voyage-law-2", "1536", "120K tokens", "$0.12")
anthropic_embedding_table.add_row("voyage-2", "1024", "120K tokens", "$0.10")
anthropic_embedding_table.add_row("voyage-lite-02-instruct", "1024", "4000 tokens", "$0.10")

# Cohere Models
cohere_embedding_table = Table(show_header=True, header_style="bold magenta")
cohere_embedding_table.add_column("Model Name", justify="left")
cohere_embedding_table.add_column("Dimensions", justify="right")
cohere_embedding_table.add_column("Context Length", justify="right")
cohere_embedding_table.add_column("Price per 1 Million Tokens", justify="left")

cohere_embedding_table.add_row("embed-multilingual-v3.0", "1024", "512 tokens", "$0.012")
cohere_embedding_table.add_row("embed-multilingual-light-v3.0", "384", "512 tokens", "$0.008")
cohere_embedding_table.add_row("embed-multilingual-v2.0", "768", "256 tokens", "$0.010")
cohere_embedding_table.add_row("embed-english-v3.0", "1024", "512 tokens", "$0.012")
cohere_embedding_table.add_row("embed-english-light-v3.0", "384", "512 tokens", "$0.008")
cohere_embedding_table.add_row("embed-english-v2.0", "4096", "512 tokens", "$0.010")
cohere_embedding_table.add_row("embed-english-light-v2.0", "1024", "512 tokens", "$0.010")

# Hugging Face Models
hf_embedding_table = Table(show_header=True, header_style="bold magenta")
hf_embedding_table.add_column("Model Name", justify="left")
hf_embedding_table.add_column("Dimensions", justify="right")
hf_embedding_table.add_column("Context Length", justify="right")
hf_embedding_table.add_column("Price per 1 Million Tokens", justify="left")

hf_embedding_table.add_row("roberta-base-nli-mean-tokens", "768", "512 tokens", "$0.75")
hf_embedding_table.add_row("distilroberta-base-nli-mean-tokens", "768", "512 tokens", "$0.75")
hf_embedding_table.add_row("paraphrase-xlm-r-multilingual-v1", "768", "512 tokens", "$0.75")
hf_embedding_table.add_row("stsb-xlm-r-multilingual", "768", "512 tokens", "$0.75")
hf_embedding_table.add_row("msmarco-distilroberta-base-v4", "768", "512 tokens", "$0.75")
hf_embedding_table.add_row("msmarco-roberta-base-v2", "768", "512 tokens", "$0.75")
hf_embedding_table.add_row("distiluse-base-multilingual-cased-v1", "512", "512 tokens", "$0.75")
hf_embedding_table.add_row("multi-qa-MiniLM-L6-cos-v1", "384", "512 tokens", "$0.75")
hf_embedding_table.add_row("msmarco-MiniLM-L6-cos-v5", "384", "512 tokens", "$0.75")
hf_embedding_table.add_row("clip-ViT-B-32-multilingual-v1", "512", "512 tokens", "$0.75")
hf_embedding_table.add_row("hkunlp/instructor-large", "768", "512 tokens", "$0.75")
hf_embedding_table.add_row("all-MiniLM-L6-v2", "384", "512 tokens", "$0.75")


# ===== STT =====


class STTOpenaiTiny(STTModel):
    cost_char: float = 0.0
    name: str = "tiny"


class STTOpenaiBase(STTModel):
    cost_char: float = 0.0
    name: str = "base"


class STTOpenaiSmall(STTModel):
    cost_char: float = 0.0
    name: str = "small"


class STTOpenaiMedium(STTModel):
    cost_char: float = 0.0
    name: str = "medium"


class STTOpenaiLarge(STTModel):
    cost_char: float = 0.0
    name: str = "large"


# Openai Models
openai_stt_table = Table(show_header=True, header_style="bold magenta")
openai_stt_table.add_column("Model Name", justify="left")
openai_stt_table.add_column("Parameters", justify="right")
openai_stt_table.add_column("VRAM GB", justify="right")

openai_stt_table.add_row("tiny", "39", "1")
openai_stt_table.add_row("base", "74", "1")
openai_stt_table.add_row("small", "244", "2")
openai_stt_table.add_row("medium", "769", "5")
openai_stt_table.add_row("large", "1550", "10")


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


cohere_rerank_table = Table(show_header=True, header_style="bold magenta")
cohere_rerank_table.add_column("Model Name", justify="left")
cohere_rerank_table.add_column("Description", justify="left")
cohere_rerank_table.add_column("Context Length", justify="right")
cohere_rerank_table.add_column("Rate Limit", justify="left")
cohere_rerank_table.add_column("Pricing for 1 Million Tokens", justify="left")

cohere_rerank_table.add_row(
    "rerank-english-v3.0",
    "A foundation model designed for efficient enterprise search and Retrieval-Augmented Generation (RAG).",
    "512 tokens",
    "N/A",
    "$2.00 / 1K searches",
)
cohere_rerank_table.add_row(
    "rerank-multilingual-v3.0",
    "A foundation model designed for efficient enterprise search and Retrieval-Augmented Generation (RAG)",
    "512 tokens",
    "N/A",
    "$2.00 / 1K searches",
)
cohere_rerank_table.add_row(
    "rerank-english-v2.0",
    "A model that allows for re-ranking English language documents.",
    "512 tokens",
    "N/A",
    "$1.00 / 1K searches",
)
cohere_rerank_table.add_row(
    "rerank-multilingual-v2.0",
    "A model for documents that are not in English. Supports the same languages as embed-multilingual-v2.0",
    "512 tokens",
    "N/A",
    "$1.00 / 1K searches",
)

# ===== TTS =====


class TTSOpenai1(TTSModel):
    cost_char: float = 1.5e-5
    name: str = "tts-1"
    voice: str


class TTSOpenai1HD(TTSModel):
    cost_char: float = 3e-5
    name: str = "tts-1-hd"
    voice: str


openai_tts = Table(show_header=True, header_style="bold magenta")
openai_tts.add_column("Model Name", justify="left")
openai_tts.add_column("Description", justify="left")
openai_tts.add_column("Context Length", justify="right")
openai_tts.add_column("Rate Limit", justify="left")
openai_tts.add_column("Pricing for 1 Million Tokens", justify="left")

openai_tts.add_row(
    "tts-1",
    "A real-time optimized text-to-speech model offering low latency.",
    "4096 characters",
    "50 RPM",
    "$15.00 per 1,000,000 characters",
)
openai_tts.add_row(
    "tts-1-hd",
    "A high-definition text-to-speech model optimized for quality.",
    "4096 characters",
    "50 RPM",
    "$30.00 per 1,000,000 characters",
)


# ===== Cross-encoder =====


hf_crossencoder_table = Table(show_header=True, header_style="bold magenta")
hf_crossencoder_table.add_column("Model Name", justify="left")
hf_crossencoder_table.add_column("Description", justify="left")
hf_crossencoder_table.add_column("Dimensions", justify="center")
hf_crossencoder_table.add_column("Language", justify="left")
hf_crossencoder_table.add_column("Use Cases", justify="left")
hf_crossencoder_table.add_column("Accuracy", justify="left")

# Adding rows with the cross-encoder model data
hf_crossencoder_table.add_row(
    "ms-marco-TinyBERT-L-2-v2",
    "Cross-encoder model for MS Marco with TinyBERT L-2 architecture",
    "-",
    "English",
    "Information Retrieval",
    "MRR@10: 32.56",
)
hf_crossencoder_table.add_row(
    "ms-marco-MiniLM-L-2-v2",
    "Cross-encoder model for MS Marco with MiniLM L-2 architecture",
    "-",
    "English",
    "Information Retrieval",
    "MRR@10: 34.85",
)
hf_crossencoder_table.add_row(
    "ms-marco-MiniLM-L-4-v2",
    "Cross-encoder model for MS Marco with MiniLM L-4 architecture",
    "-",
    "English",
    "Information Retrieval",
    "MRR@10: 37.70",
)
hf_crossencoder_table.add_row(
    "ms-marco-MiniLM-L-6-v2",
    "Cross-encoder model for MS Marco with MiniLM L-6 architecture",
    "-",
    "English",
    "Information Retrieval",
    "MRR@10: 39.01",
)
hf_crossencoder_table.add_row(
    "ms-marco-MiniLM-L-12-v2",
    "Cross-encoder model for MS Marco with MiniLM L-12 architecture",
    "-",
    "English",
    "Information Retrieval",
    "MRR@10: 39.02",
)
hf_crossencoder_table.add_row(
    "stsb-TinyBERT-L-4",
    "Cross-encoder model for Semantic Textual Similarity Benchmark with TinyBERT",
    "-",
    "English",
    "Semantic Textual Similarity",
    "STSbenchmark: 85.50",
)
hf_crossencoder_table.add_row(
    "stsb-distilroberta-base",
    "Cross-encoder model for Semantic Textual Similarity Benchmark with DistilRoBERTa",
    "-",
    "English",
    "Semantic Textual Similarity",
    "STSbenchmark: 87.92",
)
hf_crossencoder_table.add_row(
    "stsb-roberta-base",
    "Cross-encoder model for Semantic Textual Similarity Benchmark with RoBERTa",
    "-",
    "English",
    "Semantic Textual Similarity",
    "STSbenchmark: 90.17",
)
hf_crossencoder_table.add_row(
    "stsb-roberta-large",
    "Cross-encoder model for Semantic Textual Similarity Benchmark with large RoBERTa",
    "-",
    "English",
    "Semantic Textual Similarity",
    "STSbenchmark: 91.47",
)
hf_crossencoder_table.add_row(
    "quora-distilroberta-base",
    "Cross-encoder model for Quora Question Pairs with DistilRoBERTa",
    "-",
    "English",
    "Duplicate Question Detection",
    "Average Precision: 87.48",
)
hf_crossencoder_table.add_row(
    "quora-roberta-base",
    "Cross-encoder model for Quora Question Pairs with RoBERTa",
    "-",
    "English",
    "Duplicate Question Detection",
    "Average Precision: 87.80",
)
hf_crossencoder_table.add_row(
    "quora-roberta-large",
    "Cross-encoder model for Quora Question Pairs with large RoBERTa",
    "-",
    "English",
    "Duplicate Question Detection",
    "Average Precision: 87.91",
)
hf_crossencoder_table.add_row(
    "nli-deberta-v3-base",
    "Cross-encoder model for Natural Language Inference with DeBERTa v3 base",
    "-",
    "English",
    "Natural Language Inference",
    "Accuracy: 90.04 (MNLI mismatched)",
)
hf_crossencoder_table.add_row(
    "nli-deberta-base",
    "Cross-encoder model for Natural Language Inference with DeBERTa base",
    "-",
    "English",
    "Natural Language Inference",
    "Accuracy: 88.08 (MNLI mismatched)",
)
hf_crossencoder_table.add_row(
    "nli-deberta-v3-xsmall",
    "Cross-encoder model for Natural Language Inference with DeBERTa v3 xsmall",
    "-",
    "English",
    "Natural Language Inference",
    "Accuracy: 87.77 (MNLI mismatched)",
)
hf_crossencoder_table.add_row(
    "nli-deberta-v3-small",
    "Cross-encoder model for Natural Language Inference with DeBERTa v3 small",
    "-",
    "English",
    "Natural Language Inference",
    "Accuracy: 87.55 (MNLI mismatched)",
)
hf_crossencoder_table.add_row(
    "nli-roberta-base",
    "Cross-encoder model for Natural Language Inference with RoBERTa base",
    "-",
    "English",
    "Natural Language Inference",
    "Accuracy: 87.47 (MNLI mismatched)",
)
hf_crossencoder_table.add_row(
    "nli-MiniLM2-L6-H768",
    "Cross-encoder model for Natural Language Inference with MiniLM2 L6 H768",
    "-",
    "English",
    "Natural Language Inference",
    "Accuracy: 86.89 (MNLI mismatched)",
)
hf_crossencoder_table.add_row(
    "nli-distilroberta-base",
    "Cross-encoder model for Natural Language Inference with DistilRoBERTa base",
    "-",
    "English",
    "Natural Language Inference",
    "Accuracy: 83.98 (MNLI mismatched)",
)
