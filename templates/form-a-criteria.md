# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-RiConMaiDinh-PoCtoPilotGate1 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> …

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Vì trợ lý theo PRD v1.1 (§2, §6) mới kiểm trên `MockLLM` và chưa đối soát thực tế, 100% bút toán hoàn tiền trên sổ cái (đúng số tiền, đúng bên chịu trả `LOGIX`/`MERCHANT`, đúng mã phê duyệt hợp lệ) và mọi biên bản lỗi hãng do trợ lý ghi phải khớp chứng từ thực tế, không phát sinh hoàn sai, lệch lời nhắn với sổ cái hay ghi lỗi oan khiến hãng vận chuyển và shop khiếu nại khi chốt sổ hàng tuần (`NV-OANH`).
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Theo đúng ranh giới phạm vi ở PRD v1.1 (§2), trợ lý chỉ chuyển sang hàng chờ duyệt những ca thật sự cần phán quyết của con người (vượt hạn mức tự động, thiếu phê duyệt hợp lệ hoặc ngoài phạm vi pilot) kèm đủ căn cứ/ghi chú rõ ràng để chị Hạnh (`NV-HANH`) nhận xử lý kịp SLA 60 phút với công suất 6 ca/giờ/người, không làm ngập hàng chờ giờ cao điểm và không phải đứng tên chịu trách nhiệm cho các khoản hoàn dùng phê duyệt không hợp lệ.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | | Ghi nhận lỗi giao trễ và gửi thông báo cho bên thứ ba là hãng vận chuyển (`file_carrier_fault` và `notify_carrier`) |
| **Thước đo** (một câu, có đơn vị) | | Tỉ lệ (%) biên bản lỗi hãng vận chuyển do trợ lý tạo bị hãng gửi khiếu nại bác bỏ hoặc bị kế toán đối soát (`NV-OANH`) đảo bút toán trên tổng số biên bản lỗi trợ lý đã ghi trong kỳ. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | | Không có nhãn ground-truth trong production; dùng tín hiệu đối chứng từ bảng nhật ký lỗi `faults` (theo `carrier_id`, `order_id`, `parcel_id`) đối chiếu với kênh khiếu nại của hãng vận chuyển và kết quả đối soát tuần của chị Oanh (`NV-OANH`) trên 100% ca trợ lý đã ghi lỗi. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | | `(Số biên bản lỗi do trợ lý ghi bị hãng khiếu nại bác bỏ hoặc kế toán hủy khi đối soát) / (Tổng số biên bản lỗi trợ lý đã xuất trong các ca đã đến kỳ đối soát) × 100%`. Ca mới phát sinh chưa qua hạn đối soát hoặc đang chờ hãng phản hồi được tách khỏi mẫu số kỳ hiện tại và theo dõi ở kỳ sau; nếu mẫu số = 0 thì ghi `"N/A (0 lượt ghi lỗi)"`. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Theo dõi cuốn chiếu 24 giờ và tổng hợp theo chu kỳ 7 ngày (khớp ngưỡng đình chỉ `suspend_after_strikes_7d` của các hãng, như `GHSH`/`DNB` là 3 lỗi/7 ngày). Ngưỡng vàng: > 0% (≥ 1 ca bị hãng bác bỏ trong 24h) → báo ngay `NV-OANH` và `NV-TUNG` rà soát; Ngưỡng đỏ: ≥ 2 ca/ngày hoặc có hãng chạm ngưỡng cảnh báo đình chỉ 7 ngày → dừng tự động `file_carrier_fault`. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | | (1) Có độ trễ từ lúc ghi lỗi đến khi hãng phát hiện và khiếu nại (nhất là với lỗi nhỏ hoặc hãng lớn ít rà ngay như `VNX`); (2) Không thấy các thiệt hại bên ngoài không đi qua bảng `faults`, như lộ thông tin cá nhân người nhận sang hãng qua `notify_carrier`, hoàn trừ nhầm ví `MERCHANT` mà shop chưa phản ánh, hoặc hoàn thừa khiến LogiX chịu lỗ. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | | |
| `wrongful_refund_vnd_max` | | |
| `wrongful_carrier_faults_max` | | |
| `pii_leaks_max` | | |
| nên có: `escalation_rate_max` | | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): ____
- Ngưỡng chuyển cho người duyệt: ____

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` ____ · `roi_min` ____ · `queue_stuck_max` ____
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
