# Iterators và Generators

## 🔑 Khái niệm

Trong JavaScript, **Iterator** và **Generator** là hai cơ chế giúp bạn đi qua (duyệt) một tập dữ liệu **tuần tự, từng phần tử một**, mà không cần biết trước toàn bộ tập dữ liệu đó lớn đến đâu:

- **Iterator** là một *object* có phương thức `next()`; mỗi lần gọi `next()` nó trả về `{ value, done }`. Bất kỳ object nào có `Symbol.iterator` đều trở thành *iterable* và có thể dùng trong vòng lặp `for...of`, spread `...`, `Array.from(...)`, v.v. Các kiểu có sẵn như `Array`, `String`, `Map`, `Set` đều là iterable.
- **Generator** là một *function* khai báo bằng cú pháp `function*` kết hợp với từ khóa `yield`. Khi gọi, generator **không chạy ngay**, mà trả về một iterator đặc biệt. Mỗi lần gọi `next()`, code chạy đến `yield` rồi **tạm dừng**, lần gọi sau lại tiếp tục từ đúng điểm dừng — nhờ đó tạo được các chuỗi "vô hạn" mà không làm đầy bộ nhớ.

Quan hệ giữa hai khái niệm: generator *tự sản xuất* ra một iterator (bạn không phải tự viết object `next()`), còn iterator thủ công là cách triển khai ở mức thấp hơn. Cả hai cùng phục vụ mục tiêu: **lazy evaluation** — chỉ tính toán và lấy dữ liệu khi thật sự cần.

Trong repo này:

- `01_generators/app.js` — ví dụ generator tạo chuỗi id vô hạn.
- `02_iterators/app.js` — ví dụ tự định nghĩa `Symbol.iterator` và gọi trực tiếp `next()`.

## ✅ Điểm mạnh

- **Tiết kiệm bộ nhớ**: dữ liệu được tạo "lười biếng" theo từng bước, không bao giờ phải lưu trọn cả tập hợp (rất phù hợp với chuỗi vô hạn).
- **Code gọn, dễ đọc**: `function*` + `yield` diễn tả rõ luồng dữ liệu tuần tự; thao tác tay với object `next()` gần như không cần.
- **Hoạt động chung với cú pháp có sẵn**: iterable dùng được ngay trong `for...of`, spread, `Array.from`, destructuring.
- **Tập trung điểm dừng tốt**: generator còn dùng được như một *biến trạng thái* — code "nhớ" vị trí dừng giữa các lần `next()`.
- **Kết hợp tốt với `async`**: `async function*` và `yield` kết hợp với `for await...of` đọc dữ liệu streaming rất mạnh.
- **Hỗ trợ lập trình functional**: dễ lắp chuỗi xử lý (map/filter vô hạn) mà không làm phát sinh mảng trung gian.

## ⚠️ Lưu ý / Hạn chế

- Iterator là **một chiều và "dùng một lần"**: sau khi `done: true` thì hết; muốn duyệt lại phải lấy iterator mới.
- Generator **chỉ tiêu thụ được một lần** — không thể "back" (quay lại giá trị đã yield), không lấy được phần tử theo index kiểu mảng.
- Quên gọi `next()` trong `for...of`: vòng lặp tự gọi nhưng nếu handle `done` sai ở code thủ công, dễ bị **infinite loop**.
- `yield` chỉ dùng được *bên trong* `function*`; generator không gọi như hàm thường — gọi `gen()` chỉ "khởi động" iterator chứ không chạy code.

## 💡 Khi nào dùng

- Tạo **ID tự tăng vô hạn** hoặc chuỗi số theo công thức (Fibonacci, bộ đếm...) — thay vì tính sẵn cả mảng.
- Xử lý **dữ liệu streaming / phân trang** (đọc từng trang API, từng dòng file) mà không tải toàn bộ.
- Duyệt đồng bộ cấu trúc tùy chỉnh (danh sách liên kết, cây) bằng cách cho object đó thêm `Symbol.iterator`.
- Chuyển một chuỗi các bước xử lý dữ liệu thành các "bước" lazy nối tiếp nhau.
- Khi ứng dụng dùng nhiều `for...of` trên dữ liệu do chính bạn định nghĩa — hãy làm nó iterable.

## 🎯 Ví dụ minh họa

```js
// Generator tạo chuỗi id vô hạn
function* idCreator() {
  let i = 0;
  while (true) yield i++;
}
const ids = idCreator();
console.log(ids.next().value); // 0
console.log(ids.next().value); // 1

// Object tự định nghĩa Iterator
const obj = { *[Symbol.iterator]() { yield 1; yield 2; yield 3; } };
for (const x of obj) console.log(x); // 1, 2, 3
const it = obj[Symbol.iterator]();
console.log(it.next()); // { value: 1, done: false }
```

## 📚 Tham khảo / Bài tập

- Chạy `01_generators/app.js`: chạy generator `idCreator`, thử thêm `console.log(ids.next())` để thấy cả `value` lẫn `done`.
- Chạy `02_iterators/app.js` (hoặc mở `02_iterators/index.html` trên trình duyệt): tự thêm `yield 4` hoặc dùng `[...obj]`, `Array.from(obj)` để khẳng định obj là iterable.
- Tự làm: viết một generator trả về 10 số Fibonacci; viết object `range` dùng `Symbol.iterator` để dùng được `for...of`, sau đó so sánh với generator tương đương.