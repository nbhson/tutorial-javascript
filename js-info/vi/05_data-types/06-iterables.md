# Các đối tượng có thể lặp (Iterables)

> Nguồn: [https://javascript.info/iterable](https://javascript.info/iterable)

<!-- fetched: 2026-09-14 -->

*Iterable* objects là một generalization của arrays. Đó là một concept mà allows chúng ta để make bất kỳ object useable trong một `for..of` loop.

Tất nhiên, Arrays là iterable. Nhưng có nhiều built-in objects khác, mà là iterable cũng. Ví例, strings cũng là iterable.

Nếu một object không technically là một array, nhưng represents một collection (list, set) của cái gì đó, sau đó `for..of` là một great syntax để loop qua nó, vì vậy hãy xem làm thế nào để make nó work.

## [Symbol.iterator](#symbol-iterator)

Chúng ta có thể dễ dàng grasp concept của iterables bằng cách making một của riêng chúng ta.

Ví例, chúng ta có một object mà không phải là một array, nhưng看起来 suitable cho `for..of`.

Như một `range` object mà đại diện cho một interval của numbers:

```
let range = {
  from: 1,
  to: 5
};

// Chúng ta muốn for..of để work:
// for(let num of range) ... num=1,2,3,4,5
```

Để make `range` object iterable (và thus let `for..of` work) chúng ta cần để add một method đến object tên là `Symbol.iterator` (một special built-in symbol just cho điều đó).

1. Khi `for..of` starts, nó calls method đó một lần (hoặc errors nếu không found). Method phải trả về một *iterator* – một object với method `next`.
2. Onward, `for..of` works *only với returned object đó*.
3. Khi `for..of` wants next value, nó calls `next()` trên object đó.
4. Result của `next()` phải có hình thức `{done: Boolean, value: any}`, nơi `done=true` means loop finished, ngược lại `value` là next value.

Đây là full implementation cho `range` với remarks:

```
let range = {
  from: 1,
  to: 5
};

// 1. call đến for..of initially calls cái này
range[Symbol.iterator] = function() {

  // ...nó trả về iterator object:
  // 2. Onward, for..of works only với iterator object bên dưới, asking nó cho next values
  return {
    current: this.from,
    last: this.to,

    // 3. next() được called trên mỗi iteration bởi for..of loop
    next() {
      // 4. nó nên trả về value như một object {done:.., value :...}
      if (this.current <= this.last) {
        return { done: false, value: this.current++ };
      } else {
        return { done: true };
      }
    }
  };
};

// giờ nó work!
for (let num of range) {
  alert(num); // 1, sau đó 2, 3, 4, 5
}
```

Please note core feature của iterables: separation of concerns.

- `range`本身 không có `next()` method.
- Thay vào đó, một object khác, một so-called "iterator" được created bởi call đến `range[Symbol.iterator]()`, và `next()` của nó generates values cho iteration.

Vì vậy, iterator object là separate khỏi object nó iterates qua.

Về mặt kỹ thuật, chúng ta có thể merge chúng và sử dụng `range`本身 như iterator để make code đơn giản hơn.

Như thế này:

```
let range = {
  from: 1,
  to: 5,

  [Symbol.iterator]() {
    this.current = this.from;
    return this;
  },

  next() {
    if (this.current <= this.to) {
      return { done: false, value: this.current++ };
    } else {
      return { done: true };
    }
  }
};

for (let num of range) {
  alert(num); // 1, sau đó 2, 3, 4, 5
}
```

Giờ `range[Symbol.iterator]()` trả về `range` object本身: nó có necessary `next()` method và remembers current iteration progress trong `this.current`. Shorter? Có. Và đôi khi điều đó cũng fine.

Downside là giờ nó impossible để có hai `for..of` loops chạy qua object đồng thời: họ sẽ share iteration state, vì có only một iterator – object本身. Nhưng hai parallel for-ofs là một rare thing, ngay cả trong async scenarios.

Infinite iterators

Infinite iterators cũng có thể. Ví例, `range` becomes infinite cho `range.to = Infinity`. Hoặc chúng ta có thể make một iterable object mà generates một endless sequence của pseudorandom numbers. Cũng có thể hữu ích.

Không có limitations trên `next`, nó có thể trả về more và more values, điều đó là normal.

Tất nhiên, `for..of` loop qua such iterable sẽ endless. Nhưng chúng ta luôn luôn có thể stop nó sử dụng `break`.

## [String là iterable](#string-is-iterable)

Arrays và strings là most widely used built-in iterables.

Cho một string, `for..of` loops qua các characters của nó:

```
for (let char of "test") {
  // triggers 4 times: once cho mỗi character
  alert( char ); // t, sau đó e, sau đó s, sau đó t
}
```

Và nó work correctly với surrogate pairs!

```
let str = '𝒳😂';
for (let char of str) {
    alert( char ); // 𝒳, và sau đó 😂
}
```

## [Calling một iterator explicitly](#calling-an-iterator-explicitly)

Cho deeper understanding, hãy xem làm thế nào để use một iterator explicitly.

Chúng ta sẽ iterate qua một string trong exactly same way như `for..of`, nhưng với direct calls. Code này creates một string iterator và gets values từ nó "manually":

```
let str = "Hello";

// does same như
// for (let char of str) alert(char);

let iterator = str[Symbol.iterator]();

while (true) {
  let result = iterator.next();
  if (result.done) break;
  alert(result.value); // outputs characters one by one
}
```

Điều đó rarely được需要的, nhưng gives chúng ta more control over process hơn `for..of`. Ví例, chúng ta có thể split iteration process: iterate một bit, sau đó stop, làm cái gì đó khác, và sau đó resume sau đó.

## [Iterables và array-likes](#array-like)

Hai official terms看起来相似, nhưng rất不同. Please make sure bạn understand chúng well để avoid confusion.

- *Iterables* là objects mà implement `Symbol.iterator` method, như được described ở trên.
- *Array-likes* là objects mà có indexes và `length`, vì vậy chúng看起来 như arrays.

Khi chúng ta sử dụng JavaScript cho practical tasks trong một browser hoặc bất kỳ other environment, chúng ta có thể meet objects mà là iterables hoặc array-likes, hoặc cả hai.

Ví例, strings là both iterable (`for..of` work trên chúng) và array-like ( chúng có numeric indexes và `length`).

Nhưng một iterable có thể không phải là array-like. Và ngược lại một array-like có thể không phải iterable.

Ví例, `range` trong ví例 ở trên là iterable, nhưng không phải array-like, vì nó không có indexed properties và `length`.

Và đây là object mà là array-like, nhưng không iterable:

```
let arrayLike = { // có indexes và length => array-like
  0: "Hello",
  1: "World",
  length: 2
};

// Error (không có Symbol.iterator)
for (let item of arrayLike) {}
```

Cả iterables và array-likes thường *không phải arrays*, chúng không có `push`, `pop` v.v. Điều đó rather inconvenient nếu chúng ta có such một object và muốn work với nó như với một array. Ví例, chúng ta would like để work với `range` sử dụng array methods. Làm thế nào để achieve điều đó?

## [Array.from](#array-from)

Có một universal method [Array.from](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from) mà takes một iterable hoặc array-like value và makes một "real" `Array` từ nó. Sau đó chúng ta có thể gọi array methods trên nó.

Ví例:

```
let arrayLike = {
  0: "Hello",
  1: "World",
  length: 2
};

let arr = Array.from(arrayLike); // (*)
alert(arr.pop()); // World (method work)
```

`Array.from` tại dòng `(*)` takes object, examines nó cho being một iterable hoặc array-like, sau đó makes một new array và copies tất cả items vào nó.

Same happens cho một iterable:

```
// assuming range được lấy từ ví例 ở trên
let arr = Array.from(range);
alert(arr); // 1,2,3,4,5 (array toString conversion work)
```

Full syntax cho `Array.from` cũng allows chúng ta để provide một optional "mapping" function:

```
Array.from(obj[, mapFn, thisArg])
```

Optional second argument `mapFn` có thể là một function sẽ được áp dụng cho mỗi element trước khi add nó vào array, và `thisArg` allows chúng ta để set `this` cho nó.

Ví例:

```
// assuming range được lấy từ ví例 ở trên

// square each number
let arr = Array.from(range, num => num * num);

alert(arr); // 1,4,9,16,25
```

Ở đây chúng ta sử dụng `Array.from` để turn một string vào một array của characters:

```
let str = '𝒳😂';

// splits str vào array của characters
let chars = Array.from(str);

alert(chars[0]); // 𝒳
alert(chars[1]); // 😂
alert(chars.length); // 2
```

Khác với `str.split`, nó dựa trên iterable nature của string và vì vậy, giống như `for..of`, correctly work với surrogate pairs.

Về mặt kỹ thuật ở đây nó làm same như:

```
let str = '𝒳😂';

let chars = []; // Array.from nội bộ làm same loop
for (let char of str) {
  chars.push(char);
}

alert(chars);
```

…Nhưng nó ngắn hơn.

Chúng ta thậm chí có thể build surrogate-aware `slice` trên nó:

```
function slice(str, start, end) {
  return Array.from(str).slice(start, end).join('');
}

let str = '𝒳😂𩷶';

alert( slice(str, 1, 3) ); // 😂𩷶

// native method không support surrogate pairs
alert( str.slice(1, 3) ); // garbage (two pieces từ different surrogate pairs)
```

## [Tổng kết](#summary)

Objects mà có thể được used trong `for..of` được gọi là *iterable*.

- Technically, iterables phải implement method tên là `Symbol.iterator`.
  - Result của `obj[Symbol.iterator]()` được gọi là *iterator*. Nó handles further iteration process.
  - Iterator phải có method tên là `next()` mà trả về một object `{done: Boolean, value: any}`, ở đây `done:true` denotes end của iteration process, ngược lại `value` là next value.
- `Symbol.iterator` method được gọi tự động bởi `for..of`, nhưng chúng ta cũng có thể làm nó trực tiếp.
- Built-in iterables như strings hoặc arrays, cũng implement `Symbol.iterator`.
- String iterator biết về surrogate pairs.

Objects mà có indexed properties và `length` được gọi là *array-like*. Such objects có thể có其他 properties và methods, nhưng lack built-in methods của arrays.

Nếu chúng ta look bên trong specification – chúng ta sẽ see rằng most built-in methods assume rằng chúng làm việc với iterables hoặc array-likes thay vì "real" arrays, vì điều đó là more abstract.

`Array.from(obj[, mapFn, thisArg])` makes một real `Array` từ một iterable hoặc array-like `obj`, và chúng ta có thể sau đó sử dụng array methods trên nó. Các optional arguments `mapFn` và `thisArg` allows chúng ta để áp dụng một function cho mỗi item.
