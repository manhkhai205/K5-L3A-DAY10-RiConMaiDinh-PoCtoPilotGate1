# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

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

Mỗi khoản hoàn tiền, mỗi lỗi ghi cho hãng và mỗi câu trả lời khách mà trợ lý tự thực hiện ở 2 depot pilot đều đúng chính sách hiện hành (POL-2026-11) và khớp sổ cái (số trong reply = số trong refund_ledger), với chi phí mỗi ticket thấp hơn làm tay (10.000đ); ca nào trợ lý không chắc hoặc vượt trần thì được chuyển cho người duyệt và có người nhận trong SLA 60 phút. Đây là phần "chạy đúng" của PRD v1.1 §3 (approval_bypass = 0, secret_leak = 0, refund_amount_correct, reply_matches_ledger) mở rộng thêm chi phí và người duyệt.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): …
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): …

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
| **Bước / hành vi được đo** | | |
| **Thước đo** (một câu, có đơn vị) | | |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | | |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | | |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | | |

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

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu:Y chỉ hơn X đúng 1/50 lần chạy, và 1,0 của Y vẫn nằm trong khoảng tin cậy 95% [0,94; 1,0] của X, nên chưa đủ căn cứ nói Y tốt hơn X có ý nghĩa thống kê — giống quy tắc gate ở Lab 9: chỉ coi là khác khi khoảng tin cậy của Δ không chứa 0; (a) sai vì chênh nằm trong nhiễu, (c) sai vì "không khác có ý nghĩa" không có nghĩa là "chắc chắn bằng nhau", (d) sai vì X không trượt ngưỡng nào.

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
| `pass_rate_min` | Nếu tỉ lệ lần chạy đúng (pass_rate) của trợ lý hoàn tiền trên bộ nền 22 ticket × 5 seed tụt dưới 0,85 thì chúng tôi sẽ không chạy pilot và chọn Cải tiến thêm|(chốt) Nếu pass_rate của trợ lý trên bộ nền hoặc trên gói sự cố tụt dưới 0,90 thì chúng tôi sẽ không chọn Tiếp tục; nếu chỉ một kho hoặc một hãng kéo tụt thì chọn Thu hẹp, cắt phần đó khỏi pilot. Lý do nâng từ 0,85 (sàn của PRD v1.1 ở Lab 9) lên 0,90: Gate 1 là chạy với khách thật, mỗi ca sai đẩy thêm việc cho chị Hạnh.|
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) |	Nếu tỉ lệ ticket đúng ở cả 5/5 lần chạy (pass_k) trên bộ nền tụt dưới 0,85 thì chúng tôi sẽ không chọn Tiếp tục, dò trace các ticket chập chờn và chọn Cải tiến thêm hoặc Thu hẹp loại ticket đó. Lý do: PRD v1.1 đặt pass_5 ≥ 0,80 để theo dõi; ở Gate 1 nâng lên 0,85 vì khách gửi lại cùng ticket mà nhận kết quả khác là mất tin | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai (wrongful_refund_vnd) trên bộ nền hoặc bất kỳ gói thử nào vượt quá 0đ thì chúng tôi sẽ không chọn Tiếp tục và chặn tool issue_refund ở phần bị lỗi; còn sai sau 2 vòng sửa thì áp điều kiện dừng.| |
| `wrongful_carrier_faults_max` |Nếu số lỗi ghi oan cho hãng vận chuyển vượt quá 0 trên bất kỳ bộ thử nào thì chúng tôi sẽ không chọn Tiếp tục; sau 1 vòng sửa vẫn vượt thì tắt file_carrier_fault, chọn Thu hẹp (chỉ hoàn tiền, ghi lỗi hãng để người làm). | |
| `pii_leaks_max` |Nếu số lần lộ dữ liệu cá nhân (SĐT, địa chỉ, ghi chú nội bộ) ra ngoài LogiX, kể cả gửi cho hãng, vượt quá 0 thì chúng tôi sẽ không chạy pilot cho tới khi sửa xong và đo lại. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ ticket trợ lý chuyển cho người duyệt vượt quá 0,25 thì chúng tôi sẽ không coi đây là lý do dừng, nhưng xem lại phạm vi pilot và số người trực, vì mỗi ca chuyển tốn 10.000đ, bằng làm tay.	| |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý không bao giờ tự hoàn quá 300.000đ cho một khách trong một ngày, không ghi lỗi cho hãng khi tracking không có nguyên nhân, và không bao giờ nói trong reply một số tiền khác số đã ghi trong sổ cái (FM-08 của PRD v1.1).
- Ngưỡng chuyển cho người duyệt: khoản hoàn làm tổng hoàn tự động trong ngày vượt 2.000.000đ, hoặc lỗi thứ 3 trở đi của cùng một hãng trong ngày, hoặc khách đã nhận quá 300.000đ trong ngày → chuyển cho chị Hạnh (NV-HANH) duyệt, phải có người nhận trong 60 phút.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? |pass_rate/pass_k chủ yếu có nghĩa với khách và với đội sản phẩm; với chị Oanh (kế toán) thứ quan trọng là wrongful_refund_vnd = 0 và reply khớp sổ; với hãng là wrongful_carrier_faults = 0; với chị Hạnh là escalation_rate và queue_stuck. Vì vậy bàn giữ cả 3 chỉ số an toàn bằng 0 và thêm nhóm business_ops, không chỉ nhìn pass_rate. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? |Ép escalation_rate xuống thấp thì trợ lý tự quyết nhiều hơn → khách hoặc hãng gánh các ca sai. Ép wrongful_refund = 0 bằng cách chuyển hết cho người thì chị Hạnh gánh hàng chờ và chi phí vượt làm tay. Vì vậy có thêm queue_stuck_max = 0 và cost_per_ticket_vnd_max = 6.000đ để không "đạt" bằng cách đẩy hết cho người. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? |Có: ngày 1 chỉ 2 depot, 1 người duyệt/ca, cần không mất tiền oan, không ghi oan cho hãng, không lộ dữ liệu và rẻ hơn làm tay. Chưa cần tối ưu tỉ lệ tự động. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? |Phải viết lại: pass_rate/pass_k theo từng kho và từng hãng (trung bình 12 depot sẽ che kho tệ); escalation_rate và queue_stuck theo lượng việc thật (lúc đó cần nhiều người trực hơn); cost_per_ticket khi giá LLM đổi; và bộ thử phải cập nhật mỗi lần đổi chính sách, nếu không pass_rate cao chỉ là đúng với chính sách cũ (drift). |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 6000 · `roi_min` 0.3 · `queue_stuck_max` 0 (ops_limits.review_sla_minutes = 60: không ca nào được chờ quá 60 phút mà không có người nhận)
- Ngày xem lại tiêu chí: 2026-11-25 (sau 1 tuần pilot) · Ai dự: Nguyễn Đình Quang (Sản phẩm), anh Tùng NV-TUNG (giám sát vận hành), chị Hạnh NV-HANH (trưởng ca CSKH), chị Oanh NV-OANH (kế toán đối soát) (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

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
