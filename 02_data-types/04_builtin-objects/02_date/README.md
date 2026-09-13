# Built-in: Date — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**`Date`** là built-in object biểu diễn **một khoảnh khắc thời gian** (timestamp — số mili giây từ 1970-01-01 UTC, gọi là **epoch**). Tất cả logic thời gian đều nên nói bằng `Date`, vì JS engine xử lý múi giờ, leap year, DST... hộ bạn.

### Cách hoạt động nội bộ

Bên trong, một Date object chỉ lưu **duy nhất một giá trị**: số nguyên `[[DateValue]]` đếm miliseconds từ epoch UTC. Mọi getter/setter (`getFullYear`, `setHours`...) chỉ là **phép biến đổi** giá trị này theo múi giờ local hoặc UTC. Đây là lý do:

- `new Date()` và `new Date(Date.now())` tương đương.
- So sánh thời gian chính xác nhất là so `getTime()` — pure integer comparison.
- Date vượt range ±8.64×10⁹ ms (≈ ±273 năm) sẽ thành `Invalid Date`.

### Tạo Date — 4 cách chính

```js
new Date();                          // thời điểm hiện tại (local timezone)
new Date(1725012345678);             // từ timestamp (ms) — luôn UTC
new Date("2024-01-01T12:00:00Z");    // từ chuỗi ISO 8601 — Z = UTC
new Date(2024, 0, 1, 12, 30, 0);     // từ thành phần — THEO LOCAL TZ, tháng từ 0!
```

### Các phương thức chính

| Nhóm | Phương thức | Ý nghĩa |
|------|------------|---------|
| **Format** | `toISOString()` | chuỗi ISO 8601 UTC: `"2025-08-30T07:00:00.000Z"` |
| | `toLocaleDateString("vi-VN")` | hiển thị theo locale: `"30/8/2025"` |
| | `toLocaleString()`, `toLocaleTimeString()` | kết hợp ngày + giờ |
| **Timestamp** | `getTime()` / `Date.now()` | ms kể từ epoch |
| **Get (local)** | `getFullYear()`, `getMonth()`, `getDate()`, `getDay()`, `getHours()`, `getMinutes()`, `getSeconds()` | từng thành phần local |
| **Get (UTC)** | `getUTCMonth()`, `getUTCHours()`... | phiên bản UTC |
| **Set** | `setFullYear()`, `setMonth()`, `setDate()`, `setHours()`... | mutate trực tiếp object |
| **Parse** | `Date.parse(str)` | chuỗi → timestamp |

## 📐 Cấu trúc nhóm

```
02_data-types/04_builtin-objects/02_date/
├── README.md         ← bài này
├── app.js            ← demo toISOString, getTime
└── index.html
```

## ✅ Điểm mạnh — Tại sao dùng Date native

| # | Điểm mạnh | Lý do |
|---|-----------|-------|
| 1 | **Timestamp chuẩn hóa toàn cầu** | Số ms từ epoch — so sánh/trừ thời gian là integer math, không bug |
| 2 | **`toISOString()` máy đọc được** | Chuẩn ISO 8601 UTC — format lý tưởng cho API, database |
| 3 | **Locale-aware formatting built-in** | `toLocaleDateString("vi-VN")` — không cần thư viện |
| 4 | **`Date.now()` không allocate object** | Fast path cho measurement, cache-busting |
| 5 | **JSON integration** | `JSON.stringify` tự gọi `toJSON()` → ISO string |
| 6 | **DST/leap year handled** | Engine tính ngày 29/2, giờ tiết kiệm ánh sáng đúng chuẩn |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ | Cách tránh |
|---|-----|-------|-----------|
| 1 | **Tháng bắt đầu từ `0`** | `new Date(2024, 1, 1)` là **1 tháng 2**, không phải tháng 1! | Luôn `month - 1` khi dùng numeric constructor |
| 2 | **Date mutable** | `d.setDate(1)` sửa thẳng object gốc | Clone: `new Date(d.getTime())` |
| 3 | **`==`/`===` so sánh reference, không so thời điểm** | `new Date(0) === new Date(0)` → `false` | So `getTime()`: `a.getTime() === b.getTime()` |
| 4 | **Parse chuỗi không chuẩn khác nhau giữa browsers** | `new Date("12/11/2024")` — browser khác có thể khác kết quả | Chỉ dùng ISO format hoặc thư viện |
| 5 | **Chuỗi không có `Z` được hiểu là UTC, không phải local** | `new Date("2024-01-01")` = nửa đêm UTC ≠ nửa đêm VN | Dùng `new Date(2024, 0, 1)` cho local midnight |
| 6 | **`Invalid Date` không throw** | `new Date("abc").getTime()` → `NaN`, im lặng | Check `Number.isNaN(d.getTime())` |
| 7 | **`getDay()` là thứ trong tuần (0=CN), không phải ngày** | `d.getDay()` → 0-6; `d.getDate()` → 1-31 | Nhớ bảng getter |

```js
// Bẫy 1 minh họa
const feb = new Date(2024, 1, 1);      // tháng 1 (index) = Feb
console.log(feb.getMonth());            // 1
console.log(feb.toLocaleDateString("vi-VN")); // 1/2/2024

// Bẫy 6 minh họa
const bad = new Date("not-a-date");
console.log(bad.toString());            // "Invalid Date"
console.log(Number.isNaN(bad.getTime())) // true — cách detect chuẩn
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Hiển thị "đăng lúc: ..."** — `new Date(post.createdAt).toLocaleString("vi-VN")`.
2. **Tính tuổi / thời gian trước** — `(Date.now() - createdAt) / 86400000` ra số ngày.
3. **Countdown timer** — `deadline.getTime() - Date.now()` trong `setInterval`.
4. **Cache-busting URL** — `?t=${Date.now()}` chặn browser cache.
5. **Đo hiệu năng** — `const t0 = Date.now(); ...; console.log(Date.now() - t0)`.
6. **Date range picker** — validate `start <= end` bằng timestamp comparison.
7. **Scheduling/cron logic** — so `getHours()`, `getDay()` với điều kiện.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Tạo và đọc Date

```js
const now = new Date();
console.log(now.toISOString());   // "2025-08-30T07:00:00.000Z" — UTC
console.log(now.getTime());       // 1756537200000 — ms từ epoch
console.log(Date.now());          // gần bằng getTime(), không allocate

// Các thành phần local
console.log(now.getFullYear());   // 2025
console.log(now.getMonth() + 1);  // 8  — nhớ +1 vì month 0-indexed!
console.log(now.getDate());       // 30
console.log(now.getDay());        // 0-6 (0 = Chủ nhật)
console.log(now.getHours(), now.getMinutes()); // 14, 0
```

### Ví dụ 2: Date từ các nguồn khác nhau

```js
// Từ chuỗi ISO — an toàn nhất, parse nhất quán mọi engine
const iso = new Date("2024-03-15T09:30:00Z");      // 9:30 UTC
const isoLocal = new Date("2024-03-15T09:30:00");  // 9:30 local timezone
const isoDateOnly = new Date("2024-03-15");        // nửa đêm UTC (bẫy!)

// Từ thành phần — local timezone
const local = new Date(2024, 2, 15, 9, 30);  // 15/3/2024 9:30 local
//                                              ^ month 2 = Tháng 3!

// Từ timestamp
const fromTs = new Date(1710495000000);

// UTC cụ thể
const utc = new Date(Date.UTC(2024, 2, 15, 9, 30)); // 9:30 UTC chắc chắn
```

### Ví dụ 3: Tính chênh lệch — đúng cách

```js
function daysBetween(a, b) {
  const ms = Math.abs(b.getTime() - a.getTime());
  return ms / 86_400_000; // 1000 * 60 * 60 * 24
}

const start = new Date("2024-01-01");
const end = new Date("2024-01-15");
console.log(daysBetween(start, end));  // 14

// "time ago" — relative display
function timeAgo(past) {
  const s = Math.floor((Date.now() - past.getTime()) / 1000);
  if (s < 60) return `${s} giây trước`;
  if (s < 3600) return `${Math.floor(s / 60)} phút trước`;
  if (s < 86400) return `${Math.floor(s / 3600)} giờ trước`;
  return `${Math.floor(s / 86400)} ngày trước`;
}
console.log(timeAgo(new Date(Date.now() - 7200000))); // "2 giờ trước"
```

### Ví dụ 4: Clone và add ngày — tránh mutate

```js
const deadline = new Date("2024-12-25T00:00:00");

// ❌ Mutable — sửa thẳng object gốc
// deadline.setDate(deadline.getDate() + 7);

// ✅ Clone rồi mới sửa
function addDays(date, days) {
  const copy = new Date(date.getTime()); // clone an toàn
  copy.setDate(copy.getDate() + days);   // engine tự xử lý month/year overflow
  return copy;
}

const extended = addDays(deadline, 10);
console.log(deadline.toLocaleDateString("vi-VN"));  // 25/12/2024 — gốc giữ nguyên
console.log(extended.toLocaleDateString("vi-VN"));  // 1/1/2025 — tự sang năm!
```

### Ví dụ 5: So sánh và sorting dates

```js
const events = [
  { name: "Tết", date: new Date(2025, 0, 29) },
  { name: "Giỗ tổ", date: new Date(2025, 3, 7) },
  { name: "Quốc khánh", date: new Date(2025, 7, 2) }, // 2/9
];

// ❌ Sai: so Date object là so reference
console.log(new Date(2025, 0, 1) === new Date(2025, 0, 1)); // false

// ✅ Đúng: so getTime() hoặc dùng <, >
console.log(events[0].date < events[1].date); // true — relational dùng valueOf

// ✅ Sort chuẩn
const sorted = [...events].sort((a, b) => a.date - b.date);
console.log(sorted.map(e => e.name));
// ["Tết", "Giỗ tổ", "Quốc khánh"]
```

### Ví dụ 6: Countdown timer — pattern hoàn chỉnh

```js
function startCountdown(targetISO, renderFn) {
  const target = new Date(targetISO);
  const timer = setInterval(() => {
    const diff = target.getTime() - Date.now();
    if (diff <= 0) {
      clearInterval(timer);
      renderFn("Hết giờ!");
      return;
    }
    const d = Math.floor(diff / 86_400_000);
    const h = Math.floor((diff % 86_400_000) / 3_600_000);
    const m = Math.floor((diff % 3_600_000) / 60_000);
    const s = Math.floor((diff % 60_000) / 1000);
    renderFn(`${d}d ${h}h ${m}m ${s}s`);
  }, 1000);
}

// startCountdown("2026-02-17T00:00:00+07:00", console.log);
// → "150d 8h 23m 10s" cập nhật mỗi giây
```

## 🔬 So sánh với alternatives

| Thư viện | Ưu điểm | Nhược điểm | Phù hợp khi |
|----------|---------|------------|-------------|
| **Native Date** | Zero dependency, có mọi nơi | API clunky, mutable, month 0-indexed | Timestamps, format đơn giản |
| **date-fns** | Immutable, tree-shakeable, hàm thuần | Nhiều import lẻ | Dự án vừa/lớn, timezone VN |
| **Day.js** | 2KB, API kiểu moment | Plugin cho timezone/customParse | Thay thế moment.js legacy |
| **Luxon** | Intl-first, timezone robust | Bundle ~70KB | Ứng dụng đa timezone |
| **Temporal** (proposal) | Immutable, đúng design, calendar-aware | Chưa có mọi môi trường (Stage 3) | Tương lai thay thế Date |

## 📊 Performance & Best Practices

- **Dùng `Date.now()`** thay `new Date().getTime()` — không allocate object, nhanh hơn trong loop.
- **Luôn serialize bằng `toISOString()`** — API/database nhận UTC, hiển thị convert local ở client.
- **Không parse chuỗi custom bằng `new Date(str)`** — không chuẩn hóa; dùng regex hoặc thư viện.
- **Cache format function** — `new Intl.DateTimeFormat("vi-VN")` reuse thay vì gọi `toLocaleDateString` lặp lại (mỗi lần gọi tạo formatter mới, chậm ~10x).
- **So sánh bằng timestamp** — `a.getTime() === b.getTime()` hoặc `<`, `>` trực tiếp (tự gọi `valueOf`).
- **Đo hiệu năng chính xác hơn** — dùng `performance.now()` (monotonic, sub-ms) thay `Date.now()`.

## 🔗 Liên kết chéo

- Xem thêm: `02_data-types/04_builtin-objects/` — tổng quan built-in objects
- Xem thêm: `02_data-types/04_builtin-objects/01_math/` — Math cho tính toán ngày/giờ
- Xem thêm: `03_data-structures/04_json/` — Date serialize thành ISO string trong JSON
- Xem thêm: `12_asynchronous-javascript/01_event-loop/03_settimeout-setinterval/` — timer cho countdown
- Tài liệu: [MDN — Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date)
