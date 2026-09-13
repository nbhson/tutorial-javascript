# Đệ quy (Recursion)

## 🔑 Khái niệm

**Đệ quy** là kỹ thuật mà một hàm **gọi lại chính nó** để giải bài toán bằng cách thu nhỏ nó dần thành những phiên bản đơn giản hơn, cho đến khi gặp trường hợp cơ sở (base case).

File `app.js` có hai ví dụ kinh điển:

```js
function factorial(n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
console.log(factorial(5), factorial(6)); // 120 720

function fib(n) {
  return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}
console.log(fib(7)); // 13
```

**Cách `factorial(4)` chạy:**

- `factorial(4)` = `4 * factorial(3)`
- `factorial(3)` = `3 * factorial(2)`
- `factorial(2)` = `2 * factorial(1)`
- `factorial(1)` = `1` (base case → dừng đệ quy)
- → rồi "tháo ngược" từ dưới lên, ra kết quả cuối `24`.

**Base case** là điều kiện dừng — nếu thiếu, hàm gọi chính nó không bao giờ kết thúc và nổ `Maximum call stack size exceeded` (tràn ngăn xếp).

## ✅ Điểm mạnh

- **Rất tự nhiên** cho bài toán có cấu trúc lặp lại (cây, thư mục, chuỗi lồng nhau).
- Code gọn và gần với công thức toán học (`n! = n * (n-1)!`).
- Dễ chứng minh đúng sai khi base case hợp lý.
- Hữu ích khi duyệt cấu trúc phân cấp: comment trả lời lồng nhau, JSON lồng.
- Kết hợp tốt với chia để trị (divide & conquer) như quicksort, mergesort.

## ⚠️ Lưu ý / Hạn chế

- **Phải có base case**, nếu không dẫn đến tràn call stack (stack overflow).
- Mỗi lần gọi đệ quy tốn một frame trong call stack — độ sâu quá lớn sẽ lỗi (khoảng vài chục nghìn).
- `fib` kiểu đơn giản có **độ phức tạp mũ O(2^n)** — lãng phí (tính lặp lại vô số lần); nên dùng memoization hoặc vòng lặp cho số lớn.
- Đệ quy đôi khi khó đọc và khó debug hơn vòng lặp, đặc biệt với người mới.

## 💡 Khi nào dùng

- Tính giai thừa, lũy thừa, dãy Fibonacci (nhỏ).
- Duyệt cây DOM, cây thư mục, cây bình luận.
- Duyệt/flatten object hoặc mảng lồng nhau nhiều tầng.
- Thuật toán chia để trị: quicksort, mergesort, binary search.
- Backtracking: giải mê cung, sudoku, tạo hoán vị.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
function factorial(n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
console.log(factorial(5), factorial(6)); // 120 720

function fib(n) {
  return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}
console.log(fib(7)); // 13

// Đệ quy duyệt mảng lồng nhau
function flatten(arr) {
  let out = [];
  for (const item of arr) {
    if (Array.isArray(item)) out = out.concat(flatten(item));
    else out.push(item);
  }
  return out;
}
console.log(flatten([1, [2, [3, 4]], 5])); // [1, 2, 3, 4, 5]
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` (Console) hoặc chạy `node app.js` để thấy `120 720` và `13`.
- Tự thử `factorial(0)` → `1` (base case `n <= 1` bắt được).
- Tự thử `factorial(100000)` để thấy lỗi "Maximum call stack size exceeded" — hiểu giới hạn ngăn xếp.
- Tự thử `fib(50)` và so sánh thời gian chạy với viết lại bằng vòng lặp (`O(n)`).
- Viết thêm hàm `sumDigits(123)` trả về `6` theo kiểu đệ quy (chia 10 lấy dư).