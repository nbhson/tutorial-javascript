# Classes — Static và Private

## 🔑 Khái niệm

Class hỗ trợ hai hình thức thành viên đặc biệt:

**1. `static` — thuộc tính/phương thức tĩnh**

- Gắn với **chính class**, không phải instance.
- Truy cập qua `ClassName.staticMethod()` / `ClassName.staticField`.
- Bên trong static method, `this` trỏ tới **class** (không phải instance).

```js
class Counter {
  static count = 0;          // static field
  static inc() {
    this.count++;            // this = Counter
  }
}
Counter.inc();
console.log(Counter.count);  // 1
```

**2. `#private` — trường riêng tư (ES2022)**

- Thuộc tính bắt đầu bằng `#` chỉ truy cập được **bên trong class**.
- Truy cập từ ngoài (`c.#value`) → **SyntaxError**.
- Kết hợp getter/setter (`get value()` / `set value(v)`) để kiểm soát đọc/ghi.

```js
class Counter {
  #value = 42;               // private field
  get value() { return this.#value; }
  set value(v) { this.#value = v; }
}
```

## ✅ Điểm mạnh

- `static` dùng chung dữ liệu/hàm tiện ích không cần instance (counter, config, helper).
- `#private` bảo vệ dữ liệu nội bộ — không thể sửa trực tiếp từ ngoài.
- Getter/setter cho phép kiểm soát (validate) khi đọc ghi.
- Đúng chuẩn OOP: đóng gói (encapsulation) thật sự.

## ⚠️ Lưu ý / Hạn chế

- `static` method không dùng được `this.xxx` của instance (chỉ truy cập static khác).
- `#private` yêu cầu ES2022+ — trình duyệt/Node cũ không chạy được.
- Truy cập `#private` từ ngoài → SyntaxError sớm (bắt lỗi tại thời điểm phân tích, khó nuốt).
- Quên getter/setter, dữ liệu private "bất khả xâm phạm" nhưng cũng khó đọc từ ngoài.

## 💡 Khi nào dùng

- `static`: bộ đếm, hằng số cấu hình, method tiện ích không cần state instance.
- `#private`: bảo vệ dữ liệu nhạy cảm (mật, tiền, token nội bộ), chống sửa bậy.
- Getter/setter: kiểm tra giá trị trước khi gán (age >= 0, price > 0...).

## 🎯 Ví dụ minh họa

```js
class Counter {
  static count = 0;    // dùng chung cho class
  #value = 42;         // private: chỉ dùng trong class

  static inc() {
    this.count++;      // this = Counter
  }
  get value() {
    return this.#value;
  }
  set value(v) {
    this.#value = v;
  }
}

Counter.inc();
Counter.inc();
console.log(Counter.count); // 2

const c = new Counter();
console.log(c.value);  // 42
c.value = 100;          // qua setter
console.log(c.value);   // 100
// console.log(c.#value); // SyntaxError — không truy cập được
```

## 📚 Tham khảo / Bài tập

- Chạy `04_static-private/app.js` qua `index.html` hoặc `node app.js`: xem `Counter.count` tăng qua `static inc()`, và `#value` đọc ghi qua getter/setter.
- Tự thử: bỏ comment dòng `// console.log(c.#value)` để thấy **SyntaxError**; thêm `static reset() { this.count = 0; }` và gọi để đưa bộ đếm về 0.