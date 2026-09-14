# Object.keys, values, entries

> Nguồn: [https://javascript.info/keys-values-entries](https://javascript.info/keys-values-entries)

<!-- fetched: 2026-09-14 -->

Hãy step away khỏi individual data structures và talk về iterations qua chúng.

Trong previous chapter chúng ta đã thấy methods `map.keys()`, `map.values()`, `map.entries()`.

These methods là generic, có một common agreement để sử dụng chúng cho data structures. Nếu chúng ta ever create một data structure của riêng, chúng ta nên implement chúng cũng.

Chúng được support cho:

- `Map`
- `Set`
- `Array`

Plain objects cũng support similar methods, nhưng syntax là một little different.

## [Object.keys, values, entries](#object-keys-values-entries)

Cho plain objects, following methods là available:

- [Object.keys(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys) – trả về một array của keys.
- [Object.values(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/values) – trả về một array của values.
- [Object.entries(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries) – trả về một array của `[key, value]` pairs.

Xin lưu ý distinctions (so với map ví例):

|  | Map | Object |
| --- | --- | --- |
| Call syntax | `map.keys()` | `Object.keys(obj)`, nhưng không phải `obj.keys()` |
| Returns | iterable | "real" Array |

Difference đầu tiên là chúng ta phải gọi `Object.keys(obj)`, và không phải `obj.keys()`.

Tại sao vậy? Main reason là flexibility. Remember, objects là base của tất cả complex structures trong JavaScript. Vì vậy chúng ta có thể có một object của riêng như `data` mà implement `data.values()` method của nó. Và chúng ta vẫn có thể gọi `Object.values(data)` trên nó.

Difference thứ hai là `Object.*` methods trả về "real" array objects, không chỉ là iterable. Đó là chủ yếu vì historical reasons.

Ví例:

```
let user = {
  name: "John",
  age: 30
};
```

- `Object.keys(user) = ["name", "age"]`
- `Object.values(user) = ["John", 30]`
- `Object.entries(user) = [ ["name","John"], ["age",30] ]`

Đây là một ví例 của sử dụng `Object.values` để loop qua property values:

```
let user = {
  name: "John",
  age: 30
};

// loop qua values
for (let value of Object.values(user)) {
  alert(value); // John, sau đó 30
}
```

Object.keys/values/entries ignore symbolic properties

Giống như một `for..in` loop, các methods này ignore properties mà sử dụng `Symbol(...)` như keys.

Thông thường điều đó là convenient. Nhưng nếu chúng ta muốn symbolic keys too, sau đó có một separate method [Object.getOwnPropertySymbols](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertySymbols) mà trả về một array của chỉ symbolic keys. Cũng, có tồn tại một method [Reflect.ownKeys(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect/ownKeys) mà trả về *tất cả* keys.

## [Transforming objects](#transforming-objects)

Objects thiếu nhiều methods tồn tại cho arrays, ví例 `map`, `filter` và others.

Nếu chúng ta muốn áp dụng chúng, sau đó chúng ta có thể sử dụng `Object.entries` followed bởi `Object.fromEntries`:

1. Sử dụng `Object.entries(obj)` để get một array của key/value pairs từ `obj`.
2. Sử dụng array methods trên array đó, ví例 `map`, để transform这些 key/value pairs.
3. Sử dụng `Object.fromEntries(array)` trên resulting array để turn nó trở lại thành một object.

Ví例, chúng ta có một object với prices, và muốn double chúng:

```
let prices = {
  banana: 1,
  orange: 2,
  meat: 4,
};

let doublePrices = Object.fromEntries(
  // convert prices vào array, map mỗi key/value pair vào một pair khác
  // và sau đó fromEntries trả lại object
  Object.entries(prices).map(entry => [entry[0], entry[1] * 2])
);

alert(doublePrices.meat); // 8
```

Nó có thể看起来 difficult tại first sight, nhưng become easy để understand sau khi bạn sử dụng nó một hoặc hai lần. Chúng ta có thể make powerful chains của transforms theo cách này.

---

---

## Các bài tập

## [Các bài tập](#tasks)

### [Sum các properties](#sum-the-properties)

mức độ quan trọng: 5

Có một `salaries` object với arbitrary number của salaries.

Viết function `sumSalaries(salaries)` mà trả về sum của tất cả salaries sử dụng `Object.values` và `for..of` loop.

Nếu `salaries` là empty, sau đó result phải là `0`.

Ví例:

```
let salaries = {
  "John": 100,
  "Pete": 300,
  "Mary": 250
};

alert( sumSalaries(salaries) ); // 650
```

[Mở một sandbox với tests.](https://plnkr.co/edit/YT05sfV84H1lLHZf?p=preview)

lời giải

```
function sumSalaries(salaries) {

  let sum = 0;
  for (let salary of Object.values(salaries)) {
    sum += salary;
  }

  return sum; // 650
}

let salaries = {
  "John": 100,
  "Pete": 300,
  "Mary": 250
};

alert( sumSalaries(salaries) ); // 650
```

Hoặc, optionally, chúng ta cũng có thể get sum sử dụng `Object.values` và `reduce`:

```
// reduce loops qua array của salaries,
// adding chúng lên
// và trả về result
function sumSalaries(salaries) {
  return Object.values(salaries).reduce((a, b) => a + b, 0) // 650
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/qvyhOEKg1dyTp2dr?p=preview)

### [Count properties](#count-properties)

mức độ quan trọng: 5

Viết function `count(obj)` mà trả về number của properties trong object:

```
let user = {
  name: 'John',
  age: 30
};

alert( count(user) ); // 2
```

Try để make code ngắn nhất có thể.

P.S. Ignore symbolic properties, count only "regular" ones.

[Mở một sandbox với tests.](https://plnkr.co/edit/reOlvzOjTwVVSGb3?p=preview)

lời giải

```
function count(obj) {
  return Object.keys(obj).length;
}
```

[Mở solution với tests trong một sandbox.](https://plnkr.co/edit/YdiSIOFhTSRCBx5N?p=preview)
