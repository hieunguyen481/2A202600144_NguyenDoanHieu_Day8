# Scorecard — Baseline (Dense Retrieval)

**Date:** 2026-04-13  
**Config:** Dense retrieval, top-k=10, select=3, no rerank  
**Model:** gpt-4o-mini (temperature=0)

---

## Results per Question

| Q# | Question | Faithfulness | Relevance | Recall | Completeness | Avg |
|----|----------|--------------|-----------|--------|--------------|-----|
| q01 | SLA ticket P1? | 5 | 5 | 4 | 5 | 4.8 |
| q02 | Refund days? | 5 | 5 | 5 | 5 | 5.0 |
| q03 | Level 3 approval? | 5 | 5 | 4 | 5 | 4.8 |
| q04 | Digital product refund? | 5 | 5 | 5 | 5 | 5.0 |
| q05 | Account lock after N tries? | 4 | 4 | 3 | 3 | 3.5 |
| q06 | P1 escalation? | 4 | 4 | 3 | 4 | 3.8 |
| q07 | Leave policy approval? | 5 | 5 | 4 | 4 | 4.5 |
| q08 | Access control steps? | 5 | 5 | 5 | 5 | 5.0 |
| q09 | Password reset TTL? | 4 | 4 | 4 | 4 | 4.0 |
| q10 | Out-of-scope question? | 5 | 4 | 0 | 1 | 2.5 |
| **Avg** | - | **4.7** | **4.6** | **3.7** | **4.1** | **4.2** |

---

## Analysis

### Strengths ✅
- **Faithfulness high (4.7)**: Model consistently grounded in retrieved chunks
- **Relevance high (4.6)**: Mostly answering correct questions
- **Easy questions perfect (5.0)**: q02, q04, q08 all scored 5/5

### Weaknesses ❌
- **Context Recall (3.7)**: Dense miss exact keywords
  - q05 (account lock): Dense search retrieves "access control" not "account locked"
  - q06 (escalation): Dense miss "escalate" keyword, gets general SLA instead
- **Completeness (4.1)**: Some questions incomplete without all context
- **Out-of-scope (q10)**: Even though model abstains, low score due to missing any relevant context

### Error Patterns
1. **Keyword miss** (q05, q06): Dense semantic search bỊ weak trên exact terms
2. **Section variety** (q05): Document too diverse — need BM25 to find right section
3. **Abstain graceful** (q10): ✅ Model correctly says "no info" instead of bịa

---

## Recommendation

**Baseline OK but improvable.** Avg 4.2/5 is good but recall 3.7 shows density weakness.  
→ **Try Hybrid (Dense + BM25)** for next sprint to boost recall on keyword-heavy queries.

