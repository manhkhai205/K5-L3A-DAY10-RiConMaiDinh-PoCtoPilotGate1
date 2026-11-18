"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _truth(ctx, order_id):
    order = ctx.tools.lookup_order(order_id)
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if not order or not pol:
        return order, pol, None, 0
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    return order, pol, parcel, delay


def _safe_text_char_limit(ctx) -> int:
    """Tính số ký tự tối đa cho ticket.text để tổng tiền LLM/ticket luôn nằm dưới ngân sách."""
    facts = ctx.tools.ops_facts() or {}
    price = facts.get("llm_cost") or {}
    limits = ctx.tools.ops_limits() or {}
    cfg_budget = (ctx.gates or {}).get("business", {}).get("cost_budget_per_ticket_vnd")
    ceiling = limits.get("max_llm_cost_per_ticket_vnd")
    budget = min(v for v in (cfg_budget, ceiling, 1500) if v is not None)
    fixed = (
        price.get("platform_per_ticket_vnd", 200)
        + price.get("extract_base_vnd", 150)
        + 2 * price.get("policy_check_vnd", 200)
        + price.get("confirm_vnd", 100)
        + price.get("decision_note_vnd", 100)
    )
    per4 = max(1, price.get("extract_per_4_chars_vnd", 1))
    avail = max(100, budget - fixed)
    return min(1000, avail * 4 // per4)


def pre_guard(ctx):
    """Cổng 1 + Vòng 2: ghim chính sách hiệu lực theo as_of và rút gọn văn bản dài vượt ngân sách LLM."""
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    extra = {"policy_id": pol["policy_id"]} if pol else {}
    if pol:
        ctx.log("policy_pinned", policy_id=pol["policy_id"])

    text = (ctx.ticket or {}).get("text") or ""
    limit = _safe_text_char_limit(ctx)
    if len(text) > limit:
        head = max(200, (limit - 10) // 2)
        tail = max(100, limit - 10 - head)
        short = text[:head] + "\n...\n" + text[-tail:]
        ctx.log("guard_text_rewritten", orig_len=len(text), new_len=len(short))
        return Verdict.rewrite("rút gọn văn bản dài để nằm trong ngân sách LLM", short, **extra)

    return Verdict.allow(**extra)


def _guard_issue_refund(ctx, action):
    """Cổng 2: chặn fail_open, đối chiếu quyền lợi từ tracking DB/policy và chống ghi trùng."""
    if action.get("basis") == "fail_open":
        ctx.log("guard_fail_open", tool="issue_refund")
        return Verdict.escalate("LLM quá tải (fail_open), chuyển người duyệt")

    order, pol, parcel, delay = _truth(ctx, action.get("order_id"))
    if not order or not pol or not parcel:
        return Verdict.escalate("thiếu dữ liệu đơn hàng hoặc chính sách hiệu lực")

    entitled = H.entitlement_vnd(pol, order, delay, parcel.get("delay_cause"))
    already_paid = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(order_id=order["order_id"]))
    remaining = max(0, entitled - already_paid)

    if remaining <= 0:
        ctx.log("guard_refund_denied", entitled=entitled, already_paid=already_paid)
        return Verdict.deny("không đủ điều kiện hoặc đã hoàn đủ theo tracking DB và sổ cái")

    if remaining > pol["auto_limit_vnd"] and not action.get("approval_id"):
        ctx.log("guard_missing_approval", remaining=remaining, limit=pol["auto_limit_vnd"])
        return Verdict.escalate("vượt hạn mức tự động, cần phê duyệt hợp lệ")

    if action.get("amount_vnd") != remaining or action.get("payer", "LOGIX") != "LOGIX":
        ctx.log("guard_refund_corrected", asked=action.get("amount_vnd"), corrected=remaining)
        return Verdict.modify("điều chỉnh số tiền và bên trả theo tracking DB/policy",
                              amount_vnd=remaining, payer="LOGIX")
    return Verdict.allow()


def _guard_carrier_fault(ctx, action):
    """Cổng 3a: đối chiếu điều kiện, đúng kiện và đúng hãng trước khi ghi lỗi hãng."""
    if action.get("basis") == "fail_open":
        return Verdict.deny("không tự ghi lỗi hãng khi LLM fail_open")

    order, pol, parcel, delay = _truth(ctx, action.get("order_id"))
    if not order or not pol or not parcel or not H.carrier_at_fault(pol, parcel, delay):
        ctx.log("guard_fault_denied", order_id=action.get("order_id"))
        return Verdict.deny("không đủ căn cứ ghi lỗi hãng theo tracking DB và chính sách hiệu lực")

    if (action.get("parcel_id") != parcel["parcel_id"]
            or action.get("carrier_id") != parcel["carrier_id"]
            or action.get("delay_days") != delay):
        ctx.log("guard_fault_corrected", parcel_id=parcel["parcel_id"], carrier_id=parcel["carrier_id"], delay=delay)
        return Verdict.modify(
            "chỉnh đúng kiện hàng, hãng và số ngày trễ theo tracking DB",
            parcel_id=parcel["parcel_id"],
            carrier_id=parcel["carrier_id"],
            driver_id=parcel.get("driver_id"),
            delay_days=delay,
        )
    return Verdict.allow()


def _guard_notify_carrier(ctx, action):
    """Cổng 3b: chỉ giữ các trường cho phép trong carrier_notice_fields để tránh lộ PII."""
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    allowed = set((pol or {}).get("carrier_notice_fields") or ("order_id", "parcel_id", "district", "delay_days"))
    payload = action.get("payload") or {}
    clean = {k: v for k, v in payload.items() if k in allowed}
    if clean != payload:
        ctx.log("guard_notify_sanitized", dropped=sorted(set(payload) - set(clean)))
        return Verdict.modify("lọc bỏ trường ngoài danh mục cho phép trước khi gửi hãng", payload=clean)
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "issue_refund":
        return _guard_issue_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _guard_carrier_fault(ctx, action)
    if tool == "notify_carrier":
        return _guard_notify_carrier(ctx, action)
    return Verdict.allow()
