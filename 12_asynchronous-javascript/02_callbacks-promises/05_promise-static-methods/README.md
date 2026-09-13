# Promise Static Methods — `resolve` / `reject` / `all` / `race`

## 🔑 Khái niệm

Ngoài `new Promise(executor)`, Promise cung cấp các **phương thức tĩnh** (gọi trên chính `Promise`, không cần instance) để tạo và kết hợp promise:

| Phương thức | Công dụng |
|-------------|-----------|
| `Promise.resolve(value)` | tạo promise đã **fulfilled** ngay với giá trị cho trước |
| `Promise.reject(reason)` | tạo promise đã **rejected** ngay với lý do |
| `Promise.all([p1, p2, ...])` | chờ **tất cả** settle; fail nếu có bất kỳ cái nào reject |
| `Promise.race([p1, p2, ...])` | trả về kết quả của cái **settle đầu tiên** |
| `Promise.allSettled` | chờ tất cả, báo từng trạng thái dù fail hay success |
| `Promise.any` | trả về cái **fulfilled đầu tiên** |

Điểm quan trọng với `Promise.all`: các promise trong mảng chạy **song song** (không tuần tự), và chỉ khi tất cả xong thì `.then` mới chạy. Nếu một promise `reject` ngay từ đầu → `all` fail luôn.

## ✅ Điểm mạnh

- `Promise.all` chạy song song nhiều tác vụ, chỉ cần một `.then` khi đủ kết quả.
- Tạo nhanh promise thành công/thất bại để test hoặc wrap giá trị đồng bộ.
- `Promise.race` lấy kết quả nhanh nhất — hữu ích cho timeout.
- Rõ ràng: ai reject thì `all` reject, ai xong sớm thì `race` thắng.

## ⚠️ Lưu ý / Hạn chế

- `Promise.all` **từ chối toàn bộ** nếu chỉ một promise reject — cẩn thận khi gọi nhiều API độc lập.
- `race` chỉ chào đón cái settle đầu tiên (có thể là reject).
- Khai báo trong mảng không có nghĩa thứ tự kết quả theo thứ tự chạy xong.
- `Promise.reject` không có `.catch` đi kèm → unhandled rejection.

## 💡 Khi nào dùng

- Gọi đồng thời nhiều endpoint rồi gộp kết quả (`Promise.all`).
- Wrap một object thành promise cho đồng bộ API (`Promise.resolve`).
- Timeout cho một tác vụ chậm (`Promise.race([task, timeout])`).

## 🎯 Ví dụ minh họa

```js
const p1 = new Promise((res) => setTimeout(() => { console.log("5s"); res([1]); }, 5000));
const p2 = new Promise((res) => setTimeout(() => { console.log("2.5s"); res([2, 3]); }, 2500));

Promise.all([p1, p2])
  .then(function (result) {
    const [arr1, arr2] = result;
    console.log(arr1.concat(arr2)); // [1, 2, 3] — chờ cả hai xong
  })
  .catch((err) => console.log(err));

Promise.resolve("Success!")   // fulfilled ngay
  .then((v) => console.log(v)); // Success!
```

## 📚 Tham khảo / Bài tập

- Chạy `05_promise-static-methods/app.js` (qua `index.html` hoặc `node app.js`): `Promise.all([p1, p2])` chờ cả hai (in `5s`, `2.5s` rồi `[1, 2, 3]`).
- Tự thử: bỏ comment dòng `var promise3 = Promise.reject("Fail")` và thêm vào mảng `Promise.all` — xem toàn bộ rơi vào `.catch` dù p1/p2 vẫn hoàn thành. Sau đó thử `Promise.race([p1, p2])` xem ai về đích trước.