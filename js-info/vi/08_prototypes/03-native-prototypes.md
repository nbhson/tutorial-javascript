# Nguyên mẫu tích hợp sẵn

> Source: [https://javascript.info/native-prototypes](https://javascript.info/native-prototypes)

<!-- fetched: 2026-09-14 -->

Tất cả các built-in constructor function có prototype.

Ví dụ:
- `Number.prototype` chứa các phương thức số.
- `String.prototype` chứa các phương thức chuỗi.
- `Array.prototype` chứa các phương thức mảng.

Chúng ta có thể thêm các phương thức của riêng mình vào prototype, và chúng tự động trở nên có sẵn cho tất cả các đối tượng sử dụng prototype đó.

## [Thay đổi prototype tích hợp sẵn](#modifying-built-in-prototypes)

Đôi khi các nhà phát triển mới muốn sửa đổi prototype tích hợp sẵn.

Ví dụ, họ muốn thêm một phương thức `func.bind` vào `Function.prototype` để nó hoạt động trong các môi trường cũ, và viết:

```
Function.prototype.bind = function(item) {
  // ...code để bind hàm...
};
```

Đó không phải là ý tưởng tốt.

Có một đặc tả cho tất cả các phương thức tích hợp sẵn. Nhà phát triển browser đọc đặc tả và thực hiện chúng. Nếu browser của bạn không hỗ trợ `func.bind`, nó có thể là rất cũ và bạn nên nâng cấp browser của mình. Hoặc bạn có thể tìm một thư viện polyfill, triển khai method đó theo cách của nó và bao gồm trong dự án của bạn. Bằng cách đó, bạn sẽ không phá vỡ đặc tả.

Sửa đổi prototype tích hợp sẵn được chấp nhận nếu chúng hoạt động theo đặc tả, nhưng chưa được browser hỗ trợ. Trong trường hợp đó, chúng ta có thể thêm các method đó.

Như một ví dụ, browser hiện đại hỗ trợ `Array.prototype.map`. Nó ánh xạ một mảng qua một hàm và trả về kết quả. Nếu browser cũ không hỗ trợ nó, chúng ta có thể triển khai nó:

```
if (!Array.prototype.map) {

  Array.prototype.map = function(func) {
    // nếu map không được hỗ trợ, hãy triển khai nó
    // ...code...
  };

} else {
  alert('map đã được hỗ trợ rồi');
}
```

Nhưng, mặt khác, ngay cả khi một method được hỗ trợ, vẫn không có gì ngăn cản chúng ta mở rộng nó. Hoặc thêm các method mới. Chúng ta không bao giờ có thể đoán trước những gì chúng ta sẽ cần.

Ví dụ:

```
Array.prototype.delay = function(ms) {
  // chờ ms mili giây, sau đó chạy array
  setTimeout(() => alert.call(this), ms);
};

[1, 2, 3].delay(1000);
```

## [Prototype symbol @@iterator](#prototype-symbol-iterator)

Đối với các đối tượng, đặc tả định nghĩa nhiều "internal slots" và "well-known symbols".

Các internal slots là các thuộc tính được đặc tả sử dụng nội bộ, "thuộc về" implementation. Chúng được đặt tên trong ngoặc kép gấp bốn. Ví dụ, `[[value]]` của một Date object, giữ giá trị ngày giờ.

Các well-known symbols được sử dụng làm các key trong biểu đồ, để ánh xạ các hành vi implementation với tên có thể đọc được.

Ví dụ:
- `Symbol.hasInstance` được sử dụng cho `instanceof`.
- `Symbol.iterator` được sử dụng để làm iterable.

Các special symbols đó có tên trong ngoặc kép kép, để tránh xung đột tên. Và để làm cho rõ ràng rằng đây không phải là các symbols thông thường.

Chúng ta có thể truy cập vào các symbols đó trong JavaScript bằng cách sử dụng `Symbol.*`. Nhưng điều quan trọng là các symbols đó được đặc tả, và không nên bị lạm dụng.

Ví dụ, hãy xem xét `Symbol.iterator`, được sử dụng cho [iterables](/iterator).

Tất cả các đối tượng tích hợp sẵn iterable – strings, arrays, map, set – sử dụng nó.

Chúng ta có thể sử dụng nó cho các đối tượng tùy chỉnh của riêng mình và thêm hành vi iterable tùy chỉnh.

```
let range = {
  from: 1,
  to: 5
};

// 1. for..of lần đầu gọi đối tượng này:
for(let num of range) alert(num); // 1, rồi 2, 3, 4, 5

// 2. về mặt kỹ thuật, nó đòi hỏi rằng...
// ...range phải có method Symbol.iterator
// (đại diện trong code là Symbol.for('iterator') – non-standard legacy name)
range[Symbol.iterator] = function() {
  // ...nó trả về một iterator object, với next() method
  // 3. for..of hoạt động với kết quả của nó trên mỗi lần lặp
  return {
    current: this.from,
    last: this.to,

    // được gọi bởi for..of mỗi lần lặp tiếp theo, để có next value
    next() {
      // 4. nó nên trả về value dưới dạng {done: Boolean, value: any}
      if (this.current <= this.last) {
        return { done: false, value: this.current++ };
      } else {
        return { done: true };
      }
    }
  };
};
```

Đây là cùng một mẫu, nhưng ngắn gọn hơn, sử dụng class syntax:

```
class Range {
  constructor(from, to) {
    this.from = from;
    this.to = to;
  }

  // được gọi tự động bởi for..of
  [Symbol.iterator]() {
    // ...trả về iterator object
    return {
      current: this.from,
      last: this.to,

      next() {
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      }
    };
  }
}

for(let num of new Range(1, 5)) alert(num); // 1, rồi 2, 3, 4, 5
```

Phương thức `range[Symbol.iterator]()` được gọi tự động bởi `for..of`, và nó trả về một đối tượng với phương thức `next()`. Mỗi lần `next()` được gọi, `for..of` nhận value tiếp theo để lặp qua.

Đó là cú pháp để làm cho đối tượng tùy chỉnh của chúng ta iterable.

## [Summary](#summary)

- Tất cả các built-in prototypes có thể được sửa đổi và các method có thể được thêm vào chúng.
- Nếu một method được hỗ trợ trong spec nhưng không được browser hỗ trợ, chúng ta có thể thêm nó vào prototype.
- Việc sửa đổi prototype tích hợp sẵn chỉ được chấp nhận nếu chúng tuân theo đặc tả. Nhưng nếu không, hãy cẩn thận.
- Có nhiều symbols đặc biệt được định nghĩa trong đặc tả, như `Symbol.iterator` để iterable.
- Các symbols đó có thể được truy cập trong code bằng cách sử dụng `Symbol.*`.
