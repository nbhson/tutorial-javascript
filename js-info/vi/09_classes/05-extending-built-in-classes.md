# Kế thừa các built-in classes

> Nguồn: [https://javascript.info/extend-natives](https://javascript.info/extend-natives)

<!-- fetched: 2026-09-14 -->

Các built-in classes như Array, Map và các classes khác cũng có thể được extend.

Ví dụ, ở đây `PowerArray` kế thừa từ native `Array`:

```
// add one more method to it (can do more)
class PowerArray extends Array {
  isEmpty() {
    return this.length === 0;
  }
}

let arr = new PowerArray(1, 2, 5, 10, 50);
alert(arr.isEmpty()); // false

let filteredArr = arr.filter(item => item >= 10);
alert(filteredArr); // 10, 50
alert(filteredArr.isEmpty()); // false
```

Xin lưu ý một điều rất thú vị. Các built-in methods như `filter`, `map` và các methods khác – trả về các đối tượng mới chính xác của kiểu kế thừa `PowerArray`. Các internal implementation của chúng sử dụng property `constructor` của object cho việc đó.

Trong ví dụ trên,

```
arr.constructor === PowerArray
```

Khi `arr.filter()` được gọi, nó internally tạo mảng kết quả mới sử dụng chính xác `arr.constructor`, không phải `Array` basic. Điều đó thực sự rất tuyệt, vì chúng ta có thể tiếp tục sử dụng các phương thức `PowerArray` trên kết quả.

Thêm vào đó, chúng ta có thể tùy chỉnh behavior đó.

Chúng ta có thể thêm một static getter đặc biệt `Symbol.species` vào class. Nếu nó tồn tại, nó nên trả về constructor mà JavaScript sẽ sử dụng internally để tạo các entities mới trong `map`, `filter` và vân vân.

Nếu chúng ta muốn các built-in methods như `map` hoặc `filter` trả về các mảng thường, chúng ta có thể trả về `Array` trong `Symbol.species`, như ở đây:

```
class PowerArray extends Array {
  isEmpty() {
    return this.length === 0;
  }

  // built-in methods will use this as the constructor
  static get [Symbol.species]() {
    return Array;
  }
}

let arr = new PowerArray(1, 2, 5, 10, 50);
alert(arr.isEmpty()); // false

// filter creates new array using arr.constructor[Symbol.species] as constructor
let filteredArr = arr.filter(item => item >= 10);

// filteredArr is not PowerArray, but Array
alert(filteredArr.isEmpty()); // Error: filteredArr.isEmpty is not a function
```

Như bạn có thể thấy, bây giờ `.filter` trả về `Array`. Vì vậy extended functionality không được truyền xa hơn.

Các collections khác hoạt động tương tự

Các collections khác, như `Map` và `Set`, hoạt động giống hệt. Chúng cũng sử dụng `Symbol.species`.

## [Không có static inheritance trong built-ins](#khong-co-static-inheritance-trong-built-ins)

Các built-in objects có các phương thức static riêng, ví dụ `Object.keys`, `Array.isArray` v.v.

Như chúng ta đã biết, các native classes extend lẫn nhau. Ví dụ `Array` extends `Object`.

Thông thường, khi một class extend một class khác, cả static và non-static methods được inheritance. Điều đó đã được giải thích kỹ trong bài viết [Static properties and methods](/static-properties-methods#statics-and-inheritance).

Nhưng các built-in classes là một exception. Chúng không kế thừa statics từ nhau.

Ví dụ, cả `Array` và `Date` kế thừa từ `Object`, vì vậy các instances của chúng có các methods từ `Object.prototype`. Nhưng `Array.[[Prototype]]` không reference đến `Object`, vì vậy không có, ví dụ, `Array.keys()` (hoặc `Date.keys()`) static method.

Đây là cấu trúc hình cho `Date` và `Object`:

![](/article/extend-natives/object-date-inheritance.svg)

Như bạn có thể thấy, không có liên kết giữa `Date` và `Object`. Chúng độc lập, chỉ `Date.prototype` kế thừa từ `Object.prototype`.

Đó là một sự khác biệt quan trọng của inheritance giữa các built-in objects so với những gì chúng ta nhận được với `extends`.
