# Vòng Lặp và Lặp (Loops & Iterations)

## 🔑 Khái niệm

Vòng lặp (loop) là cách JavaScript thực hiện **lặp đi lặp lại một khối code** cho đến khi một điều kiện nào đó không còn đúng (hoặc có lệnh dừng). Nếu không có vòng lặp, bạn sẽ phải viết đi viết lại cùng một đoạn code rất nhiều lần — ví dụ in ra 10 số, duyệt qua 100 phần tử mảng.

Mỗi cú pháp vòng lặp trong JavaScript phục vụ một mục đích riêng:

| Vòng lặp | Dùng khi |
|---|---|
| `for` | biết trước số lần lặp |
| `while` | lặp theo điều kiện kiểm tra ở đầu |
| `do...while` | ít nhất phải chạy 1 lần rồi mới kiểm tra điều kiện |
| `for...in` | duyệt theo **key** của object (hoặc index của mảng) |
| `for...of` | duyệt theo **value** của iterable (mảng, string, Set, Map...) |

## ✅ Điểm mạnh

- **Giảm code lặp lại khủng khiếp**: thay vì viết 100 dòng cho 100 phần tử, chỉ cần 3-5 dòng.
- **Đa dạng cú pháp**: mỗi loại vòng lặp được tối ưu cho một tình huống, chọn đúng loại code sẽ tự nhiên hơn.
- **Dễ đọc và dễ bảo trì**: vòng lặp đúng loại giúp người đọc hiểu ngay ý định (đếm → `for`, kiểm tra điều kiện → `while`, duyệt object → `for...in`).
- **Kết hợp tốt với break/continue**: có thể chủ động dừng hoặc bỏ qua vòng lặp khi cần.
- **Hỗ trợ lồng nhau**: vòng lặp trong vòng lặp giải quyết được bài toán ma trận, bảng dữ liệu 2 chiều.
- **Nền tảng cho hầu hết thuật toán**: tìm kiếm, sắp xếp, tổng hợp dữ liệu đều dựa trên vòng lặp.

## ⚠️ Lưu ý / Hạn chế

- **Không được quên điều kiện dừng**: nếu biến đếm không tiến về điều kiện thoát, vòng lặp chạy vô hạn (infinite loop) làm treo trình duyệt.
- Nên dùng `let`/`const` trong vòng `for`; biến `var` khai báo trong vòng lặp vẫn bị rò rỉ ra phạm vi bên ngoài.
- `for...in` duyệt **key/index dạng chuỗi**, duyệt cả thuộc tính kế thừa qua prototype (dùng `hasOwnProperty` để lọc nếu cần). Dùng sai sẽ gặp kết quả "lạ".
- `for...of` **không dùng được trực tiếp trên object thường** — phải qua `Object.keys()`, `Object.values()` hoặc `Object.entries()`.
- Dùng `break` trước `continue` trong cùng vòng lặp sẽ tương đương với `break` (code sau `continue` trong cùng lần lặp không chạy).

## 💡 Khi nào dùng

- Lặp theo số lần đã biết: in bảng cửu chương, render danh sách bài viết `1..10`.
- Duyệt phần tử của mảng hoặc chuỗi để tính toán / biến đổi dữ liệu.
- Lặp cho đến khi dữ liệu thỏa mãn điều kiện nào đó (chờ nhập đúng, kéo dữ liệu từng trang...).
- Duyệt key/value của object khi không biết trước số lượng.
- Xử lý dữ liệu dạng bảng 2 chiều (ma trận, ô cờ, bảng điểm).

## 🎯 Ví dụ minh họa

```js
for (let i = 0; i < 5; i++) {
  console.log("Lần thứ", i); // 0 1 2 3 4
}

const user = { name: "Sơn", age: 18 };
for (const key in user) {
  console.log(key, user[key]); // name Sơn / age 18
}

const langs = ["HTML", "CSS", "JS"];
for (const value of langs) {
  console.log(value); // HTML CSS JS
}
```

## 📚 Tham khảo / Bài tập

- Xem chi tiết từng loại vòng lặp trong thư mục `01_loops/` với các file `1_for.js`, `2_for-in.js`, `3_for-of.js`, `4_while.js`, `5_do-while.js`, `6_break-continue.js`, `7_lap-long-nhau.js`.
- Chạy từng file bằng `node 01_loops/<ten-file>.js` trong terminal, quan sát kết quả in ra.
- Tự thử: viết vòng lặp tính tổng `1..100`, đảo ngược chuỗi, in ma trận `5x5`, và đếm số ký tự `a` trong một chuỗi.