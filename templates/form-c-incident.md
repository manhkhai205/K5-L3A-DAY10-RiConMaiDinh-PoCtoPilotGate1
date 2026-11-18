# Phiếu C · Sự cố và quyết định v2 · Khối 3 (phút 125–200)

**Bàn:** K5-L3A-DAY10-RiConMaiDinh-PoCtoPilotGate1 · **Thẻ đã bốc:** S5 *(đã đối chiếu số thẻ bốc từ Lab Coach; lệnh tự kiểm tra in dòng này trong report.)*

Mở `incidents/Sx/card.md` của đúng số đã bốc. Các bước trên thẻ trỏ về đúng mục trong phiếu này. Mục C3 chỉ điền phần ứng với
số thẻ của bàn; các phần khác để trống.

**Mục lục**
- [C0 · Nhật ký lần chạy vòng 2 (suốt khối)](#c0)
- [C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem · phút 125–135 · bước 0 trên thẻ](#c1)
- [C2 · Câu 3.1 · Bảng soát lỗi của thẻ · phút 135–145 · bước 1–2](#c2)
- [C3 · Câu 3.1 · Phần riêng theo thẻ · phút 135–145 · bước 3](#c3)
- [C4 · Câu 3.1 · HAZOP của thẻ (≥ 3 dòng) · phút 145–150 · bước 4](#c4)
- [C5 · Câu 3.2, 3.3 · Specification và giả định môi trường · phút 145–150 · bước 4](#c5)
- [C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa · phút 150–155 · bước 4](#c6)
- [C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn · phút 155–180 · bước 5–7](#c7)
- [C8 · Câu 3.6 · Chỉ số theo dõi mới · phút 155–180 · bước 5](#c8)
- [C9 · Câu 3.7 · Fault tree SAU khi sửa · phút 180–185 · bước 8](#c9)
- [C10 · Câu 3.7 · Risk register (≥ 1 dòng) · phút 180–185 · bước 8](#c10)
- [C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5 · phút 180–185 (runbook có thể xong trong 185–200) · bước 8](#c11)
- [C12 · Quyết định Gate 1 · v2 và ba dòng bắt buộc · phút 185–200 · bước 9](#c12)

---

<a id="c0"></a>

## C0 · Nhật ký lần chạy vòng 2

Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi một dòng vào `runs/journal.jsonl`. Điền cột "Đổi MỘT thứ gì" (tham số `--note`) và "Kết luận".

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | `R-S5-prepared-20261118-165530-49e248` | S5 · prepared | nhận thẻ S5, chưa sửa thêm (đúng cổng vòng 1 `099239f9`) | 1.0 ([1.0, 1.0]) | 1.0 | 0 · 0 · 0 | 0.5 | Cổng vòng 1 xóa sạch 25 ca hoàn sai/trùng (`890.000đ → 0đ`, `20` lỗi hãng → `0`) và chặn LLM vượt trần (`2.412đ → 765đ`), nhưng vẫn lỗ ở kho `HCM-B2B` (`10.382đ > 10.000đ`) và kéo tổng chi lên `6.541đ > 6.000đ`. |
| 2 | `R-S5-after-20261118-173837-ea077d` | S5 · after | thêm `pre_guard` `Verdict.rewrite` cắt gọn ticket dài (`≤ 1000` ký tự) và 2 monitor (`max_warehouse_cost_per_ticket_vnd`, `overlong_ticket_rate`) | 1.0 ([1.0, 1.0]) | 1.0 | 0 · 0 · 0 | 0.4 | `kho HN` giảm mạnh `4.277đ → 826đ`, tổng chi giảm `6.541đ → 5.740đ`, `ROI = 0.74`, chỉ còn duy nhất `kho HCM-B2B` (`10.681đ > 10.000đ`). |
| 3 | `R-S5-after-20261118-232104-f25da3` | S5 · after | thu hẹp `business.pilot_scope` bỏ `HCM-B2B` (chỉ giữ `HN`, `HCM`, `DN`, `CT`) + gộp đủ 3 monitor trong `monitors.py` | 1.0 ([1.0, 1.0]) | 1.0 | 0 · 0 · 0 | 0.0 | Sạch toàn bộ lỗi và trần: `chi phí/ticket = 2.446đ` (`≤ 6.000đ`), `ROI = 3.09`, `tiết kiệm ròng = 135.963đ/ngày`, `độ phủ = 0.6`, `0` ca ùn. |
| 4 | `R-base-after-20261118-232104-f25da3` | base · after | (kiểm không regression trên bộ nền 22 ticket × 5 seed) | 1.0 ([1.0, 1.0]) | 1.0 | 0 · 0 · 0 | 0.2273 | Không làm hỏng ca nào đang đúng (`110/110` pass, `cost = 4.456đ`, `ROI = 1.24`, `vượt trần: không`). |

---

<a id="c1"></a>

## C1 · Câu 3.0 · Mốc prepared và đối chiếu pre-mortem

Chạy **trước khi sửa bất cứ thứ gì**:

```bash
python3 -m lab10.grade --incident Sx
```

- Mã lần chạy grade: `R-S5-grade-20261118-165530-49e248` · base: `R-S5-before-20261118-165530-49e248` · prepared: `R-S5-prepared-20261118-165530-49e248`
- Cổng vòng 1 đỡ được ô / con số nào (so cột base với cột prepared): Cổng vòng 1 đã đỡ được phần lớn lỗi kỹ thuật/an toàn: `pass_rate` tăng `0.8333 → 1.0`, `pass_k` tăng `0.8333 → 1.0`, `tiền hoàn sai` giảm `890.000đ → 0đ` (ngày tệ nhất `178.000đ → 0đ`), `lỗi ghi oan cho hãng` giảm `20 → 0`, `tiền LLM ticket đắt nhất` giảm `2.412đ → 765đ` (nhờ `cost_budget_per_ticket_vnd = 1500`), `tiết kiệm ròng` đảo từ `-60.486đ/ngày` (`ROI -0.33`) sang `+103.770đ/ngày` (`ROI 0.53`).
- Khối kinh doanh và vận hành còn dòng nào vượt trần: Còn 2 điểm đỏ trên gói S5: (1) **Vượt trần:** `kho HCM-B2B: mỗi ticket tốn 10.382đ > làm tay 10.000đ` (`review_rate = 1.0`, 12/12 đơn sỉ đều chuyển người); (2) **Ngưỡng đã ký chưa đạt:** `cost_per_ticket_vnd = 6.541đ > 6.000đ` (trong đó 3 ticket lẻ dài ở `kho HN` là `S5-70`, `S5-73`, `S5-76` bị `cost_budget_per_ticket_vnd = 1500` chuyển sang người duyệt với giá `10.200đ/ticket`, đẩy `kho HN` từ `1.244đ` ở base lên `4.277đ` và kéo `escalation_rate` lên `0.5`).

**Mở lại pre-mortem (Phiếu B mục B6), viết bằng bút khác màu.** Với thẻ S1, S3, S4, S5 đây là một phần của phần riêng theo thẻ.

- Sự cố trên thẻ thuộc lăng kính nào (kỹ thuật, kinh doanh, con người và vận hành, pháp lý)? Thuộc cả 3 lăng kính: **Kinh doanh** (nhóm đơn sỉ `HCM-B2B` luôn lỗ khi tự động hóa; chi phí/ticket vượt trần `6.000đ`), **Kỹ thuật** (hoàn trùng `ledger_seed` / đa kênh, văn bản dài đội chi phí LLM), và **Con người và vận hành** (tỉ lệ chuyển người duyệt vọt lên `0.5` khiến công duyệt `150.000đ/ngày` chiếm phần lớn chi phí).
- Có nằm trong các lý do bàn đã viết không? Nếu có: cổng vòng 1 đã đỡ được bao nhiêu (đọc cột prepared trong report)? Nếu không: vì sao cả bàn không nghĩ tới? **Có một phần (nhưng bỏ sót góc độ phạm vi & chi phí phụ trợ):** Pre-mortem B6 ở vòng 1 đã đoán trúng nhánh hoàn trùng (`Kỹ thuật`) và rủi ro chi phí (`Kinh doanh`: `kho ?` đắt hơn làm tay), nên cổng vòng 1 đã đỡ sạch `890.000đ` hoàn sai và chặn ticket LLM vượt `1.500đ`. Tuy nhiên bàn **không nghĩ tới hai điểm**: (1) Kho sỉ `HCM-B2B` vẫn để `pilot_scope: "all"` nên `100%` đơn sỉ phải trả `platform + LLM + công duyệt = 10.382đ > làm tay`; (2) Cổng `cost_budget_per_ticket_vnd = 1500` chặn đọc LLM nhưng lại đẩy luôn các đơn lẻ dài hợp lệ (`S5-70`, `S5-73`, `S5-76`) sang người duyệt tốn `10.200đ/ticket`, thay vì cắt bớt phần bảng kê thừa trước khi đọc.
- Lý do còn thiếu, thêm bây giờ:

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được bằng gì (trace / data / config nào) |
|---|---|---|
| *(Thêm vòng 2)* Nhóm đơn sỉ (`HCM-B2B`, giá trị ≥ 2 triệu) có quyền lợi luôn vượt hạn mức tự động và thiếu approval sẵn nhưng vẫn nằm trong `pilot_scope`, khiến trợ lý trả thêm phí hệ thống/LLM rồi mới escalate nên luôn đắt hơn làm tay | Kinh doanh | Report `ops.segments["HCM-B2B"]` (`10.382đ/ticket`, `review_rate = 1.0`), `world_patch.json` (`O-2550..O-2561`), `config/operating_gates.json` mục `business.pilot_scope` |
| *(Thêm vòng 2)* Khách dán bảng kê dài (`5.200–7.450` ký tự) khiến cổng ngân sách LLM `1.500đ` đẩy cả ticket lẻ hợp lệ (`S5-70`, `S5-73`, `S5-76`) sang người duyệt tốn `10.200đ/ticket`, làm đội `cost_per_ticket_vnd` lên `6.541đ > 6.000đ` | Kinh doanh · Con người và vận hành | Trace `S5-70@11` ở mốc `prepared` (`business_gate: cost_budget_per_ticket_vnd`), `ops.segments["HN"]` (`1.244đ → 4.277đ`), `ops.cost.review_cost_per_day_vnd = 150.000đ` |

---

<a id="c2"></a>

## C2 · Câu 3.1 · Bảng soát lỗi của thẻ

Dò ít nhất 2 ticket hỏng theo kiểu KHÁC nhau:

```bash
python3 -m lab10.trace --suite Sx --ticket <ID> --seed 11
```

Ba loại lỗi: **giới hạn của hệ thống** · **lỗi ngữ cảnh** · **lỗi chìm** (cả người dùng lẫn hệ thống đều không nhận ra; nguy hiểm nhất,
người chịu hại thường là bên thứ ba). Định nghĩa đầy đủ và ví dụ: Phiếu B mục B2.

**Tác hại của thẻ:** cho ai `CFO / LogiX (lỗ tài chính) & Chị Oanh NV-OANH (đối soát) & Hãng vận chuyển (lỗi oan)` · đo bằng gì `chi phí mỗi ticket (đ), ROI, tiền hoàn sai (đ)` · bao nhiêu ở mốc base `6.083đ/ticket (kho HCM-B2B 11.326đ > làm tay), ROI = -0.33 (lỗ ròng 60.486đ/ngày), hoàn sai 890.000đ, LLM max 2.412đ; ở mốc prepared: còn kho HCM-B2B 10.382đ > làm tay và cost_per_ticket 6.541đ > 6.000đ`

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | `S5-02@11` (base) & `S5-20@11` (base): `S5-20@11` có `SỔ CÁI` ghi thêm `20.000đ` (`05 tool issue_refund`), `LỖI HÃNG` ghi `VNX` 4 ngày (`06 tool file_carrier_fault`) và reply `"LogiX đã hoàn 20.000đ cho đơn O-2520"`, dù `ledger_seed` đã có `T-CSKH-2520` hoàn tay `20.000đ` cho `O-2520`. (`S5-02@11` cũng hoàn lần 2 `25.000đ` cho `O-2501` ngay sau `S5-01` vì gửi qua Zalo). | Khách tưởng được hoàn tiếp (hoặc im lặng); **LogiX mất tiền 2 lần**, **chị Oanh (`NV-OANH`)** lệch sổ đối soát tuần, **hãng `VNX`/`GHSH`** bị ghi 2 lỗi oan cho 1 đơn | cao | **Lỗi chìm** |
| 2 | `S5-50@11` (base) & `S5-70@11` (prepared): Khách dán bảng kê dài `5.227`–`5.473` ký tự (`--- Danh sách hàng và trao đổi trước đó ---`). Ở `base`, `S5-50@11` tốn `2.412đ` LLM (> trần `1.500đ`). Ở `prepared`, `S5-70@11` (`HN`, đơn lẻ hợp lệ `18.000đ`) chạm `02 business_gate cost_budget_per_ticket_vnd` (`next_call: 1518 > 1500`) → `03 result: escalated` tốn `200đ` + `10.000đ` duyệt tay = `10.200đ` (thay vì `~665đ`). | **LogiX / CFO** chịu đội chi phí (`kho HN` vọt từ `1.244đ` lên `4.277đ/ticket`); **chị Hạnh (`NV-HANH`)** phải duyệt thêm ca lẻ không cần thiết | cao | **Giới hạn hệ thống / Lỗi ngữ cảnh** |
| 3 | `S5-51@11` (base & prepared): Đơn sỉ `O-2551` (`HCM-B2B`, `goods_value = 2.350.000đ`) chạy qua `01 llm_extract`, `02 tracking`, `03 policy`, `04 proposal {"amount_vnd": 230000}` rồi dừng ở `05 result {"status": "escalated", "reason": "vượt hạn mức tự động, chưa có phê duyệt", "cost_vnd": 565}` → mỗi ticket tốn `565đ` máy + `10.000đ` người duyệt = `10.565đ` (toàn kho `HCM-B2B` trung bình `10.382đ > 10.000đ` làm tay). | **CFO / LogiX** trả tiền cả trợ lý lẫn người làm tay cho `12/12` đơn ở `HCM-B2B` (`review_rate = 1.0`) | cao | **Lỗi ngữ cảnh** |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 (`S5-20@11`, `S5-02@11`) | Lỗi 2 (`S5-50@11`, `S5-70@11`) | Lỗi 3 (`S5-51@11`) |
|---|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | Không (nhận đúng ý định `LATE`). | **Đúng** (khách dán thêm danh sách/lịch sử dài > 5.000 ký tự làm `read_cost` phình to quá trần, trong khi phần thông tin cần thiết chỉ nằm ở vài dòng đầu). | Không. |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | Liên quan gián tiếp (thiếu bước đọc lịch sử hoàn đã ghi trong sổ cái trong ngày). | **Đúng** (dữ liệu bảng kê sản phẩm đính kèm là nhiễu đối với bước phân loại ý định `LATE`, nhưng vẫn tính đủ tiền token/ký tự). | **Đúng** (thiếu kiểm tra trước xem đơn thuộc nhóm sỉ `HCM-B2B` luôn vượt `auto_limit_vnd` và không có `approval_id`, khiến tự động hóa vô nghĩa). |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | **Đúng** (`T-CSKH-2520` do CSKH hoàn tay đã ghi vào `ledger_seed`, nhưng cờ `order.refund_status` chỉ cập nhật theo batch đêm nên ở `base` trợ lý vẫn ghi đè thêm lần 2 vào sổ cái). | Không. | Không. |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | Không. | Khi nhiều ticket dài cộng dồn ở `prepared`, `cost_budget_per_ticket_vnd` chuyển hàng loạt ca lẻ hợp lệ về người duyệt. | **Đúng (hiệu ứng tích lũy kinh tế)**: `12` đơn `HCM-B2B` luôn escalate kéo chi phí toàn hệ thống vượt ngưỡng `6.000đ` (`6.541đ`). |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 | Lỗi 3 |
|---|---|---|---|
| Vì sao người gặp coi đây là lỗi | Chị Oanh (`NV-OANH`) đối soát cuối tuần thấy cùng 1 đơn `O-2520` / `O-2501` bị chi 2–3 lần tiền thật trên sổ cái; hãng bị ghi nhiều strike cho 1 đơn. | CFO thấy tiền LLM (`2.412đ`) vượt trần `1.500đ` (ở base) hoặc ticket đơn lẻ `HN` vẫn tốn `10.200đ` phí người duyệt dù rất đơn giản (ở prepared). | CFO thấy ở `HCM-B2B` doanh nghiệp trả `10.382đ/ticket` (gồm cả tiền trợ lý lẫn công duyệt tay), đắt hơn `10.000đ` làm tay cũ. |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | Khác: cổng `write_gate` cộng dồn `ledger_rows(order_id=...)` theo thời gian thực thay cho cờ `refund_status` (đã làm ở vòng 1 trong `_guard_issue_refund` và chặn sạch ở `prepared`). | Khác: tiền xử lý ở `pre_guard` (`Verdict.rewrite`) rút gọn/giới hạn độ dài văn bản đưa vào LLM theo ngân sách ký tự (giữ phần đầu + cuối) thay vì đẩy cả ticket lẻ sang người duyệt. | Trao quyền kiểm soát & cấu hình phạm vi: loại kho sỉ `HCM-B2B` khỏi `business.pilot_scope` trong `config/operating_gates.json` (chỉ giữ kho lẻ `HN`, `HCM`, `DN`, `CT`). |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | Ticket trùng (`S5-02`, `S5-03`, `S5-05`, `S5-20`) bị `write_gate` chặn ghi (`denied`), trả lời khách là đơn đã được hoàn; ca hoàn bổ sung (`S5-21`) chỉ bù phần chênh `12.000đ`. | Ticket lẻ dài (`S5-70`, `S5-73`, `S5-76`) được `pre_guard` cắt gọn trước khi gọi LLM nên trợ lý tự hoàn hợp lệ chỉ tốn `~665–800đ`, không làm phiền chị Hạnh (`NV-HANH`). | Toàn bộ ticket kho `HCM-B2B` (`S5-50..S5-61`) đi thẳng luồng làm tay CSKH ngay từ đầu (`0đ` phí nền tảng/LLM, chi phí đúng `10.000đ/ticket`). |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | Theo dõi `duplicate_refund_blocked` / `already_paid` trên sổ cái (đã kiểm soát ở vòng 1). | Theo dõi tỉ lệ ticket vượt trần ký tự/LLM và chi phí mỗi ticket theo kho trong `monitors.py` (mục C8). | Theo dõi **chi phí mỗi ticket theo kho** (`warehouse_max_cost_per_ticket_vnd` / `ops.segments[wh].cost_per_ticket_vnd`) để kịp phát hiện kho đắt hơn `10.000đ`. |

Yêu cầu: ít nhất **hai lỗi có nguồn khác nhau** ở phần 2, và ít nhất một lỗi được xếp đúng là **lỗi chìm**.

---

<a id="c3"></a>

## C3 · Câu 3.1 · Phần riêng theo thẻ (chỉ điền phần của số đã bốc; làm trong khoảng 5 phút)

| Thẻ | Điền phần nào |
|---|---|
| S1 | Mục C1 (đối chiếu pre-mortem) + **C3.5** (mở lại bản đồ dữ liệu: các trường của `parcel`) |
| S2 | **C3.1** Mức kiểm soát của con người |
| S3 | Mục C1 + **C3.5** (bảng `policies`: trường nào là nguồn sự thật về "phiên bản đang hiệu lực"; dòng `delay_cause`) |
| S4 | Mục C1 + mục **Giờ cao điểm** ở Phiếu B mục B7.6 (bổ sung bằng bút khác màu nếu đã viết) |
| S5 | Mục C1 + **C3.5** + mục **C8** dùng cho một con số kinh doanh (chi phí mỗi ticket theo kho) |
| S6 | **C3.2** Hình dung của người và của hệ thống |
| S7 | **C3.3** Hiệu chỉnh lòng tin (người đặt hàng, người nhận hàng) |
| S8 | **C3.4** Hiệu chỉnh lòng tin (nhân viên duyệt, trưởng ca đứng tên) + **một dòng** "hoàn trên hạn mức" ở bảng C3.1 Bước 2 |

### C3.1 · Mức kiểm soát của con người ở từng lệnh ghi (S2; S8 chỉ một dòng)

**Cách làm:** (1) soát các dấu hiệu cho thấy con người **cần giữ nhiều quyền kiểm soát hơn**; (2) lập bảng
*ai · ở việc nào · cần mức kiểm soát nào* (thấp / vừa / cao / chưa rõ), thêm một cột: **hệ thống hiện đang cho mức nào**.
Chỗ hai cột lệch nhau chính là nơi đặt gate.

**Bước 1 · Dấu hiệu cần nhiều quyền kiểm soát hơn (đánh dấu, ghi bằng chứng từ thẻ)**

| Dấu hiệu | Có? | Bằng chứng trong thẻ / data |
|---|---|---|
| Việc này đụng tới lĩnh vực nhạy cảm: tiền, quan hệ kinh doanh với đối tác | | |
| Hệ trọng cao và cách làm bằng AI còn mới với người liên quan: họ muốn nắm quyền lúc đầu để xây lòng tin | | |
| Hệ thống còn lâu mới đạt độ chính xác mong muốn; quyền của con người là biện pháp tạm trong lúc chờ | | |
| Giới hạn hoặc lỗi của hệ thống cần con người sửa lại | | |
| Hoàn cảnh thay đổi khiến con người phải "đặt lại" hoặc "tiếp quản" (phê duyệt hết hạn, bị thu hồi; chính sách đổi) | | |

**Bước 2 · Bảng mức kiểm soát**

| Ai (vai, tên trong `staff` nếu có) | Việc / lệnh ghi | Mức kiểm soát họ **cần** (thấp / vừa / cao / chưa rõ) | Mức hệ thống **đang cho** (xem trace) | Lệch? |
|---|---|---|---|---|
| | `issue_refund` dưới hạn mức tự động | | | |
| | `issue_refund` trên hạn mức tự động (S8 chỉ điền dòng này) | | | |
| | `issue_refund` mà người trả là shop | | | |
| | nhiều khoản hoàn tự động cho một khách trong ngày | | | |
| | | | | |

→ Mỗi dòng "Lệch" là một nhánh của fault tree và một ứng viên cho gate. Ghi rõ gate **trả quyền về cho ai** (chuyển người
duyệt, chờ duyệt, trần).

**Ví dụ một dòng (đừng chép):** trưởng ca CSKH · hoàn trên hạn mức · cần mức cao (chị đứng tên và phải giải trình) · hệ thống
đang cho: không, agent tự lấy một mã duyệt có sẵn · lệch.

### C3.2 · Hình dung của người và hình dung của hệ thống (S6)

**Cách làm:** thảo luận theo nhóm rồi ghi cho **từng nhóm người dùng**: họ là ai, mục tiêu chính là gì, và hiện
nay họ làm việc này **từng bước ra sao**, đồng đều hay mỗi nơi một kiểu. Dòng cuối: **hệ thống đang mang hình dung nào**, đọc từ trace.

| | Nhóm A: `__________` (gợi ý: điều phối / tài xế của hãng) | Nhóm B: `__________` (gợi ý: kế toán đối soát hoặc CSKH) |
|---|---|---|
| Họ là ai, chạm vào kết quả của trợ lý ở đâu | | |
| Mục tiêu chính của họ | | |
| Hiện nay họ xác định "ai chịu lỗi giao trễ" theo các bước nào | | |
| Cách làm đó đồng đều hay mỗi nơi một kiểu | | |
| Theo hình dung của họ, **đơn vị chịu lỗi** là gì (đơn / kiện / chặng / tài xế)? | | |

**Hệ thống đang mang hình dung nào?** (đọc trace một ticket hỏng: `tracking.parcels` so với dòng `file_carrier_fault`)

- Với hệ thống, đơn vị chịu lỗi là: `__________`. Bằng chứng: ticket `______@seed ____`, dòng trace: `__________`.
- Chỗ hai hình dung vênh nhau: `__________`.
- Khi đầu vào không đủ để áp hình dung của con người (không biết kiện nào), hệ thống đang làm gì: `__________`; nên làm gì: `__________`.

→ Mỗi chỗ vênh là một nhánh của fault tree. Gate tốt làm cho hệ thống hành xử theo hình dung của người chịu hậu quả.

### C3.3 · Hiệu chỉnh lòng tin · người đặt hàng và người nhận hàng (S7)

**Cách làm:** đặt ba mốc trên một trục: **không tin · tin vừa đủ · tin quá mức**. Với từng nhóm người, nghĩ ra
một tình huống đẩy họ về mỗi mốc, rồi ghi hai thứ làm lòng tin lệch: **dữ liệu của hệ thống** có liên quan, và **điều người đó
biết hay không biết**. Mục tiêu là lòng tin khớp với việc hệ thống thực sự làm. Người nhận hàng không dùng hệ thống, không ký gì với LogiX.
Chỉ cần hai mốc có trong thẻ; mốc còn lại để trống nếu không có bằng chứng.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** | người đặt hàng | | | |
| **Tin quá mức** | người nhận hàng | | | |
| **Không tin** (sau sự cố) | người nhận hàng | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào rời hệ thống mà người liên quan **không biết** là nó rời đi: `__________` → tới `__________`.
- Để lòng tin khớp thực tế, có hai đường: **giải thích** cho người dùng dữ liệu đi đâu, hoặc **làm cho hệ thống chỉ làm đúng
  điều người ta tưởng**. Với người nhận hàng (không có kênh nào để giải thích), đường khả thi là: `__________`.
- Biện pháp đó là giảm khả năng lộ hay bảo đảm không lộ: `__________`.

### C3.4 · Hiệu chỉnh lòng tin · nhân viên duyệt và trưởng ca đứng tên (S8)

Cùng cách làm như C3.3. Mốc "tin quá mức" là trước kiểm toán, mốc "không tin" là sau kiểm toán.

| Mốc | Nhóm | Tình huống cụ thể (lấy từ thẻ / ticket) | Dữ liệu của hệ thống liên quan (trường nào, đi tới đâu) | Điều người đó biết / không biết |
|---|---|---|---|---|
| **Tin quá mức** (trước kiểm toán) | nhân viên duyệt | | | |
| **Tin quá mức** (trước kiểm toán) | trưởng ca đứng tên | | | |
| **Không tin** (sau kiểm toán) | nhân viên duyệt | | | |
| **Không tin** (sau kiểm toán) | trưởng ca đứng tên | | | |
| **Tin vừa đủ** (trạng thái muốn tới) | cả hai | | | |

**Rút ra:**
- Dữ liệu nào của hệ thống làm lòng tin lệch: `__________`.
- Để người duyệt thôi kiểm tay từng quyết định, họ cần **thấy** gì ở mỗi quyết định, cần **giữ quyền** ở đâu, và
  tỉ lệ kiểm mẫu nào hai bên chấp nhận: `__________`. Ghi các con số đó vào `config/operating_gates.json` mục `operations`.
- Kèm **một dòng** "`issue_refund` trên hạn mức tự động" ở bảng C3.1 Bước 2.

### C3.5 · Mở lại bản đồ dữ liệu (S1, S3, S5; viết bằng bút khác màu)

Mở lại Phiếu B mục B3. Ghi ở đây những dòng đổi so với vòng 1:

| Trường / bảng | Vòng 1 bàn đã coi là (nguồn sự thật / bản sao / chưa hỏi) | Sau khi đọc thẻ thì thấy | Ảnh hưởng tới tiền hay lỗi hãng thế nào |
|---|---|---|---|
| `orders[].refund_status` & `ledger_seed` / `ledger` | Vòng 1 mới ghi `ledger_seed` là dữ liệu đọc và tin `refund_status == "REFUNDED"` là cờ chặn hoàn lại | `order.refund_status` chỉ làm mới theo batch đêm (`agent.py`), chưa phản ánh các ca CSKH hoàn tay trong ngày (`T-CSKH-2520`, `T-CSKH-2521`) hay ca gửi lặp trong ngày (`S5-01` → `S5-02`); **nguồn sự thật duy nhất về tiền đã hoàn là `ledger` (`ledger_rows(order_id=...)`)** | Ở mốc `base` gây hoàn trùng 2–3 lần (`890.000đ` hoàn sai) và ghi lỗi hãng oan `20` lần; cổng vòng 1 dùng `ledger_rows` đã chặn sạch ở `prepared` |
| `orders[].warehouse_id` & `goods_value_vnd` (`HCM-B2B`) | Vòng 1 chưa phân biệt kho sỉ `HCM-B2B` với 4 kho lẻ (`HN`, `HCM`, `DN`, `CT`) khi đặt `pilot_scope: "all"` | Toàn bộ 12 đơn ở `HCM-B2B` (`O-2550..O-2561`) đều có `goods_value ≥ 2.200.000đ` → tiền bồi thường `> auto_limit_vnd (200.000đ)` và chưa có `approval` sẵn, nên `100%` ca đều `escalated` | Mỗi ticket ở `HCM-B2B` tốn thêm `200đ–565đ` tiền máy trên `10.000đ` công người (`10.382đ > làm tay`), kéo `cost_per_ticket` toàn hệ thống lên `6.541đ > 6.000đ` |
| `ticket.text` (độ dài đầu vào) | Vòng 1 chưa hỏi về phân phối độ dài `ticket.text` ngoài 22 ticket ngắn ở bộ nền | Khách gửi qua kênh `email` có thể dán kèm bảng kê hàng / lịch sử trao đổi dài `5.200–7.450` ký tự (`S5-50`, `S5-70`, `S5-73`, `S5-76`) | Ở `base`, phí đọc LLM vọt lên `2.412đ > trần 1.500đ`; ở `prepared`, cổng `cost_budget_per_ticket_vnd = 1500` chuyển luôn các ticket lẻ `HN` sang người duyệt (`10.200đ/ticket`), đẩy chi phí kho `HN` lên `4.277đ` |

---

<a id="c4"></a>

## C4 · Câu 3.1 · HAZOP của thẻ (ít nhất 3 dòng, viết bằng dữ kiện của thẻ)

*Mục riêng, không ghi đè HAZOP vòng 1 ở Phiếu B mục B4. Năm guideword và nghĩa của chúng: xem Phiếu B mục B4.*

Tool chọn phân tích: `pre_guard` / `issue_refund` (luồng chi phí và phạm vi xử lý của thẻ S5)

| Tham số / dòng dữ liệu | Guideword (WRONG / INVALID / INCOMPLETE / PERTURBED / INCAPABLE) | Lệch cụ thể (mã ticket, trường dữ liệu của thẻ) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `ticket.text` (độ dài truyền vào `llm.extract`) | PERTURBED / OVERLONG | `S5-50`, `S5-70`, `S5-73`, `S5-76`: khách dán bảng kê `5.227–7.451` ký tự khiến `read_cost` vượt trần `1.500đ` (`2.412đ` ở base) | Ở `base` tốn tiền LLM vượt trần; ở `prepared` cổng `cost_budget_per_ticket_vnd = 1500` đẩy ca lẻ `HN` sang người duyệt tốn `10.200đ/ca` | Vòng 1 có `cost_budget_per_ticket_vnd = 1500` (chỉ escalate, chưa cắt gọn text) | Trong `pre_guard(ctx)`: nếu `len(text)` vượt ngưỡng ký tự an toàn của ngân sách LLM thì `Verdict.rewrite` giữ phần đầu + phần cuối, giảm `read_cost` trước khi gọi LLM (tầng chặn/tiền xử lý) |
| `business.pilot_scope` (`orders[].warehouse_id = "HCM-B2B"`) | INVALID | `S5-50..S5-61` (`O-2550..O-2561`): kho sỉ `HCM-B2B` có `goods_value ≥ 2.200.000đ` → `100%` đơn vượt `auto_limit_vnd` phải chuyển người duyệt (`review_rate = 1.0`) | LogiX trả `10.382đ/ticket` (`> 10.000đ` làm tay) cho mọi đơn sỉ; kéo tổng chi phí/ticket vượt `6.000đ` | `business.pilot_scope` đang để `"mode": "all"` (chưa lọc kho sỉ) | Đặt `business.pilot_scope` = `{"mode": "warehouse", "warehouses": ["HN", "HCM", "DN", "CT"], "percent": 100}` để kho sỉ `HCM-B2B` đi thẳng làm tay (tầng phạm vi / kinh doanh) |
| `order.refund_status` vs `ledger_rows` | WRONG / INCOMPLETE | `S5-20` (`O-2520`, đã có `T-CSKH-2520` hoàn tay `20.000đ`), `S5-21` (`T-CSKH-2521` hoàn `10.000đ`), `S5-01→S5-02`: cờ `refund_status` cập nhật trễ theo batch đêm | Ở `base` gây hoàn trùng `890.000đ` và `20` lỗi hãng oan, đẩy `ROI` xuống `-0.33` | Cổng vòng 1 `_guard_issue_refund` đã đọc `ledger_rows(order_id=...)` và chặn sạch ở `prepared` | Giữ nguyên cổng `_guard_issue_refund` vòng 1 và bổ sung cảnh báo chi phí theo kho trong `lab10/monitors.py` (tầng chặn + phát hiện) |
| `ops.segments[wh].cost_per_ticket_vnd` (theo dõi vận hành) | INCAPABLE (tự động hóa mất hiệu quả kinh tế) | *(Chưa có cảnh báo tự động theo từng kho trong `monitors.py`)*: nếu một kho bán lẻ mới xuất hiện hàng loạt đơn giá trị cao hoặc ticket dài tương tự `HCM-B2B`, hệ thống sẽ âm thầm lỗ mà `escalation_rate` đơn lẻ không tách rõ theo kho | CFO chỉ phát hiện lỗ sau 2 tuần chạy pilot qua báo cáo kế toán của chị Oanh (`NV-OANH`) | `lab10/monitors.py` mới có mỗi `escalation_rate` tổng thể | Thêm hàm đo chi phí mỗi ticket lớn nhất theo kho trong `lab10/monitors.py` (tầng phát hiện) |

Bắt buộc: ít nhất ba dòng, trong đó **một dòng là nhánh bàn chưa thấy trên trace** lúc viết.

---

<a id="c5"></a>

## C5 · Câu 3.2, 3.3 · Specification và giả định môi trường

### Câu 3.2 · Một specification mà nếu bị vi phạm thì gây ra tác hại trên thẻ

Kiểm được bằng code hoặc bằng một con số trong report: Với mọi nhóm ticket (theo kho) nằm trong phạm vi pilot, chi phí trung bình mỗi ticket qua trợ lý (tiền LLM + nền tảng + công người duyệt nếu bị chuyển) phải ≤ 6.000đ (ngưỡng cost_per_ticket_vnd_max đã ký) và luôn < 10.000đ làm tay; không ticket nào tốn tiền LLM quá 1.500đ (ops_limits.max_llm_cost_per_ticket_vnd); và tổng tiền hoàn cho một đơn không bao giờ vượt quyền lợi của đơn đó theo chính sách hiện hành (không hoàn hai lần). Vi phạm vế đầu là đúng triệu chứng 1 của CFO (kho sỉ HCM-B2B 10.382đ/ticket > 10.000đ làm tay), vế hai là triệu chứng 2 (ticket dài tốn 2.412đ LLM ở mốc base), vế ba là triệu chứng 3 (đơn hoàn hai, ba lần).

Kiểm bằng gì (hàm trong guards.py, dòng report nào): dòng chi phí mỗi ticket (đ) · làm tay, tiền LLM ticket đắt nhất (đ) · trần, số kho đắt hơn làm tay và cột chi phí/ticket trong khối theo kho và hãng của report lab10.eval / lab10.grade; dòng NGƯỠNG ĐÃ KÝ CHƯA ĐẠT: cost_per_ticket_vnd; vế ba kiểm bằng _guard_issue_refund trong lab10/guards.py (cộng ledger_rows(order_id=…) rồi chỉ cho hoàn phần còn lại) và dòng wrongful_refund_vnd. Theo dõi trong production bằng monitor mới wasted_llm_share (lab10/monitors.py).

### Câu 3.3 · Một giả định về môi trường mà người thiết kế đã ngầm tin, nhưng nhiều khả năng sai ngoài thực tế

Giả định (thứ nằm NGOÀI phần mềm): Mọi kho có cùng "kiểu" ticket với kho bán lẻ: đơn giá trị nhỏ, khoản hoàn nằm dưới hạn mức tự động (auto_limit_vnd = 200.000đ của REFUND-v3), nên trợ lý tự xử lý xong được phần lớn ticket.

Vì sao có thể sai: Kho sỉ HCM-B2B bán đơn số lượng lớn, khoản bồi thường gần như luôn vượt 200.000đ (vd S5-51: đề xuất 230.000đ, kết quả escalated vì "vượt hạn mức tự động, chưa có phê duyệt"), nên trợ lý đọc xong vẫn phải chuyển chị Hạnh: LogiX trả cả tiền máy lẫn 10.000đ công người. Từ 2026-12-01 hạn mức tự động của REFUND-v4 còn 100.000đ, nên giả định này sẽ còn sai ở nhiều kho hơn, không chỉ kho sỉ.

---

<a id="c6"></a>

## C6 · Câu 3.4 · Fault tree TRƯỚC khi sửa (mã lần chạy: `R-S5-prepared-20261118-165530-49e248`)

**Khung tư duy.** Đi từ **tác hại** ngược về nguyên nhân, không đi từ lỗi mình tình cờ thấy. Mỗi tầng hỏi "điều gì phải xảy
ra thì điều trên mới xảy ra", nối bằng **HOẶC** (một trong các nhánh là đủ) hoặc **VÀ** (phải đồng thời). Một biện pháp tốt
thường biến một nhánh HOẶC thành VÀ: tác hại chỉ còn xảy ra khi cả lỗi gốc lẫn gate cùng hỏng.

**Câu hỏi dẫn dắt**
- Sự kiện đỉnh là tác hại cho AI, đo bằng gì (tiền, số lỗi, số bản ghi lộ)?
- Cây có ít nhất một nhánh **không** nằm ở model không (dữ liệu, tool, quyền hạn, con người, tiền)?
- **Specification** nào của phần mềm bị vi phạm ở mỗi lá? **Giả định về môi trường** nào (thứ nằm ngoài phần mềm) đã sai?
- Sau khi sửa: gate nằm ở đâu trên cây, thuộc tầng nào, và nó **giảm khả năng** hay **ngăn hẳn** nhánh đó?

Ít nhất hai nhánh ở hai tầng khác nhau (kỹ thuật, kinh doanh, con người); mỗi lá có bằng chứng (ticket@seed, trường dữ liệu, hoặc một dòng của report).

```
[ĐỈNH] Tác hại: Chi phí mỗi ticket qua trợ lý đắt hơn làm tay / vượt ngưỡng (cho ai: CFO & LogiX, đo bằng: cost_per_ticket_vnd theo kho & toàn bộ, wrongful_refund_vnd, ROI)
 └─ HOẶC
 ├─ [1] Đưa nhóm đơn sỉ HCM-B2B luôn phải chuyển người duyệt vào phạm vi pilot · tầng: kinh doanh (phạm vi pilot)
 │ └─ vì: 100% đơn HCM-B2B (goods_value ≥ 2,2tr) vượt auto_limit_vnd 200k và thiếu approval → luôn escalate tốn 200–565đ máy + 10.000đ duyệt · bằng chứng: ticket S5-51@11, ops.segments["HCM-B2B"].cost_per_ticket_vnd = 10382đ (> 10000đ)
 ├─ [2] Khách dán bảng kê dài > 5.000 ký tự làm vọt phí LLM hoặc bị đẩy sang người duyệt · tầng: đầu vào / vận hành
 │ └─ vì: pre_guard không cắt gọn phần bảng kê thừa nên ở base tốn 2.412đ LLM, còn ở prepared cổng cost_budget=1500 đẩy đơn lẻ HN sang người duyệt tốn 10.200đ · bằng chứng: ticket S5-70@11 (prepared), S5-50@11 (base), ops.segments["HN"] tăng 1.244đ → 4.277đ
 └─ [3] Hoàn trùng nhiều lần khi khách nhắn đa kênh hoặc đã hoàn tay trước đó (gây lỗ ở mốc base; đã được cổng vòng 1 chặn ở prepared) · tầng: data / hành động
 └─ vì: agent chỉ đọc cờ order.refund_status cập nhật theo batch đêm thay vì cộng dồn ledger_rows(order_id=...) · bằng chứng: ticket S5-20@11 (ledger_seed T-CSKH-2520) & S5-02@11 (base: wrongful_refund_vnd = 890.000đ, ROI = -0.33)
```

| Lá | Specification bị vi phạm (phần mềm phải làm gì) | Giả định môi trường đã sai (thế giới ngoài phần mềm) |
|---|---|---|
| [1] | Nhóm phân khúc có tỉ lệ tự động hóa ≈ 0% và chi phí dự kiến vượt `manual_cost_per_ticket_vnd` (`10.000đ`) phải bị loại khỏi `business.pilot_scope` để không trả thêm phí nền tảng/LLM | Thiết kế giả định mọi kho trong hệ thống đều có cơ cấu đơn hàng bán lẻ phù hợp với hạn mức tự động `200.000đ` |
| [2] | Hệ thống phải giới hạn độ dài văn bản truyền vào `llm.extract` trong ngân sách ký tự cho phép (hoặc tách phần đầu/cuối) trước khi đẩy ticket lẻ hợp lệ sang người duyệt tốn `10.000đ` | Thiết kế giả định nội dung ticket khiếu nại giao trễ luôn ngắn vài câu như 22 ticket bộ nền, không dán kèm bảng kê hàng nghìn ký tự |
| [3] | Mọi lệnh `issue_refund` bắt buộc kiểm tra số tiền đã chi thực tế trên bảng `ledger` theo thời gian thực (`entitled - already_paid`), không tin vào cờ `refund_status` cập nhật trễ | Thiết kế giả định kênh CSKH tổng đài không hoàn tay trong ngày, hoặc `refund_status` luôn phản ánh tức thời mọi giao dịch hoàn tiền |

**Ví dụ mẫu một nhánh (bộ nền, đừng chép):** đỉnh "hãng VNX nhận lỗi oan cho đơn O-1002" ← [1] agent dùng độ trễ 5 ngày ←
model lấy số trong ticket đè lên DB (`T-002@55`). Spec bị vi phạm: độ trễ dùng để ghi lỗi phải lấy từ tracking DB. Giả định
môi trường sai: "khách ghi đúng số ngày trễ". Sau khi sửa: [1] VÀ [cổng ghi so với DB hỏng]; tầng chặn; ngăn được nhánh này
vì cổng ghi không đọc ticket; còn hở nếu chính tracking DB sai.

---

<a id="c7"></a>

## C7 · Câu 3.5 · Bảng sửa: nguyên nhân → chỗ sửa → giảm hay ngăn

Sửa NGOÀI model, đúng chỗ cho từng nguyên nhân. Code: `lab10/guards.py` (`pre_guard`, `write_gate`). Con số và quy trình:
`config/operating_gates.json` (phạm vi, người trực, trần, ngân sách, kiểm mẫu, ghi chú giải thích, cổng pháp lý). Rồi chạy:

```bash
python3 -m lab10.eval --suite Sx --stage after --note "đổi MỘT thứ: ..."
python3 -m lab10.grade --incident Sx
```

| Nhánh fault tree | Nguyên nhân | Chỗ sửa (hàm + nhánh trong `guards.py`, hoặc khoá trong `operating_gates.json`) | Tầng (phát hiện / chặn / giới hạn thiệt hại / vận hành) | GIẢM khả năng hay NGĂN hẳn? Vì sao | Mã lần chạy sau khi sửa |
|---|---|---|---|---|---|
| [1] | Kho sỉ `HCM-B2B` luôn escalate tốn `10.382đ > 10.000đ` làm tay | `config/operating_gates.json` → `business.pilot_scope` (`mode: "warehouse"`, giữ `["HN", "HCM", "DN", "CT"]`, cắt `HCM-B2B`) + cập nhật `operations.stop_conditions` | Tầng vận hành / giới hạn phạm vi | **NGĂN hẳn** cho kho `HCM-B2B` (ticket ngoài phạm vi không vào agent nên `0đ` phí LLM/platform); chỉ **GIẢM** nếu phát sinh kho sỉ mới chưa khai báo (nhờ `stop_conditions` + monitor C8) | `R-S5-after-20261118-232104-f25da3` (`2.446đ/ticket`, `ROI = 3.09`) |
| [2] | Ticket dài > 5.000 ký tự đẩy đơn lẻ `HN` sang người duyệt tốn `10.200đ` | `lab10/guards.py` → `pre_guard(ctx)` (`_safe_text_char_limit` + `Verdict.rewrite` cắt gọn văn bản giữ đầu + cuối và giữ `policy_id`) | Tầng chặn / tiền xử lý trước LLM | **GIẢM khả năng / NGĂN** đội chi phí do phụ lục dài trên hầu hết ticket; còn hở nếu thông tin cốt lõi bị kẹp đúng giữa phần cắt | `R-S5-after-20261118-173837-ea077d` (`kho HN: 4.277đ → 826đ`) & `R-S5-after-20261118-232104-f25da3` |
| [3] | Hoàn trùng đa kênh / trùng với `ledger_seed` làm mất tiền thật | `lab10/guards.py` → `write_gate` (`_guard_issue_refund` đã chốt ở vòng 1: kiểm tra `ledger_rows(order_id=...)`) | Tầng chặn trước lệnh ghi | **NGĂN hẳn** mọi lệnh hoàn lặp/vượt phần còn lại trên cùng `order_id` đã có trong `ledger` | `R-S5-prepared-20261118-165530-49e248` (`890.000đ → 0đ`) |

---

<a id="c8"></a>

## C8 · Câu 3.6 · Chỉ số theo dõi mới (thước đo → dữ liệu → cách tính)

Thêm **ít nhất một hàm** trong `lab10/monitors.py` và đăng ký vào `MONITORS`. Chỉ số `escalation_rate` có sẵn không tính là chỉ số mới.
Thẻ S5 dùng mục này cho một con số kinh doanh: chi phí mỗi ticket theo kho (tách tiền máy, công người, tiền mất).

| | Chỉ số theo dõi mới của bàn |
|---|---|
| **Tên trong `MONITORS`** | `max_warehouse_cost_per_ticket_vnd` *(cùng với `wasted_llm_share` và `overlong_ticket_rate` đã đăng ký trong `lab10/monitors.py`)* |
| **Bước / hành vi được đo** | Hiệu quả kinh tế tổng hợp theo từng kho (`warehouse`), tách đủ 3 dòng tiền: tiền máy (`cost_vnd`), công người (`review_units × 10.000đ` + phí giữ chỗ chia đều), và tiền mất/sai (nếu đối chiếu được) |
| **Thước đo** (một câu, có đơn vị) | Chi phí vận hành trung bình mỗi ticket của kho đắt nhất trong ngày (đơn vị: `đồng/ticket`), phản ánh kho nào qua trợ lý đang đắt hơn làm tay (`10.000đ`). |
| **Dữ liệu** (trường nào của trial, không có nhãn) | Không dùng nhãn pass/fail; đọc từ danh sách `trials` trong production: `warehouse`, `cost_vnd` (tiền máy + nền tảng), `review_kind` (`"escalated"` = 1.0 ca, `"recheck"` = `0.4` hoặc `1.0` ca theo `decision_note`), đơn giá công duyệt `10.000đ/ca` và phí giữ chỗ ca trực (`30.000đ/người` phân bổ hoặc tính trong tổng chi phí kho). |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Gom các trial theo từng `warehouse` (bỏ qua kho `?` hoặc tách nhóm riêng nếu thiếu `order_id`). Với mỗi kho `w`: `chi_phí_kho(w) = (sum(cost_vnd) + sum(review_units) * 10000) / count(trials in w)`. Chỉ số trả về `max(chi_phí_kho(w))` across các kho có `count >= 1`; nếu không có trial nào trong phạm vi trả về `0`. |
| **Khung thời gian / ngưỡng báo động** | Tổng hợp cuối mỗi ca (`480` phút) và cuốn chiếu 7 ngày. **Ngưỡng vàng:** có kho `> 6.000đ/ticket` (vượt `cost_per_ticket_vnd_max` đã ký) → `NV-OANH` và Sản phẩm kiểm tra phân khúc kho đó; **Ngưỡng đỏ:** có kho `> 10.000đ/ticket` (đắt hơn làm tay) → `NV-TUNG` cắt ngay kho đó khỏi `business.pilot_scope`. |
| **Điểm mù** (chỉ số này KHÔNG thấy gì) | Vì production không có nhãn đúng/sai ngay lập tức nên công thức từ `trials` chưa cộng được khoản "tiền mất do hoàn sai" (chỉ thấy sau khi chị Oanh `NV-OANH` đối soát tuần); ngoài ra nếu một kho bị cắt hoàn toàn khỏi `pilot_scope` thì kho đó không sinh trial nên không hiện trong mẫu số. |
| Giá trị trên bộ nền · trên thẻ (đọc mục `monitor` của report) | `R-S5-grade-20261118-232105-f25da3`: `max_warehouse_cost_per_ticket_vnd`: `base 4586.4 → S5 11325.67` (before) · `base 4646.4 → S5 826.0` (after); `wasted_llm_share`: `0.1617 → 0.4897` (before) · `0.1435 → 0.0` (after); `overlong_ticket_rate`: `0.0 → 0.3` (before) · `0.0 → 0.166667` (after) — cả 3 đều **sáng đèn ✅** |

---

<a id="c9"></a>

## C9 · Câu 3.7 · Fault tree SAU khi sửa (mã lần chạy: `R-S5-after-20261118-232104-f25da3`)

Vẽ lại cây ở C6. Ở mỗi nhánh đã xử lý, thêm một nút `VÀ [gate … hỏng]` và ghi:

```
[ĐỈNH] Chi phí mỗi ticket qua trợ lý đắt hơn làm tay / vượt ngưỡng (hiện tại: 2.446đ/ticket, ROI = 3.09, 0đ hoàn sai)
 └─ HOẶC
 ├─ [1] Đưa nhóm đơn sỉ luôn escalate vào pilot VÀ [gate pilot_scope loại HCM-B2B + monitor max_warehouse_cost_per_ticket_vnd / wasted_llm_share + stop_conditions hỏng]
 ├─ [2] Khách dán bảng kê > 5.000 ký tự làm vọt phí LLM / đẩy duyệt VÀ [gate pre_guard Verdict.rewrite + cost_budget_per_ticket_vnd + monitor overlong_ticket_rate hỏng]
 └─ [3] Hoàn trùng đa kênh / trùng ledger_seed VÀ [gate _guard_issue_refund (ledger_rows) vòng 1 hỏng] (còn hở: nếu chính CSKH chưa kịp nhập khoản hoàn tay vào ledger trước lúc agent chạy)
```

| Nhánh | Gate (hàm trong `guards.py` / khoá config / metric trong `monitors.py`) | Tầng gate (phát hiện / chặn / giới hạn thiệt hại / vận hành) | Giảm hay ngăn? Vì sao | Nhánh còn hở |
|---|---|---|---|---|
| [1] | `config/operating_gates.json` (`business.pilot_scope` = 4 kho lẻ `["HN","HCM","DN","CT"]`, `operations.stop_conditions`) + `monitors.py` (`max_warehouse_cost_per_ticket_vnd`, `wasted_llm_share`) | Tầng vận hành / giới hạn phạm vi + tầng phát hiện | **NGĂN hẳn** cho `HCM-B2B` (đơn sỉ không vào agent, tốn `0đ` tiền máy); **GIẢM** cho các kho khác nhờ monitor phát hiện kịp khi chi phí tăng | Kho mới mở hoặc thay đổi chính sách `REFUND-v4` ngày `2026-12-01` (hạ `auto_limit_vnd` `200k → 100k`) làm một kho lẻ tăng escalate vượt `6.000đ` |
| [2] | `lab10/guards.py` (`pre_guard` dùng `_safe_text_char_limit` + `Verdict.rewrite`) + `business.cost_budget_per_ticket_vnd` (`1500`) + `monitors.py` (`overlong_ticket_rate`) | Tầng chặn / tiền xử lý trước LLM + tầng phát hiện | **NGĂN** tiền LLM vượt trần `1.500đ` (max còn `998đ`) và **GIẢM mạnh** việc đẩy nhầm ca lẻ sang người duyệt (`kho HN: 4.277đ → 826đ`) | Nếu phần lý do/chỉ dẫn quan trọng bị đặt đúng đoạn giữa văn bản dài bị cắt bỏ, hoặc `checkout_note` quá dài vượt phần ngân sách còn lại |
| [3] | `lab10/guards.py` (`write_gate` → `_guard_issue_refund` cộng dồn `ledger_rows(order_id=...)`) | Tầng chặn trước lệnh ghi | **NGĂN hẳn** hoàn trùng trên cùng `order_id` (`wrongful_refund_vnd: 890.000đ → 0đ`, `wrongful_carrier_faults: 20 → 0`) | Hoàn tay bên ngoài chưa kịp đồng bộ vào bảng `ledger` tại thời điểm agent kiểm tra |

---

<a id="c10"></a>

## C10 · Câu 3.7 · Risk register (thêm ít nhất 1 dòng sau sự cố)

| Rủi ro | Khả năng | Tác động | Người phụ trách (PIC, một người) | Dấu hiệu (metric nào, ngưỡng nào) | Xử lý | Ảnh hưởng bước đánh giá | Nhóm chức năng (GOVERN / MAP / MEASURE / MANAGE) |
|---|---|---|---|---|---|---|---|
| Có kho hoặc nhóm đơn mới (tương tự kho sỉ `HCM-B2B` hoặc kho `?`) có tỉ lệ escalate cao khiến chi phí/ticket vượt làm tay (`> 10.000đ`) | Trung bình | Cao (lỗ ròng tài chính, phản đối từ CFO) | `Nguyễn Đình Quang` (phối hợp `NV-OANH`) | `ops.segments[wh].cost_per_ticket_vnd > 10.000đ` hoặc `ops.segments_worse_than_manual ≥ 1` (kèm metric mới trong `monitors.py > 10.000đ`) | Chuyển quyết định từ `Tiếp tục` sang `Thu hẹp`, cắt kho lỗ khỏi `business.pilot_scope` về làm tay | Quyết định Gate 1 v2 chọn **Thu hẹp** (không mở pilot toàn bộ 100%) | **MANAGE** / **MEASURE** |
| Khách gửi ticket dài bất thường (> 5.000 ký tự) khi không bị cắt gọn hoặc `checkout_note` quá dài làm vượt trần LLM `1.500đ` và đẩy sang người duyệt (`10.200đ/ca`) | Cao | Trung bình – Cao (đội chi phí & tăng tải chị Hạnh) | `Vũ Đức Anh` (phối hợp `Nguyễn Viết Mạnh Khải`) | `ops.cost.llm_cost_max_per_ticket_vnd > 1.500đ` hoặc `escalation_rate > 0.25` (trên `monitors.py` và report) | Kiểm tra `pre_guard` cắt gọn đầu/cuối theo ngân sách ký tự và theo dõi ca `business_gate` trong trace | Nếu tỉ lệ chuyển người ở kho lẻ vượt `0.25` hoặc chi phí vượt `6.000đ`, dừng mở rộng và cải tiến pre-processing | **MEASURE** / **MAP** |
| Hoàn tiền trùng do kênh CSKH hoàn tay chưa đồng bộ tức thời với `order.refund_status` trong ngày | Trung bình | Cao (mất tiền thật + lỗi hãng oan + lệch đối soát) | `Phạm Kiều Oanh (NV-OANH)` | `ops.refund.wrongful_refund_worst_day_vnd > 0đ` hoặc `wrongful_carrier_faults > 0` (trong report) | Duy trì kiểm `ledger_rows(order_id=...)` trong `write_gate`; nếu phát sinh ca lọt kiểm mẫu `10%`, `NV-TUNG` tắt `issue_refund` | Bắt buộc giữ cổng kiểm `ledger` ở mọi vòng; nếu `wrongful_refund_vnd > 0` thì không được chọn `Tiếp tục` | **GOVERN** / **MANAGE** |

Quy tắc: **mỗi dòng phải đổi được một quyết định.** Cột "Dấu hiệu" phải là một metric có trong `monitors.py` hoặc trong report.

---

<a id="c11"></a>

## C11 · Câu 3.7 · Cập nhật checklist 9 nhóm việc và Runbook phần 4–5

### Cập nhật checklist (bảng gốc ở Phiếu B mục B5)

Ghi các dòng đổi sau sự cố. Mỗi dòng vẫn phải có một PIC có tên.

| # nhóm | Trạng thái mới (Xong / Chưa / Không áp dụng) | Bằng chứng mới (mã lần chạy, mục phiếu, số trong report) | PIC |
|---|---|---|---|
| 6 (Chi phí) | **Xong** | Đã thu hẹp `business.pilot_scope` bỏ `HCM-B2B` + thêm `pre_guard` `Verdict.rewrite`; ở `R-S5-after-20261118-232104-f25da3`, `cost_per_ticket = 2.446đ ≤ 6.000đ`, `ROI = 3.09 ≥ 0.3`, `tiền LLM max = 998đ ≤ 1.500đ`, `0` kho đắt hơn làm tay | Nguyễn Đình Quang |
| 7 (Vận hành) | **Xong** | Đã cập nhật `operations.stop_conditions` trong `config/operating_gates.json`, hoàn thiện Runbook 4–5 và cài đủ 3 monitor mới trong `lab10/monitors.py` (`max_warehouse_cost_per_ticket_vnd`, `wasted_llm_share`, `overlong_ticket_rate`, đều sáng đèn ✅ ở `R-S5-grade-20261118-232105-f25da3`) | Vũ Đức Anh |
| 8 (Con người, pháp lý) | Xong | Trên gói S5 (`R-S5-prepared-20261118-165530-49e248`), `pii_leaks = 0`, `wrongful_carrier_faults = 0`, thời gian chờ duyệt tối đa `0.0` phút (`0` ca ùn), giữ kiểm mẫu `10%` kèm `decision_note: true` và đứng tên `NV-HANH` | Vũ Đức Anh |

### Runbook 4 · Sau sự cố trên thẻ (vòng 2)

| Câu hỏi | Trả lời |
|---|---|
| Tín hiệu nào ở Runbook 2 (Phiếu B mục B7.5) lẽ ra phải báo trước sự cố này? Nó đã có chưa? | Tín hiệu **"Chi phí mỗi ticket so với làm tay"** (dòng `chi phí mỗi ticket` + khối `theo kho và hãng` trong report) **đã có** từ Runbook 2 vòng 1 với ngưỡng vàng `> 6.000đ` (hoặc có kho `> làm tay`) và ngưỡng đỏ `≥ 10.000đ`. Tuy nhiên ở vòng 1 bàn mới chỉ nhìn `kho ?` (`5` trials) mà chưa có hàm riêng trong `lab10/monitors.py` để tự động báo động kho đắt nhất khi chạy production không có nhãn. |
| Bàn thêm hoặc đổi ngưỡng nào, từ bao nhiêu thành bao nhiêu? | (1) Làm rõ trong `operations.stop_conditions` của `config/operating_gates.json`: bổ sung điều kiện dừng/thu hẹp riêng theo phân khúc **"có kho chi phí/ticket vượt 10.000đ (đắt hơn làm tay) → cắt ngay kho đó khỏi `business.pilot_scope`"**; (2) Đề xuất bổ sung chỉ số giám sát chi phí theo kho trong `lab10/monitors.py` với ngưỡng vàng `> 6.000đ/ticket` và ngưỡng đỏ `> 10.000đ/ticket`. |
| Bàn đổi gì về **người** (số người trực, ai đứng tên, ai được gọi)? | Giữ nguyên `reviewers_on_shift = 1` (`NV-HANH` đứng tên duyệt, công suất `6 ca/giờ`, `0` ca ùn trên cả base và S5), nhưng chuyển toàn bộ `12` ca/ngày của kho sỉ `HCM-B2B` về **đội CSKH làm tay ngay từ đầu** (không đi qua trợ lý) để không mất thêm `200–565đ` tiền máy/ticket lên phần công làm tay `10.000đ` của nhân viên. |
| Bàn đổi gì về **phạm vi** hoặc **quy trình** (kiểm mẫu, ghi chú giải thích, trần)? | **Đổi phạm vi:** thu hẹp `business.pilot_scope` từ `"mode": "all"` sang `"mode": "warehouse"` chỉ chạy pilot cho 4 kho bán lẻ (`HN`, `HCM`, `DN`, `CT`), loại kho sỉ `HCM-B2B`; **Giữ nguyên quy trình tin cậy:** `decision_note: true`, `review_sampling_pct: 10`, `max_queue_wait_minutes: 60`; **Bổ sung tiền xử lý:** đề xuất `pre_guard` cắt gọn ticket quá dài theo ngân sách LLM `1.500đ` trước khi đẩy sang người duyệt. |
| Nói gì với bên thứ ba bị ảnh hưởng (hãng, shop, người nhận, nhân viên duyệt), ai nói, trong bao lâu? | - **Với CFO & chị Oanh (`NV-OANH`):** trong vòng **24 giờ** (trước `17h` như email CFO), `Nguyễn Đình Quang` và `Vũ Đức Anh` gửi lại bảng chi phí tách riêng kho lẻ vs kho sỉ `HCM-B2B` và báo cáo đã chặn hoàn trùng `890.000đ` (`S5-02/03/05/20`) bằng kiểm tra `ledger_rows` thực tế.<br>- **Với hãng vận chuyển (`GHSH`, `VNX`, `MKD`):** `NV-OANH` đối soát và gỡ mọi biên bản lỗi phát sinh ở giai đoạn chưa lắp cổng (nhất là `20` lỗi oan từ các ca hoàn trùng trước khi có cổng vòng 1) trong kỳ đối soát tuần (≤ 7 ngày để không chạm `suspend_after_strikes_7d`).<br>- **Với chị Hạnh (`NV-HANH`, trưởng ca duyệt):** thông báo tách kho sỉ `HCM-B2B` khỏi trợ lý và cắt gọn ticket lẻ dài để giảm tải các ca `escalated` vô ích (giảm tỉ lệ chuyển duyệt từ `50%`). |
| Dữ liệu cá nhân nào đã rời hệ thống mà không thu hồi được? Báo cho ai? | Trên cả 3 mốc (`base`, `prepared`, `after`) của gói S5, **`pii_leaks = 0`** (không có dữ liệu cá nhân người đặt/người nhận nào rời hệ thống sang hãng vận chuyển; `legal.pii_fields_blocked_to_third_party` và `_guard_notify_carrier` vẫn hoạt động bình thường). Không cần gửi thông báo sự cố lộ PII; `NV-TUNG` ghi nhận xác nhận an toàn dữ liệu trong biên bản rà soát tuần. |
| Sự cố lộ ra trước qua số máy đo, phản hồi của người, hay đọc nội dung? Nguồn nào bàn chưa có? | Lộ ra trước qua **phản hồi của người và bảng kế toán tổng hợp sau 2 tuần** (email CFO kèm báo cáo chị Oanh `NV-OANH`: kho sỉ đắt hơn làm tay, ticket dài tốn tiền LLM, đơn hoàn 2–3 lần), chứ không lộ trên `pass_rate` trung bình. Nguồn bàn còn thiếu là **chỉ số chi phí mỗi ticket tách theo từng kho trong `lab10/monitors.py`** chạy cảnh báo tự động cuối mỗi ca. |

### Runbook 5 · Ba kịch bản "nếu … thì …" cho tuần đầu chạy thử thật

1. Nếu số ticket tăng gấp `3` lần trong một giờ thì: Khi hàng chờ vượt `4 ca` hoặc thời gian chờ lâu nhất `> 30 phút`, `NV-TUNG` / `NV-HANH` gọi thêm `1` người dự phòng (nâng công suất `6 → 12 ca/giờ`); nếu vẫn vượt `10 ca/giờ` hoặc chạm SLA `60 phút`, thu hẹp `business.pilot_scope.percent` xuống `50%` (hoặc giữ 2 kho ổn định nhất) và đưa phần dư về xử lý thủ công.
2. Nếu nhà cung cấp LLM lỗi quá `5` phút (hoặc phát sinh `429 RateLimitError` liên tục làm `_guard_issue_refund` / `_guard_carrier_fault` chặn `fail_open` khiến `escalation_rate > 0.50`) thì: `NV-TUNG` chuyển sang chế độ làm tay tạm thời (tắt các công tắc ghi tự động trong `config/switches.json` trong tối đa `5 phút`), chuyển ticket vào hàng chờ CSKH do `NV-HANH` điều phối để khách không bị trả lời sai hoặc chậm quá SLA `60 phút`, chỉ bật lại sau khi lỗi nhà cung cấp LLM ổn định ≥ 15 phút.
3. Nếu người duyệt báo không tin một quyết định của trợ lý thì: `NV-HANH` tạm giữ ca đó để kiểm tra lại `decision_note` và dấu vết `guard` trong trace; nếu phát hiện ca hoàn dùng phê duyệt không hợp lệ hoặc sai căn cứ tracking DB, `NV-TUNG` tắt ngay công tắc thao tác ghi liên quan trong `config/switches.json`, nâng `operations.review_sampling_pct` từ `10%` lên `30%–100%` (tạm thời) trong khi Kỹ sư cổng vá `guards.py` và chị Oanh (`NV-OANH`) đối soát sửa sổ cái.

---

<a id="c12"></a>

## C12 · Quyết định Gate 1 · v2 (phút 185–200)

Quyết định phải khớp bằng chứng và khớp tiêu chí đã ký. Chọn **Tiếp tục** khi report còn dòng vượt trần, hoặc còn ngưỡng đã ký
chưa đạt, là quyết định không đạt. **Thu hẹp**, **Cải tiến thêm**, **Dừng** có lý do và có số thì đều là quyết định đạt.
Cột v1 nằm ở Phiếu B mục B8; không sửa cột đó.

| | **v2** (phút 185–200, SAU sự cố) |
|---|---|
| Commit ký tiêu chí | 692592d |
| Hash chốt cổng vòng 1 | 099239f9 |
| Mã lần chạy dùng làm bằng chứng | thẻ, mốc base: `R-S5-before-20261118-232105-f25da3` · prepared: `R-S5-prepared-20261118-232105-f25da3` · after: `R-S5-after-20261118-232105-f25da3` · eval after: `R-S5-after-20261118-232104-f25da3` · report tự kiểm tra: `R-S5-grade-20261118-232105-f25da3` |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | Mốc after: không còn ("Không vượt trần kinh doanh / vận hành nào. Mọi ngưỡng đã ký đều đạt"). Mốc prepared còn 2 dòng: kho `HCM-B2B`: mỗi ticket tốn `10.382đ > làm tay 10.000đ` và `NGƯỠNG ĐÃ KÝ CHƯA ĐẠT: cost_per_ticket_vnd ≤ 6000` (thực tế `6.541đ`) |
| Kho hoặc hãng có số xấu nhất: `kho HCM-B2B` (mốc `prepared`: `10.382đ > làm tay 10.000đ`) và sau khi cắt chỉ còn 4 kho lẻ (cao nhất là `kho HN: 826đ/ticket` ở mốc `after`). Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Khối "theo kho và hãng" trong output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | Có, và đây chính là lý do đổi quyết định. Trung bình cả gói (`6.541đ`) che mất rằng riêng kho sỉ thì tự động hoá luôn lỗ dù trợ lý không sai một ca nào (`pass 1.0`): ticket ở đó vượt hạn mức tự động nên đọc xong vẫn chuyển người. Bốn kho còn lại sau khi thêm `pre_guard` `rewrite` đều rất rẻ (`712–826đ/ticket`) |
| Quyết định (khoanh một) | **Thu hẹp** *(Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng)* |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | `R-S5-after-20261118-232104-f25da3`: đạt **5/5** chỉ số bắt buộc trên gói S5 (`pass_rate 1.0`, `pass_k 1.0`, hoàn sai `0đ`, lỗi hãng oan `0`, lộ PII `0`), so với `base` (`R-S5-before-20261118-232105-f25da3`: `pass_rate 0.8333`, hoàn sai `890.000đ`, `20` lỗi hãng oan) |
| Bằng chứng 2 | Sau khi cắt kho `HCM-B2B` khỏi phạm vi và thêm `pre_guard` `rewrite`: chi phí mỗi ticket `6.541đ → 2.446đ` (`≤ 6.000đ` đã ký), `ROI 0.53 → 3.09` (`≥ 0.3`), tiết kiệm ròng `135.963đ/ngày`, tỉ lệ chuyển người `0.5 → 0.0`, `0` ca ùn; tiền LLM ticket đắt nhất `998đ ≤ trần 1.500đ` |
| Bằng chứng 3 | Bộ nền sau khi sửa (`R-base-after-20261118-232104-f25da3`): `pass_rate 1.0`, độ phủ `1.0`, không ca mới hỏng (`5 regression ✅`); 3 monitor mới đều sáng đèn (`6 monitor ✅`): `wasted_llm_share` (`base 0.1617 → S5 0.4897` ở before; `0.1435 → 0.0` ở after), `max_warehouse_cost_per_ticket_vnd` (`4586.4 → 11325.67` before; `4646.4 → 826.0` after), `overlong_ticket_rate` (`0.0 → 0.3` before; `0.0 → 0.166667` after) |
| Khớp dòng nào trong `decision_rule` đã ký? |Dòng "Thu hẹp": "3 chỉ số an toàn đều bằng 0, nhưng … một ngưỡng business_ops chưa đạt ở một phần (một kho …): chỉ chạy pilot ở phần đã đạt và ghi rõ phần bị cắt." Ở mốc prepared đúng một ngưỡng business_ops (cost_per_ticket_vnd) trượt và nguyên nhân nằm ở đúng một kho |
| Nếu Thu hẹp: cắt kho nào / còn bao nhiêu phần trăm / mấy người trực, và ticket bị cắt đi đâu |Cắt kho HCM-B2B (business.pilot_scope = warehouse với ["HN","HCM","DN","CT"]); độ phủ trên gói S5 còn 60% (18 ticket/ngày trong phạm vi, 12 ngoài phạm vi); vẫn 1 người trực, 6 ca/giờ, kiểm mẫu 10%. Ticket kho sỉ đi thẳng quy trình làm tay của CSKH (10.000đ/ticket, không tốn thêm tiền máy), không qua trợ lý |
| Nếu Cải tiến thêm: giả thuyết cụ thể (nhánh nào của fault tree) + hạn |(Không áp dụng.) Ghi nhận để xem lại: nếu có phê duyệt trước cho đơn sỉ (approval theo hợp đồng B2B) thì kho sỉ có thể quay lại phạm vi; đo lại trước 2026-12-01 |
| Nếu Dừng: bài học ghi lại |	(Không áp dụng.) |
| Ngày quyết định lại (trừ khi Dừng) |2026-11-25 (sau 1 tuần pilot) và bắt buộc trước 2026-12-01 (REFUND-v4 hạ hạn mức tự động xuống 100.000đ) |
| PIC ký |	Nguyễn Đình Quang (Sản phẩm và kinh doanh) · Nguyễn Viết Mạnh Khải (Kỹ sư cổng, nhóm trưởng) · Vũ Đức Anh (Vận hành và pháp lý) |

**Chỉ ở v2**
- Quyết định đổi hay giữ so với v1? Vì con số nào: Đổi từ Tiếp tục (v1) sang Thu hẹp. v1 chỉ dựa trên bộ nền (chi phí 4.456đ, ROI 1,24, không có kho sỉ), trong khi dòng "Tiếp tục" đã ký đòi đạt cả trên gói sự cố. Trên gói S5, mốc prepared có chi phí mỗi ticket 6.541đ > 6.000đ đã ký và kho HCM-B2B 10.382đ > 10.000đ làm tay, nên giữ Tiếp tục là không khớp tiêu chí.
- Report tự kiểm tra: mã lần chạy `R-S5-grade-20261118-232105-f25da3` (`PASS-VISIBLE`) · ô nào còn đỏ (nguyên nhân × tầng): không còn ô đỏ (`integrity`, `criteria`, `visible`, `regression`, `monitor` đều ✅; `hidden` do team chấm chạy). Ở mốc `prepared`, ô đỏ là `kinh doanh × phạm vi pilot` (kho sỉ đắt hơn làm tay) và `đầu vào × vận hành` (ticket dài ở `HN` bị đẩy duyệt), không phải lỗi model.
- Cổng vòng 1 (mốc prepared) đã đỡ được gì trước khi bàn biết sự cố, và bỏ sót gì: Đỡ được phần lớn 2/3 triệu chứng của CFO trước khi biết thẻ: (2) ticket dài: trần `cost_budget_per_ticket_vnd = 1.500đ` hạ tiền LLM ticket đắt nhất từ `2.412đ → 765đ` (vòng 2 thêm `pre_guard` `Verdict.rewrite` để giữ luôn ca lẻ `HN` ở `826đ/ticket` thay vì đẩy sang người duyệt `10.200đ`); (3) hoàn hai, ba lần: `_guard_issue_refund` trừ phần sổ cái đã hoàn của đơn, đưa hoàn sai từ `890.000đ → 0đ` và lỗi hãng oan `20 → 0`. Bỏ sót (1): kho sỉ đắt hơn làm tay, vì vòng 1 bàn để `pilot_scope = all` và bộ nền không có kho sỉ.
- Report ghi "được phép cân nhắc Tiếp tục" hay "không đủ căn cứ"? Quyết định của bàn có khớp không: Mốc `after` ghi "Được phép cân nhắc 'Tiếp tục'", nhưng chỉ vì phạm vi đã bị cắt; trên toàn bộ phạm vi (`prepared`) report ghi "KHÔNG đủ căn cứ để chọn 'Tiếp tục'". Vì vậy bàn chọn **Thu hẹp**: đúng nghĩa là Tiếp tục trên phần đã đạt, có ghi rõ phần bị cắt, không phải Tiếp tục toàn bộ.
- Một thứ bộ thử hôm nay chưa đo, và nó ảnh hưởng quyết định ra sao: Lượng ticket thật mỗi kho mỗi ngày. Report tính tiền cho một ngày giả lập (`18` ticket trong phạm vi). Nếu kho `HN` (hiện `826đ/ticket`, cao nhất trong 4 kho còn lại) hoặc các kho bán lẻ thật phát sinh nhiều đơn giá trị cao khi `REFUND-v4` hạ hạn mức xuống `100.000đ` ngày `2026-12-01`, tỉ lệ chuyển người tăng có thể đẩy chi phí vượt `6.000đ` và buộc phải thu hẹp tiếp hoặc thêm người trực.

**Ba dòng bắt buộc** (chép nguyên ba câu này sang `submission/submission.json`, mục `three_lines`)
1. Một giả định về môi trường mà thiết kế của đội đang dựa vào, có thể sai ngoài thực tế: Mọi kho có ticket kiểu bán lẻ với khoản hoàn dưới hạn mức tự động 200.000đ nên trợ lý tự xử lý xong được, trong khi kho sỉ HCM-B2B gần như luôn vượt hạn mức (vd S5-51: 230.000đ) và từ 2026-12-01 hạn mức còn 100.000đ.
2. Gate của đội chỉ GIẢM khả năng hay thực sự NGĂN được tác hại? Vì sao: NGĂN được tiền mất (cổng sổ cái chặn mọi khoản vượt quyền lợi của đơn: hoàn sai 890.000đ → 0đ) và ngăn ticket vượt 1.500đ tiền LLM (pre_guard cắt gọn văn bản dài và trần ngân sách chặn trước khi đọc: max 998đ), nhưng chỉ GIẢM lỗ chi phí: cắt kho sỉ đưa chi phí từ 6.541đ xuống 2.446đ/ticket (ROI 3.09), còn kho khác vẫn có thể đắt lên khi tỉ lệ chuyển người tăng, nên phải theo dõi bằng monitor wasted_llm_share và max_warehouse_cost_per_ticket_vnd.
3. Vì data là mock, cần đo lại gì trong pilot thật trước Bước đánh giá 2: chi phí thật mỗi ticket theo từng kho (tiền LLM thật theo độ dài ticket và công duyệt thật của chị Hạnh), tỉ lệ ticket mỗi kho vượt hạn mức tự động, và tiết kiệm ròng/ROI theo lượng ticket thật mỗi ngày, đo lại trước và sau 2026-12-01 khi REFUND-v4 có hiệu lực.
