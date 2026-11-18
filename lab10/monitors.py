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
    đắt hơn làm tay. Không cần nhãn: chỉ dùng cost_vnd và status có sẵn trong production.
    0 = không phí đồng nào; càng gần 1 thì tự động hoá càng chỉ thêm chi phí."""
    total = sum(float(t.get("cost_vnd") or 0) for t in trials)
    if total <= 0:
        return 0.0
    wasted = sum(float(t.get("cost_vnd") or 0) for t in trials if t.get("status") == "escalated")
    return round(wasted / total, 4)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "wasted_llm_share": wasted_llm_share,   # S5: tỉ lệ tiền máy tiêu vào ticket đọc xong vẫn chuyển người
}
STARTER_MONITORS = ("escalation_rate",)