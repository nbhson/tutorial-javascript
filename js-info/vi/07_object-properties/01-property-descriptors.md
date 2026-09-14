# cờ và mô tả thuộc tính

> Source: [https://javascript.info/property-descriptors](https://javascript.info/property-descriptors)

<!-- fetched: 2026-09-14 -->

Như chúng ta đã biết, các đối tượng có thể lưu trữ các thuộc tính.

Cho đến nay, một thuộc tính là một cặp "key-value" đơn giản đối với chúng ta. Nhưng một thuộc tính đối tượng thực sự là một thứ linh hoạt và mạnh mẽ hơn nhiều.

Trong chương này, chúng ta sẽ nghiên cứu các tùy chọn cấu hình bổ sung, và trong chương tiếp theo, chúng ta sẽ xem cách biến chúng thành các hàm getter/setter một cách vô hình.

## [cờ thuộc tính](#property-flags)

Thuộc tính đối tượng, ngoài **`value`**, có ba thuộc tính đặc biệt (được gọi là "cờ"):

- **`writable`** – nếu `true`, giá trị có thể thay đổi, nếu không thì chỉ đọc.
- **`enumerable`** – nếu `true`, thì được liệt kê trong các vòng lặp, nếu không thì không.
- **`configurable`** – nếu `true`, thuộc tính có thể bị xóa và các thuộc tính này có thể được sửa đổi, nếu không thì không.

Chúng ta chưa thấy chúng vì nói chung chúng không hiện ra. Khi chúng ta tạo một thuộc tính "theo cách thông thường", tất cả đều là `true`. Nhưng chúng ta cũng có thể thay đổi chúng bất cứ lúc nào.

Đầu tiên, hãy xem cách lấy các cờ đó.

Phương thức [Object.getOwnPropertyDescriptor](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyDescriptor) cho phép truy vấn *toàn bộ* thông tin về một thuộc tính.

Cú pháp là:

```
let descriptor = Object.getOwnPropertyDescriptor(obj, propertyName);
```

`obj`
:   Đối tượng để lấy thông tin từ đó.

`propertyName`
:   Tên của thuộc tính.

Giá trị trả về là một đối tượng mô tả "thuộc tính" (property descriptor): nó chứa giá trị và tất cả các cờ.

Ví dụ:

```
let user = {
  name: "John"
};

let descriptor = Object.getOwnPropertyDescriptor(user, 'name');

alert( JSON.stringify(descriptor, null, 2 ) );
/* property descriptor:
{
  "value": "John",
  "writable": true,
  "enumerable": true,
  "configurable": true
}
*/
```

Để thay đổi các cờ, chúng ta có thể sử dụng [Object.defineProperty](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty).

Cú pháp là:

```
Object.defineProperty(obj, propertyName, descriptor)
```

`obj`, `propertyName`
:   Đối tượng và thuộc tính của nó để áp dụng mô tả.

`descriptor`
:   Đối tượng mô tả thuộc tính để áp dụng.

Nếu thuộc tính tồn tại, `defineProperty` cập nhật các cờ của nó. Nếu không, nó tạo thuộc tính mới với giá trị và cờ đã cho; trong trường hợp đó, nếu một cờ không được cung cấp, nó được giả định là `false`.

Ví dụ, đây là thuộc tính `name` được tạo với tất cả các cờ falsy:

```
let user = {};

Object.defineProperty(user, "name", {
  value: "John"
});

let descriptor = Object.getOwnPropertyDescriptor(user, 'name');

alert( JSON.stringify(descriptor, null, 2 ) );
/*
{
  "value": "John",
  "writable": false,
  "enumerable": false,
  "configurable": false
}
 */
```

So sánh với `user.name` được tạo "bình thường" ở trên: giờ đây tất cả các cờ đều là falsy. Nếu đó không phải là những gì chúng ta muốn thì tốt hơn là đặt chúng thành `true` trong `descriptor`.

Giờ hãy xem hiệu ứng của các cờ qua ví dụ.

## [Không thể ghi](#non-writable)

Hãy làm cho `user.name` không thể ghi (không thể gán lại) bằng cách thay đổi cờ `writable`:

```
let user = {
  name: "John"
};

Object.defineProperty(user, "name", {
  writable: false
});

user.name = "Pete"; // Error: Cannot assign to read only property 'name'
```

Giờ không ai có thể thay đổi tên của người dùng của chúng ta, trừ khi họ áp dụng `defineProperty` của riêng họ để ghi đè lên cái của chúng ta.

Lỗi chỉ xuất hiện trong chế độ strict

Ở chế độ không strict, không có lỗi xảy ra khi ghi vào các thuộc tính không thể ghi và tương tự. Nhưng hoạt động vẫn sẽ không thành công. Các hành động vi phạm cờ chỉ bị bỏ qua một cách im lặng trong chế độ không strict.

Đây là cùng một ví dụ, nhưng thuộc tính được tạo từ đầu:

```
let user = { };

Object.defineProperty(user, "name", {
  value: "John",
  // cho các thuộc tính mới, chúng ta cần liệt kê rõ ràng những gì là true
  enumerable: true,
  configurable: true
});

alert(user.name); // John
user.name = "Pete"; // Error
```

## [Không liệt kê được](#non-enumerable)

Giờ hãy thêm `toString` tùy chỉnh vào `user`.

Theo mặc định, `toString` tích hợp sẵn cho các đối tượng là không liệt kê được, nó không hiện ra trong `for..in`. Nhưng nếu chúng ta thêm một `toString` của riêng mình, thì theo mặc định nó sẽ hiện ra trong `for..in`, như thế này:

```
let user = {
  name: "John",
  toString() {
    return this.name;
  }
};

// Theo mặc định, cả hai thuộc tính của chúng ta đều được liệt kê:
for (let key in user) alert(key); // name, toString
```

Nếu chúng ta không thích điều đó, thì chúng ta có thể đặt `enumerable:false`. Khi đó nó sẽ không xuất hiện trong vòng lặp `for..in`, giống như cái tích hợp sẵn:

```
let user = {
  name: "John",
  toString() {
    return this.name;
  }
};

Object.defineProperty(user, "toString", {
  enumerable: false
});

// Giờ toString của chúng ta biến mất:
for (let key in user) alert(key); // name
```

Các thuộc tính không liệt kê được cũng bị loại trừ từ `Object.keys`:

```
alert(Object.keys(user)); // name
```

## [Không thể cấu hình](#non-configurable)

Cờ không thể cấu hình (`configurable:false`) đôi khi được đặt sẵn cho các đối tượng và thuộc tính tích hợp sẵn.

Một thuộc tính không thể cấu hình không thể bị xóa, các thuộc tính của nó không thể bị sửa đổi.

Ví dụ, `Math.PI` là không thể ghi, không liệt kê được và không thể cấu hình:

```
let descriptor = Object.getOwnPropertyDescriptor(Math, 'PI');

alert( JSON.stringify(descriptor, null, 2 ) );
/*
{
  "value": 3.141592653589793,
  "writable": false,
  "enumerable": false,
  "configurable": false
}
*/
```

Vì vậy, lập trình viên không thể thay đổi giá trị của `Math.PI` hoặc ghi đè lên nó.

```
Math.PI = 3; // Error, because it has writable: false

// delete Math.PI won't work either
```

Chúng ta cũng không thể thay đổi `Math.PI` thành `writable` nữa:

```
// Error, because of configurable: false
Object.defineProperty(Math, "PI", { writable: true });
```

Không có gì chúng ta có thể làm với `Math.PI`.

Việc làm cho một thuộc tính không thể cấu hình là một con đường một chiều. Chúng ta không thể thay đổi nó trở lại bằng `defineProperty`.

**Xin lưu ý: `configurable: false` ngăn chặn việc thay đổi các cờ thuộc tính và xóa thuộc tính, trong khi cho phép thay đổi giá trị của nó.**

Ở đây `user.name` là không thể cấu hình, nhưng chúng ta vẫn có thể thay đổi nó (vì nó có thể ghi được):

```
let user = {
  name: "John"
};

Object.defineProperty(user, "name", {
  configurable: false
});

user.name = "Pete"; // works fine
delete user.name; // Error
```

Và ở đây chúng ta làm cho `user.name` trở thành một hằng số "bị niêm phong vĩnh viễn", giống như `Math.PI` tích hợp sẵn:

```
let user = {
  name: "John"
};

Object.defineProperty(user, "name", {
  writable: false,
  configurable: false
});

// won't be able to change user.name or its flags
// all this won't work:
user.name = "Pete";
delete user.name;
Object.defineProperty(user, "name", { value: "Pete" });
```

Chỉ có một thay đổi thuộc tính duy nhất có thể xảy ra: writable true → false

Có một ngoại lệ nhỏ về việc thay đổi các cờ.

Chúng ta có thể thay đổi `writable: true` thành `false` cho một thuộc tính không thể cấu hình, do đó ngăn chặn việc sửa đổi giá trị của nó (để thêm một lớp bảo vệ khác). Không phải theo chiều ngược lại.

## [Object.defineProperties](#object-defineproperties)

Có một phương thức [Object.defineProperties(obj, descriptors)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperties) cho phép xác định nhiều thuộc tính cùng một lúc.

Cú pháp là:

```
Object.defineProperties(obj, {
  prop1: descriptor1,
  prop2: descriptor2
  // ...
});
```

Ví dụ:

```
Object.defineProperties(user, {
  name: { value: "John", writable: false },
  surname: { value: "Smith", writable: false },
  // ...
});
```

Vì vậy, chúng ta có thể đặt nhiều thuộc tính cùng một lúc.

## [Object.getOwnPropertyDescriptors](#object-getownpropertydescriptors)

Để lấy tất cả các mô tả thuộc tính cùng một lúc, chúng ta có thể sử dụng phương thức [Object.getOwnPropertyDescriptors(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyDescriptors).

Kết hợp với `Object.defineProperties`, nó có thể được sử dụng như một cách "hiểu biết về cờ" để sao chép một đối tượng:

```
let clone = Object.defineProperties({}, Object.getOwnPropertyDescriptors(obj));
```

Thông thường khi chúng ta sao chép một đối tượng, chúng ta sử dụng phép gán để sao chép các thuộc tính, như thế này:

```
for (let key in user) {
  clone[key] = user[key]
}
```

…Nhưng điều đó không sao chép các cờ. Vì vậy nếu chúng ta muốn một bản sao "tốt hơn" thì `Object.defineProperties` được ưu tiên.

Một sự khác biệt khác là `for..in` bỏ qua các thuộc tính symbolic và không liệt kê được, nhưng `Object.getOwnPropertyDescriptors` trả về *tất cả* các mô tả thuộc tính bao gồm cả symbolic và không liệt kê được.

## [Niêm phong một đối tượng trên toàn cầu](#sealing-an-object-globally)

Các mô tả thuộc tính hoạt động ở cấp độ các thuộc tính riêng lẻ.

Cũng có các phương thức hạn chế truy cập vào *toàn bộ* đối tượng:

[Object.preventExtensions(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/preventExtensions)
:   Cấm thêm các thuộc tính mới vào đối tượng.

[Object.seal(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal)
:   Cấm thêm/xóa các thuộc tính. Đặt `configurable: false` cho tất cả các thuộc tính hiện có.

[Object.freeze(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze)
:   Cấm thêm/xóa/thay đổi các thuộc tính. Đặt `configurable: false, writable: false` cho tất cả các thuộc tính hiện có.

Và cũng có các phương thức kiểm tra cho chúng:

[Object.isExtensible(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isExtensible)
:   Trả về `false` nếu cấm thêm thuộc tính, nếu không thì `true`.

[Object.isSealed(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isSealed)
:   Trả về `true` nếu cấm thêm/xóa thuộc tính, và tất cả các thuộc tính hiện có đều có `configurable: false`.

[Object.isFrozen(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isFrozen)
:   Trả về `true` nếu cấm thêm/xóa/thay đổi thuộc tính, và tất cả các thuộc tính hiện tại đều là `configurable: false, writable: false`.

Các phương thức này hiếm khi được sử dụng trong thực tế.
