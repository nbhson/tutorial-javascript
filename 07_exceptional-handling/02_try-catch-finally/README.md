# try / catch / finally

## 🔑 Khái niệm

`try...catch...finally` là cấu trúc **bắt và xử lý lỗi**:

- **`try`** — khối code có thể gây lỗi, JavaScript thử chạy nó.
- **`catch`** — chỉ chạy khi có lỗi được ném trong `try`; nhận tham số là giá trị bị ném.
- **`finally`** — **luôn luôn chạy**, thành công hay thất bại đều chạy, kể cả khi có `return` hoặc `throw` trong `try`.

```js
try {
  risky(); // code có thể ném lỗi
} catch (e) {
  handle(e); // chạy nếu có lỗi
} finally {
  cleanup(); // luôn chạy, thường để dọn dẹp
}
```

Hai quy tắc cốt lõi được minh họa trong `app.js`:

1. **`finally` luôn chạy** — kể cả khi `try` ném lỗi và `catch` xử lý xong.
2. **`finally` lồng nhau** — cấp trong chạy trước, rồi lỗi mới được cấp ngoài bắt.

Ví dụ trong `app.js`:

```js
try { risky(); }
catch (e) { console.log("catch", e.message); }
finally { console.log("finally"); }
```

## ✅ Điểm mạnh

- **An toàn tuyệt đối cho tài nguyên**: dọn dẹp bằng `finally` không bao giờ bị bỏ sót.
- Riêng `catch` có thể bỏ tham số (ES2019) khi chỉ cần `finally` để xử lý hậu kỳ.
- Nhiều khối `try...catch` lồng nhau giúp xử lý lỗi theo từng tầng trách nhiệm.
- Lỗi được bắt đúng chỗ, chương trình tiếp tục chạy phần còn lại thay vì dừng.
- Phân tách rõ ba giai đoạn: chạy thử / xử lý lỗi / dọn dẹp.

## ⚠️ Lưu ý / Hạn chế

- **Chỉ bắt được lỗi đồng bộ** trong `try`; lỗi bên trong callback, setInterval, promise không bị bắt trực tiếp.
- Nếu `finally` tự ném lỗi, lỗi đó sẽ **che** lỗi gốc của `try` — khó debug.
- `return` trong `try` không ngăn được `finally` chạy (nhưng giá trị return của `try` vẫn được giữ).
- Quá nhiều `try...catch` lồng nhau làm code khó theo dõi — hãy để lỗi "nổi lên" tầng phù hợp.

## 💡 Khi nào dùng

- Gọi API, đọc file, thao tác localStorage — dễ lỗi mạng/lỗi dữ liệu.
- Đóng tài nguyên bắt buộc: xóa loading spinner, đóng modal, xóa timers — đặt ở `finally`.
- Xử lý JSON chưa chắc hợp lệ (`JSON.parse`).
- Chuyển lỗi hệ thống thành thông báo thân thiện với người dùng.

## 🎯 Ví dụ minh họa

```js
// Nội dung app.js trong thư mục
function risky() {
  throw new Error("fail");
}

try {
  risky();
} catch (e) {
  console.log("catch", e.message); // catch fail
} finally {
  console.log("finally");          // luôn in ra
}

// finally lồng trong finally
try {
  try {
    throw new Error("inner");
  } finally {
    console.log("inner finally");  // chạy trước
  }
} catch (e) {
  console.log("outer catch");      // chạy sau
}
```

## 📚 Tham khảo / Bài tập

- Mở `index.html` trên trình duyệt (Console) để thấy thứ tự: `catch fail` → `finally` → `inner finally` → `outer catch`.
- Chạy `node app.js` trong terminal với cùng kết quả.
- Tự thử: thêm `return 42;` vào cuối khối `try` và thấy `finally` vẫn in ra trước khi hàm kết thúc.
- Viết hàm `readSetting()` có `try` đọc localStorage, `catch` trả về giá trị mặc định, `finally` in `"done"`.