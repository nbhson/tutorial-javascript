# Optional chaining '?.'

> Nguồn: [https://javascript.info/optional-chaining](https://javascript.info/optional-chaining)

<!-- fetched: 2026-09-14 -->

Một tính năng mới gần đây

Đây là một tính năng mới được thêm vào ngôn ngữ.
Các trình duyệt cũ có thể cần [polyfills](https://javascript.info/polyfills).

Optional chaining `?.` là một cách an toàn để access các nested object properties, ngay cả khi một intermediate property không tồn tại.

## [Problem "non-existing property"](#the-non-existing-property-problem)

Nếu bạn mới bắt đầu đọc tutorial và học JavaScript, có lẽ problem chưa chạm đến bạn, nhưng nó khá phổ biến.

Như mộtví dụví dụ, hãy nói chúng ta có các objects `user` lưu trữ thông tin về users của chúng ta.

Hầu hết các users của chúng ta có addresses trong property `user.address`, với street `user.address.street`, nhưng một số không cung cấp chúng.

Trong trường hợp như vậy, khi chúng ta cố gắng get `user.address.street`, và user tình cờ là không có address, chúng ta nhận được error:

```
let user = {}; // a user without "address" property

alert(user.address.street); // Error!
```

Đó là result expected. JavaScript làm việc như thế này. Vì `user.address` là `undefined`, một attempt để get `user.address.street` fail với error.

Trong nhiều practical cases, chúng ta sẽ prefer get `undefined` thay vì error ở đây (có nghĩa là "no street").

…Và mộtví dụví dụ khác. Trong Web development, chúng ta có thể get một object tương ứng với một web page element bằng cách sử dụng một special method call, như `document.querySelector('.elem')`, và nó return `null` khi không có element như vậy.

```
// document.querySelector('.elem') là null nếu không có element
let html = document.querySelector('.elem').innerHTML; // error nếu nó là null
```

Một lần nữa, nếu element không tồn tại, chúng ta sẽ nhận được error accessing `.innerHTML` property của `null`. Và trong một số cases, khi absence của element là bình thường, chúng ta muốn tránh error và chỉ accept `html = null` như là result.

Làm thế nào chúng ta có thể làm điều đó?

Solution obvious sẽ là check giá trị bằng cách sử dụng `if` hoặc conditional operator `?`, trước khi accessing property của nó, như thế này:

```
let user = {};

alert(user.address ? user.address.street : undefined);
```

Nó hoạt động, không có error… Nhưng nó quite inelegant. Như bạn có thể thấy, `"user.address"` xuất hiện hai lần trong code.

Ở đây là những gì giống nhau sẽ trông như thế nào cho `document.querySelector`:

```
let html = document.querySelector('.elem') ? document.querySelector('.elem').innerHTML : null;
```

Chúng ta có thể thấy rằng element search `document.querySelector('.elem')` thực sự được gọi hai lần ở đây. Không tốt.

Đối với các deeply nested properties, nó trở nên even uglier hơn, vì nhiều repetitions được required.

Ví dụ, hãy get `user.address.street.name` theo cách tương tự.

```
let user = {}; // user không có address

alert(user.address ? user.address.street ? user.address.street.name : null : null);
```

Đó là just awful, một người thậm chí có thể có problems hiểu such code.

Có một little better way để viết nó, bằng cách sử dụng toán tử `&&`:

```
let user = {}; // user không có address

alert( user.address && user.address.street && user.address.street.name ); // undefined (không error)
```

AND'ing toàn bộ path đến property đảm bảo rằng tất cả các components tồn tại (nếu không, evaluation stops), nhưng cũng không ideal.

Như bạn có thể thấy, property names vẫn bị duplicated trong code. Ví dụ, trong code ở trên, `user.address` xuất hiện ba lần.

Đó là lý do tại sao optional chaining `?.` được thêm vào ngôn ngữ. Để giải quyết problem này một lần cho tất cả!

## [Optional chaining](#optional-chaining)

Optional chaining `?.` dừng evaluation nếu giá trị trước `?.` là `undefined` hoặc `null` và return `undefined`.

**Sau đó trong bài viết này, để ngắn gọn, chúng ta sẽ nói rằng cái gì đó "tồn tại" nếu nó không phải là `null` và không phải là `undefined`.**

Nói cách khác, `value?.prop`:

- hoạt động như `value.prop`, nếu `value` tồn tại,
- ngược lại (khi `value` là `undefined/null`) nó return `undefined`.

Ở đây là cách an toàn để access `user.address.street` bằng cách sử dụng `?.`:

```
let user = {}; // user không có address

alert( user?.address?.street ); // undefined (không error)
```

Code là short và clean, không có duplication ở tất cả.

Ở đây là mộtví dụví dụ với `document.querySelector`:

```
let html = document.querySelector('.elem')?.innerHTML; // sẽ là undefined, nếu không có element
```

Reading address với `user?.address` hoạt động ngay cả khi `user` object không tồn tại:

```
let user = null;

alert( user?.address ); // undefined
alert( user?.address.street ); // undefined
```

Xin lưu ý: syntax `?.` làm optional giá trị trước nó, nhưng không phải bất kỳ further nào.

Ví dụ, trong `user?.address.street.name` `?.` cho phép `user` được safe là `null/undefined` (và return `undefined` trong trường hợp đó), nhưng đó chỉ là cho `user`. Các properties further được access theo cách regular. Nếu chúng ta muốn một số trong số chúng là optional, sau đó chúng ta sẽ cần thay thế thêm `.` với `?.`.

Không overuse optional chaining

Chúng ta nên sử dụng `?.` chỉ ở nơi mà nó ok nếu có gì đó không tồn tại.

Ví dụ, nếu theo code logic của chúng ta `user` object phải tồn tại, nhưng `address` là optional, sau đó chúng ta nên viết `user.address?.street`, chứ không phải `user?.address?.street`.

Sau đó, nếu `user` tình cờ là undefined, chúng ta sẽ thấy một programming error về nó và fix nó. Ngược lại, nếu chúng ta overuse `?.`, coding errors có thể bị silenced ở nơi không appropriate, và trở nên more difficult để debug.

Variable trước `?.` phải được declare

Nếu không có variable `user` ở tất cả, thì `user?.anything` trigger một error:

```
// ReferenceError: user is not defined
user?.address;
```

Variable phải được declared (víví dụ `let/const/var user` hoặc như là một function parameter). Optional chaining chỉ hoạt động cho các declared variables.

## [Short-circuiting](#short-circuiting)

Như đã nói trước đó, `?.` ngay lập tức dừng ("short-circuits") evaluation nếu phần left không tồn tại.

Vì vậy, nếu có bất kỳ further function calls hoặc operations nào ở right của `?.`, chúng sẽ không được thực hiện.

Ví dụ:

```
let user = null;
let x = 0;

user?.sayHi(x++); // không có "user", vì vậy execution không đạt đến sayHi call và x++

alert(x); // 0, value not incremented
```

## [Các variants khác: ?.(), ?.[]](#other-variants)

Optional chaining `?.` không phải là một operator, nhưng là một special syntax construct, cũng hoạt động với functions và square brackets.

Ví dụ, `?.()` được sử dụng để gọi một function có thể không tồn tại.

Trong code bên dưới, một số users của chúng ta có method `admin`, và một số không:

```
let userAdmin = {
  admin() {
    alert("Tôi là admin");
  }
};

let userGuest = {};

userAdmin.admin?.(); // Tôi là admin

userGuest.admin?.(); // không có gì xảy ra (không có method như vậy)
```

Ở đây, trong cả hai dòng chúng ta trước tiên sử dụng dot (`userAdmin.admin`) để get property `admin`, vì chúng ta giả định rằng `user` object tồn tại, vì vậy nó safe để đọc từ nó.

Sau đó `?.()` checks phần left: nếu function `admin` tồn tại, sau đó nó chạy (đó là trường hợp cho `userAdmin`). Ngược lại (cho `userGuest`) evaluation stops mà không có errors.

Syntax `?.[]` cũng hoạt động, nếu chúng ta muốn sử dụng brackets `[]` để access properties thay vì dot `.`. Tương tự như các cases trước, nó cho phép safe read một property từ một object có thể không tồn tại.

```
let key = "firstName";

let user1 = {
  firstName: "John"
};

let user2 = null;

alert( user1?.[key] ); // John
alert( user2?.[key] ); // undefined
```

Cũng chúng ta có thể sử dụng `?.` với `delete`:

```
delete user?.name; // delete user.name nếu user tồn tại
```

Chúng ta có thể sử dụng `?.` cho safe reading và deleting, nhưng không writing

Optional chaining `?.` không có use ở left side của một assignment.

Ví dụ:

```
let user = null;

user?.name = "John"; // Error, không hoạt động
// vì nó evaluates to: undefined = "John"
```

## [Tổng kết](#summary)

Syntax optional chaining `?.` có ba forms:

1. `obj?.prop` – return `obj.prop` nếu `obj` tồn tại, ngược lại `undefined`.
2. `obj?.[prop]` – return `obj[prop]` nếu `obj` tồn tại, ngược lại `undefined`.
3. `obj.method?.()` – call `obj.method()` nếu `obj.method` tồn tại, ngược lại return `undefined`.

Như chúng ta có thể thấy, tất cả chúng là straightforward và simple để sử dụng. `?.` checks phần left cho `null/undefined` và cho phép evaluation proceed nếu nó không phải vậy.

Một chain của `?.` cho phép safe access các nested properties.

Tuy nhiên, chúng ta nên apply `?.` carefully, chỉ ở nơi mà nó acceptable, theo code logic của chúng ta, rằng phần left không tồn tại. Vì vậy nó sẽ không hide programming errors từ chúng ta, nếu chúng xảy ra.
