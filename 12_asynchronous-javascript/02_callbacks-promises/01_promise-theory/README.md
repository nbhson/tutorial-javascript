# Promise — Lý thuyết nền tảng

## 🔑 Khái niệm

**Promise** là đối tượng được trả về bởi một hàm bất đồng bộ, **đại diện cho trạng thái hiện tại** của hoạt động đó. Promises chính là nền tảng của lập trình bất đồng bộ hiện đại trong JavaScript.

Một promise có 3 trạng thái:

- `pending` — promise đã được tạo, tác vụ chưa thành công hoặc thất bại.
- `fulfilled` — tác vụ **thành công**; khi đó handler `.then()` được gọi.
- `rejected` — tác vụ **thất bại**; khi đó handler `.catch()` được gọi.

Chuỗi xử lý điển hình: `fetch()` trả về promise → `.then()` kiểm tra/parse → `.catch()` bắt lỗi → `.finally()` luôn chạy.

## ✅ Điểm mạnh

- Ưu tiên cao (microtask): kết quả được xử lý ngay khi call stack trống.
- Xử lý lỗi tập trung, tránh lồng callback.
- Dễ kết hợp nhiều promise bằng `Promise.all`...
- Là nền tảng cho `async/await`.

## ⚠️ Lưu ý / Hạn chế

- A promise **chỉ settle một lần** — trạng thái không quay lại `pending`.
- Nếu không có `.catch()`, lỗi rejection có thể "rơi im lặng" (hoặc ném lỗi unhandled).
- `then()` luôn trả về promise mới — dễ tạo chain dài vô tình.
- Phải kiểm tra `response.ok` vì `fetch` không throw khi HTTP lỗi.

## 💡 Khi nào dùng

- Fetch dữ liệu, gọi API, đọc file — bất kỳ tác vụ bất đồng bộ nào.
- Xử lý theo giai đoạn: kiểm tra response → parse JSON → render.
- Chờ nhiều tác vụ cùng lúc (`Promise.all`).

## 🎯 Ví dụ minh họa

```js
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.json();   // trả về promise → nối tiếp .then
  })
  .then((data) => console.log(data.title))
  .catch((error) => console.error(`Could not get post: ${error}`));
```

## 📚 Tham khảo / Bài tập

- Folder này **không có file chạy** — mở DevTools Console của trình duyệt và dán đoạn trên để thử.
- Tự thử: dùng `Promise.all` gọi 2-3 endpoint cùng lúc và in ra `url: status` của từng cái, rồi đổi sang một URL lỗi để xem `.catch` bắt lỗi như nào.