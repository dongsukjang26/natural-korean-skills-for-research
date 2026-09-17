# AI 용어 표기 정책 (연구 모드)

연구 모드에서 AI 용어를 영문으로 두는 이유는 두 가지입니다. 독자가 원문 논문을 찾을 때 한 번 더 번역하지 않아도 되고, 같은 개념이 문서마다 다른 음차로 갈라지지 않습니다. `어텐션`, `애텐션`, `주의 메커니즘`은 전부 attention이지만 검색으로는 이어지지 않습니다.

대신 조사, 어미, 문장 골격은 전부 한국어입니다. 목표는 영문 용어를 박아 넣은 한국어 문장이지, 한국어 조사를 붙인 영어 문장이 아닙니다.

## 판단 기준

용어를 만날 때마다 한 가지만 물으면 됩니다.

> 논문과 코드에서 그 형태로 쓰이는가, 아니면 한국어에 이미 들어온 말인가?

- 논문과 코드의 형태가 표준이면 → **1층 (영문 그대로)**
- 한국어 사전과 업계에서 한글로 굳었으면 → **2층 (한글 음차)**
- 영어로 되돌릴 이유가 없는 일반 개념이면 → **3층 (한국어 단어)**

세 층의 경계는 시간이 지나면 움직입니다. `모델`과 `데이터`는 예전에 1층이었다가 2층으로 내려왔습니다. 확신이 서지 않으면 그 분야 한국어 문서 두세 편을 보고 다수를 따릅니다.

---

## 1층 — 영문 그대로

연구 모드에서만 적용합니다. 일반 모드에서는 한글로 풀어 씁니다.

### 구조와 기법

transformer, attention, self-attention, cross-attention, multi-head attention, encoder, decoder, residual connection, layer norm, positional encoding, RoPE, MoE, mixture of experts, diffusion, autoregressive, state space model, Mamba

### 학습과 튜닝

pretraining, fine-tuning, SFT, instruction tuning, RLHF, DPO, PPO, GRPO, LoRA, QLoRA, PEFT, adapter, distillation, knowledge distillation, quantization, pruning, curriculum learning, continual learning, catastrophic forgetting

### 최적화

loss, cross-entropy, gradient, gradient clipping, backpropagation, optimizer, Adam, AdamW, learning rate, warmup, scheduler, batch size, micro-batch, gradient accumulation, epoch, step, checkpoint, overfitting, underfitting, regularization, dropout, weight decay, mixed precision

### 추론과 서빙

inference, decoding, greedy decoding, beam search, sampling, temperature, top-k, top-p, KV cache, speculative decoding, flash attention, latency, throughput, TTFT, tokens per second, batching, serving

### 데이터와 표현

token, tokenizer, tokenization, embedding, vocabulary, context window, context length, corpus, data leakage, deduplication, synthetic data, chunking

### 평가와 실험

baseline, ablation, ablation study, benchmark, eval, evaluation harness, SOTA, zero-shot, few-shot, in-context learning, chain-of-thought, CoT, held-out, test set, validation set, seed, variance, reproducibility 관련 표기는 3층의 `재현`을 씁니다

### 응용과 시스템

RAG, retrieval, reranking, vector store, agent, tool use, function calling, MCP, guardrail, alignment, hallucination, jailbreak, prompt, prompt injection, system prompt

### 약어와 고유명사

LLM, VLM, MLLM, GPT, BERT, T5, CLIP, ViT, GPU, TPU, CUDA, FLOPs, HBM, API, SDK, arXiv, Hugging Face, PyTorch, JAX

---

## 2층 — 한글 음차

두 모드 모두 한글로 씁니다. 굳이 영문으로 되돌리지 않습니다.

모델, 데이터, 데이터셋*, 파라미터, 하이퍼파라미터*, 레이어, 벡터, 행렬, 네트워크, 알고리즘, 라이브러리, 프레임워크, 서버, 클라이언트, 메모리, 캐시, 코드, 스크립트, 로그, 테스트, 샘플, 노이즈, 시퀀스, 인덱스, 파이프라인, 워크플로, 클러스터, 노드, 컨테이너

`*` 표시한 말은 흔들립니다. `데이터셋`과 `dataset`, `하이퍼파라미터`와 `hyperparameter`가 둘 다 쓰입니다. 문서 하나 안에서 하나로 통일하면 됩니다.

### 2층을 영문으로 쓰면 안 되는 이유

```
✗ model을 3 epoch 동안 train했고, data는 clean한 subset만 썼다.
✓ 모델을 3 epoch 동안 학습했고, 데이터는 깨끗한 부분만 썼다.
```

첫 문장은 한국어 조사를 붙인 영어 문장입니다. 읽는 속도가 느려지고, 영문 용어가 너무 흔해져서 정작 중요한 용어(epoch)가 묻힙니다. 영문 용어는 한 문장에 둘까지가 읽기 편합니다.

---

## 3층 — 한국어 단어

두 모드 모두 한국어로 씁니다.

학습, 훈련, 사전 학습*, 추론, 성능, 정확도, 정밀도, 재현율, 가중치, 편향*, 수렴, 발산, 분포, 오차, 실험, 평가, 비교, 재현, 검증, 한계, 개선, 결과, 관측, 가설, 근거, 규모, 속도, 비용

`*` 표시:

- **사전 학습**: `pretraining`과 `사전 학습`이 둘 다 표준입니다. 문서 안에서 통일합니다.
- **편향**: 사회적 편향은 `편향`, 모델의 bias 항은 `bias`입니다. 아래 동음이의 절을 보세요.

---

## 같은 단어, 두 뜻

기술 개념이면 영문, 일반적인 뜻이면 한국어입니다.

| 단어 | 기술 개념 (영문) | 일반적인 뜻 (한국어) |
|---|---|---|
| bias | "마지막 층의 bias를 0으로 초기화했다" | "데이터에 성별 편향이 있다" |
| scale | "scaling law를 따른다" | "규모가 두 배로 커졌다" |
| attention | "attention 가중치를 시각화했다" | "이 부분에 주의가 필요하다" |
| head | "attention head 12개" | (한국어 대응 없음) |
| token | "context가 4천 token을 넘었다" | (한국어 대응 없음) |
| prompt | "system prompt를 바꿨다" | "빠른 응답" 같은 일반 뜻은 다른 말로 |
| temperature | "temperature를 0.7로 뒀다" | "온도가 올라갔다" |
| memory | "KV cache가 메모리를 먹는다" (하드웨어는 2층) | — |

---

## 조사 결합

한글로 읽었을 때의 받침을 기준으로 고릅니다. 괄호 안은 읽는 소리입니다.

| 용어 | 받침 | 조사 | 예 |
|---|---|---|---|
| token (토큰) | 있음 | 을/은/과/으로 | "token을 자른다" |
| loss (로스) | 없음 | 를/는/와/로 | "loss가 줄었다" |
| gradient (그래디언트) | 없음 | 를/는/로 | "gradient를 잘랐다" |
| embedding (임베딩) | 있음 | 을/은/으로 | "embedding을 붙였다" |
| baseline (베이스라인) | 있음 | 을/은/으로 | "baseline보다 높다" |
| LLM (엘엘엠) | 있음 | 을/은/으로 | "LLM으로 요약한다" |
| GPU (지피유) | 없음 | 를/는/로 | "GPU를 두 장 썼다" |
| RAG (래그) | 있음 | 을/은/으로 | "RAG을 붙였다" |
| API (에이피아이) | 없음 | 를/는/로 | "API를 호출한다" |

읽는 소리가 갈리는 약어는 괄호 없이 그대로 쓰고, 조사는 더 흔한 발음을 따릅니다.

### `-하다` 직결 금지

영어 어근에 `-하다`를 바로 붙이면 읽기가 걸립니다. 조사를 넣거나 한국어 동사로 바꿉니다.

```
✗ fine-tuning했다        ✓ fine-tuning을 했다 / fine-tuning으로 학습했다
✗ eval돌렸다             ✓ eval을 돌렸다
✗ quantization하면       ✓ quantization을 하면 / 양자화하면
✗ prompting해서          ✓ prompt를 써서
```

### 복수형

영어 복수 `-s`와 한국어 `-들`을 둘 다 붙이지 않습니다. 한국어는 복수를 잘 표시하지 않습니다.

```
✗ 여러 baseline들과 비교했다
✗ 여러 baselines와 비교했다
✓ 여러 baseline과 비교했다
```

### 대소문자

- 약어는 대문자: LLM, RAG, SFT, MoE
- 논문과 모델 고유명사는 원표기: Transformer(논문), BERT, Llama
- 일반 명사로 굳은 말은 소문자: transformer 구조, attention 층

---

## 코드와 수식이 섞일 때

- 식별자, 함수명, 파일명은 백틱으로 감쌉니다: `AdamW`, `model.generate()`, `config.yaml`
- 백틱 안은 문체 규칙 밖입니다. 조사도 백틱 밖에 붙입니다: `` `AdamW`를 썼다 ``
- 수식 기호는 그대로 둡니다. `학습률 α를 3e-4로 뒀다`

---

## 일반 모드에서는

일반 모드 독자는 논문을 찾아보지 않습니다. 1층 용어도 한국어로 풀고, 꼭 필요하면 한 번만 영문을 괄호에 넣습니다.

```
연구 모드: attention은 각 token이 다른 token을 얼마나 참고할지 정하는 가중치다.
일반 모드: 문장을 읽을 때 어떤 단어가 어떤 단어와 관련이 깊은지 따지는 방식입니다.
           이걸 어텐션(attention)이라고 부릅니다.
```

일반 모드에서 영문 용어가 한 문단에 세 개를 넘으면 독자를 잃습니다.

---

## 출처와 한계

용어 구분은 다음을 참고했습니다.

- Google 머신러닝 용어집 한국어판 — 영문 유지(ReLU, BERT, GAN, TPU), 음차(어텐션, 임베딩, 레이어, 토큰), 한국어 번역(과적합, 손실, 정규화, 경사하강법)의 세 갈래를 확인했습니다. <https://developers.google.com/machine-learning/glossary?hl=ko>
- 국립국어원 표준 전문용어와 다듬은 말 — 정부 표준 용어 기준. <https://www.korean.go.kr/front/imprv/stndrdList.do?mn_id=159>
- TTA 정보통신용어사전 — 국내 통신과 정보 분야 표준 용어. <https://terms.tta.or.kr/>
- 국내 AI 기술 블로그와 논문 리뷰 글의 실제 용법. "Attention 레이어", "LoRA", "loss 수렴", "SFTTrainer 클래스"처럼 영문 기법명 + 한글 음차 + 한국어 서술이 섞인 형태가 일반적입니다.

한계를 밝힙니다. Google 용어집은 **음차**(어텐션, 임베딩)를 택했고, 이 문서는 연구 모드에서 **영문 유지**를 택했습니다. 용어집은 개념을 처음 배우는 독자를 향하고, 이 문서의 연구 모드는 원문 논문을 함께 읽는 독자를 향하기 때문입니다. 독자가 입문자라면 일반 모드 쪽이 맞습니다.

국내에 AI 분야 표기를 확정한 단일 표준은 없습니다. 이 분류는 관행을 정리한 것이지 규범이 아닙니다. 소속 조직에 용어집이 있으면 그쪽이 먼저입니다.
