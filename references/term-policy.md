# 용어 표기 정책

용어를 영문으로 두는 이유는 두 가지입니다. 독자가 원문 논문이나 문서를 찾을 때 한 번 더 번역하지 않아도 되고, 같은 개념이 문서마다 다른 음차로 갈라지지 않습니다. `어텐션`, `애텐션`, `주의 메커니즘`은 전부 attention이지만 검색으로는 이어지지 않습니다.

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

### 머신러닝 구조와 기법

transformer, attention, self-attention, cross-attention, multi-head attention, encoder, decoder, residual connection, layer norm, positional encoding, RoPE, MoE, mixture of experts, diffusion, autoregressive, state space model

### 학습과 튜닝

pretraining, fine-tuning, SFT, instruction tuning, RLHF, DPO, PPO, GRPO, LoRA, QLoRA, PEFT, adapter, distillation, quantization, pruning, curriculum learning, continual learning, catastrophic forgetting

### 최적화

loss, cross-entropy, gradient, gradient clipping, backpropagation, optimizer, Adam, AdamW, learning rate, warmup, scheduler, batch size, gradient accumulation, epoch, step, checkpoint, overfitting, underfitting, regularization, dropout, weight decay, mixed precision

### 추론과 서빙

inference, decoding, greedy decoding, beam search, sampling, temperature, top-k, top-p, KV cache, speculative decoding, flash attention, TTFT, batching, serving

### 데이터와 표현

token, tokenizer, tokenization, embedding, vocabulary, context window, corpus, data leakage, deduplication, synthetic data, chunking

### 평가와 실험

baseline, ablation, benchmark, eval, SOTA, zero-shot, few-shot, in-context learning, chain-of-thought, held-out, test set, validation set, seed, p-value, effect size

### 응용과 시스템

RAG, retrieval, reranking, vector store, agent, tool use, function calling, MCP, guardrail, alignment, hallucination, jailbreak, prompt, prompt injection, system prompt

### 운영체제와 동시성

thread, process, context switch, scheduler, preemption, deadlock, livelock, race condition, mutex, semaphore, spinlock, page fault, virtual memory, syscall, garbage collection, JIT, memory barrier

### 네트워크와 분산 시스템

latency, throughput, bandwidth, RTT, tail latency, congestion control, packet loss, handshake, backpressure, load balancer, reverse proxy, CDN, consensus, Raft, Paxos, quorum, leader election, gossip, idempotency

### 데이터베이스

transaction, isolation level, snapshot isolation, index, query plan, sharding, partitioning, replication, eventual consistency, linearizability, ACID, B-tree, LSM tree, WAL, vacuum, deadlock detection

### 프로그래밍 언어와 컴파일러

type inference, type checking, generics, closure, immutability, ownership, borrow checker, compiler, parser, AST, IR, SSA, inlining, dead code elimination, monomorphization

### 보안

threat model, attack surface, sandbox, side-channel, timing attack, fuzzing, CVE, supply chain, least privilege, zero trust

### HCI와 사용자 연구

usability, think-aloud, within-subjects, between-subjects, counterbalancing, Likert scale, IRB, cognitive load

### 약어와 고유명사

LLM, VLM, GPT, BERT, CLIP, ViT, GPU, TPU, CUDA, FLOPs, HBM, API, SDK, RPC, gRPC, HTTP, TLS, arXiv, Hugging Face, PyTorch, Linux, Kubernetes

---

## 2층 — 한글 음차

이미 한국어로 굳은 외래어입니다. 굳이 영문으로 되돌리지 않습니다.

모델, 데이터, 데이터셋*, 파라미터, 하이퍼파라미터*, 레이어, 벡터, 행렬, 네트워크, 알고리즘, 라이브러리, 프레임워크, 서버, 클라이언트, 메모리, 캐시, 버퍼, 큐, 스택, 코드, 스크립트, 로그, 테스트, 샘플, 노이즈, 시퀀스, 인덱스, 파이프라인, 워크플로, 클러스터, 노드, 컨테이너, 커널, 스레드*, 프로세스*, 패킷, 프로토콜, 소켓

`*` 표시한 말은 흔들립니다. `데이터셋`과 `dataset`, `스레드`와 `thread`가 둘 다 쓰입니다. 문서 하나 안에서 하나로 통일하면 됩니다.

### 2층을 영문으로 쓰면 안 되는 이유

```
✗ model을 3 epoch 동안 train했고, data는 clean한 subset만 썼다.
✓ 모델을 3 epoch 동안 학습했고, 데이터는 깨끗한 부분만 썼다.
```

첫 문장은 한국어 조사를 붙인 영어 문장입니다. 읽는 속도가 느려지고, 영문 용어가 너무 흔해져서 정작 중요한 용어(epoch)가 묻힙니다. **영문 용어는 한 문장에 둘까지가 읽기 편합니다.**

---

## 3층 — 한국어 단어

학습, 훈련, 사전 학습*, 추론, 성능, 정확도, 정밀도, 재현율, 가중치, 편향*, 수렴, 발산, 분포, 오차, 실험, 평가, 비교, 재현, 검증, 한계, 개선, 결과, 관측, 가설, 근거, 규모, 속도, 비용, 지연, 병목, 처리량*, 신뢰구간, 유의수준, 표본, 분산

`*` 표시:

- **사전 학습**: `pretraining`과 `사전 학습`이 둘 다 표준입니다. 문서 안에서 통일합니다.
- **편향**: 사회적 편향은 `편향`, 모델의 bias 항은 `bias`입니다.
- **처리량**: `throughput`도 흔히 씁니다. 성능 수치를 다루는 문맥이면 `throughput`이 대조하기 좋습니다.

---

## 같은 단어, 두 뜻

기술 개념이면 영문, 일반적인 뜻이면 한국어입니다.

| 단어 | 기술 개념 (영문) | 일반적인 뜻 (한국어) |
|---|---|---|
| bias | "마지막 층의 bias를 0으로 초기화했다" | "데이터에 성별 편향이 있다" |
| scale | "scaling law를 따른다" | "규모가 두 배로 커졌다" |
| attention | "attention 가중치를 시각화했다" | "이 부분에 주의가 필요하다" |
| memory | "KV cache가 메모리를 먹는다" | "기억에 의존하는 설계" |
| temperature | "temperature를 0.7로 뒀다" | "온도가 올라갔다" |
| queue | "요청 queue가 쌓였다" | "줄을 선다" |
| lock | "lock을 잡은 채로 I/O를 한다" | "잠금 화면" |

---

## 영문 병기

용어를 **처음 쓸 때만** 병기하고 그다음부터는 하나로 통일합니다. 쿠버네티스 한글화 가이드도 같은 규칙을 씁니다. 영문 병기는 문서에서 해당 용어가 처음 등장할 때 한 번만 표기하고, 한 페이지 안에서 같은 단어는 일관되게 씁니다.

```
연구자만 읽는 글:   이 구조는 attention을 쓴다. ... attention 가중치를 보면
입문자가 섞인 글:   이 구조는 어텐션(attention)을 쓴다. ... 어텐션 가중치를 보면
```

**한 문서 안에서 표기를 바꾸지 않습니다.** 앞에서 `attention`이라 썼으면 뒤에서 `어텐션`으로 돌아가지 않습니다. 같은 용어를 두 번 이상 병기하지도 않습니다.

학회 투고용 국문 논문은 예외입니다. 국내 학회의 국문 논문 규정은 대체로 한글 역어를 본문에 쓰고 원어를 괄호에 병기하도록 합니다. 투고 원고는 해당 학회 지침을 따릅니다.

---

## 조사 결합

한글로 읽었을 때의 받침을 기준으로 고릅니다. 괄호 안은 읽는 소리입니다.

| 용어 | 받침 | 조사 | 예 |
|---|---|---|---|
| token (토큰) | 있음 | 을/은/으로 | "token을 자른다" |
| loss (로스) | 없음 | 를/는/로 | "loss가 줄었다" |
| gradient (그래디언트) | 없음 | 를/는/로 | "gradient를 잘랐다" |
| embedding (임베딩) | 있음 | 을/은/으로 | "embedding을 붙였다" |
| baseline (베이스라인) | 있음 | 을/은/으로 | "baseline보다 높다" |
| deadlock (데드락) | 있음 | 을/은/으로 | "deadlock으로 멈췄다" |
| LLM (엘엘엠) | 있음 | 을/은/으로 | "LLM으로 요약한다" |
| GPU (지피유) | 없음 | 를/는/로 | "GPU를 두 장 썼다" |
| API (에이피아이) | 없음 | 를/는/로 | "API를 호출한다" |
| RAG (래그) | 있음 | 을/은/으로 | "RAG을 붙였다" |

### `-하다` 직결 금지

영어 어근에 `-하다`를 바로 붙이면 읽기가 걸립니다. 조사를 넣거나 한국어 동사로 바꿉니다.

```
✗ fine-tuning했다        ✓ fine-tuning을 했다 / fine-tuning으로 학습했다
✗ profiling해보면        ✓ profiling을 해 보면
✗ quantization하면       ✓ quantization을 하면 / 양자화하면
✗ deploy했다             ✓ 배포했다
```

### 복수형

영어 복수 `-s`와 한국어 `-들`을 둘 다 붙이지 않습니다. 한국어는 복수를 잘 표시하지 않습니다.

```
✗ 여러 baseline들과 비교했다
✗ 여러 baselines와 비교했다
✓ 여러 baseline과 비교했다
```

### 대소문자

- 약어는 대문자: LLM, RAG, SFT, MoE, ACID, WAL
- 논문과 모델 고유명사는 원표기: Transformer(논문), BERT, Llama, Raft
- 일반 명사로 굳은 말은 소문자: transformer 구조, attention 층

---

## 코드와 수식이 섞일 때

- 식별자, 함수명, 파일명은 백틱으로 감쌉니다: `AdamW`, `model.generate()`, `config.yaml`
- 백틱 안은 문체 규칙 밖입니다. 조사도 백틱 밖에 붙입니다: `` `AdamW`를 썼다 ``
- 수식 기호에도 받침 기준으로 조사를 붙입니다: "학습률 α를 3e-4로 뒀다", "batch size B가 커지면"

---

## 출처와 한계

- [Google 머신러닝 용어집 한국어판](https://developers.google.com/machine-learning/glossary?hl=ko) — 영문 유지(ReLU, BERT, GAN, TPU), 음차(어텐션, 임베딩, 레이어, 토큰), 한국어 번역(과적합, 손실, 정규화, 경사하강법)의 세 갈래를 확인했습니다.
- [쿠버네티스 한글화 모범 사례](https://kubernetes.io/ko/docs/contribute/localization_ko_best_practice/) — 영문 병기를 첫 등장 한 번만 하고 한 페이지 안에서 일관되게 쓴다는 규칙.
- [국립국어원 표준 전문용어](https://www.korean.go.kr/front/imprv/stndrdList.do?mn_id=159) — 정부 고시 표준 용어와 외래어 표기 기준.
- [TTA 정보통신용어사전](https://terms.tta.or.kr/) — 국내 정보통신 분야 표준 용어.
- 국내 AI와 CS 기술 블로그, 논문 리뷰 글의 실제 용법. "Attention 레이어", "LoRA", "loss 수렴", "tail latency"처럼 영문 기법명과 한글 음차, 한국어 서술이 섞인 형태가 일반적입니다.

한계를 밝힙니다. Google 용어집은 **음차**(어텐션, 임베딩)를 택했고, 이 문서는 **영문 유지**를 택했습니다. 용어집은 개념을 처음 배우는 독자를 향하고, 이 문서는 원문 논문과 코드를 함께 읽는 독자를 향하기 때문입니다. 독자가 입문자라면 병기 쪽이 맞습니다.

국내에 AI와 CS 분야 표기를 확정한 단일 표준은 없습니다. 이 분류는 관행을 정리한 것이지 규범이 아닙니다. 소속 조직이나 투고 학회에 용어집이 있으면 그쪽이 먼저입니다.
