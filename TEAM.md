# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): RiConMaiDinh
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-RiConMaiDinh-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S5

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên             | MSSV        | Vai                        | Trưởng nhóm |
| --- | --------------------- | ----------- | -------------------------- | ----------- |
| 1   | Nguyễn Viết Mạnh Khải | 2A202603664 | **Kỹ sư cổng**             | Nhóm trưởng |
| 2   | Nguyễn Đình Quang     | 2A202603620 | **Sản phẩm và kinh doanh** | Thành viên  |
| 3   | Vũ Đức Anh            | 2A202603573 | **Vận hành và pháp lý**    | Thành viên  |
| 4   |                       |             |                            |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenVietManhKhai-2A202603664

### Phần việc phụ trách

- Vai trong bàn: **Kỹ sư cổng** & **Nhóm trưởng**.
- Thiết lập repo, cấu hình remote `upstream`/`origin`, chạy `lab10.criteria sign` và `lab10.checkpoint`.
- Phiếu A: Câu 1.3 (mục A2 cột Offline — đo lỗi ghi sai ở bước `file_carrier_fault`), mục A5 (thông tin ký tiêu chí).
- Phiếu B: Câu 2.1–2.2 (`B0`, `B1`, `B2`), Pre-mortem nhánh Kỹ thuật (`B6`), Câu 2.6–2.8 (`B7.1–B7.3`, code cổng vòng 1 trong `lab10/guards.py` và 2 behavioral test `--adhoc`), phối hợp chốt quyết định v1 (`B8`).
- Phiếu C (thẻ `S5`): dò trace `S5-70@11`, bổ sung nhánh `Verdict.rewrite` trong `pre_guard` (`lab10/guards.py`), thêm monitor `max_warehouse_cost_per_ticket_vnd` và `overlong_ticket_rate` trong `lab10/monitors.py`, cập nhật `C0`, `C7`, `C8`, `C9`, `C11`, `C12` và gom bài bằng `lab10.check_submission --collect`.

### Đóng góp cụ thể

- Vòng 1: Xây dựng 3 cổng phòng ngừa trong `lab10/guards.py` (`pre_guard` ghim chính sách `H.effective_policy`, `_guard_issue_refund` chặn `fail_open`, kiểm tra `ledger_rows` chống hoàn trùng và đối chiếu quyền lợi `H.entitlement_vnd`, `_guard_carrier_fault` & `_guard_notify_carrier` kiểm tra `H.carrier_at_fault` và lọc trường payload chống lộ PII). Xóa sạch lỗi `T-002@55` ở bộ nền (`pass_rate: 0.9909 → 1.0`) và chặn sẵn `890.000đ` hoàn sai / `20` lỗi oan hãng ở thẻ `S5` ngay từ mốc `prepared`.
- Vòng 2 (`S5`): Bổ sung `_safe_text_char_limit` + `Verdict.rewrite` trong `pre_guard` để rút gọn văn bản dài > 1000 ký tự (giữ phần đầu + cuối và giữ `policy_id`), giúp ticket dài ở kho `HN` (`S5-70`, `S5-73`, `S5-76`) được xử lý tự động thay vì đẩy sang người duyệt tốn `10.200đ/ca` (hạ chi phí kho `HN` từ `4.277đ → 826đ/ticket`). Cài đặt `max_warehouse_cost_per_ticket_vnd` và `overlong_ticket_rate` trong `lab10/monitors.py`, đồng thời dọn hợp nhất với `wasted_llm_share`.
- Có sử dụng trợ lý AI hỗ trợ đọc codebase, rà soát cấu trúc phiếu, gợi ý thiết kế guard/monitor và kiểm tra các lệnh đánh giá; mọi ngưỡng, logic cổng và số liệu đều đã được chạy kiểm chứng trực tiếp trên bộ nền và gói sự cố `S5`.

### Bằng chứng

- Commit: `3cda061` (`TEAM.md`), `edd4615` (Câu 1.3), `692592d` (`Sign acceptance criteria`), `5f1c5f5` (chốt cổng vòng 1 `099239f9` & v1), `4a9abc1` (`pre_guard` rewrite & monitors vòng 2).
- Mã lần chạy:
  - Bộ nền `base`: `R-base-before-20261118-161229-b45eeb` · `prepared`: `R-base-prepared-20261118-164254-337f61` · `after`: `R-base-after-20261118-232104-f25da3` (`110/110` pass, không regression).
  - Thẻ `S5`: `R-S5-after-20261118-173837-ea077d` (thêm `rewrite` + monitor) · `R-S5-after-20261118-232104-f25da3` (sau cắt `HCM-B2B`: `2.446đ/ticket`, `ROI = 3.09`, `0` hoàn sai, `0` lỗi oan, `0` lộ PII) · `R-S5-grade-20261118-232105-f25da3` (`PASS-VISIBLE`, 5/5 mục trên máy đạt ✅).
- Phiếu: mục A2 (1.3), A5; Phiếu B (`B0`, `B1`, `B2`, `B6` Kỹ thuật, `B7.1–B7.3`, `B8`); Phiếu C (`C0`, `C7`, `C8`, `C9`, `C12`).

### Exit ticket

- **Điều học được:** Cổng phòng ngừa cấp hệ thống nằm ngoài model/prompt (ghim policy, kiểm sổ cái `ledger_rows`, lọc PII và tiền xử lý `Verdict.rewrite` trước LLM) ổn định và kiểm soát rủi ro kinh tế/pháp lý chắc chắn hơn nhiều so với việc sửa prompt hay trông chờ model tự đoán đúng.
- **Điều còn chưa chắc:** Trên dữ liệu thật ngoài production, nếu khách đặt phần thông tin quan trọng nằm ở giữa một email rất dài (> 5.000 ký tự) thì việc cắt đầu + cuối ở `pre_guard` có thể làm mất ngữ cảnh; cần theo dõi thêm tỉ lệ lỗi/hoàn thiếu trên các ca `guard_text_rewritten` khi chạy pilot thật.

---

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
