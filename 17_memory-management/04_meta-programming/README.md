# Metaprogramming — Proxy và Reflect

## 🔑 Khái niệm

**Metaprogramming** là kỹ thuật lập trình trong đó chương trình có thể **đọc, sinh, phân tích hoặc tự sửa đổi** chính chương trình (hoặc chương trình khác) khi đang chạy. Trong JavaScript, nó hiện thực qua:

- **Reflection** — khả năng nhìn vào / can thiệp cấu trúc và hành vi của object lúc runtime, gồm:
  - *Introspection*: chỉ đọc cấu trúc (ví dụ `Object.keys()`).
  - *Self-Modification*: sửa đổi chính mình (ví dụ tự thêm property bằng hàm của chính object).
  - *Intercession*: thay đổi ngữ nghĩa của toán tử / hành vi mặc định.
- **Reflect API (ES6, giống `Math`)** — tập hàm tiện ích chuẩn hóa các thao tác thường làm thủ công: `Reflect.get()`, `Reflect.set()`, `Reflect.has()`, `Reflect.apply()`, `Reflect.construct()`, `Reflect.ownKeys()`, `Reflect.defineProperty()`... Dùng để *forward* mặc định bên trong Proxy.
- **Proxy (ES6)** — "wraper" bọc quanh object (`target`), cho phép **trap** (can thiệp) các thao tác qua `handler`: `get`, `set`, `has`, `apply`, `construct`, `deleteProperty`, `ownKeys`... Khi bạn thao tác qua proxy, trap chạy trước/sau lời gọi thật.

Kết hợp kinh điển: `Proxy` = nơi viết logic can thiệp; `Reflect` = nơi gọi *đúng hành vi mặc định* bên trong trap (giữ nguyên ngữ nghĩa gốc). Đây là nền tảng của **reactivity** (Vue/Polymer), validation, logging, computed property, observe changes.

File `app.js` trong thư mục này là ví dụ hoàn chỉnh: Proxy log mỗi lần GET/SET property trên object `employee` và dùng `Reflect` để chuyển tiếp mặc định.

## ✅ Điểm mạnh

- **Không xâm lấn**: kiểm soát hành vi object từ bên ngoài mà không sửa code gốc.
- **Reactivity**: phát hiện và phản ứng với mọi thay đổi property — nền tảng các framework hiện đại.
- **Validation/Tiền-điều-kiện**: chặn gán giá trị sai (loại, phạm vi) ngay tại `set` trap.
- **Computed / lười tạo property**: tính `fullName`, lỗi thân thiện cho property không tồn tại tại `get` trap.
- **Reflect chuẩn hóa** thao tác động — ít "lách" bằng cách kiểm tra thủ công.
- **Logging / tạo nhật ký truy cập** mà code ứng dụng không đổi.

## ⚠️ Lưu ý / Hạn chế

- **Hiệu năng**: mỗi lần truy cập qua proxy tốn thêm trap; đừng bọc proxy vào "hot path" vô tội vạ.
- **Khó gỡ lỗi**: hành vi bị ẩn sau trap, không ít lần phải "nhìn xuyên proxy" mới hiểu tại sao.
- **Ma thuật quá mức**: viết nhiều proxy làm code khó đọc, khó suy đoán — hãy giới hạn đúng chỗ.
- `Reflect.set` trả `false` khi không thể set (ví dụ property non-writable) — cần check để tránh im lặng thất bại.

## 💡 Khi nào dùng

- Xây dựng **system reactive** (state → UI) kiểu Vue: proxy thay cho việc poll hay setter thủ công.
- Validate **input/API boundary** ở một điểm tập trung thay vì rải rác.
- **Log / audit** mọi truy cập hoặc thay đổi dữ liệu nhạy cảm.
- Tạo **"computed" property ảo** (như `fullName`) hay message thân thiện cho field không tồn tại.
- Bọc **thư viện bên thứ ba** để thêm hành vi (thống kê, cache, đảo ngược) mà không fork code.

## 🎯 Ví dụ minh họa

```js
const employee = { firstName: 'Tapas', lastName: 'Adhikary' };

const logHandler = {
  get(target, field) {
    console.log('GET', field);              // truy vấn trước
    return Reflect.get(target, field);      // forward hành vi mặc định
  },
  set(target, key, value) {
    console.log('SET', key, '=', value);
    return Reflect.set(target, key, value);
  },
};

const p = new Proxy(employee, logHandler);
console.log(p.firstName);   // GET firstName -> Tapas
console.log(p.lastName);    // GET lastName -> Adhikary
p.age = 15;                 // SET age = 15
```

## 📚 Tham khảo / Bài tập

- Chạy `app.js` trong thư mục này (hoặc mở `index.html` với console): quan sát lần lượt `GET`, `SET`, rồi in `proxy` (chứa handler + target) và `employee` để thấy `age` đã được thêm thật.
- Xem `flow-1.png` để nắm luồng: code → handler (trap) → target → kết quả.
- Tự làm: thêm trap `get` trả `"No such property as, '${field}'!"` khi field không tồn tại, và trap `set` ném lỗi nếu `key === 'age' && !Number.isInteger(value)` (ví dụ gán `p.age = 'abc'` sẽ báo lỗi).
- Tự làm: viết một version "reactive" nhỏ — mỗi khi `set` chạy, tự động cập nhật một phần tử HTML (giống ví dụ trong `18_dom-apis/02_dom-advanced/05_reactivity`).