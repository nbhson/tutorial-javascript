# Vòng Lặp (Loops)

## 🔑 Khái niệm

Đây là thư mục thực hành các loại vòng lặp cơ bản trong JavaScript, theo đúng lộ trình roadmap.sh. Mỗi file `.js` demo một loại vòng lặp riêng:

- `1_for.js` — vòng lặp `for` kinh điển với `for (khởi tạo; điều kiện; bước nhảy)`.
- `2_for-in.js` — `for...in` duyệt **key** của object (hoặc index của mảng/chuỗi).
- `3_for-of.js` — `for...of` duyệt **value** của mảng, chuỗi, iterable.
- `4_while.js` — `while` kiểm tra điều kiện **trước** khi chạy thân vòng lặp.
- `5_do-while.js` — `do...while` chạy thân vòng lặp **ít nhất 1 lần** rồi mới kiểm tra điều kiện.
- `6_break-continue.js` — dùng `break` dừng vòng lặp, `continue` bỏ qua lần lặp hiện tại.
- `7_lap-long-nhau.js` — vòng lặp lồng nhau (nested loop) duyệt mảng 2 chiều.

Điểm khác biệt cốt lõi giữa `while` và `do...while`: nếu điều kiện sai từ đầu, `while` không chạy lần nào, còn `do...while` vẫn chạy đúng 1 lần.

## ✅ Điểm mạnh

- **Mỗi file một chủ đề nhỏ** → học từng khái niệm một mà không bị quá tải.
- Được sắp xếp theo độ phức tạp tăng dần: từ vòng lặp đếm đơn giản đến lồng nhau.
- Ghép cặp trực tiếp với lý thuyết trên roadmap.sh (for, while, do...while, for...in, for...of, break/continue).
- Mỗi file chạy độc lập được với `node <tên-file>.js` → kiểm tra kết quả ngay.
- Ví dụ dùng dữ liệu gần gũi (object thông tin cá nhân, mảng ngôn ngữ, ma trận số).

## ⚠️ Lưu ý / Hạn chế

- `for...in` duyệt theo **key**: với object ra tên thuộc tính, với mảng ra index (dạng chuỗi `"0","1"...`), với chuỗi ra vị trí ký tự.
- `for...in` còn duyệt cả thuộc tính kế thừa từ prototype (xem ví dụ `forEach2` ở bài callback) — cần lọc bằng `hasOwnProperty` nếu muốn chính xác.
- `for...of` không duyệt trực tiếp object thường được; phải chuyển qua `Object.keys()`/`Object.values()`.
- Khi mảng có phần tử "trống" (như `courses.length = 10` trong `2_for-in.js`), `for...in` chỉ chạy qua các ô có dữ liệu thực, không chạy các ô trống.
- Vòng lặp lồng nhau làm tăng độ phức tạp theo bậc hai — tránh lồng quá sâu với dữ liệu lớn.

## 💡 Khi nào dùng

- `for` — khi biết chính xác số lần lặp (chạy 10 lần, chạy theo `array.length`).
- `for...in` — khi cần liệt kê key của object.
- `for...of` — khi cần lấy từng giá trị của mảng / chuỗi / iterable.
- `while` — khi chưa biết trước số lần lặp, chỉ biết điều kiện dừng.
- `do...while` — khi thân vòng lặp **bắt buộc** chạy ít nhất 1 lần (vd: hiện menu hỏi người dùng, luôn hỏi trước rồi mới kiểm tra).
- `break`/`continue` — khi muốn thoát sớm hoặc bỏ qua những phần tử không cần xử lý.
- Vòng lặp lồng nhau — khi xử lý bảng 2 chiều, ma trận, bảng cửu chương.

## 🎯 Ví dụ minh họa

```js
// 1_for.js — vòng lặp for
for (let i = 0; i < 5; i++) {
  console.log(i); // 0 1 2 3 4
}

// 6_break-continue.js — break/continue
for (let i = 0; i < 10; i++) {
  if (i === 5) continue;  // bỏ qua 5
  if (i === 8) break;     // dừng ở 8
  console.log(i);         // 0 1 2 3 4 6 7
}
```

## 📚 Tham khảo / Bài tập

- `node 1_for.js` — xem cú pháp `for` chuẩn.
- `node 2_for-in.js` — chạy và quan sát: key object, index mảng, vị trí ký tự, và hành vi với mảng có ô trống.
- `node 3_for-of.js` — so sánh kết quả với `for...in`; thử dùng `Object.entries()` để duyệt cả key lẫn value.
- `node 4_while.js` và `node 5_do-while.js` — thử đổi `i < 10` thành `i < 0` để thấy khác biệt: `while` không chạy, `do...while` chạy 1 lần.
- `node 6_break-continue.js` — tự thêm một điều kiện `continue` khác và đoán kết quả trước khi chạy.
- `node 7_lap-long-nhau.js` — tự viết vòng lặp in bảng cửu chương 2-9 hoặc một ma trận 3x3 khác.