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

Mỗi sub-folder có `README.md` chi tiết + `app.js` runnable.

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
