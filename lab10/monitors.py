"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def wasted_llm_share(trials):
    """S5 (kinh doanh): phần tiền máy (LLM + nền tảng) tiêu vào những ticket mà trợ lý đọc xong
    vẫn phải chuyển người. Tiền này là lỗ thuần: LogiX trả cả tiền máy lẫn công người (10.000đ),
    đắt hơn làm tay. Không cần nhãn: chỉ dùng cost_vnd và status có sẵn trong production."""
    total = sum(float(t.get("cost_vnd") or 0) for t in trials)
    if total <= 0:
        return 0.0
    wasted = sum(float(t.get("cost_vnd") or 0) for t in trials if t.get("status") == "escalated")
    return round(wasted / total, 4)


def _trial_review_units(t):
    rk = t.get("review_kind")
    if rk == "escalated":
        return 1.0
    if rk == "recheck":
        has_note = any(e.get("type") == "decision_note" for e in t.get("events", []))
        return 0.4 if has_note else 1.0
    return 0.0


def max_warehouse_cost_per_ticket_vnd(trials):
    """Chi phí trung bình mỗi ticket (tiền máy + công người) của kho đắt nhất (bỏ qua kho '?')."""
    by_wh = {}
    for t in trials:
        wh = t.get("warehouse")
        if not wh or wh == "?":
            continue
        by_wh.setdefault(wh, []).append(t)
    if not by_wh:
        return 0.0
    costs = []
    for sub in by_wh.values():
        total = sum(t.get("cost_vnd", 0) + _trial_review_units(t) * 10000 for t in sub)
        costs.append(total / len(sub))
    return round(max(costs), 2)


def overlong_ticket_rate(trials):
    """Tỉ lệ ticket có nội dung dài vượt ngưỡng ký tự an toàn của ngân sách LLM (> 1200 ký tự)."""
    if not trials:
        return 0.0
    hits = sum(len(((t.get("ticket") or {}).get("text") or "")) > 1200 for t in trials)
    return round(hits / len(trials), 6)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "wasted_llm_share": wasted_llm_share,
    "max_warehouse_cost_per_ticket_vnd": max_warehouse_cost_per_ticket_vnd,
    "overlong_ticket_rate": overlong_ticket_rate,
}
STARTER_MONITORS = ("escalation_rate",)
