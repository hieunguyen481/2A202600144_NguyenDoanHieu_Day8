# Tuning Log — RAG Pipeline (Day 08 Lab)

> Template: Ghi lại mỗi thay đổi và kết quả quan sát được.
> A/B Rule: Chỉ đổi MỘT biến mỗi lần.

---

## Baseline (Sprint 2)

**Ngày:** 2026-04-13  
**Config:**
```
retrieval_mode = "dense"
chunk_size = 400 tokens
overlap = 80 tokens
top_k_search = 10
top_k_select = 3
use_rerank = False
llm_model = gpt-4o-mini
embedding_model = text-embedding-3-small (OpenAI)
```

**Scorecard Baseline:**
| Metric | Average Score |
|--------|--------------|
| Faithfulness | 5/5 |
| Answer Relevance | 5/5 |
| Context Recall | 4/5 |
| Completeness | 4/5 |

**Câu hỏi khó nhất (điểm thấp):**
- **q05 (Account lock)**: context recall = 3/5 — Dense search chỉ lấy documents về access control, bỏ lỡ IT Helpdesk FAQ (đồng nghĩa)
- **q06 (P1 Escalation)**: context recall = 4/5 — Cần chính xác từ "escalate" nhưng dense lấy chung SLA sections

**Giả thuyết nguyên nhân (Error Tree):**
- [x] Retrieval: Dense bỏ lỡ exact keyword / alias (q05 account lock vs tài khoản khóa)
- [x] Retrieval: Top-k bỏ lỡ section từ document khác (q06 escalation rules)
- [ ] Indexing: OK – chunking hợp lý, metadata đủ
- [ ] Generation: OK – model grounded tốt, citation chính xác

---

## Variant 1: Hybrid (Dense + BM25) (Sprint 3)

**Ngày:** 2026-04-13  
**Biến thay đổi:** `retrieval_mode = "dense"` → `retrieval_mode = "hybrid"`  
**Lý do chọn biến này:**

Corpus có lẫn lộn:
- **Ngôn ngữ tự nhiên**: Policy text, SLA description
- **Tên riêng + mã lỗi**: "P1", "ERR-403", "Level 3", "ticket"

Dense (semantic) tốt cho ý nghĩa nhưng hay bỏ lỡ exact term. BM25 (keyword) mạnh với term chính xác.

Evidence:
- q05: Dense đưa "access control" (semantic gần) nhưng BM25 lấy "account locked" (exact match)
- q06: Dense miss "escalate" keyword → hybrid + BM25 tìm được

**Config thay đổi:**
```
retrieval_mode = "hybrid"     # Dense (60%) + BM25 (40%) with RRF
top_k_search = 10             # Same as baseline
top_k_select = 3              # Same as baseline
use_rerank = False            # Same as baseline
```

**Scorecard Variant 1 (Hybrid):**
| Metric | Baseline | Hybrid | Delta |
|--------|----------|--------|-------|
| Faithfulness | 5/5 | 5/5 | ±0 |
| Answer Relevance | 5/5 | 5/5 | ±0 |
| Context Recall | 4/5 | 5/5 | +1 |
| Completeness | 4/5 | 5/5 | +1 |

**Nhận xét:**
- ✅ **q05 cải thiện**: Hybrid lấy được IT Helpdesk FAQ (account lock) nhờ BM25 keyword match
- ✅ **q06 cải thiện**: Hybrid tìm được exact "escalate" section từ SLA document
- ✅ **q01, q02, q03 giữ nguyên tốt**: Vừa semantic (dense) vừa keyword (hybrid) đều match → không có degradation
- ⚠️ **q04, q07 OK**: Hybrid không tệ hơn dense (vẫn grounded)

**Kết luận:**
✅ **Hybrid tốt hơn Baseline**

Bằng chứ:
- Context Recall: 4/5 → 5/5 (+1 điểm)
- Completeness: 4/5 → 5/5 (+1 điểm)
- **Câu hỏi cụ thể**: 
  - q05 (account lock): Dense miss → Hybrid hit
  - q06 (escalation): Dense miss → Hybrid hit
  
**Chọn Hybrid cho Sprint 4** vì:
1. RRF tư tưởng: combine best of both (semantic + keyword)
2. Corpus đa dạng → hybrid phù hợp
3. Không tốn rerank/transformation overhead
4. Average score tăng 2 điểm (8 → 10)

---

## Variant 2 (nếu có thời gian)

**Biến thay đổi:** ___________  
**Config:**
```
# TODO
```

**Scorecard Variant 2:**
| Metric | Baseline | Variant 1 | Variant 2 | Best |
|--------|----------|-----------|-----------|------|
| Faithfulness | ? | ? | ? | ? |
| Answer Relevance | ? | ? | ? | ? |
| Context Recall | ? | ? | ? | ? |
| Completeness | ? | ? | ? | ? |

---

## Tóm tắt học được

> TODO (Sprint 4): Điền sau khi hoàn thành evaluation.

1. **Lỗi phổ biến nhất trong pipeline này là gì?**
   > _____________

2. **Biến nào có tác động lớn nhất tới chất lượng?**
   > _____________

3. **Nếu có thêm 1 giờ, nhóm sẽ thử gì tiếp theo?**
   > _____________
