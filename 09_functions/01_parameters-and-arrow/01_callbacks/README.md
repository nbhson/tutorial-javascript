# Callbacks (Hàm gọi lại)

## 🔑 Khái niệm

**Callback** là một hàm được **truyền vào như đối số của hàm khác** và được hàm đó **gọi lại** từ bên trong. Ba tính chất để nhận diện (ghi rõ trong `1_call-back.js`):

1. Nó **là một hàm**.
2. Nó **là một đối số** khi gọi hàm khác.
3. Nó **được gọi lại** bên trong hàm nhận đối số.

Ví dụ gốc trong `1_call-back.js`:

```js
function myFunction(param) {
  if (typeof param === "function") {
    param("Sơn Nguyễn");      // gọi callback
  }
}
function myCallback(value) {
  console.log("Value: ", value);
}
myFunction(myCallback);        // Value: Sơn Nguyễn
```

Sáu file trong thư mục đi từ **hiểu callback** đến **tự tái tạo các phương thức mảng**:

| File | Phương thức tái tạo | Ý nghĩa |
|---|---|---|
| `1_call-back.js` | — | định nghĩa callback cơ bản |
| `2_foreach.js` | `forEach2` | chạy callback với từng phần tử (kết hợp `for...in` + `hasOwnProperty`) |
| `3_filter.js` | `filter2` | giữ phần tử khi callback trả `true` |
| `4_some.js` | `some2` | `true` nếu có ít nhất một phần tử thỏa điều kiện |
| `5_every.js` | `every2` | `true` nếu **tất cả** phần tử thỏa điều kiện |
| `6_map.js` | `map2` | biến đổi và trả về mảng mới |

## ✅ Điểm mạnh

- Cách học "tự viết lại map/filter" giúp hiểu gốc rễ các phương thức mảng phổ biến.
- Callback trong `forEach`/`map`/`filter` được gọi với 3 đối số `(giá trị, index, mảng)` — các file tái tạo thể hiện rõ điều này.
- `hasOwnProperty` được dùng khéo léo để lọc các key kế thừa từ prototype (tránh duyệt nhầm `forEach2` khi dùng `for...in`).
- `some2`/`every2` minh họa **early exit** (dừng sớm) khi đã đủ kết quả.
- Tách từng khái niệm ra 1 file, dễ đọc dễ test.
- Nền tảng cho cách hiểu về event, API, Promise ở các bài sau.

## ⚠️ Lưu ý / Hạn chế

- Khi tự viết phương thức bằng `for...in`, phải dùng `hasOwnProperty` để **không duyệt cả thuộc tính prototype** — `this` của callback không đảm bảo (với arrow sẽ dùng `this` ngoài).
- `some` dừng ngay khi gặp phần tử thỏa mãn; `every` dừng ngay khi gặp phần tử không thỏa — đừng nhầm ý nghĩa trả về.
- `map` luôn trả mảng **cùng độ dài**; `filter` có thể trả mảng ngắn hơn.
- Callback không phải là hàm → gọi sẽ lỗi `TypeError`; nên kiểm tra `typeof callback === "function"` (cách làm đúng trong `1_call-back.js`).
- Lạm dụng callback lồng sâu sẽ rơi vào "callback hell" — gợi ý dùng Promise/async sau này.

## 💡 Khi nào dùng

- Duyệt và biến đổi mảng: `map` (đổi giá trị), `filter` (lọc), `forEach` (chạy tác động phụ).
- Kiểm tra sự tồn tại: `some` (có bất kỳ), `every` (tất cả).
- Xử lý sự kiện DOM, hẹn giờ, gọi API thành công/thất bại.
- Truyền "hành vi" cho thư viện (sort theo tiêu chí, validate theo rule).

## 🎯 Ví dụ minh họa

```js
// 1_call-back.js — gọi lại callback
function myFunction(param) {
  if (typeof param === "function") param("Sơn Nguyễn");
}
myFunction((value) => console.log("Value:", value));

// 6_map.js — map2 biến đổi từng phần tử
var courses = ["HTML", "CSS", "JS", "PHP"];
Array.prototype.map2 = function (callBack) {
  var result = [];
  for (let i = 0; i < this.length; i++) {
    result.push(callBack(this[i], i));
  }
  return result;
};
console.log(courses.map2((c, i) => c + " (free)"));
// ["HTML (free)", "CSS (free)", "JS (free)", "PHP (free)"]
```

## 📚 Tham khảo / Bài tập

- `node 1_call-back.js` — quan sát cách callback được gọi lại với tham số.
- `node 2_foreach.js` — xem `forEach2` in từng `course, index, rootArray`; thử bỏ dòng `hasOwnProperty` để thấy nó duyệt cả `forEach2` (key tự thêm).
- `node 3_filter.js` — đổi điều kiện `course.coin === 0` thành `> 100` và xem kết quả.
- `node 4_some.js` và `node 5_every.js` — sửa dữ liệu `coin` để so sánh khi nào `true`, khi nào `false`.
- `node 6_map.js` — tự thêm hậu tố khác (vd: `!!`) hoặc hoán đổi `i` và `c` trong callback.