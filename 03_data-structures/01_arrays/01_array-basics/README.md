# Array Basics — Methods Cơ Bản

> Tổng hợp 5 file demo: 1_mang.js, 2_foreach.js, 3_filter.js, 4_map.js, 5_reduce.js

## Khái niệm cốt lõi

JavaScript Array có **3 nhóm methods** quan trọng nhất:

| Nhóm | Methods | Mục đích | Trả về |
|---|---|---|---|
| **Iterate** | forEach, for...of | Duyệt phần tử | undefined |
| **Transform** | map, filter, find, slice | Tạo array mới | Array mới |
| **Reduce** | reduce, reduceRight | Gom thành giá trị duy nhất | Any value |
| **Test** | some, every, includes | Kiểm tra điều kiện | boolean |
| **Search** | indexOf, findIndex, includes | Tìm kiếm | number/boolean |

### Phân biệt mutate vs non-mutate

| Mutate (đổi original) | Non-mutate (tạo mới) |
|---|---|
| push, pop, shift, unshift | concat, slice |
| sort, reverse | toSorted, toReversed |
| fill, splice | — |
| delete (sparse) | — |

## Điểm mạnh

- Immutable pattern: map/filter/reduce tạo array mới, không mutate
- Chainable: `[...].map(...).filter(...).reduce(...)`
- Arrow function syntax gọn gàng
- Built-in optimized native code

## Bẫy thường gặp

- forEach không return được giá trị (khác map)
- filter return boolean, không phải truthy/falsy check
- reduce không có initial value → dùng element đầu làm accumulator
- map callback nhận (value, index, array) — index thường bỏ qua

## Ví dụ từ 5 files

```js
// 1_mang.js — basic ops
const arr = [1, 2, 3, 4, 5];
arr.push(6);          // thêm cuối → [1,2,3,4,5,6]
arr.pop();            // xóa cuối → 6, arr=[1,2,3,4,5]
arr.shift();          // xóa đầu → 1, arr=[2,3,4,5]
arr.unshift(0);       // thêm đầu → [0,2,3,4,5]
arr.splice(1, 1);     // xóa 1 phần tử tại index 1 → [0,3,4,5]

// 2_foreach.js
arr.forEach((v, i) => console.log(`[${i}]: ${v}`));
// forEach KHÔNG thể break — dùng for...of thay thế

// 3_filter.js
const evens = arr.filter(x => x % 2 === 0);
// filter tạo array mới với các phần tử thỏa condition

// 4_map.js
const doubled = arr.map(x => x * 2);
// map transform mỗi phần tử, trả array cùng length

// 5_reduce.js
const sum = arr.reduce((acc, x) => acc + x, 0);
// reduce gom tất cả thành 1 giá trị (initial=0)
```

## Liên kết chéo

- Xem: `03_data-structures/02_keyed-collections` (Map/Set)
- Xem: `05_loops-and-iterations/01_loops` (for...of)
