# Hàm mũi tên nhìn từ góc độ khác

> Nguồn: [https://javascript.info/arrow-functions](https://javascript.info/arrow-functions)

<!-- fetched: 2026-09-14 -->

Hãy cùng xem lại về hàm mũi tên.

Hàm mũi tên không chỉ đơn giản là "cách viết tắt" cho các đoạn code nhỏ. Chúng có một số tính năng rất đặc thù và hữu ích.

JavaScript đầy rẫy những tình huống mà chúng ta cần viết một hàm nhỏ và truyền nó đến một nơi khác.

Ví dụ:

- `arr.forEach(func)` – `func` được thực thi bởi `forEach` cho mỗi phần tử mảng.
- `setTimeout(func)` – `func` được thực thi bởi bộ lập lịch tích hợp.
- …còn nhiều tình huống khác.

Việc tạo ra một hàm và truyền nó đi ở đâu đó chính là tinh thần cốt lõi của JavaScript.

Và trong những hàm như vậy, chúng ta thường không muốn rời khỏi ngữ cảnh hiện tại. Đó chính là lúc hàm mũi tên phát huy tác dụng.

## [Hàm mũi tên không có "this"](#arrow-functions-have-no-this)

Như chúng ta đã nhớ từ chương [Các phương thức object, "this"](/object-methods), hàm mũi tên không có `this`. Nếu `this` được truy cập, nó sẽ được lấy từ bên ngoài.

Ví dụ, chúng ta có thể dùng nó để lặp qua các phần tử bên trong một phương thức object:

```
let group = {
  title: "Nhóm của chúng tôi",
  students: ["John", "Pete", "Alice"],

  showList() {
    this.students.forEach(
      student => alert(this.title + ': ' + student)
    );
  }
};

group.showList();
```

Trong `forEach`, hàm mũi tên được sử dụng, nên `this.title` trong đó chính xác là cùng giá trị với phương thức bên ngoài `showList`. Tức là: `group.title`.

Nếu ta sử dụng hàm "thông thường", sẽ có lỗi:

```
let group = {
  title: "Nhóm của chúng tôi",
  students: ["John", "Pete", "Alice"],

  showList() {
    this.students.forEach(function(student) {
      // Lỗi: Cannot read property 'title' of undefined
      alert(this.title + ': ' + student);
    });
  }
};

group.showList();
```

Lỗi xảy ra vì `forEach` chạy các hàm với `this=undefined` theo mặc định, nên việc truy cập `undefined.title` sẽ bị lỗi.

Điều này không ảnh hưởng đến hàm mũi tên, vì chúng không có `this`.

Hàm mũi tên không thể gọi với `new`

Việc không có `this` đồng nghĩa với một hạn chế khác: hàm mũi tên không thể dùng làm constructor. Chúng không thể được gọi với `new`.

Hàm mũi tên VS bind

Có một sự khác biệt tinh tế giữa hàm mũi tên `=>` và hàm thông thường được gọi với `.bind(this)`:

- `.bind(this)` tạo ra một "phiên bản đã bind" của hàm.
- Hàm mũi tên `=>` không tạo ra bất kỳ binding nào. Hàm đơn giản là không có `this`. Việc tìm kiếm `this` được thực hiện giống hệt cách tìm kiếm biến thông thường: trong môi trường lexical bao quanh.

## [Hàm mũi tên không có "arguments"](#arrows-have-no-arguments)

Hàm mũi tên cũng không có biến `arguments`.

Điều đó thật tuyệt vời cho các bộ decorator, khi chúng ta cần chuyển tiếp lời gọi với `this` và `arguments` hiện tại.

Ví dụ, `defer(f, ms)` nhận một hàm và trả về một wrapper bao quanh nó, trì hoãn lời gọi đi `ms` mili giây:

```
function defer(f, ms) {
  return function() {
    setTimeout(() => f.apply(this, arguments), ms);
  };
}

function sayHi(who) {
  alert('Xin chào, ' + who);
}

let sayHiDeferred = defer(sayHi, 2000);
sayHiDeferred("John"); // Xin chào, John sau 2 giây
```

Thứ tự tương tự khi không dùng hàm mũi tên sẽ trông như thế này:

```
function defer(f, ms) {
  return function(...args) {
    let ctx = this;
    setTimeout(function() {
      return f.apply(ctx, args);
    }, ms);
  };
}
```

Ở đây chúng ta phải tạo thêm các biến `args` và `ctx` để hàm bên trong `setTimeout` có thể lấy chúng.

## [Tóm tắt](#summary)

Hàm mũi tên:

- Không có `this`
- Không có `arguments`
- Không thể gọi với `new`
- Chúng cũng không có `super`, nhưng chúng ta chưa học nó. Chúng ta sẽ học ở chương [Kế thừa lớp](/class-inheritance)

Điều đó là vì chúng được thiết kế cho các đoạn code ngắn, không có "ngữ cảnh" riêng, mà làm việc trong ngữ cảnh hiện tại. Và chúng thực sự tỏa sáng trong trường hợp sử dụng đó.
