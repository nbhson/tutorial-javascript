# async / await

## 🔑 Khái niệm

`async/await` là cú pháp (ES2017) giúp làm việc với promise **như code đồng bộ** — dễ đọc hơn nhiều so với chuỗi `.then()`.

- Thêm `async` trước một hàm → hàm trở thành **async function**, luôn trả về một Promise.
- Bên trong async function, dùng `await` trước một lời gọi trả về promise: code **chờ** tại điểm đó cho đến khi promise settle. If fulfilled → nhận được giá trị; if rejected → lỗi được **ném ra** như throw.

```js
async function fetchProducts() {
  try {
    const response = await fetch(".../products.json"); // chờ fetch()
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    const data = await response.json(); // chờ parse JSON
    console.log(data[0].name);
  } catch (error) {
    console.error(`Could not get products: ${error}`);
  }
}
```

Điểm cốt lõi: `await` chỉ hợp lệ **bên trong async function**. Có thể dùng `try/catch` quen thuộc để bắt lỗi thay vì `.catch`.

## ✅ Điểm mạnh

- Code nhìn tuần tự, dễ đọc, dễ bảo trì cho chuỗi nhiều bước.
- Lỗi xử lý bằng `try/catch` truyền thống — quen thuộc với đa số dev.
- Vẫn đầy đủ sức mạnh promise: `Promise.all` kết hợp được với `await`.
- Giảm "callback hell" và chain `.then()` dài ngoằng.

## ⚠️ Lưu ý / Hạn chế

- Quên `await` → bạn nhận về Promise chứ không phải giá trị.
- `await` ngoài async function → `SyntaxError`.
- `await` tuần tự nhiều tác vụ độc lập sẽ chậm — hãy dùng `Promise.all`.
- Nếu không `try/catch`, lỗi bị ném ra → unhandled rejection.

## 💡 Khi nào dùng

- Đọc/ghi dữ liệu tuần tự phụ thuộc nhau (tạo -> sửa -> hiển thị).
- Mọi tác vụ fetch/API — đặc biệt khi cần xử lý nhiều bước.
- Làm sạch callback chain khi migrate code cũ sang promise.

## 🎯 Ví dụ minh họa

```js
async function getUser(id) {
  const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  if (!res.ok) throw new Error("Bad request");
  return res.json();
}

async function main() {
  try {
    const user = await getUser(1);
    console.log(user.name); // Leanne Graham
  } catch (err) {
    console.error(err.message);
  }
}
main();
```

## 📚 Tham khảo / Bài tập

- Folder có `02_async-await/app.js` đang **trống** — hãy tự dán code `async function` ở trên vào và chạy (qua `node app.js` hoặc DevTools).
- Tự thử: viết async function thực hiện 2 lần `await fetch` tuần tự, sau đó đổi sang `Promise.all` và so sánh thời gian hoàn thành.