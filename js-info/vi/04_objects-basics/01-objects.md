# Đối tượng (Objects)

> Source: [https://javascript.info/object](https://javascript.info/object)

<!-- fetched: 2026-09-14 -->

Như chúng ta đã biết từ chương [Data types](/types), có tám data types trong JavaScript. Bảy trong số đó được gọi là "primitive", vì giá trị của chúng chỉ chứa một thứ (dù là string hay number hay bất kỳ thứ gì).

Ngược lại, objects được sử dụng để lưu trữ các bộ sưu tập có key của various data và các entity phức tạp hơn. Trong JavaScript, objects thâm nhập hầu hết mọi khía cạnh của ngôn ngữ. Vì vậy chúng ta phải hiểu chúng trước khi đi sâu vào bất kỳ đâu khác.

Một object có thể được tạo với dấu ngoặc nhọn `{…}` với một danh sách *properties* tùy chọn. Một property là cặp "key: value", trong đó `key` là một string (cũng được gọi là "tên property"), và `value` có thể là bất kỳ thứ gì.

Chúng ta có thể hình dung một object như một tủ có các tập tin được gắn nhãn. Mọi piece data được lưu trữ trong tập tin của nó theo key. Dễ dàng tìm thấy tập tin theo tên hoặc thêm/xóa tập tin.

![](/article/object/object.svg)

Một object trống ("empty cabinet") có thể được tạo bằng một trong hai cú pháp:

```
let user = new Object(); // cú pháp "object constructor"
let user = {};  // cú pháp "object literal"
```

![](/article/object/object-user-empty.svg)

Thường thì dấu ngoặc nhọn `{...}` được sử dụng. Khai báo đó được gọi là *object literal*.

## [Literals và properties](#literals-and-properties)

Chúng ta có thể ngay lập tức đặt một số properties vào `{...}` như các cặp "key: value":

```
let user = {     // một object
  name: "John",  // theo key "name" lưu giá trị "John"
  age: 30        // theo key "age" lưu giá trị 30
};
```

Một property có một key (còn được gọi là "tên" hoặc "identifier") trước dấu hai chấm `":"` và một value ở bên phải nó.

Trong object `user`, có hai properties:

1. Property đầu tiên có tên là `"name"` và value là `"John"`.
2. Property thứ hai có tên là `"age"` và value là `30`.

Object `user` resulting có thể được hình dung như một tủ với hai tập tin được gắn nhãn "name" và "age".

![](/article/object/object-user.svg)

Chúng ta có thể thêm, xóa và đọc các tập tin từ nó bất cứ lúc nào.

Giá trị của property có thể truy cập được bằng dot notation:

```
// lấy giá trị property của object:
alert( user.name ); // John
alert( user.age ); // 30
```

Giá trị có thể là bất kỳ loại nào. Hãy thêm một boolean:

```
user.isAdmin = true;
```

![](/article/object/object-user-isadmin.svg)

Để xóa một property, chúng ta có thể sử dụng toán tử `delete`:

```
delete user.age;
```

![](/article/object/object-user-delete.svg)

Chúng ta cũng có thể sử dụng các property names nhiều từ, nhưng sau đó chúng phải được quoted:

```
let user = {
  name: "John",
  age: 30,
  "likes birds": true  // tên property nhiều từ phải được quoted
};
```

![](/article/object/object-user-props.svg)

Property cuối cùng trong danh sách có thể kết thúc bằng dấu phẩy:

```
let user = {
  name: "John",
  age: 30,
}
```

Điều đó được gọi là "trailing" hoặc "hanging" comma. Làm cho việc thêm/xóa/chuyển properties dễ dàng hơn, vì tất cả các dòng trở nên giống nhau.

## [Square brackets](#square-brackets)

Đối với các property nhiều từ, dot access không hoạt động:

```
// điều này sẽ cho syntax error
user.likes birds = true
```

JavaScript không hiểu điều đó. Nó nghĩ rằng chúng ta đang address `user.likes`, và sau đógiữ syntax error khi gặp `birds` không mong đợi.

Dot yêu cầu key phải là một valid variable identifier. Điều đó ngụ ý: không chứa khoảng trắng, không bắt đầu bằng số và không bao gồm các ký tự đặc biệt (`$` và `_` được phép).

Có một alternative "square bracket notation" hoạt động với bất kỳ string nào:

```
let user = {};

// set
user["likes birds"] = true;

// get
alert(user["likes birds"]); // true

// delete
delete user["likes birds"];
```

Giờ mọi thứ đều ổn. Xin lưu ý rằng string bên trong brackets được quoted đúng cách (bất kỳ loại quotes nào cũng được).

Square brackets cũng cung cấp một cách để obtain tên property như kết quả của bất kỳ expression nào – khác với một literal string – như từ một variable như sau:

```
let key = "likes birds";

// same as user["likes birds"] = true;
user[key] = true;
```

Ở đây, biến `key` có thể được tính toán tại run-time hoặc phụ thuộc vào input của người dùng. Và sau đó chúng ta sử dụng nó để truy cập property. Điều đó cho chúng ta một mức độ linh hoạt rất lớn.

Ví dụ:

```
let user = {
  name: "John",
  age: 30
};

let key = prompt("What do you want to know about the user?", "name");

// access by variable
alert( user[key] ); // John (nếu nhập "name")
```

Dot notation không thể được sử dụng theo cách tương tự:

```
let user = {
  name: "John",
  age: 30
};

let key = "name";
alert( user.key ) // undefined
```

### [Computed properties](#computed-properties)

Chúng ta có thể sử dụng square brackets trong một object literal, khi tạo một object. Điều đó được gọi là *computed properties*.

Ví dụ:

```
let fruit = prompt("Which fruit to buy?", "apple");

let bag = {
  [fruit]: 5, // tên của property được lấy từ biến fruit
};

alert( bag.apple ); // 5 nếu fruit="apple"
```

Ý nghĩa của một computed property rất đơn giản: `[fruit]` có nghĩa là tên property nên được lấy từ `fruit`.

Vì vậy, nếu một visitor nhập `"apple"`, `bag` sẽ trở thành `{apple: 5}`.

Về cơ bản, điều đó hoạt động tương tự như:

```
let fruit = prompt("Which fruit to buy?", "apple");
let bag = {};

// take property name from the fruit variable
bag[fruit] = 5;
```

…Nhưng trông đẹp hơn.

Chúng ta có thể sử dụng các expressions phức tạp hơn bên trong square brackets:

```
let fruit = 'apple';
let bag = {
  [fruit + 'Computers']: 5 // bag.appleComputers = 5
};
```

Square brackets mạnh mẽ hơn nhiều so với dot notation. Chúng cho phép bất kỳ property names nào và variables. Nhưng chúng cũng cồng kềnh hơn để viết.

Vì vậy, phần lớn thời gian, khi property names đã biết và đơn giản, dot được sử dụng. Và nếu chúng ta cần thứ gì đó phức tạp hơn, thì chúng ta chuyển sang square brackets.

## [Property value shorthand](#property-value-shorthand)

Trong code thực tế, chúng ta thường sử dụng các biến hiện có như values cho property names.

Ví dụ:

```
function makeUser(name, age) {
  return {
    name: name,
    age: age,
    // ...other properties
  };
}

let user = makeUser("John", 30);
alert(user.name); // John
```

Trongví dụ dụ trên, các properties có cùng tên với các biến. Trường hợp sử dụng tạo một property từ một variable rất phổ biến, vì vậy có một *property value shorthand* đặc biệt để làm cho nó ngắn hơn.

Thay vì `name:name` chúng ta có thể chỉ viết `name`, như thế này:

```
function makeUser(name, age) {
  return {
    name, // same as name: name
    age,  // same as age: age
    // ...
  };
}
```

Chúng ta có thể sử dụng cả normal properties và shorthands trong cùng một object:

```
let user = {
  name,  // same as name:name
  age: 30
};
```

## [Property names limitations](#property-names-limitations)

Như chúng ta đã biết, một variable không thể có tên bằng một trong các language-reserved words như "for", "let", "return" v.v.

Nhưng đối với một object property, không có restriction như vậy:

```
// these properties are all right
let obj = {
  for: 1,
  let: 2,
  return: 3
};

alert( obj.for + obj.let + obj.return );  // 6
```

Nói ngắn gọn, không có limitations trên property names. Chúng có thể là bất kỳ strings hoặc symbols nào (một type đặc biệt cho identifiers, sẽ được cover sau).

Các types khác được autoconvert thành string.

Ví dụ, một number `0` trở thành một string `"0"` khi được sử dụng làm property key:

```
let obj = {
  0: "test" // same as "0": "test"
};

// cả hai alerts đều access cùng một property (số 0 được convert thành string "0")
alert( obj["0"] ); // test
alert( obj[0] ); // test (cùng property)
```

Có một gotcha nhỏ với một property đặc biệt được gọi là `__proto__`. Chúng ta không thể set nó thành một non-object value:

```
let obj = {};
obj.__proto__ = 5; // assign a number
alert(obj.__proto__); // [object Object] - value là một object, không hoạt động như mong đợi
```

Như chúng ta thấy từ code, việc assign cho một primitive `5` bị bỏ qua.

Chúng ta sẽ cover bản chất đặc biệt của `__proto__` trong [các chương sau](/prototype-inheritance), và đề xuất các [cách để fix](/prototype-methods) behavior như vậy.

## [Property existence test, "in" operator](#property-existence-test-in-operator)

Một feature đáng chú ý của objects trong JavaScript, so với nhiều ngôn ngữ khác, là có thể truy cập bất kỳ property nào. Sẽ không có lỗi nếu property không tồn tại!

Reading một non-existing property chỉ trả về `undefined`. Vì vậy chúng ta có thể dễ dàng kiểm tra xem property có tồn tại không:

```
let user = {};

alert( user.noSuchProperty === undefined ); // true means "no such property"
```

Cũng có một operator đặc biệt `"in"` cho việc đó.

Cú pháp là:

```
"key" in object
```

Ví dụ:

```
let user = { name: "John", age: 30 };

alert( "age" in user ); // true, user.age tồn tại
alert( "blabla" in user ); // false, user.blabla không tồn tại
```

Xin lưu ý rằng bên trái của `in` phải là *tên property*. Điều đó thường là một string được quoted.

Nếu chúng ta bỏ qua quotes, điều đó có nghĩa là một variable nên chứa tên thực tế để được kiểm tra. Ví dụ:

```
let user = { age: 30 };

let key = "age";
alert( key in user ); // true, property "age" tồn tại
```

Tại sao operator `in` tồn tại? Không đủ để compare với `undefined` sao?

Chà, phần lớn thời gian, comparison với `undefined` hoạt động tốt. Nhưng có một trường hợp đặc biệt khi nó fail, nhưng `"in"` hoạt động chính xác.

Đó là khi một object property tồn tại, nhưng lưu trữ `undefined`:

```
let obj = {
  test: undefined
};

alert( obj.test ); // nó là undefined, vậy - không có property như vậy?

alert( "test" in obj ); // true, property tồn tại!
```

Trong code ở trên, property `obj.test` về mặt kỹ thuật tồn tại. Vì vậy operator `in` hoạt động đúng.

Các tình huống như vậy xảy ra rất hiếm, vì `undefined` không nên được assign một cách explicit. Chúng ta chủ yếu sử dụng `null` cho các giá trị "unknown" hoặc "empty". Vì vậy operator `in` là một khách lạ hiếm trong code.

## [Vòng lặp "for..in"](#forin)

Để duyệt qua tất cả các keys của một object, có một dạng đặc biệt của vòng lặp: `for..in`. Đây là một thứ hoàn toàn khác từ construct `for(;;)` mà chúng ta đã học trước đó.

Cú pháp:

```
for (key in object) {
  // executes the body for each key among object properties
}
```

Ví dụ, hãy output tất cả các properties của `user`:

```
let user = {
  name: "John",
  age: 30,
  isAdmin: true
};

for (let key in user) {
  // keys
  alert( key );  // name, age, isAdmin
  // values cho các keys
  alert( user[key] ); // John, 30, true
}
```

Lưu ý rằng tất cả các construct "for" cho phép chúng ta khai báo looping variable bên trong loop, như `let key` ở đây.

Ngoài ra, chúng ta có thể sử dụng một tên biến khác ở đây thay vì `key`. Ví dụ, `"for (let prop in obj)"` cũng được sử dụng rộng rãi.

### [Ordered như một object](#ordered-like-an-object)

Các objects có ordered không? Nói cách khác, nếu chúng ta loop qua một object, chúng ta có nhận được tất cả các properties theo cùng thứ tự chúng được thêm không? Chúng ta có thể dựa vào điều này không?

Câu trả lời ngắn gọn là: "ordered theo một cách đặc biệt": các integer properties được sort, các properties khác xuất hiện theo creation order. Chi tiết sẽ theo sau.

Làmví dụ dụ, hãy xem xét một object với các mã điện thoại:

```
let codes = {
  "49": "Germany",
  "41": "Switzerland",
  "44": "Great Britain",
  // ..,
  "1": "USA"
};

for (let code in codes) {
  alert(code); // 1, 41, 44, 49
}
```

Object có thể được sử dụng để đề xuất một danh sách các options cho người dùng. Nếu chúng ta đang tạo một site chủ yếu cho audience Đức thì chúng ta có lẽ muốn `49` là first.

Nhưng nếu chúng ta chạy code, chúng ta thấy một bức tranh hoàn toàn khác:

- USA (1) đi trước
- sau đó Switzerland (41) và vân vân.

Các mã điện thoại đi theo ascending sorted order, vì chúng là integers. Vì vậy chúng ta thấy `1, 41, 44, 49`.

Integer properties? Đó là gì?

Thuật ngữ "integer property" ở đây có nghĩa là một string có thể được convert sang-and-from một integer mà không thay đổi.

Vì vậy, `"49"` là một integer property name, vì khi nó được transform thành một số nguyên và trở lại, nó vẫn giống nhau. Nhưng `"+49"` và `"1.2"` thì không:

```
// Number(...) explicitly converts to a number
// Math.trunc là một built-in function loại bỏ phần thập phân
alert( String(Math.trunc(Number("49"))) ); // "49", same, integer property
alert( String(Math.trunc(Number("+49"))) ); // "49", not same "+49" ⇒ not integer property
alert( String(Math.trunc(Number("1.2"))) ); // "1", not same "1.2" ⇒ not integer property
```

…Mặt khác, nếu các keys là non-integer, thì chúng được liệt kê theo creation order,ví dụ dụ:

```
let user = {
  name: "John",
  surname: "Smith"
};
user.age = 25; // thêm một cái nữa

// non-integer properties được liệt kê theo creation order
for (let prop in user) {
  alert( prop ); // name, surname, age
}
```

Vì vậy, để fix vấn đề với các mã điện thoại, chúng ta có thể "gian lận" bằng cách làm cho các mã trở thành non-integer. Thêm dấu cộng `"+"` trước mỗi mã là đủ.

Như thế này:

```
let codes = {
  "+49": "Germany",
  "+41": "Switzerland",
  "+44": "Great Britain",
  // ..,
  "+1": "USA"
};

for (let code in codes) {
  alert( +code ); // 49, 41, 44, 1
}
```

Giờ nó hoạt động như mong đợi.

## [Tổng kết](#summary)

Objects là các associative arrays với một số feature đặc biệt.

Chúng lưu trữ các properties (key-value pairs), trong đó:

- Property keys phải là strings hoặc symbols (thường là strings).
- Values có thể là bất kỳ loại nào.

Để truy cập một property, chúng ta có thể sử dụng:

- Dot notation: `obj.property`.
- Square brackets notation `obj["property"]`. Square brackets cho phép lấy key từ một variable, như `obj[varWithKey]`.

Các operators bổ sung:

- Để xóa một property: `delete obj.prop`.
- Để kiểm tra xem một property với key cho trước có tồn tại không: `"key" in obj`.
- Để iterate qua một object: vòng lặp `for (let key in obj)`.

Những gì chúng ta đã học trong chương này được gọi là "plain object", hoặc chỉ là `Object`.

Có nhiều kinds khác nhau của objects trong JavaScript:

- `Array` để lưu trữ các bộ sưu tập dữ liệu có thứ tự,
- `Date` để lưu trữ thông tin về date và time,
- `Error` để lưu trữ thông tin về lỗi.
- …Vân vân.

Chúng có các feature đặc biệt mà chúng ta sẽ học sau. Đôi khi người ta nói gì đó như "Array type" hoặc "Date type", nhưng chính thức chúng không phải là các types riêng biệt, mà thuộc về một single "object" data type. Và chúng extend nó theo nhiều cách khác nhau.

Objects trong JavaScript rất powerful. Ở đây chúng ta mới chỉ scratch the surface của một topic really huge. Chúng ta sẽ làm việc chặt chẽ với objects và học thêm về chúng trong các parts sau của tutorial.

---

---

## Tasks

## [Tasks](#tasks)

### [Xin chào, object](#hello-object)

importance: 5

Viết code, một dòng cho mỗi action:

1. Tạo một object trống `user`.
2. Thêm property `name` với value `John`.
3. Thêm property `surname` với value `Smith`.
4. Thay đổi giá trị của `name` thành `Pete`.
5. Xóa property `name` khỏi object.

solution

```
let user = {};
user.name = "John";
user.surname = "Smith";
user.name = "Pete";
delete user.name;
```

### [Check for emptiness](#check-for-emptiness)

importance: 5

Viết hàm `isEmpty(obj)` trả về `true` nếu object không có properties, `false` ngược lại.

Nó nên hoạt động như thế này:

```
let schedule = {};

alert( isEmpty(schedule) ); // true

schedule["8:30"] = "get up";

alert( isEmpty(schedule) ); // false
```

[Mở một sandbox với tests.](https://plnkr.co/edit/pUmzYUWsFLsINnYc?p=preview)

solution

Chỉ cần loop qua object và `return false` ngay lập tức nếu có ít nhất một property.

```
function isEmpty(obj) {
  for (let key in obj) {
    // if the loop has started, there is a property
    return false;
  }
  return true;
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/T2UGamT15SRs5Zsd?p=preview)

### [Sum object properties](#sum-object-properties)

importance: 5

Chúng ta có một object lưu trữ salaries của team:

```
let salaries = {
  John: 100,
  Ann: 160,
  Pete: 130
}
```

Viết code để sum tất cả salaries và lưu trong biến `sum`. Phải là `390` trongví dụ dụ trên.

Nếu `salaries` trống, thì kết quả phải là `0`.

solution

```
let salaries = {
  John: 100,
  Ann: 160,
  Pete: 130
};

let sum = 0;
for (let key in salaries) {
  sum += salaries[key];
}

alert(sum); // 390
```

### [Multiply numeric property values by 2](#multiply-numeric-property-values-by-2)

importance: 3

Tạo một hàm `multiplyNumeric(obj)` nhân tất cả các numeric property values của `obj` với `2`.

Ví dụ:

```
// before the call
let menu = {
  width: 200,
  height: 300,
  title: "My menu"
};

multiplyNumeric(menu);

// after the call
menu = {
  width: 400,
  height: 600,
  title: "My menu"
};
```

Xin lưu ý rằng `multiplyNumeric` không cần trả về gì. Nó nên modify object tại chỗ.

P.S. Sử dụng `typeof` để check cho một number ở đây.

[Mở một sandbox với tests.](https://plnkr.co/edit/Ug2Qh01TgHmOdIOL?p=preview)

solution

```
function multiplyNumeric(obj) {
  for (let key in obj) {
    if (typeof obj[key] == 'number') {
      obj[key] *= 2;
    }
  }
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/ktw3kzoedDNy1Lnq?p=preview)
