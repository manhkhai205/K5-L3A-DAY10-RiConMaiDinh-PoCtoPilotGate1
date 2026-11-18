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

## NguyenDinhQuang-2A202603620

### Phần việc phụ trách

- Vai trong bàn: **Sản phẩm và kinh doanh** (Thành viên).
- Phiếu A: Câu 1.1 (`A1` mục tiêu cấp hệ thống), Câu 1.5 (`A3` đọc khoảng tin cậy), Câu 1.6 (`A4` bản tiêu chí thành công, 4 câu hỏi soát, ranh giới đầu ra) và điền/đại diện chốt `config/acceptance_criteria.json`.
- Phiếu B: Câu 2.3 (`B3` bản đồ dữ liệu và ví dụ concept drift `REFUND-v3 → REFUND-v4`), Pre-mortem nhánh Kinh doanh (`B6`), Câu 2.9 (`B7.4` cổng kinh doanh trong `config/operating_gates.json` mục `business`), tham gia chốt quyết định Gate 1 v1 (`B8`).
- Phiếu C (thẻ `S5`): Câu 3.2 (`C5` specification về chi phí/ticket và ngân sách LLM), thêm chỉ số `wasted_llm_share` trong `lab10/monitors.py`, thu hẹp `business.pilot_scope` loại kho sỉ `HCM-B2B` trong `config/operating_gates.json`, viết quyết định Gate 1 v2 (`C12`) và cập nhật `submission/submission.json`.

### Đóng góp cụ thể

- Vòng 1: Xây dựng Bản tiêu chí chấp nhận (`config/acceptance_criteria.json`: `pass_rate_min = 0.9`, `pass_k_min = 0.85`, `wrongful_refund_vnd_max = 0`, `wrongful_carrier_faults_max = 0`, `pii_leaks_max = 0`, `cost_per_ticket_vnd_max = 6000`, `roi_min = 0.3`, `queue_stuck_max = 0`, kèm `decision_rule` cho cả 4 quyết định) và ký trước khi đo. Lập bản đồ dữ liệu + ví dụ concept drift ngày `2026-12-01` (`REFUND-v4`, `B3`); đặt cổng kinh doanh (`daily_refund_cap_vnd = 2000000`, `cost_budget_per_ticket_vnd = 1500`, `roi_min = 0.3`).
- Vòng 2 (`S5`): Phân tích bài toán kinh tế theo phân khúc kho, xác định kho sỉ `HCM-B2B` là nguyên nhân gây lỗ cố định (`10.382đ > 10.000đ` làm tay ở mốc `prepared` dù `pass_rate = 1.0`), thu hẹp `business.pilot_scope` thành `{"mode": "warehouse", "warehouses": ["HN", "HCM", "DN", "CT"], "percent": 100}`, bổ sung monitor `wasted_llm_share` trong `lab10/monitors.py` và hoàn thiện quyết định **Thu hẹp** ở mục `C12` + 3 dòng bắt buộc trong `submission/submission.json` (giảm chi phí/ticket từ `6.541đ → 2.446đ`, `ROI 0.53 → 3.09`).
- Có sử dụng trợ lý AI hỗ trợ rà soát câu chữ phiếu và đối chiếu các bảng số liệu report; mọi ngưỡng tiêu chí, phạm vi kho và quyết định v1/v2 đều do cả bàn thống nhất dựa trên `data/world.json` và số liệu chạy thực tế.

### Bằng chứng

- Commit: `9da517b`, `c6f395a` (Phiếu A `1.1`, `1.5`, `1.6` & `config/acceptance_criteria.json`), `872dc5b` (Phiếu B `B3`, `B7.4` & `business` trong `config/operating_gates.json`), `8a72607` (S5: cắt `HCM-B2B`, `wasted_llm_share`, Phiếu C `3.2`, `C12`, `submission/submission.json`).
- Mã lần chạy: `R-base-prepared-20261118-164254-337f61` (v1), `R-S5-after-20261118-232104-f25da3` (`2.446đ/ticket`, `ROI = 3.09`, độ phủ `0.6`), `R-S5-grade-20261118-232105-f25da3` và `R-S5-grade-20261118-234441-1a9d87` (`PASS-VISIBLE`).
- Phiếu: Phiếu A (`A1` câu 1.1, `A3`, `A4`), Phiếu B (`B3`, `B6` Kinh doanh, `B7.4`, `B8`), Phiếu C (`C5` câu 3.2, `C7` nhánh `[1]`, `C12`).

### Exit ticket

- **Điều học được:** Một trợ lý đạt `pass_rate = 1.0` vẫn có thể là pilot thất bại về mặt kinh doanh nếu phạm vi chạy thử bao gồm phân khúc luôn phải chuyển người duyệt (`HCM-B2B`), vì khi đó doanh nghiệp phải trả cả tiền máy lẫn công duyệt tay; phân tách chi phí theo từng phân khúc (`by_segment`) là bắt buộc trước khi mở rộng.
- **Điều còn chưa chắc:** Khi chính sách `REFUND-v4` có hiệu lực từ `2026-12-01` (giảm `auto_limit_vnd` từ `200.000đ` xuống `100.000đ`), tỉ lệ đơn bán lẻ ở `HN` và `HCM` vượt hạn mức tự động mới có tăng mạnh làm chi phí/ticket vượt ngưỡng `6.000đ` hay không.

---

## VuDucAnh-2A202603573

### Phần việc phụ trách

- Vai trong bàn: **Vận hành và pháp lý** (Thành viên).
- Phiếu A: Câu 1.2 (`A1` mục tiêu từ góc nhìn chị Oanh `NV-OANH` và chị Hạnh `NV-HANH`), Câu 1.4 (`A2` cột Telemetry production không cần nhãn cho hành vi `file_carrier_fault` & `notify_carrier`).
- Phiếu B: Câu 2.4 (`B4` HAZOP vòng 1 trên `file_carrier_fault` + 4 dòng mở rộng ngoài kỹ thuật; `B5` Checklist 9 nhóm việc lần 1 có PIC từng dòng), Pre-mortem nhánh Con người và vận hành & Pháp lý (`B6`), Câu 2.10 (`B7.5` Runbook 1–3, `B7.6` Giờ cao điểm) và điền `operations`, `legal` trong `config/operating_gates.json`.
- Phiếu C (thẻ `S5`): kéo thẻ sự cố, ghi `Thẻ đã bốc: S5`, đo mốc `prepared` ban đầu (`C0` dòng 1, `C1` đối chiếu pre-mortem), dò trace và điền bảng soát lỗi (`C2`), cập nhật bản đồ dữ liệu (`C3.5`), HAZOP thẻ (`C4`), Câu 3.3 giả định môi trường (`C5`), Fault tree trước khi sửa (`C6`), đặc tả thước đo chi phí theo kho (`C8`), Risk register (`C10`), cập nhật checklist & viết Runbook 4–5 (`C11`), siết `operations.stop_conditions` trong `config/operating_gates.json`, khởi tạo `submission/submission.json` và đồng bộ `submission/` chuẩn LF.

### Đóng góp cụ thể

- Vòng 1: Thiết lập cổng vận hành và pháp lý trong `config/operating_gates.json` (`pic: "NV-TUNG"`, `approver_id: "NV-HANH"`, `reviewers_on_shift: 1`, `review_capacity_per_hour: 6`, `max_queue_wait_minutes: 60`, `decision_note: true`, `review_sampling_pct: 10`, chặn PII gửi bên thứ ba trong `pii_fields_blocked_to_third_party` và bật `carrier_fault_requires_recorded_cause: true`). Viết Runbook 1–3 và kịch bản Giờ cao điểm khớp thông số hàng chờ và tác động chi phí/ROI (`+30.000đ`/người trực thêm).
- Vòng 2 (`S5`): Dò trace và phân loại 3 lỗi trên `S5` (`S5-20@11`/`S5-02@11` là lỗi chìm do độ trễ batch `refund_status` so với `ledger_seed`, `S5-50@11`/`S5-70@11` ticket dài đội phí, và `S5-51@11` đơn sỉ `HCM-B2B` luôn escalate); cập nhật bản đồ dữ liệu `C3.5`; viết đặc tả chỉ số chi phí mỗi ticket theo kho (`C8`); bổ sung ngưỡng cắt ngay kho đắt hơn `10.000đ` vào `operations.stop_conditions`; lập 3 dòng Risk register (`C10`) và hoàn thiện Runbook 4–5 (`C11`).
- Có sử dụng trợ lý AI hỗ trợ đọc codebase (`lab10/agent.py`, `lab10/ops.py`, `lab10/tools.py`), đối chiếu `data/world.json`, soạn thảo/rà soát câu chữ trong phiếu và kiểm tra đồng bộ LF/`check_submission`; mọi con số, trace và quyết định vận hành đều được kiểm chứng trực tiếp bằng lệnh chạy của nhóm.

### Bằng chứng

- Commit: `2b54bc8` (Phiếu A `1.2`, `1.4`), `bfd605d` (Phiếu B `B4`, `B5`, `B6`, `B7.5`, `B7.6` & `operations`/`legal` trong `config/operating_gates.json`), `3d0bb01` (Phiếu C `S5`: `C0–C8`, `C10–C11`, `stop_conditions`, `TEAM.md`, `submission.json`), và commit hoàn thiện cuối cùng (`TEAM.md` cá nhân + đồng bộ `submission/`).
- Mã lần chạy: `R-base-before-20261118-161051-bde05c` & `R-base-after-20261118-161320-d2021f` (kiểm thử cổng ops/legal vòng 1), `R-S5-grade-20261118-165530-49e248` (mốc `prepared` trước khi sửa vòng 2), và `R-S5-grade-20261118-234441-1a9d87` (`PASS-VISIBLE`, `0` lộ PII, `0` lỗi oan hãng, `0` ca ùn).
- Phiếu: Phiếu A (`A1` câu 1.2, `A2` câu 1.4), Phiếu B (`B4`, `B5`, `B6`, `B7.5`, `B7.6`), Phiếu C (`C1`, `C2`, `C3.5`, `C4`, `C5` câu 3.3, `C6`, `C8`, `C10`, `C11`).

### Exit ticket

- **Điều học được:** Cổng vận hành và pháp lý trong `config/operating_gates.json` không chỉ là thủ tục giấy tờ mà tác động trực tiếp đến kinh tế và độ tin cậy của hệ thống (như `decision_note: true` + `review_sampling_pct: 10` giảm 60% công kiểm lại và giữ lòng tin người duyệt, còn `carrier_fault_requires_recorded_cause: true` và chặn PII bảo vệ bên thứ ba ở tầng hệ thống).
- **Điều còn chưa chắc:** Ngoài production thật, độ trễ đồng bộ giữa thao tác hoàn tay của CSKH (`T-CSKH-...`) với bảng sổ cái `ledger` (hoặc tần suất nhân viên mất lòng tin chuyển sang kiểm 100%) có thể khác mô phỏng; cần đo lại độ trễ đồng bộ và hàng chờ thực tế của chị Hạnh (`NV-HANH`) trong tuần đầu pilot.
