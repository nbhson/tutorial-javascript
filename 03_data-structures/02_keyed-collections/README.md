# Keyed Collections (Map, Set, WeakMap, WeakSet)

## 🔑 Khái niệm

**Keyed collections** là các cấu trúc dữ liệu truy cập **theo khóa** (key), khác với mảng truy cập theo index. JavaScript cung cấp 4 loại: `Map`, `Set`, `WeakMap`, `WeakSet`.

**So sánh nhanh:**

| | Trả về khi thêm trùng | Khóa được phép | `size` | Lặp được (for...of) |
|---|---|---|---|---|
| `Map` | ghi đè khóa trùng | **bất kỳ** (object, function, primitive) | có | có |
| `Set` | bỏ qua phần tử trùng | — | có | có |
| `WeakMap` | ghi đè | **chỉ object** | **không** | **không** |
| `WeakSet` | bỏ qua | **chỉ object** | **không** | **không** |

**Vì sao "Weak"?** "Weak" = tham chiếu **yếu**: khóa là object, và khi object đó không còn được tham chiếu ở nơi khác, **garbage collector (GC) có thể thu hồi** nó — không lo rò rỉ bộ nhớ. Điều đó cũng nghĩa là WeakMap/WeakSet **không thể** liệt kê (không `size`, không iterable) vì danh sách có đầy biến mất.

Chi tiết từng loại ở 4 bài con:

- `01_map/` — khóa–giá trị, khóa tùy ý (bất kỳ kiểu).
- `02_weakmap/` — như Map nhưng khóa chỉ object, GC thu hồi được.
- `03_set/` — tập hợp các giá trị **duy nhất**.
- `04_weakset/` — như Set nhưng chỉ object, GC thu hồi được.

## ✅ Điểm mạnh

- `Map` giữ **thứ tự chèn** và `size` dễ lấy hơn object.
- `Map` cho phép khóa là **object/function** — không bị ép thành chuỗi như object thường.
- `Set` tự loại trùng — với `[...set]` có ngay mảng unique.
- `WeakMap`/`WeakSet` không chặn GC → rất hợp làm **cache, metadata, quản lý DOM**.
- Tìm kiếm khóa nhanh hơn duyệt mảng (`has`/`get` O(1) trung bình).

## ⚠️ Lưu ý / Hạn chế

- `WeakMap`/`WeakSet` **chỉ nhận object**: `wm.set(1, "x")` → `TypeError`.
- `WeakMap`/`WeakSet` **không có `size`**, **không `keys()`**, **không lặp được**.
- Map khóa object so sánh theo **tham chiếu** — `m.set({}, 1)` rồi `m.get({})` trả `undefined` vì hai object khác nhau.
- `Map` **không** thay thế object: JSON.stringify(object) có sẵn, còn Map phải tự chuyển.

## 💡 Khi nào dùng

- Chữ key–giá trị phức tạp, thứ tự quan trọng, cần `size` → `Map`.
- Cache/thuộc tính ẩn gắn với instance mà muốn GC xử lý → `WeakMap`.
- Cần danh sách phần tử **không trùng** → `Set`.
- Đánh dấu "đã xử lý" cho các object (vòng quét, visited nodes) → `WeakSet`.

## 🎯 Ví dụ minh họa

```js
// Map
const m = new Map();
m.set("a", 1);
m.set({ id: 1 }, "obj");          // khóa là object ✓
console.log(m.size);              // 2
console.log(m.get("a"));          // 1
for (const [k, v] of m) console.log(k, v); // lặp được

// Set — tự bỏ trùng
const s = new Set([1, 2, 2, 3]);
console.log([...s]);              // [1, 2, 3]

// WeakMap — khóa object, không size/iterable
let wm = new WeakMap();
let o = {};
wm.set(o, "secret");
console.log(wm.get(o));           // "secret"
```

## 📚 Tham khảo / Bài tập

- Học lần lượt 4 bài con, mỗi bài có `app.js` chạy được ngay (`node app.js` hoặc mở `index.html`).
- Tự thử: 1) tạo `Map` lưu 3 sản phẩm theo tên và lấy `size`, lặp in; 2) `Set` tổng hợp danh sách Chrome histó trùng; 3) dùng `WeakMap` làm cache kết quả tính toán cho từng object.
- Tài liệu: [MDN — Map](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map), [MDN — Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set), [javascript.info/map-set](https://javascript.info/map-set).