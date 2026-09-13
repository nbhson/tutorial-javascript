# Iterator (Symbol.iterator)

## 🔑 Khái niệm

**Iterator** là một object đóng vai trò "con trỏ duyệt tuần tự": nó có phương thức `next()` trả về object `{ value, done }` (`done === true` khi đã duyệt hết). Bất kỳ object nào có thể trả về một iterator qua key `Symbol.iterator` được gọi là **iterable** — và từ đó có thể dùng trong `for...of`, spread `...`, `Array.from()`, destructuring, `yield*`, v.v.

Các kiểu dữ liệu có sẵn (`Array`, `String`, `Map`, `Set`, `arguments`, `NodeList`...) đều là iterable — bạn chỉ cần `for...of` mà không cần biết cấu trúc bên trong.

Trong ví dụ `02_iterators/app.js`, một object thường được cho "khả năng duyệt" bằng cách định nghĩa `*[Symbol.iterator]()` (generator làm nốt phần còn lại). Sau đó vừa dùng được với `for...of`, vừa có thể gọi tay `it.next()`.

**Phân biệt nhanh**:
- **Iterator** = object có `next()` (mức thấp, có thể viết tay).
- **Iterable** = object có `Symbol.iterator` (có thể dùng trong `for...of`).
- **Generator** = `function*` dùng `yield`; gọi generator là có ngay một iterator mà không cần viết `next()` thủ công.

## ✅ Điểm mạnh

- **Chuẩn chung của ngôn ngữ**: iterable "cắm" được vào mọi cú pháp duyệt có sẵn.
- **Tách biệt cấu trúc dữ liệu khỏi cách duyệt**: bạn quyết định thứ tự / logic `next()`, code dùng thì chỉ cần `for...of`.
- **Lazy**: chỉ sinh giá trị tiếp theo khi được yêu cầu.
- **An toàn với dữ liệu tùy chỉnh**: hợp chuẩn cho danh sách, cây, luồng tự định nghĩa.
- **Kết hợp tay với `next()`** linh hoạt — kiểm soát từng bước một (chính là nền tảng khi tự viết iterator thủ công).

## ⚠️ Lưu ý / Hạn chế

- Iterator "dùng một lần": sau `done: true` không duyệt lại được; muốn duyệt lại phải lấy iterator mới từ `Symbol.iterator`.
- Gọi `next()` sau khi đã `done` vẫn phải tiếp tục trả `{ done: true }` (không lỗi nhưng không có giá trị).
- Một object chỉ trở thành *iterable* khi có `Symbol.iterator`; thiếu nó sẽ lỗi "not iterable" khi dùng `for...of`.
- Dễ nhầm giữa Iterator, Iterable và Generator — nhớ: iterable *trả về* iterator; generator *là* một "nhà máy" tạo iterator tự động.

## 💡 Khi nào dùng

- Cho **class / cấu trúc tự tạo** (danh sách liên kết, tree, Range) dùng được với `for...of`.
- Tạo **chuỗi giá trị theo quy tắc** mà không muốn viết cả mảng trước (bộ đếm, bảng cửu chương, dãy số).
- **Chuyển đổi dữ liệu qua spread / Array.from** cho các kiểu chưa phải array.
- Khi cần **điều khiển từng bước** (duyệt có điểm dừng, kiểm tra trạng thái giữa chừng) thay vì để vòng lặp chạy liền mạch.

## 🎯 Ví dụ minh họa

```js
const obj = { *[Symbol.iterator]() { yield 1; yield 2; yield 3; } };

for (const x of obj) console.log(x);   // 1, 2, 3

const it = obj[Symbol.iterator]();
console.log(it.next());                // { value: 1, done: false }
console.log(it.next());                // { value: 2, done: false }
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` của thư mục này, hoặc mở `index.html` trong trình duyệt (bật Console để xem kết quả).
- Tự làm: thêm `yield 4`; chạy lại rồi thử `console.log([...obj])` và `console.log(Array.from(obj))` để xác nhận obj là iterable.
- Tự làm thêm một object `range(start, end)` dùng `[Symbol.iterator]()` trả về object `next()` viết *tay* (không dùng generator) để phân biệt rõ Iterator vs Generator.