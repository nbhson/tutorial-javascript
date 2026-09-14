# Xử lý lỗi, "try...catch"

> Nguồn: [https://javascript.info/try-catch](https://javascript.info/try-catch)

<!-- fetched: 2026-09-14 -->

Không quan trọng chúng ta giỏi lập trình đến đâu, đôi khi scripts của chúng ta vẫn có lỗi. Chúng có thể xảy ra do lỗi của chúng ta, một đầu vào user không mong đợi, một response server sai, và hàng nghìn lý do khác.

Thông thường, một script "chết" (dừng ngay lập tức) khi có lỗi, in nó ra console.

Nhưng có một cấu trúc cú pháp `try...catch` cho phép chúng ta "bắt" lỗi để script có thể, thay vì chết, làm điều gì đó hợp lý hơn.

## [Cú pháp "try…catch"]( #cu-phap-try-catch)

Construct `try...catch` có hai block chính: `try`, và sau đó là `catch`:

```
try {

  // code...

} catch (err) {

  // error handling

}
```

Nó hoạt động như sau:

1. Đầu tiên, code trong `try {...}` được thực thi.
2. Nếu không có lỗi, thì `catch (err)` bị bỏ qua: execution đến cuối `try` và tiếp tục, bỏ qua `catch`.
3. Nếu một lỗi xảy ra, thì `try` execution bị dừng, và control flow đến đầu của `catch (err)`. Biến `err` (chúng ta có thể dùng bất kỳ tên nào) sẽ chứa error object với chi tiết về những gì đã xảy ra.

![](/article/try-catch/try-catch-flow.svg)

Vì vậy, một lỗi bên trong block `try {...}` không giết script – chúng ta có cơ hội xử lý nó trong `catch`.

Hãy xem một số ví dụ.

- Một ví dụ không có lỗi: hiển thị `alert` `(1)` và `(2)`:

  ```
  try {

    alert('Start of try runs');  // (1) <--

    // ...no errors here

    alert('End of try runs');   // (2) <--

  } catch (err) {

    alert('Catch is ignored, because there are no errors'); // (3)

  }
  ```
- Một ví dụ có lỗi: hiển thị `(1)` và `(3)`:

  ```
  try {

    alert('Start of try runs');  // (1) <--

    lalala; // error, variable is not defined!

    alert('End of try (never reached)');  // (2)

  } catch (err) {

    alert(`Error has occurred!`); // (3) <--

  }
  ```

`try...catch` chỉ hoạt động cho runtime errors

Để `try...catch` hoạt động, code phải runnable. Nói cách khác, nó phải là valid JavaScript.

Nó sẽ không hoạt động nếu code sai về mặt cú pháp, ví dụ nó có unmatched curly braces:

```
try {
  {{{{{{{{{{{{
} catch (err) {
  alert("The engine can't understand this code, it's invalid");
}
```

JavaScript engine đầu tiên đọc code, sau đó chạy nó. Các lỗi xảy ra ở phase đọc được gọi là "parse-time" errors và không thể recover (từ bên trong code đó). Đó là vì engine không thể hiểu code.

Vì vậy, `try...catch` chỉ có thể xử lý các lỗi xảy ra trong code hợp lệ. Những lỗi như vậy được gọi là "runtime errors" hoặc, đôi khi, "exceptions".

`try...catch` hoạt động synchronously

Nếu một exception xảy ra trong code "scheduled", như trong `setTimeout`, thì `try...catch` sẽ không bắt được nó:

```
try {
  setTimeout(function() {
    noSuchVariable; // script will die here
  }, 1000);
} catch (err) {
  alert( "won't work" );
}
```

Đó là vì function đó được thực thi sau, khi engine đã rời khỏi construct `try...catch`.

Để bắt một exception bên trong một scheduled function, `try...catch` phải nằm bên trong function đó:

```
setTimeout(function() {
  try {
    noSuchVariable; // try...catch handles the error!
  } catch {
    alert( "error is caught here!" );
  }
}, 1000);
```

## [Error object](#error-object)

Khi một lỗi xảy ra, JavaScript tạo một object chứa chi tiết về nó. Object đó sau đó được truyền như một argument cho `catch`:

```
try {
  // ...
} catch (err) { // <-- "error object", có thể dùng từ khác thay vì err
  // ...
}
```

Đối với tất cả các built-in errors, error object có hai properties chính:

`name`
:   Tên lỗi. Ví dụ, cho một undefined variable đó là `"ReferenceError"`.

`message`
:   Thông điệp dạng text về chi tiết lỗi.

Có các properties non-standard khác có sẵn trong hầu hết các environments. Một trong những properties được sử dụng rộng rãi và được hỗ trợ nhiều nhất là:

`stack`
:   Current call stack: một string với thông tin về chuỗi các nested calls dẫn đến lỗi. Được sử dụng cho mục đích debugging.

Ví dụ:

```
try {
  lalala; // error, variable is not defined!
} catch (err) {
  alert(err.name); // ReferenceError
  alert(err.message); // lalala is not defined
  alert(err.stack); // ReferenceError: lalala is not defined at (...call stack)

  // Can also show an error as a whole
  // Error được convert thành string như "name: message"
  alert(err); // ReferenceError: lalala is not defined
}
```

## [Optional "catch" binding](#optional-catch-binding)

Một bổ sung gần đây

Đây là một bổ sung gần đây cho ngôn ngữ.
Các browser cũ có thể cần [polyfills](https://javascript.info/polyfills).

Nếu chúng ta không cần chi tiết lỗi, `catch` có thể bỏ qua nó:

```
try {
  // ...
} catch { // <-- không có (err)
  // ...
}
```

## [Sử dụng "try…catch"]( #su-dung-try-catch)

Hãy khám phá một use case thực tế của `try...catch`.

Như chúng ta đã biết, JavaScript hỗ trợ phương thức [JSON.parse(str)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/parse) để đọc các giá trị được encode bằng JSON.

Thường thì nó được dùng để decode data nhận được qua network, từ server hoặc nguồn khác.

Chúng ta nhận nó và gọi `JSON.parse` như thế này:

```
let json = '{"name":"John", "age": 30}'; // data from the server

let user = JSON.parse(json); // convert the text representation to JS object

// now user is an object with properties from the string
alert( user.name ); // John
alert( user.age );  // 30
```

Bạn có thể tìm thấy thông tin chi tiết hơn về JSON trong chương [JSON methods, toJSON](/json).

**Nếu `json` bị malformed, `JSON.parse` tạo ra một lỗi, vì vậy script "chết".**

Chúng ta có thể chấp nhận điều đó không? Tất nhiên là không!

Cách này, nếu có gì sai với data, visitor sẽ không bao giờ biết (trừ khi họ mở developer console). Và mọi người thực sự không thích khi thứ gì đó "chỉ chết" mà không có thông báo lỗi.

Hãy dùng `try...catch` để xử lý lỗi:

```
let json = "{ bad json }";

try {

  let user = JSON.parse(json); // <-- khi lỗi xảy ra...
  alert( user.name ); // doesn't work

} catch (err) {
  // ...execution nhảy đến đây
  alert( "Our apologies, the data has errors, we'll try to request it one more time." );
  alert( err.name );
  alert( err.message );
}
```

Ở đây chúng ta dùng block `catch` chỉ để hiển thị message, nhưng chúng ta có thể làm nhiều hơn: gửi một network request mới, đề xuất một alternative cho visitor, gửi thông tin về lỗi đến logging facility, … . Tất cả tốt hơn nhiều so với chỉ chết.

## [Ném lỗi của chính chúng ta](#nem-loi-cua-chinh-chung-ta)

Điều gì xảy ra nếu `json` về mặt cú pháp đúng, nhưng không có required property `name`?

Như thế này:

```
let json = '{ "age": 30 }'; // incomplete data

try {

  let user = JSON.parse(json); // <-- no errors
  alert( user.name ); // no name!

} catch (err) {
  alert( "doesn't execute" );
}
```

Ở đây `JSON.parse` chạy bình thường, nhưng sự vắng mặt của `name` thực sự là một lỗi đối với chúng ta.

Để unified error handling, chúng ta sẽ sử dụng toán tử `throw`.

### [Toán tử "Throw"]( #toan-tu-throw)

Toán tử `throw` tạo ra một lỗi.

Cú pháp là:

```
throw <error object>
```

Về mặt kỹ thuật, chúng ta có thể sử dụng bất cứ thứ gì làm error object. Đó có thể thậm chí là một primitive, như một number hoặc một string, nhưng tốt hơn là dùng objects, ưu tiên với properties `name` và `message` (để stay somewhat compatible với built-in errors).

JavaScript có nhiều built-in constructors cho standard errors: `Error`, `SyntaxError`, `ReferenceError`, `TypeError` và các loại khác. Chúng ta có thể dùng chúng để tạo error objects cũng được.

Cú pháp của chúng là:

```
let error = new Error(message);
// or
let error = new SyntaxError(message);
let error = new ReferenceError(message);
// ...
```

Đối với built-in errors (không phải cho bất kỳ objects nào, chỉ cho errors), property `name` chính xác là tên của constructor. Và `message` được lấy từ argument.

Ví dụ:

```
let error = new Error("Things happen o_O");

alert(error.name); // Error
alert(error.message); // Things happen o_O
```

Hãy xem `JSON.parse` tạo ra loại lỗi gì:

```
try {
  JSON.parse("{ bad json o_O }");
} catch (err) {
  alert(err.name); // SyntaxError
  alert(err.message); // Unexpected token b in JSON at position 2
}
```

Như chúng ta thấy, đó là `SyntaxError`.

Và trong trường hợp của chúng ta, sự vắng mặt của `name` là một lỗi, vì users phải có `name`.

Vì vậy hãy ném nó:

```
let json = '{ "age": 30 }'; // incomplete data

try {

  let user = JSON.parse(json); // <-- no errors

  if (!user.name) {
    throw new SyntaxError("Incomplete data: no name"); // (*)
  }

  alert( user.name );

} catch (err) {
  alert( "JSON Error: " + err.message ); // JSON Error: Incomplete data: no name
}
```

Ở dòng `(*)`, toán tử `throw` tạo ra một `SyntaxError` với `message` đã cho, giống như JavaScript tự tạo nó. Execution của `try` dừng ngay lập tức và control flow nhảy vào `catch`.

Bây giờ `catch` trở thành một nơi duy nhất cho tất cả error handling: cả cho `JSON.parse` và các trường hợp khác.

## [Rethrowing](#rethrowing)

Trong ví dụ trên chúng ta dùng `try...catch` để xử lý incorrect data. Nhưng có thể *một unexpected error khác* xảy ra trong block `try {...}`? Như một programming error (variable không defined) hoặc thứ gì khác, không chỉ cái "incorrect data" này.

Ví dụ:

```
let json = '{ "age": 30 }'; // incomplete data

try {
  user = JSON.parse(json); // <-- quên đặt "let" trước user

  // ...
} catch (err) {
  alert("JSON Error: " + err); // JSON Error: ReferenceError: user is not defined
  // (no JSON Error actually)
}
```

Tất nhiên, mọi thứ đều có thể xảy ra! Programmers mắc lỗi. Ngay cả trong open-source utilities được hàng triệu người dùng trong nhiều thập kỷ – bất ngờ một bug có thể được phát hiện dẫn đến những hack khủng khiếp.

Trong trường hợp của chúng ta, `try...catch` được đặt để bắt lỗi "incorrect data". Nhưng theo bản chất của nó, `catch` nhận *tất cả* các lỗi từ `try`. Ở đây nó nhận một unexpected error, nhưng vẫn hiển thị cùng message `"JSON Error"`. Đó là sai và cũng làm code khó debug hơn.

Để tránh các vấn đề như vậy, chúng ta có thể sử dụng kỹ thuật "rethrowing". Quy tắc đơn giản:

**Catch chỉ nên xử lý những lỗi mà nó biết và "rethrow" tất cả các lỗi khác.**

Kỹ thuật "rethrowing" có thể được giải thích chi tiết hơn như sau:

1. Catch nhận tất cả các lỗi.
2. Trong block `catch (err) {...}` chúng ta phân tích error object `err`.
3. Nếu chúng ta không biết cách xử lý nó, chúng ta làm `throw err`.

Thông thường, chúng ta có thể kiểm tra error type bằng toán tử `instanceof`:

```
try {
  user = { /*...*/ };
} catch (err) {
  if (err instanceof ReferenceError) {
    alert('ReferenceError'); // "ReferenceError" cho việc truy cập undefined variable
  }
}
```

Chúng ta cũng có thể lấy tên error class từ property `err.name`. Tất cả native errors đều có nó. Một option khác là đọc `err.constructor.name`.

Trong mã dưới đây, chúng ta dùng rethrowing để `catch` chỉ xử lý `SyntaxError`:

```
let json = '{ "age": 30 }'; // incomplete data
try {

  let user = JSON.parse(json);

  if (!user.name) {
    throw new SyntaxError("Incomplete data: no name");
  }

  blabla(); // unexpected error

  alert( user.name );

} catch (err) {

  if (err instanceof SyntaxError) {
    alert( "JSON Error: " + err.message );
  } else {
    throw err; // rethrow (*)
  }

}
```

Error throwing ở dòng `(*)` từ bên trong `catch` block "rơi ra" khỏi `try...catch` và có thể bị bắt bởi một outer `try...catch` construct (nếu tồn tại), hoặc nó giết script.

Vì vậy block `catch` thực sự chỉ xử lý những lỗi mà nó biết cách deal with và "bỏ qua" tất cả các lỗi khác.

Ví dụ dưới đây minh họa cách các lỗi như vậy có thể bị bắt bởi một level `try...catch` khác:

```
function readData() {
  let json = '{ "age": 30 }';

  try {
    // ...
    blabla(); // error!
  } catch (err) {
    // ...
    if (!(err instanceof SyntaxError)) {
      throw err; // rethrow (don't know how to deal with it)
    }
  }
}

try {
  readData();
} catch (err) {
  alert( "External catch got: " + err ); // caught it!
}
```

Ở đây `readData` chỉ biết cách xử lý `SyntaxError`, trong khi outer `try...catch` biết cách xử lý mọi thứ.

## [try…catch…finally]( #try-catch-finally)

Đợi đã, chưa xong đâu.

Construct `try...catch` có thể có thêm một code clause: `finally`.

Nếu nó tồn tại, nó chạy trong tất cả các cases:

- sau `try`, nếu không có lỗi,
- sau `catch`, nếu có lỗi.

Cú pháp mở rộng trông như thế này:

```
try {
   ... try to execute the code ...
} catch (err) {
   ... handle errors ...
} finally {
   ... execute always ...
}
```

Thử chạy mã này:

```
try {
  alert( 'try' );
  if (confirm('Make an error?')) BAD_CODE();
} catch (err) {
  alert( 'catch' );
} finally {
  alert( 'finally' );
}
```

Mã có hai cách execution:

1. Nếu bạn trả lời "Yes" cho "Make an error?", thì `try -> catch -> finally`.
2. Nếu bạn nói "Không", thì `try -> finally`.

Clause `finally` thường được sử dụng khi chúng ta bắt đầu làm gì đó và muốn finalize nó trong bất kỳ case nào của outcome.

Ví dụ, chúng ta muốn đo thời gian mà function tính số Fibonacci `fib(n)` tốn. Tự nhiên, chúng ta có thể bắt đầu đo trước khi nó chạy và kết thúc sau đó. Nhưng nếu có lỗi trong quá trình gọi function thì sao? Cụ thể, implementation của `fib(n)` trong code dưới đây trả về lỗi cho negative hoặc non-integer numbers.

Clause `finally` là một nơi tuyệt vời để kết thúc việc đo đạc bất kể gì.

Ở đây `finally` đảm bảo rằng thời gian sẽ được đo đúng trong cả hai tình huống – khi `fib` thực thi thành công và khi có lỗi trong nó:

```
let num = +prompt("Enter a positive integer number?", 35)

let diff, result;

function fib(n) {
  if (n < 0 || Math.trunc(n) != n) {
    throw new Error("Must not be negative, and also an integer.");
  }
  return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}

let start = Date.now();

try {
  result = fib(num);
} catch (err) {
  result = 0;
} finally {
  diff = Date.now() - start;
}

alert(result || "error occurred");

alert( `execution took ${diff}ms` );
```

Bạn có thể kiểm tra bằng cách chạy code với nhập `35` vào `prompt` – nó executes bình thường, `finally` sau `try`. Và sau đó nhập `-1` – sẽ có lỗi ngay lập tức, và execution sẽ tốn `0ms`. Cả hai measurements đều được thực hiện đúng.

Nói cách khác, function có thể kết thúc bằng `return` hoặc `throw`, không quan trọng. Clause `finally` executes trong cả hai cases.

Variables là local bên trong `try...catch...finally`

Xin lưu ý rằng các biến `result` và `diff` trong mã trên được khai báo *trước* `try...catch`.

Nếu không, nếu chúng ta khai báo `let` trong `try` block, nó sẽ chỉ visible bên trong nó.

`finally` và `return`

Clause `finally` hoạt động cho *bất kỳ* exit từ `try...catch`. Đó bao gồm cả explicit `return`.

Trong ví dụ dưới đây, có một `return` trong `try`. Trong trường hợp này, `finally` được thực thi ngay trước khi control trả về outer code.

```
function func() {

  try {
    return 1;

  } catch (err) {
    /* ... */
  } finally {
    alert( 'finally' );
  }
}

alert( func() ); // first works alert from finally, and then this one
```

`try...finally`

Construct `try...finally`, không có clause `catch`, cũng hữu ích. Chúng ta áp dụng nó khi chúng ta không muốn handle errors ở đây (để chúng fall through), nhưng muốn chắc chắn rằng các processes chúng ta đã bắt đầu được finalized.

```
function func() {
  // start doing something that needs completion (like measurements)
  try {
    // ...
  } finally {
    // complete that thing even if all dies
  }
}
```

Trong mã trên, một lỗi bên trong `try` luôn fall out, vì không có `catch`. Nhưng `finally` hoạt động trước khi execution flow rời khỏi function.

## [Global catch]( #global-catch)

Environment-specific

Thông tin từ phần này không phải là một phần của core JavaScript.

Hãy tưởng tượng chúng ta có một fatal error bên ngoài `try...catch`, và script chết. Như một programming error hoặc một vài điều khủng khiếp khác.

Có cách nào để react trên các occurrences như vậy không? Chúng ta có thể muốn log lỗi, hiển thị gì đó cho user (thông thường họ không thấy error messages), v.v.

Không có trong specification, nhưng environments thường cung cấp nó, vì nó thực sự hữu ích. Ví dụ, Node.js có [`process.on("uncaughtException")`](https://nodejs.org/api/process.html#process_event_uncaughtexception) cho việc đó. Và trong browser chúng ta có thể gán một function cho property đặc biệt [window.onerror](https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers/onerror), sẽ chạy trong trường hợp uncaught error.

Cú pháp:

```
window.onerror = function(message, url, line, col, error) {
  // ...
};
```

`message`
:   Error message.

`url`
:   URL của script nơi error xảy ra.

`line`, `col`
:   Line và column numbers nơi error xảy ra.

`error`
:   Error object.

Ví dụ:

```
<script>
  window.onerror = function(message, url, line, col, error) {
    alert(`${message}\n At ${line}:${col} of ${url}`);
  };

  function readData() {
    badFunc(); // Whoops, something went wrong!
  }

  readData();
</script>
```

Vai trò của global handler `window.onerror` thường không phải là recover script execution – điều đó có lẽ impossible trong trường hợp programming errors, mà là gửi error message cho developers.

Cũng có các web-services cung cấp error-logging cho các cases như vậy, như <https://muscula.com> hoặc <https://www.sentry.io>.

Chúng ta hoạt động như thế này:

1. Chúng ta register tại service và nhận một piece of JS (hoặc script URL) từ họ để chèn vào pages.
2. JS script đó thiết lập một custom `window.onerror` function.
3. Khi một lỗi xảy ra, nó gửi một network request về nó đến service.
4. Chúng ta có thể log in vào web interface của service và xem errors.

## [Summary](#summary)

Construct `try...catch` cho phép handle runtime errors. Nó thực sự cho phép "try" chạy code và "catch" các errors có thể xảy ra trong nó.

Cú pháp là:

```
try {
  // run this code
} catch (err) {
  // if an error happened, then jump here
  // err is the error object
} finally {
  // do in any case after try/catch
}
```

Có thể không có section `catch` hoặc không có `finally`, vì vậy các constructs ngắn hơn `try...catch` và `try...finally` cũng valid.

Error objects có các properties sau:

- `message` – human-readable error message.
- `name` – string với error name (error constructor name).
- `stack` (non-standard, nhưng well-supported) – stack tại thời điểm tạo error.

Nếu error object không cần thiết, chúng ta có thể bỏ qua nó bằng cách sử dụng `catch {` thay vì `catch (err) {`.

Chúng ta cũng có thể tạo ra lỗi của riêng mình bằng toán tử `throw`. Về mặt kỹ thuật, argument của `throw` có thể là bất cứ thứ gì, nhưng thường nó là một error object kế thừa từ built-in `Error` class. Xem thêm về extending errors trong chương tiếp theo.

*Rethrowing* là một pattern rất quan trọng của error handling: một `catch` block thường expect và biết cách xử lý particular error type, vì vậy nó nên rethrow những errors mà nó không biết.

Ngay cả khi chúng ta không có `try...catch`, hầu hết environments cho phép chúng ta setup một "global" error handler để bắt các errors "rơi ra". In-browser, đó là `window.onerror`.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Finally or just the code?](#finally-or-just-the-code)

importance: 5

So sánh hai code fragments.

1. Cái đầu tiên dùng `finally` để execute code sau `try...catch`:

   ```
   try {
     work work
   } catch (err) {
     handle errors
   } finally {
     cleanup the working space
   }
   ```
2. Fragment thứ hai đặt cleaning ngay sau `try...catch`:

   ```
   try {
     work work
   } catch (err) {
     handle errors
   }

   cleanup the working space
   ```

Chắc chắn chúng ta cần cleanup sau khi work, không quan trọng có error hay không.

Có advantage nào ở đây khi dùng `finally` không, hay cả hai code fragments đều equal? Nếu có advantage như vậy, thì cho ví dụ khi nó matters.

solution

Sự khác biệt trở nên rõ ràng khi chúng ta nhìn vào code bên trong một function.

Hành vi khác nhau nếu có một "jump out" của `try...catch`.

Ví dụ, khi có `return` bên trong `try...catch`. Clause `finally` hoạt động trong case của *bất kỳ* exit từ `try...catch`, thậm chí qua `return` statement: ngay sau khi `try...catch` xong, nhưng trước khi calling code nhận control.

```
function f() {
  try {
    alert('start');
    return "result";
  } catch (err) {
    /// ...
  } finally {
    alert('cleanup!');
  }
}

f(); // cleanup!
```

…Hoặc khi có `throw`, như ở đây:

```
function f() {
  try {
    alert('start');
    throw new Error("an error");
  } catch (err) {
    // ...
    if("can't handle the error") {
      throw err;
    }

  } finally {
    alert('cleanup!')
  }
}

f(); // cleanup!
```

Đó là `finally` đảm bảo cleanup ở đây. Nếu chúng ta chỉ đặt code ở cuối `f`, nó sẽ không chạy trong những tình huống này.