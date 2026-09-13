# Lịch sử ngắn gọn của JavaScript — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

JavaScript ra đời năm **1995**, do **Brendan Eich** tạo ra tại **Netscape Communications Corporation** — ban đầu chỉ là một ngôn ngữ kịch bản nhỏ cho trình duyệt, được phát triển trong khoảng **10 ngày**. Từ một công cụ khiêm tốn, nó trở thành một trong những ngôn ngữ phổ biến nhất thế giới, minh chứng cho **"Định luật Atwood"**: *"Bất kỳ ứng dụng nào có thể được viết bằng JavaScript, cuối cùng sẽ được viết bằng JavaScript."* — Jeff Atwood, đồng sáng lập Stack Overflow.

### Timeline lịch sử chi tiết

| Năm | Sự kiện | Ý nghĩa |
|-----|---------|---------|
| **1995** | Brendan Eich tạo JS tại Netscape; tên đầu là **Mocha**, đổi thành **LiveScript** | Ngôn ngữ kịch bản đầu tiên cho trình duyệt web |
| **1996** | Đổi tên thành **JavaScript** (mượn danh tiếng Java dù không liên quan); Netscape 2.0 ra mắt | Marketing decision — tên gây hiểu lầm phổ biến đến nay |
| **1997** | Gửi chuẩn hóa cho **ECMA International** → **ECMAScript 1 (ES1)** | Bắt đầu quá trình chuẩn hóa, tránh Fragmentation |
| **1998** | **ES2** — đồng bộ với ISO/IEC 16262 | International standard hóa |
| **1999** | **ES3** — thêm regex, `try/catch`, improved string handling | Phiên bản đầu tiên được hầu hết trình duyệt hỗ trợ rộng |
| **1999–2009** | "**Thập kỷ im lặng**"; dự án **ES4** bị từ bỏ (chính trị + độ phức tạp) | ES4 tham vọng quá mức (static typing, class, module) gây chia rẽ |
| **2006** | **Ecma International** thành lập **TC39** (Technical Committee 39) | Ủy ban chuyên trách phát triển ECMAScript |
| **2009** | **ES5** — `"use strict"`, `JSON`, `Array.prototype` methods, `Object.create` | Bước ngoặt chất lượng — strict mode, better object manipulation |
| **2009** | **Node.js** ra đời bởi Ryan Dahl | JavaScript chạy được trên server, không chỉ browser |
| **2015** | **ES6 / ES2015** — bước ngoặt lớn nhất: `let`/`const`, `class`, arrow, `Promise`, `import`/`export`, destructuring, spread, template string, `Map`/`Set`, `Symbol`, generator | Kỷ nguyên hiện đại của JavaScript |
| **2016** | **ES2016** — `**` (lũy thừa), `Array.prototype.includes` | increments nhỏ |
| **2017** | **ES2017** — `async`/`await`, `Object.values()`/`Object.entries()`, `padStart`/`padEnd` | Async programming đạt maturity |
| **2018–2024** | **ES2018→ES2024** — Optional chaining `?.`, nullish coalescing `??`, private class fields `#`, `Array.at()`, top-level await, `matchAll`, pipeline operator (stage) | Tinh chỉnh, năng suất developer |
| **ESNext** | Tên gọi động cho phiên bản đang phát triển (Stage 0–3 proposals) | Không phải bản release cụ thể |

### Vì sao ES4 thất bại?

ES4 (2007) tham vọng quá mức: static typing, class, module, pattern matching, coroutines. Cộng đồng chia rẽ thành hai phe:
- **Phe ES4** (Mozilla, Opera): muốn nâng cấp lớn.
- **Phe ES3.1** (Google, Microsoft, Yahoo): muốn nâng cấp nhẹ, ổn định.

Kết quả: ES4 bị hủy, thay vào đó ES3.1 được phát triển và trở thành **ES5 (2009)**. Nhiều ý tưởng của ES4 (class, module) cuối cùng được "hồi sinh" vào **ES6 (2015)** với cách tiếp cận thận trọng hơn.

### Quá trình chuẩn hóa — TC39

TC39 (Technical Committee 39) là ủy ban gồm đại diện từ Google, Mozilla, Microsoft, Apple, Google, Facebook… họp hàng tháng để phê duyệt tính năng mới. Quy trình gồm **4 giai đoạn (stages)**:

```
Stage 0 (Strawman)  →  Ý tưởng, thảo luận mở
       ↓
Stage 1 (Proposal)  →  Được chấp nhận nghiên cứu, có sponsor
       ↓
Stage 2 (Draft)     →  Spec初步, API có thể thay đổi
       ↓
Stage 3 (Candidate) →  Spec gần như cuối cùng, browser bắt đầu implement
       ↓
Stage 4 (Finished)  →  Chính thức đưa vào ECMAScript standard
```

Chỉ tính năng đạt **Stage 4** mới được đưa vào chuẩn ECMAScript chính thức. Tính năng ở stage thấp có thể bị thay đổi hoặc bỏ mà không báo trước.

## 📐 Cấu trúc kiến thức

```
02_history-of-javascript/
├── README.md                 ← bài tổng quan này
│   ● Lịch sử 1995 → nay
│   ● Bảng timeline
│   ● ES4 thất bại và bài học
│   ● Quy trình TC39 4 stages
│   ● Tầm quan trọng của hiểu lịch sử
```

## ✅ Điểm mạnh — Tại sao nên hiểu lịch sử

| # | Lợi ích | Giải thích |
|---|---------|-----------|
| 1 | **Giải thích được các "bẫy" kỳ lạ** | `typeof null === "object"`, `NaN !== NaN` — là di sản từ những ngày đầu |
| 2 | **Hiểu vì sao ES6 đổi nhiều đến vậy** | ES4 thất bại → TC39 thận trọng hơn → ES6 được thiết kế kỹ lưỡng |
| 3 | **Dự đoán xu hướng tương lai** | Biết quy trình TC39 → biết tính năng nào sắp ra đời |
| 4 | **Ra quyết định transpile hay không** | Hiểu version history giúp chọn target ES cho Babel |
| 5 | **Tự tin phỏng vấn** | Câu "Nêu lịch sử và các phiên bản JavaScript" xuất hiện trong hầu hết interview |
| 6 | **Hiểu quan hệ ECMAScript – JavaScript** | ECMAScript là chuẩn, JavaScript là implementation — tên khác nhau nhưng cùng một ngôn ngữ nền |
| 7 | **Đánh giá được "cũ/mới" của tính năng** | Biết method nào có từ ES5 (an toàn) hay ES2020 (cần polyfill) |
| 8 | **Hiểu vai trò của Node.js** | JavaScript không còn giới hạn ở browser — chạy được backend, desktop, mobile |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ |
|---|-----|-------|
| 1 | **JavaScript ≠ Java** | Chỉ trùng tên vì mục đích marketing; hai ngôn ngữ hoàn toàn khác nhau về cú pháp, kiểu dữ liệu, runtime |
| 2 | **ES4 bị hủy → hiểu sai quy trình** | ES4 không "thất bại vô nghĩa" — nó cho thấy TC39 cần quy trình stage rõ ràng hơn |
| 3 | **ES6 = ES2015 — cùng một thứ** | Nhiều người gọi "ES6" nhưng tên chính thức là ES2015; từ đó mỗi năm có tên năm |
| 4 | **Tính năng mới không phải browser nào cũng hỗ trợ** | Optional chaining (ES2020) chưa support trên Safari cũ — cần kiểm tra compat-table |
| 5 | **Không phải mọi "proposal" đều thành chuẩn** | Pipeline operator `|>` đang ở Stage 2 — cú pháp có thể đổi |
| 6 | **ES3 (1999) vẫn là nền tảng quan trọng** | Nhiều legacy codebase chạy trên ES3-only environment (IE6/7) |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Giải thích cho đồng nghiệp** vì sao một bug kỳ lạ tồn tại — ví dụ `typeof null === "object"`.
2. **Ra quyết định transpile** — biết tính năng nào từ ES version nào để set target trong Babel/tsconfig.
3. **Chọn thư viện tương thích** — hiểu tính năng nào có từ ES2015 vs ES2020 để tránh polyfill không cần thiết.
4. **Theo dõi tính năng mới** — đọc TC39 proposal blog, biết stage của tính năng sắp ra mắt.
5. **Phỏng vấn kỹ thuật** — câu hỏi kinh điển về lịch sử và phiên bản JS.
6. **Debug legacy code** — nhận diện code viết cho ES5 vs ES6 qua cú pháp (`var` vs `let`, function vs arrow).
7. **Đánh giá risk khi dùng tính năng Stage 2** — chưa ổn định, có thể bị thay đổi hoặc drop.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cú pháp qua các thời kỳ

```js
// ── ES3 (1999) — var, function declaration, regex, try/catch ──
var tuoi = 30;
function chao(ten) {
  return "Xin chào, " + ten;
}
try {
  var result = chao("Nam");
} catch (e) {
  console.log("Lỗi:", e.message);
}

// ── ES5 (2009) — strict mode, JSON, Array methods ──
"use strict";
var obj = JSON.parse('{"ten": "Nam", "tuoi": 30}');
var keys = Object.keys(obj);            // ["ten", "tuoi"]
var mapped = keys.map(function(k) {     // map callback là function expression
  return obj[k];
});

// ── ES6 / ES2015 (2015) — bước ngoặt lớn ──
let ten = "Nam";
const getTuoi = () => 30;              // arrow function
console.log(`Xin chào ${ten}, ${getTuoi()} tuổi`);  // template literal

// ── ES2017 (2017) — async/await ──
async function layDuLieu() {
  const response = await fetch("/api/user");
  const data = await response.json();
  return data;
}

// ── ES2020 (2020) — optional chaining, nullish coalescing ──
const cauHinh = { server: { port: 3000 } };
console.log(cauHinh?.server?.port ?? 3000); // 3000
```

### Ví dụ 2: Minh họa sự tiến hóa của Array methods

```js
// ES5: forEach với function expression
[1, 2, 3].forEach(function(n) {
  console.log(n);
});

// ES6: arrow function + map
const doubled = [1, 2, 3].map(n => n * 2);

// ES2016: includes (thay indexOf > -1)
console.log([1, 2, 3].includes(2)); // true

// ES2019: flat + flatMap
const nested = [1, [2, [3, 4]]];
console.log(nested.flat(2)); // [1, 2, 3, 4]
```

### Ví dụ 3: Kiểm tra hỗ trợ trình duyệt

```js
// Check thủ công: tính năng có tồn tại không?
console.log("at" in Array.prototype);          // true (ES2022)
console.log("group" in Array.prototype);        // true (ES2024 proposal)
console.log("replaceAll" in String.prototype); // true (ES2021)

// Dùng feature detection thay vì browser sniffing
if (typeof IntersectionObserver !== "undefined") {
  // dùng IntersectionObserver — ES2018
} else {
  // fallback cho trình duyệt cũ
}
```

## 🔬 So sánh với alternatives

| Cách học lịch sử | Ưu điểm | Nhược điểm |
|-----------------|---------|-----------|
| **Tutorial có timeline** (bài này) | Ngắn gọn, có ví dụ code thực tế | Không chi tiết bằng tài liệu gốc |
| **Đọc ECMAScript specification** | Chính xác tuyệt đối | Khó đọc, nặng về kỹ thuật |
| **Watch Brendan Eich talk** | Hiểu từ người sáng tạo | Tiếng Anh, cần time |
| **Đọc blog TC39 meetings** | Cập nhật tính năng mới nhất | Chuyên sâu, không phải beginner-friendly |
| **Xem kangax/compat-table** | Biết chính xác browser support | Chỉ là bảng, không có ngữ cảnh lịch sử |

## 📊 Performance & Best Practices

- **Always target ES2015+** trừ khi phải hỗ trợ IE — modern browsers support hầu hết ES6 features.
- **Dùng Babel** để transpile nếu cần hỗ trợ browser cũ — set `targets` trong `.babelrc` theo thống kê người dùng.
- **Kiểm tra caniuse.com** cho từng tính năng cụ thể — không dựa vào "ES2020 = all browsers support".
- **Write future-proof code**: dùng `let`/`const` thay `var`, arrow function thay anonymous function, template literals thay string concat.
- **Theo dõi TC39 proposals** — biết tính năng nào sắp ra để chuẩn bị tâm thế (optional chaining đã ở Stage 4 từ 2019).

## 🔗 Liên kết chéo

- Xem thêm: `00_introduction/03_versions/` — các phiên bản ES chi tiết, bảng timeline
- Xem thêm: `00_introduction/04_how-to-run-javascript/` — cách chạy JS trong browser và Node
- Xem thêm: `01_variables/01_declarations/01_let-and-const/` — `let`/`const` từ ES6 thay `var`
- Xem thêm: `02_data-types/03_type-casting-and-coercion/` — coercion rules được định nghĩa trong ES spec
- Xem thêm: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function từ ES6
- Xem thêm: `17_memory-management/03_v8-engine/` — V8 engine và cách JS runtime hoạt động
- Tài liệu: [ECMAScript History on Wikipedia](https://en.wikipedia.org/wiki/JavaScript#History), [TC39 Proposals](https://github.com/tc39/proposals), [MDN — ECMAScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Year_topics)
