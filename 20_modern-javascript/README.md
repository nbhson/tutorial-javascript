# Modern JavaScript (ES6+) — Elective

> Nhóm elective — các tính năng ES6+ được spread across nhiều roadmap topics, được gom lại đây để tham khảo tổng hợp.

## Bản đồ kiến thức

Các tính năng ES6+ không nằm riêng trong một ô roadmap, mà phân tán:

| Tính năng | Nằm ở group nào | Link |
|---|---|---|
| Template Literals | `02_data-types` (String) | `01_template-literals/` |
| Destructuring | `03_data-structures` (Arrays/Objects) | `02_destructuring-spread-rest/` |
| Spread/Rest | `09_functions` (Parameters) | `02_destructuring-spread-rest/` |
| Optional Chaining | `04_equality-comparisons` | `03_optional-chaining-nullish/` |
| Nullish Coalescing | `04_equality-comparisons` | `03_optional-chaining-nullish/` |
| Default Params | `09_functions/01_parameters` | `04_enhanced-literals-default-params/` |
| Enhanced Object Literals | `02_data-types` (Objects) | `04_enhanced-literals-default-params/` |
| Logical Operators | `08_expressions-and-operators` | `05_misc/` |

## Cấu trúc nhóm

```
20_modern-javascript/
+-- 01_template-literals/          # ``, ${}, tagged templates
|   +-- 01_template-string/
|   +-- 02_tagged-templates/
+-- 02_destructuring-spread-rest/  # {[a,b] = arr}, {...obj}
|   +-- 01_destructuring-rest/
|   +-- 02_spread/
+-- 03_optional-chaining-nullish/  # obj?.prop, a ?? b
|   +-- 01_optional-chaining/
|   +-- 02_nullish-coalescing/
+-- 04_enhanced-literals-default-params/
|   +-- 01_enhanced-object-literals/
|   +-- 02_default-params/
+-- 05_misc/                       # && || short-circuit
    +-- 01_logical-or/
```

## Lộ trình học đề xuất

1. **Nền tảng:** `01_template-literals` → `02_destructuring-spread-rest`
2. **Safety:** `03_optional-chaining-nullish`
3. **Syntax sugar:** `04_enhanced-literals-default-params`
4. **Pattern:** `05_misc` (logical operators)

Mỗi bài học có `README.md` chi tiết + `app.js` / `index.html` runnable.

## Thời gian hoàn thành

| Mục | Thời gian dự kiến |
|---|---|
| 01_template-literals | 30 phút |
| 02_destructuring-spread-rest | 45 phút |
| 03_optional-chaining-nullish | 20 phút |
| 04_enhanced-literals-default-params | 30 phút |
| 05_misc | 15 phút |
| **Tổng** | **~2 giờ** |

## Liên kết chéo

- Template literals → `02_data-types/01_primitive-types/01_string`
- Destructuring → `03_data-structures/01_arrays`
- Optional chaining → `04_equality-comparisons/01_loose-strict`
- Default params → `09_functions/01_parameters-and-arrow/06_function-parameters`

## 🆕 ES2023–ES2025 Features — Bảng tổng hợp

Bảng bổ sung các tính năng mới nhất (chi tiết đầy đủ: `22_es2025-features/README.md`):

| Tính năng | Phiên bản | Browser support | Mô tả |
|---|---|---|---|
| `toSorted` / `toReversed` / `toSpliced` / `with` | ES2023 | Chrome 110+, Firefox 115+, Safari 16.4+ | Copy-on-write array methods (immutable) |
| `Object.groupBy` / `Map.groupBy` | ES2024 | Chrome 117+, Firefox 119+, Safari 17.4+ | Nhóm mảng theo key |
| `Promise.withResolvers()` | ES2024 | Chrome 119+, Firefox 121+, Safari 17.4+ | Tạo promise + resolve/reject tách riêng |
| `ArrayBuffer.prototype.transfer()` | ES2024 | Chrome 114+, Firefox 127+, Safari 17+ | Transfer ownership buffer, zero-copy |
| **Iterator Helpers** | ES2025 | Chrome 122+, Firefox 131+, Safari 18.4+ | `map/filter/take/drop...` lazy trên `Iterator.prototype` |
| **Set Methods** (`union`, `intersection`...) | ES2025 | Chrome 122+, Firefox 127+, Safari 17+ | Phép toán tập hợp chuẩn toán học |
| **`Promise.try()`** | ES2025 | Chrome 122+, Firefox 128+, Safari 17.5+ | Function → promise, bắt cả lỗi sync |
| **`RegExp.escape()`** | ES2025 | Chrome 123+, Firefox 127+, Safari 17.4+ | Escape chuỗi an toàn cho regex |
| **Import Attributes** (`with { type: "json" }`) | ES2025 | Chrome 123+, Firefox 123+, Safari 17.2+ | Import JSON module với type rõ ràng |
| **JSON Modules** | ES2025 | Chrome 123+, Firefox 123+, Safari 17.2+ | Import file .json như ES module |
| `Float16Array` | ES2025 | Chrome 135+, Firefox 129+, Safari 18.2+ | TypedArray 16-bit float (AI/ML, GPU) |
| JSON.parse source text access | ES2026 | Chrome 114+, Firefox 128+, Safari 17.4+ | Giữ text gốc của số — BigInt-safe parsing (đã ship sớm dù thuộc ES2026) |
| Temporal API | ES2027 | — (Stage 3 → dự kiến Stage 4/2026) | Thay thế Date — dự kiến thuộc ES2027, chưa vào ES2026 |

### Lộ trình học thêm

Sau khi hoàn thành các mục ES6 ở trên, tiếp tục với:

1. **ES2023–2024:** `toSorted/toReversed/toSpliced/with`, `Object/Map.groupBy`, `Promise.withResolvers`
2. **ES2025:** Iterator Helpers → Set Methods → `Promise.try` / `RegExp.escape` → Import Attributes
3. **ES2026:** Xem `23_es2026-features/README.md`
4. **Chi tiết đầy đủ:** `22_es2025-features/README.md` (~580 dòng, kèm ví dụ + browser support + bẫy)
