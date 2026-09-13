# 03. Cấu trúc dữ liệu (Data Structures)

## 🔑 Khái niệm

Nhóm này trang bị các **cấu trúc dữ liệu có sẵn** của JavaScript — chia làm 3 loại theo cách tài liệu MDN/roadmap.sh mô tả:

1. **Indexed Collections (truy cập theo chỉ số):** `Array` và `TypedArray`. Phần tử được truy cập bằng số index `0, 1, 2...`.
2. **Keyed Collections (truy cập theo khóa):** `Map`, `Set`, `WeakMap`, `WeakSet`. Dữ liệu được lưu theo khóa không nhất thiết phải là số.
3. **Structured Data (dữ liệu có cấu trúc):** `JSON` — định dạng chuẩn để trao đổi dữ liệu giữa client – server.

| Cấu trúc | Khóa | Thứ tự | Trùng | GC "mềm" |
|---|---|---|---|---|
| `Array` | index 0-based | có | được | không |
| `Map` | bất kỳ (kể cả object) | có | không (ghi đè) | không |
| `Set` | mỗi phần tử là "khóa" | có | tự loại trùng | không |
| `WeakMap` | **chỉ object** | không | không | có |
| `WeakSet` | **chỉ object** | không | không | có |
| `TypedArray` | index, kiểu cố định | có | được | không |

## ✅ Điểm mạnh

- Chọn đúng cấu trúc → code nhanh và sạch hơn nhiều.
- `Map`/`Set` cho thao tác khóa/ngăn trùng rất gọn so với object thủ công.
- `WeakMap`/`WeakSet` không chặn garbage collector → tránh rò rỉ bộ nhớ.
- `TypedArray` cho thao tác dữ liệu nhị phân (file, audio, canvas, WebGL) hiệu quả.
- `JSON` là "ngôn ngữ chung" của web: API, lưu trữ local, giao tiếp đều dùng.

## ⚠️ Lưu ý / Hạn chế

- `WeakMap`/`WeakSet` **chỉ nhận object** (primitive sẽ báo lỗi), **không có `size`**, **không lặp được**.
- `Map` khóa object so sánh theo **tham chiếu**, không phải theo nội dung.
- `JSON.stringify` bỏ qua `undefined`/`function`/`Symbol`, đổi `NaN` → `null`.
- Array methods làm quen nhiều nhất là nhóm `forEach/map/filter/reduce` — học kỹ trong `01_arrays`.

## 💡 Khi nào dùng

- Danh sách có thứ tự → `Array` (kèm `map/filter/reduce`).
- Liên kết khóa–giá trị phức tạp (khóa không phải chuỗi) → `Map`.
- Khi cần "unique", chống trùng → `Set`.
- Cache metadata kèm object mà không muốn giữ object sống mãi → `WeakMap`.
- Gửi/nhận dữ liệu với server, lưu `localStorage` → `JSON`.

## 🎯 Ví dụ minh họa

```js
// Array
const arr = [1, 2, 3];
console.log(arr.map((n) => n * 2)); // [2, 4, 6]

// Map — khóa là object được phép
const m = new Map();
m.set({ id: 1 }, "giá trị");
console.log(m.size); // 1

// Set — tự loại trùng
const s = new Set([1, 2, 2, 3]);
console.log([...s]); // [1, 2, 3]

// JSON
console.log(JSON.stringify({ a: 1 })); // {"a":1}
```

## 📚 Tham khảo / Bài tập

- Nhóm này gồm 4 bài con: `01_arrays/`, `02_keyed-collections/`, `03_typed-arrays/`, `04_json/`.
- Mỗi bài đều có `app.js` hoặc `*.js` — chạy bằng `node <file>.js` (hoặc mở `index.html`).
- Tự thử: lấy danh sách môn học có `{ name, page }`, dùng `filter` lọc page > 0, `map` đổi tên, `reduce` tính tổng page; sau đó chuyển qua `Map` lưu theo key `name`.