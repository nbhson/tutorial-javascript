# Chuyển đổi object sang primitive

> Nguồn: [https://javascript.info/object-toprimitive](https://javascript.info/object-toprimitive)

<!-- fetched: 2026-09-14 -->

Những gì xảy ra khi các objects được thêm `obj1 + obj2`, subtracted `obj1 - obj2` hoặc printed bằng cách sử dụng `alert(obj)`?

JavaScript không cho phép bạn customize cách các operators hoạt động trên objects. Khác với một số programming languages khác, như Ruby hoặc C++, chúng ta không thể implement một special object method để xử lý addition (hoặc các operators khác).

Trong trường hợp của các operations như vậy, objects được auto-converted sang primitives, và sau đó operation được carried out over these primitives và kết quả là một primitive value.

Đó là một important limitation: result của `obj1 + obj2` (hoặc một math operation khác) không thể là một object khác!

Ví dụ, chúng ta không thể làm cho các objects đại diện cho vectors hoặc matrices (hoặc achievements hoặc whatever), thêm chúng và expect một "summed" object như là result. Such architectural feats là automatically "off the board".

Vì vậy, vì chúng ta không thể technically làm nhiều ở đây, không có maths với objects trong thực tế projects. Khi nó xảy ra, với rare exceptions, nó là vì một coding mistake.

Trong chương này chúng ta sẽ cover làm thế nào một object chuyển đổi sang primitive và làm thế nào để customize nó.

Chúng ta có hai purposes:

1. Nó sẽ cho phép chúng ta understand những gì đang xảy ra trong trường hợp của coding mistakes, khi một operation như vậy happened accidentally.
2. Có những exceptions, nơi các operations như vậy là possible và look good. Ví dụ, subtracting hoặc comparing dates (`Date` objects). Chúng ta sẽ gặp chúng sau.

## [Conversion rules](#conversion-rules)

Trong chương [Type Conversions](/type-conversions) chúng ta đã thấy các rules cho numeric, string và boolean conversions của primitives. Nhưng chúng ta đã leave a gap cho objects. Giờ, khi chúng ta biết về methods và symbols, nó become possible để fill it.

1. Không có conversion sang boolean. Tất cả các objects là `true` trong một boolean context, đơn giản như vậy. Chỉ tồn tại numeric và string conversions.
2. Numeric conversion happens khi chúng ta subtract các objects hoặc apply mathematical functions. Ví dụ, các `Date` objects (sẽ được cover trong chương [Date and time](/date)) có thể được subtracted, và result của `date1 - date2` là time difference giữa hai dates.
3. Như đối với string conversion – nó thường happens khi chúng ta output một object với `alert(obj)` và trong các contexts tương tự.

Chúng ta có thể implement string và numeric conversion của riêng chúng ta, bằng cách sử dụng các special object methods.

Giờ hãy đi vào technical details, vì đó là cách duy nhất để cover topic in-depth.

## [Hints](#hints)

Làm thế nào JavaScript decide nên áp dụng conversion nào?

Có ba variants của type conversion, happens trong các situations khác nhau. Chúng được gọi là "hints", như được described trong [specification](https://tc39.github.io/ecma262/#sec-toprimitive):

`"string"`
:   Đối với một object-to-string conversion, khi chúng ta đang làm một operation trên một object mà expects một string, như `alert`:

    ```
    // output
    alert(obj);

    // using object như là một property key
    anotherObj[obj] = 123;
    ```

`"number"`
:   Đối với một object-to-number conversion, như khi chúng ta đang làm maths:

    ```
    // explicit conversion
    let num = Number(obj);

    // maths (ngoại trừ binary plus)
    let n = +obj; // unary plus
    let delta = date1 - date2;

    // less/greater comparison
    let greater = user1 > user2;
    ```

    Most built-in mathematical functions cũng include such conversion.

`"default"`
:   Xảy ra trong rare cases khi operator là "không chắc" nên expect type nào.

    Ví dụ, binary plus `+` có thể hoạt động cả với strings (concatenates them) và numbers (adds them). Vì vậy nếu một binary plusget một object như là một argument, nó sử dụng `"default"` hint để convert nó.

    Cũng, nếu một object được compared sử dụng `==` với một string, number hoặc một symbol, nó cũng unclear nên conversion nào được làm, vì vậy `"default"` hint được sử dụng.

    ```
    // binary plus sử dụng "default" hint
    let total = obj1 + obj2;

    // obj == number sử dụng "default" hint
    if (user == 1) { ... };
    ```

    Các greater và less comparison operators, như `<` `>`, có thể hoạt động với cả strings và numbers too. Vẫn, chúng sử dụng `"number"` hint, không phải `"default"`. Đó là vì historical reasons.

Trong thực tế though, things là một chút simpler.

Tất cả các built-in objects trừ một case (`Date` object, chúng ta sẽ learn nó sau) implement `"default"` conversion same way như `"number"`. Và chúng ta probably nên làm same.

Vẫn, nó quan trọng để know about tất cả 3 hints, soon we'll see why.

**Để làm conversion, JavaScript tries để find và call ba object methods:**

1. Call `obj[Symbol.toPrimitive](hint)` – method với symbolic key `Symbol.toPrimitive` (system symbol), nếu method như vậy tồn tại,
2. Nếu không nếu hint là `"string"`
   - try calling `obj.toString()` hoặc `obj.valueOf()`, whatever exists.
3. Nếu không nếu hint là `"number"` hoặc `"default"`
   - try calling `obj.valueOf()` hoặc `obj.toString()`, whatever exists.

## [Symbol.toPrimitive](#symbol-toprimitive)

Hãy bắt đầu từ method đầu tiên. Có một built-in symbol tên là `Symbol.toPrimitive` mà nên được sử dụng để named conversion method, như thế này:

```
obj[Symbol.toPrimitive] = function(hint) {
  // here goes code to convert this object to a primitive
  // nó phải return một primitive value
  // hint = một trong "string", "number", "default"
};
```

Nếu method `Symbol.toPrimitive` tồn tại, nó được sử dụng cho tất cả các hints, và không cần thêm methods nào.

Ví dụ, ở đây `user` object implement nó:

```
let user = {
  name: "John",
  money: 1000,

  [Symbol.toPrimitive](hint) {
    alert(`hint: ${hint}`);
    return hint == "string" ? `{name: "${this.name}"}` : this.money;
  }
};

// conversions demo:
alert(user); // hint: string -> {name: "John"}
alert(+user); // hint: number -> 1000
alert(user + 500); // hint: default -> 1500
```

Như chúng ta có thể thấy từ code, `user` becomes một self-descriptive string hoặc một money amount, tùy thuộc vào conversion. Single method `user[Symbol.toPrimitive]` xử lý tất cả các conversion cases.

## [toString/valueOf](#tostring-valueof)

Nếu không có `Symbol.toPrimitive` sau đó JavaScript tries để tìm các methods `toString` và `valueOf`:

- Đối với hint `"string"`: call `toString` method, và nếu nó không tồn tại hoặc nếu nó return một object thay vì một primitive value, sau đó call `valueOf` (vì vậy `toString` có priority cho string conversions).
- Đối với các hints khác: call `valueOf`, và nếu nó không tồn tại hoặc nếu nó return một object thay vì một primitive value, sau đó call `toString` (vì vậy `valueOf` có priority cho maths).

Methods `toString` và `valueOf` đến từ ancient times. Chúng không phải là symbols (symbols không tồn tại lâu như vậy), mà là các "regular" string-named methods. Chúng cung cấp một alternative "old-style" way để implement conversion.

Các methods này phải return một primitive value. Nếu `toString` hoặc `valueOf` return một object, sau đó nó bị ignored (same như nếu không có method).

Theo mặc định, một plain object có following `toString` và `valueOf` methods:

- `toString` method return một string `"[object Object]"`.
- `valueOf` method return objectbản thân.

Ở đây là demo:

```
let user = {name: "John"};

alert(user); // [object Object]
alert(user.valueOf() === user); // true
```

Vì vậy nếu chúng ta cố gắng sử dụng một object như là một string, như trong một `alert` hoặc vậy, sau đó theo mặc định chúng ta thấy `[object Object]`.

Default `valueOf` được mentioned ở đây chỉ để completeness, để tránh any confusion. Như bạn có thể thấy, nó return objectbản thân, và vì vậy bị ignored. Đừng hỏi tôi tại sao, đó là vì historical reasons. Vì vậy chúng ta có thể assume nó không tồn tại.

Hãy implement các methods này để customize conversion.

Ví dụ, ở đây `user` làm cùng như ở trên bằng cách sử dụng một combination của `toString` và `valueOf` thay vì `Symbol.toPrimitive`:

```
let user = {
  name: "John",
  money: 1000,

  // cho hint="string"
  toString() {
    return `{name: "${this.name}"}`;
  },

  // cho hint="number" hoặc "default"
  valueOf() {
    return this.money;
  }

};

alert(user); // toString -> {name: "John"}
alert(+user); // valueOf -> 1000
alert(user + 500); // valueOf -> 1500
```

Như chúng ta có thể thấy, behavior là giống hệt nhưví dụví dụ trước với `Symbol.toPrimitive`.

Thường chúng ta muốn một single "catch-all" place để xử lý tất cả các primitive conversions. Trong trường hợp này, chúng ta có thể implement `toString` only, như thế này:

```
let user = {
  name: "John",

  toString() {
    return this.name;
  }
};

alert(user); // toString -> John
alert(user + 500); // toString -> John500
```

Trong absence của `Symbol.toPrimitive` và `valueOf`, `toString` sẽ xử lý tất cả các primitive conversions.

### [Một conversion có thể return bất kỳ primitive type nào](#a-conversion-can-return-any-primitive-type)

Thing quan trọng cần biết về tất cả các primitive-conversion methods là chúng không necessarily return "hinted" primitive.

Không có control whether `toString` return exactly một string, hoặc whether `Symbol.toPrimitive` method return một number cho hint `"number"`.

Chỉ mandatory thing: các methods này phải return một primitive, không phải một object.

Historical notes

Vì historical reasons, nếu `toString` hoặc `valueOf` return một object, không có error, nhưng such value bị ignored (như nếu method không tồn tại). Đó là vì trong ancient times không có good "error" concept trong JavaScript.

Ngược lại, `Symbol.toPrimitive` là stricter, nó *phải* return một primitive, nếu không sẽ có error.

## [Further conversions](#further-conversions)

Như chúng ta đã biết, nhiều operators và functions perform type conversions,ví dụví dụ multiplication `*` converts operands sang numbers.

Nếu chúng ta pass một object như là một argument, sau đó có hai stages của calculations:

1. Object được convert sang một primitive (sử dụng các rules described ở trên).
2. Nếu necessary cho further calculations, resulting primitive cũng được convert.

Ví dụ:

```
let obj = {
  // toString xử lý tất cả conversions trong absence của các methods khác
  toString() {
    return "2";
  }
};

alert(obj * 2); // 4, object convert sang primitive "2", sau đó multiplication làm nó thành một number
```

1. Multiplication `obj * 2` trước tiên convert object sang primitive (đó là một string `"2"`).
2. Sau đó `"2" * 2` trở thành `2 * 2` (string được convert sang number).

Binary plus sẽ concatenates strings trong cùng situation, vì nó gladly accepts một string:

```
let obj = {
  toString() {
    return "2";
  }
};

alert(obj + 2); // "22" ("2" + 2), conversion sang primitive đã return một string => concatenation
```

## [Tổng kết](#summary)

Object-to-primitive conversion được gọi tự động bởi nhiều built-in functions và operators mà expect một primitive như là một value.

Có 3 types (hints) của nó:

- `"string"` (cho `alert` và các operations khác mà cần một string)
- `"number"` (cho maths)
- `"default"` (few operators, thông thường các objects implement nó same way như `"number"`)

Specification mô tả explicitly toán tử nào sử dụng hint nào.

Conversion algorithm là:

1. Call `obj[Symbol.toPrimitive](hint)` nếu method tồn tại,
2. Nếu không nếu hint là `"string"`
   - try calling `obj.toString()` hoặc `obj.valueOf()`, whatever exists.
3. Nếu không nếu hint là `"number"` hoặc `"default"`
   - try calling `obj.valueOf()` hoặc `obj.toString()`, whatever exists.

Tất cả các methods này phải return một primitive để work (nếu defined).

Trong thực tế, thông thường đủ để implement chỉ `obj.toString()` như là một "catch-all" method cho string conversions mà nên return một "human-readable" representation của một object, cho logging hoặc debugging purposes.
