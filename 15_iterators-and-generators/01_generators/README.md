# Generator

## 🔑 Khái niệm

**Generator** là một hàm đặc biệt được khai báo bằng cú pháp `function*` và dùng từ khóa `yield` để "nhả ra" từng giá trị. Khác với hàm thường chạy từ đầu đến cuối rồi trả về một kết quả, một generator khi được gọi sẽ:

1. **Không chạy ngay lập tức** — chỉ trả về một generator object (chính là một iterator).
2. Mỗi lần gọi `next()`: code chạy đến `yield` kế tiếp, nhả giá trị `yield ...`, rồi **tạm dừng** tại đó.
3. Lần gọi `next()` sau: tiếp tục chạy từ đúng điểm dừng cho đến `yield` kế tiếp hoặc hết hàm (khi đó `done: true`).

Nhờ cơ chế tạm dừng đó, generator có thể biểu diễn các chuỗi **vô hạn** mà không tốn bộ nhớ, vì mỗi giá trị chỉ được tính khi bạn "kéo" nó ra bằng `next()`. Trong repo này, `01_generators/app.js` minh họa đúng mô hình này với hàm `idCreator()` chạy vòng lặp `while (true)` nhưng không bao giờ treo máy.

## ✅ Điểm mạnh

- **Lazy (lười biếng)**: giá trị được tạo theo nhu cầu — lý tưởng cho chuỗi vô hạn hoặc dữ liệu quá lớn.
- **Giữ trạng thái tự động**: vị trí dừng và biến cục bộ được lưu giữa các lần `next()` mà không cần biến toàn cục.
- **Code tuần tự dễ đọc**: viết luồng dữ liệu giống như dùng vòng lặp thường, thay vì callback chồng nhau.
- **Tương thích mọi nơi iterable dùng được**: `for...of`, spread, `Array.from`, destructuring.
- **Nền tảng cho async streaming**: `async function*` + `for await...of` rất mạnh để đọc tài nguyên theo khối.

## ⚠️ Lưu ý / Hạn chế

- Không dùng `yield` bên ngoài `function*` — gặp lỗi cú pháp.
- Generator **chỉ duyệt một chiều, một lần**: sau khi hết thì phải tạo generator mới.
- Gọi `gen()` không thực thi thân hàm; quên `next()` (hoặc không dùng `for...of`) sẽ thấy mọi thứ "không chạy".
- Mỗi generator object có trạng thái riêng: hai biến trỏ tới cùng generator sẽ "chia sẻ" vị trí dừng — dễ gây nhầm lẫn khi lưu generator trong nhiều chỗ.

## 💡 Khi nào dùng

- Sinh **ID tự tăng / chuỗi công thức vô hạn** (Fibonacci, bộ đếm) mà không tạo cả mảng.
- Duyệt từng trang dữ liệu, từng dòng file, hoặc stream — xử lý từng phần mà không giữ toàn bộ.
- Làm dữ liệu tuần tự cho `for...of` mà khởi tạo tốn kém mỗi vòng.
- Chia một thuật toán dài thành các bước tạm dừng được (ví dụ duyệt cây, backtracking).
- Viết pipeline xử lý dữ liệu lazy nhiều tầng.

## 🎯 Ví dụ minh họa

```js
function* idCreator() {
  let i = 0;
  while (true) yield i++;
}
const ids = idCreator();
console.log(ids.next().value); // 0
console.log(ids.next().value); // 1
console.log(ids.next().value); // 2
// ... tiếp tục vô hạn nhưng không tốn bộ nhớ
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục này: quan sát chuỗi `0, 1, 2, ...`; thử in cả `ids.next()` (giữ nguyên vị trí) để xem `{ value, done }`.
- Tự làm: viết `function* fib()` yield dãy Fibonacci; dùng `for...of` kèm biến đếm để dừng sau 10 số.
- Tự làm: `async function*` lặp `await fetch(...)` từng trang, xem khác biệt khi dùng `for await...of`.