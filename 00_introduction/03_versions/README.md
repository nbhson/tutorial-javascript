# Các phiên bản JavaScript (ES5 → ESNext)

## 🔑 Khái niệm

JavaScript được chuẩn hóa bởi **ECMA International** với tên chính thức **ECMAScript**. Mỗi phiên bản thêm tính năng mới; kể từ **ES6**, cứ mỗi tháng 6 hằng năm lại có một bản phát hành mang tên năm (ECMAScript 2016, 2017…). Hiểu các phiên bản này giúp bạn biết tính năng nào mình đang dùng, và hạn chế tương thích đến đâu.

**Dòng thời gian (timeline):**

- **ES1 (1997)** — chuẩn đầu tiên.
- **ES2 (1998)** — đồng bộ đặc tả ISO.
- **ES3 (1999)** — `regex`, `try/catch`.
- **ES5 (2009)** — `"use strict"`, `JSON`, hàng loạt Array methods (`forEach`, `map`, `filter`...).
- **ES6 / ES2015 (2015)** — cột mốc lớn: `let`/`const`, `class`, arrow function, Promise, module(`import`/`export`), destructuring, spread/rest, template string, Map/Set, Symbol, generator, default parameters, `for...of`.
- **ES2016** — toán tử lũy thừa `**`, `Array.prototype.includes`.
- **ES2017** — `async`/`await`, `Object.values()`/`Object.entries()`, String padding (`padStart`/`padEnd`), trailing commas.
- **ES2018 → ESNext** — Object spread/rest, `async iteration`, optional chaining (`?.`), nullish coalescing (`??`), private class fields (`#`), `Array.at()`, top-level await, v.v. xuất hiện dần qua các năm.
- **ESNext** — *tên động* chỉ phiên bản đang phát triển; không phải một release cụ thể.

**Quy trình TC39 (4 giai đoạn):**

```
Proposal → Stage 0 (Ý tưởng) → Stage 1 (Đề xuất) → Stage 2 (Draft)
         → Stage 3 (Candidate) → Stage 4 (Finished) → Chính thức vào Spec
```

- Chỉ tính năng đạt **Stage 4** mới được đưa vào chuẩn ECMAScript chính thức.
- Tính năng ở stage thấp có thể bị thay đổi hoặc bỏ mà không báo trước.

**Cách kiểm tra hỗ trợ trình duyệt:**

- [kangax.github.io/compat-table](https://kangax.github.io/compat-table/) — bảng so sánh chi tiết theo tính năng.
- [caniuse.com](https://caniuse.com) — mức hỗ trợ theo trình duyệt.
- Trong code, có thể kiểm tra thủ công: `"at" in Array.prototype`.

## ✅ Điểm mạnh

- Biết tính năng thuộc phiên bản nào → đánh giá rủi ro tương thích khi dùng.
- Hiểu "ESNext" → đọc tài liệu hay blog mới không bị bối rối bởi thuật ngữ.
- Nắm quy trình TC39 → biết tính năng nào đủ "chín muồi" để dùng trong production.
- Nắm mốc ES5/ES6 → dễ học các bài sau của lộ trình (roadmap) theo thứ tự hợp lý.
- Tự tin khi phỏng vấn về các phiên bản JS.

## ⚠️ Lưu ý / Hạn chế

- Tính năng ở **Stage 0–2** chưa nên dùng rộng rãi; cú pháp có thể đổi.
- Trình duyệt cũ không hiểu tính năng mới → cần **transpile** (Babel) cho production nếu nhắm trình duyệt cũ.
- Không phải mọi tính năng Stage 4 đều có ngay trên mọi trình duyệt; hãy kiểm tra bằng compat-table/caniuse.
- `class` trong ES6 vẫn chỉ là **syntactic sugar** trên prototype — nắm chắc điều này để tránh hiểu sai về "OOP kiểu Java".

## 💡 Khi nào dùng

- Chọn cú pháp cho dự án khi phải hỗ trợ nhiều trình duyệt (school, government site...).
- Đọc spec hoặc bảng tin "What's new in ES202X".
- Quyết định nhúng một proposal mới (vd. `Array.groupBy`) vào codebase.
- Học roadmap: sắp xếp thứ tự học tính năng theo version ra mắt.

## 🎯 Ví dụ minh họa

```js
// Các "thế hệ" cú pháp khác nhau
// ES5: callback + var
var mang = [1, 2, 3];
var gapDoi = mang.map(function (n) { return n * 2; });

// ES6: arrow + template string
const gapBa = mang.map((n) => n * 3);
console.log(`Kết quả: ${gapDoi.join(",")} | ${gapBa.join(",")}`);

// ES2016: includes
console.log(mang.includes(2)); // true

// ES2017: async/await
async function layDuLieu() {
  const p = await Promise.resolve(42);
  return p;
}

// ESNext tiêu biểu: optional chaining + nullish coalescing
const cauHinh = {};
console.log(cauHinh?.server?.port ?? 3000); // 3000
```

## 📚 Tham khảo / Bài tập

- Nhóm này **chưa có file `app.js`** — hãy chạy ví dụ trên trong DevTools (F12 → Console).
- Tự thử: chọn 5 tính năng ES6+ bạn chưa dùng (vd. destructuring, `for...of`, generator), viết ví dụ nhỏ và mở [compat-table](https://kangax.github.io/compat-table/) xem mức hỗ trợ của chúng trong trình duyệt hiện tại.
- Tài liệu: [ECMA-262 spec](https://tc39.es/ecma262/), [caniuse.com](https://caniuse.com).