# Các phiên bản JavaScript (ES5 → ESNext) — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

JavaScript được chuẩn hóa bởi **ECMA International** với tên chính thức là **ECMAScript** (viết tắt **ES**). Mỗi phiên bản thêm tính năng mới vào ngôn ngữ. Kể từ **ES6 (2015)**, TC39 chuyển sang mô hình **phát hành hằng năm** — mỗi tháng 6 hằng năm công bố bản mới, đặt tên theo năm (ECMAScript 2016, 2017, 2018…).

Việc hiểu các phiên bản này giúp bạn:
- Biết tính năng bạn đang dùng có từ phiên bản nào.
- Đánh giá được mức độ tương thích với trình duyệt mục tiêu.
- Quyết định có cần transpile (Babel) hay không.
- Tự tin khi đọc tài liệu kỹ thuật và phỏng vấn.

### Dòng thời gian chi tiết

| Phiên bản | Năm | Tính năng tiêu biểu |
|-----------|-----|---------------------|
| **ES1 (ESMAScript 1)** | 1997 | Chuẩn đầu tiên — base language spec |
| **ES2 (ESMAScript 2)** | 1998 | Đồng bộ với ISO/IEC 16262 |
| **ES3** | 1999 | `RegExp`, `try/catch`, improved string handling |
| **ES5** | 2009 | `"use strict"`, `JSON.parse/stringify`, `Array.forEach/map/filter`, `Object.create`, `get/set` accessors |
| **ES6 / ES2015** | 2015 | `let`/`const`, `class`, arrow `=>`, `Promise`, `import`/`export`, destructuring, spread/rest, template literals, `Map`/`Set`, `Symbol`, `for...of`, default params, `Math.*` extensions |
| **ES2016** | 2016 | `**` (exponentiation), `Array.prototype.includes` |
| **ES2017** | 2017 | `async`/`await`, `Object.values()`/`Object.entries()`, `padStart`/`padEnd`, trailing commas in func params |
| **ES2018** | 2018 | Object rest/spread `{...obj}`, `Promise.finally()`, async iteration (`for await...of`), regex `s` flag |
| **ES2019** | 2019 | `Array.prototype.flat/flatMap`, `Object.fromEntries`, `String.prototype.trimStart/trimEnd`, optional catch binding |
| **ES2020** | 2020 | `BigInt`, `import()`, `Promise.allSettled`, `String.matchAll`, `globalThis`, optional chaining `?.`, nullish coalescing `??` |
| **ES2021** | 2021 | `Logical assignment` (`||=`, `&&=`, `??=`), `String.prototype.replaceAll`, numeric separator `1_000_000`, `Promise.any` |
| **ES2022** | 2022 | `Array.prototype.at()`, `Object.hasOwn()`, `#private` fields, top-level `await` (modules), regex `RegExp.prototype.dotAll` |
| **ES2023** | 2023 | `Array.prototype.toReversed/toSorted/toSpliced`, `Object.groupBy`, `findLast/findLastIndex`, Hashbang syntax |
| **ES2024** | 2024 | `Promise.withResolvers`, `RegExp v` flag (unicode sets), `Array.prototype.with`, `Set.prototype.intersection/union/difference` |
| **ESNext** | — | Tên gọi động cho phiên bản đang phát triển (Stage 0–3 proposals) |

### Quy trình TC39 — 4 Giai đoạn (Stages)

```
Stage 0 (Strawman)      → Ý tưởng, thảo luận mở trên mailing list
       ↓
Stage 1 (Proposal)      → Có TC39 sponsor, spec draft bắt đầu
       ↓
Stage 2 (Draft)         → Spec chi tiết, API design stabilize
       ↓
Stage 3 (Candidate)     → Spec nearly final, browser implement thử nghiệm
       ↓
Stage 4 (Finished)      → Chính thức đưa vào ECMAScript standard
```

**Quy tắc quan trọng:**
- Chỉ tính năng **Stage 4** mới được coi là "chính thức" của ECMAScript.
- Tính năng **Stage 0–2** có thể bị thay đổi cú pháp hoặc bị bỏ hoàn toàn — không nên dùng trong production.
- Tính năng **Stage 3** thường đã ổn định API — có thể dùng với Babel polyfill.
- Mỗi năm (tháng 6), TC39 họp và quyết định đưa tính năng Stage 3 nào lên Stage 4.

### Cách kiểm tra hỗ trợ trình duyệt

1. **[kangax.github.io/compat-table](https://kangax.github.io/compat-table/)** — bảng so sánh chi tiết theo từng tính năng, cập nhật real-time.
2. **[caniuse.com](https://caniuse.com)** — mức hỗ trợ theo trình duyệt (phiên bản cụ thể).
3. **Kiểm tra thủ công trong code:**
   ```js
   // Check tính năng có tồn tại không
   console.log("at" in Array.prototype);          // ES2022
   console.log("group" in Array.prototype);        // ES2023
   console.log(typeof globalThis !== "undefined"); // ES2020
   ```

## 📐 Cấu trúc nhóm

```
03_versions/
└── README.md
    ● Timeline ES1 → ESNext
    ● Bảng tính năng tiêu biểu mỗi version
    ● Quy trình TC39 4 stages
    ● Cách kiểm tra browser compatibility
    ● Lưu ý khi deploy production
```

## ✅ Điểm mạnh — Tại sao nên nắm vững

| # | Lợi ích | Giải thích |
|---|---------|-----------|
| 1 | **Đánh giá risk tương thích** | Biết tính năng từ ES nào → ước lượng browser support |
| 2 | **Đọc spec/blog đúng cách** | Phân biệt được "ES2020 feature" với "Stage 2 proposal" |
| 3 | **Ra quyết định transpile** | Dùng Babel target `'> 1%'` thay vì mặc định |
| 4 | **Tự tin phỏng vấn** | Câu "ES6 có những gì?" và "ESNext là gì?" xuất hiện thường xuyên |
| 5 | **Cập nhật công nghệ có hệ thống** | Biết tính năng nào sắp ra → chuẩn bị codebase trước |
| 6 | **Hiểu vì sao code cũ/làm việc differently** | ES5 vs ES6 có behavioral differences (e.g., `var` vs `let` TDZ) |
| 7 | **Sử dụng proper feature detection** | `if ("flatMap" in Array.prototype)` thay vì browser sniffing |
| 8 | **Tham gia discussion TC39** | Theo dõi proposals trên github.com/tc39 |

## ⚠️ Bẫy thường gặp & Hạn chế

| # | Bẫy | Ví dụ |
|---|-----|-------|
| 1 | **Tính năng Stage 0–2 chưa ổn định** | Pipeline operator `|>` (Stage 2) — cú pháp có thể đổi |
| 2 | **ES6 ≠ ES2015 only** | "ES6" là tên gọi không chính thức; tên chuẩn là ES2015. Từ 2016 mỗi năm có tên riêng. |
| 3 | **Trình duyệt cũ không hiểu tính năng mới** | Safari 14 không support `?.` — cần polyfill hoặc transpile |
| 4 | **`class` ES6 vẫn là prototype** | Hiểu `class extends` → thực chất là `Sub.prototype = Object.create(Super.prototype)` |
| 5 | **ESNext không phải bản release** | Chỉ là tên gọi động, không có version number cụ thể |
| 6 | **Transpile ≠ polyfill** | Babel transpile cú pháp (arrow → function), polyfill thêm method mới (Promise, Object.assign) |
| 7 | **Tính năng Stage 4 ≠ được hỗ trợ 100%** | Vẫn cần kiểm tra caniuse — IE11 hỗ trợ ES5 nhưng không phải ES6+ |
| 8 | **Nhầm `nullish coalescing` với `logical OR`** | `"" ?? "default"` → `""` (vì `""` không nullish), nhưng `"" \|\| "default"` → `"default"` |

## 💡 Khi nào dùng — Tình huống thực tế

1. **Chọn cú pháp cho dự án** — khi phải hỗ trợ nhiều trình duyệt (trường học, government site) — ưu tiên ES5-safe hoặc transpile.
2. **Đọc spec hoặc bảng tin "What's new in ES202X"** — phân biệt được tính năng nào đã chính thức.
3. **Quyết định nhúng proposal mới** — ví dụ `Array.groupBy` (ES2024) vào codebase — kiểm tra stage và polyfill.
4. **Học roadmap theo thứ tự** — sắp xếp thứ tự học tính năng theo version ra mắt, tránh bỏ sót nền tảng.
5. **Debug lỗi "undefined is not a function"** — có thể do browser không support method từ ES version cao hơn.
6. **Viết compatibility layer** — tạo polyfill cho tính năng Stage 3 chưa được browser support đầy đủ.
7. **Review code** — phát hiện dùng tính năng ES2020 trong codebase target ES2017.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Các "thế hệ" cú pháp khác nhau

```js
// ── ES5 (2009): var + function expression + callback ──
var mang = [1, 2, 3];
var gapDoi = mang.map(function (n) { return n * 2; });

// ── ES6 / ES2015 (2015): arrow + template string + let/const ──
const gapBa = mang.map((n) => n * 3);
console.log(`ES5: ${gapDoi.join(",")} | ES6: ${gapBa.join(",")}`);
// ES5: 2, 4, 6 | ES6: 3, 6, 9

// ── ES2016 (2016): includes, exponentiation ──
console.log(mang.includes(2));   // true
console.log(2 ** 10);            // 1024

// ── ES2017 (2017): async/await ──
async function layDuLieu() {
  const p = await Promise.resolve(42);
  return p;
}

// ── ES2020 (2020): optional chaining + nullish coalescing ──
const cauHinh = {};
console.log(cauHinh?.server?.port ?? 3000); // 3000 — ?? chỉ thay nullish, không thay falsy
console.log(cauHinh?.server?.port || 3000); // 3000 — || thay mọi falsy ((bao gồm 0, ""))
```

### Ví dụ 2: Feature detection — cách professional check compatibility

```js
// Kiểm tra thủ công tính năng có tồn tại
const features = {
  optionalChaining: typeof Symbol !== "undefined" && "optionalChaining" in {},
  arrayFlat: "flat" in Array.prototype,
  promiseAllSettled: "allSettled" in Promise,
  globalThis: typeof globalThis !== "undefined",
  atMethod: "at" in Array.prototype,
};

console.log(features);
// {
//   arrayFlat: true,
//   promiseAllSettled: true,
//   globalThis: true,
//   atMethod: true,
//   ...
// }

// fallback nếu không có
const safeFlat = features.arrayFlat
  ? (arr) => arr.flat()
  : (arr) => arr.reduce((acc, val) => acc.concat(Array.isArray(val) ? val : [val]), []);
```

### Ví dụ 3: So sánh behavior giữa ES5 và ES6+

```js
// ── ES5: var có function scope, hoisted về undefined ──
function testVar() {
  if (true) {
    var x = 10;
  }
  console.log(x); // 10 — var thoát khỏi if block!
}
testVar();

// ── ES6: let có block scope, TDZ ──
function testLet() {
  if (true) {
    let y = 10;
  }
  // console.log(y); // ReferenceError: y is not defined
}
testLet();

// ── ES6: const không gán lại được ──
const CONST_VAL = 100;
// CONST_VAL = 200; // TypeError: Assignment to constant variable
```

### Ví dụ 4: Timeline — xác định version của một method

```js
// Xác định method thuộc version nào
const methods = [
  ["forEach", "ES5 (2009)"],
  ["includes", "ES2016"],
  ["flat", "ES2019"],
  ["at", "ES2022"],
  ["toSorted", "ES2023"],
];

for (const [method, version] of methods) {
  const supported = method in Array.prototype;
  console.log(`${method.padEnd(12)} → ${supported ? "✅" : "❌"} (${version})`);
}
// forEach         → ✅ (ES5 (2009))
// includes        → ✅ (ES2016)
// flat            → ✅ (ES2019)
// at              → ✅ (ES2022)
// toSorted        → ✅ (ES2023)
```

## 🔬 So sánh với alternatives

| Phương án | Ưu điểm | Nhược điểm |
|-----------|---------|------------|
| **Học theo version timeline** (bài này) | Có trật tự, dễ theo dõi tiến trình | Cần nhớ nhiều version numbers |
| **Học theo feature category** (biến, hàm, object…) | Tập trung vào concept hơn year | Thiếu ngữ cảnh lịch sử |
| **ĐỌC ECMAScript spec trực tiếp** | Chính xác tuyệt đối | Khó đọc, nặng về kỹ thuật |
| **Dùng Babel playground** | Thấy instant result của tính năng mới | Không hiểu "tại sao" và "khi nào" |
| **Xem kangax compat-table** | Biết browser support chi tiết | Chỉ là bảng, không có giải thích |

## 📊 Performance & Best Practices

- **Target ES2015+ cho frontend** — trừ khi phải hỗ trợ IE, hãy transpile xuống ES2015 và dùng polyfill cho tính năng mới hơn.
- **Kiểm tra caniuse trước khi dùng tính năng ES mới** — đặc biệt quan trọng với government/school projects.
- **Write conditional fallback** — dùng feature detection thay vì browser sniffing (`if ("flat" in Array.prototype)`).
- **Dùng TypeScript strict mode** — phát hiện lỗi type trước khi chạy, bù đắp dynamic typing của JS.
- **Update dependencies định kỳ** — Babel, polyfill packages thường xuyên để support latest browser versions.
- **Know your audience** — statistic usage của browser target project quyết định ES target.

## 🔗 Liên kết chéo

- Xem thêm: `00_introduction/02_history-of-javascript/` — lịch sử ra đời và các mốc quan trọng
- Xem thêm: `01_variables/01_declarations/01_let-and-const/` — `let`/`const` từ ES6 thay `var`
- Xem thêm: `02_data-types/03_type-casting-and-coercion/` — coercion rules định nghĩa trong ES spec
- Xem thêm: `09_functions/01_parameters-and-arrow/03_arrow-functions/` — arrow function từ ES2015
- Xem thêm: `20_modern-javascript/03_optional-chaining-nullish/` — `?.` và `??` từ ES2020
- Xem thêm: `20_modern-javascript/04_enhanced-literals-default-params/` — default params, shorthand properties từ ES2015
- Tài liệu: [ECMA-262 Specification](https://tc39.es/ecma262/), [caniuse.com](https://caniuse.com), [kangax.github.io/compat-table](https://kangax.github.io/compat-table/)
