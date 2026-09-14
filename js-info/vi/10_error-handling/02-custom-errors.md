# Lỗi tùy chỉnh (Custom errors), mở rộng Error

> Nguồn: [https://javascript.info/custom-errors](https://javascript.info/custom-errors)

<!-- fetched: 2026-09-14 -->

Khi chúng ta phát triển thứ gì đó, chúng ta thường cần các error classes riêng để phản ánh những điều cụ thể có thể sai trong tasks của chúng ta. Cho errors trong network operations chúng ta có thể cần `HttpError`, cho database operations `DbError`, cho searching operations `NotFoundError` v.v.

Các errors của chúng ta nên hỗ trợ các basic error properties như `message`, `name` và, ưu tiên, `stack`. Nhưng chúng cũng có thể có các properties riêng, ví dụ objects `HttpError` có thể có property `statusCode` với giá trị như `404` hoặc `403` hoặc `500`.

JavaScript cho phép dùng `throw` với bất kỳ argument nào, vì vậy về mặt kỹ thuật các custom error classes của chúng ta không cần inherit từ `Error`. Nhưng nếu chúng ta inherit, thì sẽ có thể dùng `obj instanceof Error` để identify error objects. Vì vậy tốt hơn là inherit từ nó.

Khi application lớn dần, các errors của chúng ta tự nhiên hình thành một hierarchy. Ví dụ, `HttpTimeoutError` có thể inherit từ `HttpError`, và vân vân.

## [Extending Error](#extending-error)

Làm một ví dụ, hãy xem xét function `readUser(json)` nên đọc JSON với user data.

Đây là ví dụ về một `json` valid có thể trông như thế nào:

```
let json = `{ "name": "John", "age": 30 }`;
```

Bên trong, chúng ta sẽ dùng `JSON.parse`. Nếu nó nhận malformed `json`, thì nó throw `SyntaxError`. Nhưng ngay cả khi `json` về mặt cú pháp đúng, đó cũng không có nghĩa là nó là một user valid, đúng không? Nó có thể thiếu data cần thiết. Ví dụ, nó có thể không có properties `name` và `age` mà là essential cho users của chúng ta.

Function `readUser(json)` của chúng ta sẽ không chỉ đọc JSON, mà còn kiểm tra ("validate") data. Nếu không có required fields, hoặc format sai, thì đó là một lỗi. Và đó không phải là `SyntaxError`, vì data về mặt cú pháp đúng, nhưng một loại lỗi khác. Chúng ta sẽ gọi nó là `ValidationError` và tạo một class cho nó. Một error loại đó cũng nên mang thông tin về offending field.

Class `ValidationError` của chúng ta nên inherit từ class `Error`.

Class `Error` là built-in, nhưng đây là mã giả định của nó để chúng ta hiểu những gì chúng ta đang extend:

```
// The "pseudocode" for the built-in Error class defined by JavaScript itself
class Error {
  constructor(message) {
    this.message = message;
    this.name = "Error"; // (different names for different built-in error classes)
    this.stack = <call stack>; // non-standard, but most environments support it
  }
}
```

Bây giờ hãy inherit `ValidationError` từ nó và thử nó trong action:

```
class ValidationError extends Error {
  constructor(message) {
    super(message); // (1)
    this.name = "ValidationError"; // (2)
  }
}

function test() {
  throw new ValidationError("Whoops!");
}

try {
  test();
} catch(err) {
  alert(err.message); // Whoops!
  alert(err.name); // ValidationError
  alert(err.stack); // a list of nested calls with line numbers for each
}
```

Xin lưu ý: ở dòng `(1)` chúng ta gọi parent constructor. JavaScript yêu cầu chúng ta gọi `super` trong child constructor, vì vậy đó là bắt buộc. Parent constructor thiết lập property `message`.

Parent constructor cũng thiết lập property `name` thành `"Error"`, vì vậy ở dòng `(2)` chúng ta reset nó về giá trị đúng.

Hãy thử dùng nó trong `readUser(json)`:

```
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

// Usage
function readUser(json) {
  let user = JSON.parse(json);

  if (!user.age) {
    throw new ValidationError("No field: age");
  }
  if (!user.name) {
    throw new ValidationError("No field: name");
  }

  return user;
}

// Working example with try..catch

try {
  let user = readUser('{ "age": 25 }');
} catch (err) {
  if (err instanceof ValidationError) {
    alert("Invalid data: " + err.message); // Invalid data: No field: name
  } else if (err instanceof SyntaxError) { // (*)
    alert("JSON Syntax Error: " + err.message);
  } else {
    throw err; // unknown error, rethrow it (**)
  }
}
```

Block `try..catch` trong mã trên xử lý cả `ValidationError` của chúng ta và built-in `SyntaxError` từ `JSON.parse`.

Xin lưu ý xem chúng ta dùng `instanceof` để kiểm tra specific error type ở dòng `(*)`.

Chúng ta cũng có thể nhìn vào `err.name`, như thế này:

```
// ...
// instead of (err instanceof SyntaxError)
} else if (err.name == "SyntaxError") { // (*)
// ...
```

Phiên bản `instanceof` tốt hơn nhiều, vì trong tương lai chúng ta sẽ extend `ValidationError`, tạo subtypes của nó, như `PropertyRequiredError`. Và `instanceof` check sẽ tiếp tục hoạt động cho các inheriting classes mới. Vì vậy đó là future-proof.

Cũng quan trọng là nếu `catch` gặp một unknown error, thì nó rethrow nó ở line `(**)`. Block `catch` chỉ biết cách xử lý validation và syntax errors, các loại khác (do typo trong code hoặc các lý do unknown khác) nên fall through.

## [Further inheritance](#further-inheritance)

Class `ValidationError` rất generic. Nhiều thứ có thể sai. Property có thể vắng mặt hoặc có thể ở wrong format (như string value cho `age` thay vì number). Hãy tạo một class cụ thể hơn `PropertyRequiredError`, chính xác cho absent properties. Nó sẽ mang thêm thông tin về property bị thiếu.

```
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

class PropertyRequiredError extends ValidationError {
  constructor(property) {
    super("No property: " + property);
    this.name = "PropertyRequiredError";
    this.property = property;
  }
}

// Usage
function readUser(json) {
  let user = JSON.parse(json);

  if (!user.age) {
    throw new PropertyRequiredError("age");
  }
  if (!user.name) {
    throw new PropertyRequiredError("name");
  }

  return user;
}

// Working example with try..catch

try {
  let user = readUser('{ "age": 25 }');
} catch (err) {
  if (err instanceof ValidationError) {
    alert("Invalid data: " + err.message); // Invalid data: No property: name
    alert(err.name); // PropertyRequiredError
    alert(err.property); // name
  } else if (err instanceof SyntaxError) {
    alert("JSON Syntax Error: " + err.message);
  } else {
    throw err; // unknown error, rethrow it
  }
}
```

Class mới `PropertyRequiredError` dễ sử dụng: chúng ta chỉ cần truyền property name: `new PropertyRequiredError(property)`. Human-readable `message` được tạo bởi constructor.

Xin lưu ý rằng `this.name` trong `PropertyRequiredError` constructor lại được gán thủ công. Điều đó có thể trở nên hơi tedious – để gán `this.name = <class name>` trong mọi custom error class. Chúng ta có thể tránh nó bằng cách tạo một "basic error" class riêng gán `this.name = this.constructor.name`. Và sau đó inherit tất cả custom errors của chúng ta từ nó.

Hãy gọi nó là `MyError`.

Đây là mã với `MyError` và các custom error classes khác, được đơn giản hóa:

```
class MyError extends Error {
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
  }
}

class ValidationError extends MyError { }

class PropertyRequiredError extends ValidationError {
  constructor(property) {
    super("No property: " + property);
    this.property = property;
  }
}

// name is correct
alert( new PropertyRequiredError("field").name ); // PropertyRequiredError
```

Bây giờ custom errors ngắn gọn hơn nhiều, đặc biệt `ValidationError`, vì chúng ta đã loại bỏ dòng `"this.name = ..."` trong constructor.

## [Wrapping exceptions](#wrapping-exceptions)

Mục đích của function `readUser` trong mã trên là "đọc user data". Có thể xảy ra nhiều loại errors trong quá trình đó. Hiện tại chúng ta có `SyntaxError` và `ValidationError`, nhưng trong tương lai function `readUser` có thể lớn dần và có thể generate các loại errors khác.

Code gọi `readUser` nên handle những errors này. Hiện tại nó dùng nhiều `if`s trong `catch` block, check class và handle known errors và rethrow unknown ones.

Scheme như thế này:

```
try {
  ...
  readUser()  // the potential error source
  ...
} catch (err) {
  if (err instanceof ValidationError) {
    // handle validation errors
  } else if (err instanceof SyntaxError) {
    // handle syntax errors
  } else {
    throw err; // unknown error, rethrow it
  }
}
```

Trong mã trên chúng ta thấy hai types errors, nhưng có thể nhiều hơn.

Nếu function `readUser` generate nhiều loại errors, thì chúng ta nên tự hỏi: chúng ta có thực sự muốn check cho tất cả error types one-by-one mỗi lần không?

Thường câu trả lời là "Không": chúng ta muốn "one level above all that". Chỉ muốn biết có "data reading error" không – tại sao chính xác nó xảy ra thường irrelevant (error message describes it). Hoặc, thậm chí tốt hơn, chúng ta muốn có cách lấy error details, nhưng chỉ khi chúng ta cần.

Kỹ thuật chúng ta mô tả ở đây được gọi là "wrapping exceptions".

1. Chúng ta sẽ tạo một class mới `ReadError` để đại diện cho generic "data reading" error.
2. Function `readUser` sẽ bắt data reading errors xảy ra bên trong nó, như `ValidationError` và `SyntaxError`, và generate `ReadError` thay thế.
3. Object `ReadError` sẽ giữ reference đến original error trong property `cause` của nó.

Sau đó code gọi `readUser` chỉ phải check `ReadError`, không phải mọi loại data reading errors. Và nếu nó cần thêm chi tiết của error, nó có thể check property `cause`.

Đây là code định nghĩa `ReadError` và demo việc dùng nó trong `readUser` và `try..catch`:

```
class ReadError extends Error {
  constructor(message, cause) {
    super(message);
    this.cause = cause;
    this.name = 'ReadError';
  }
}

class ValidationError extends Error { /*...*/ }
class PropertyRequiredError extends ValidationError { /* ... */ }

function validateUser(user) {
  if (!user.age) {
    throw new PropertyRequiredError("age");
  }

  if (!user.name) {
    throw new PropertyRequiredError("name");
  }
}

function readUser(json) {
  let user;

  try {
    user = JSON.parse(json);
  } catch (err) {
    if (err instanceof SyntaxError) {
      throw new ReadError("Syntax Error", err);
    } else {
      throw err;
    }
  }

  try {
    validateUser(user);
  } catch (err) {
    if (err instanceof ValidationError) {
      throw new ReadError("Validation Error", err);
    } else {
      throw err;
    }
  }

}

try {
  readUser('{bad json}');
} catch (e) {
  if (e instanceof ReadError) {
    alert(e);
    // Original error: SyntaxError: Unexpected token b in JSON at position 1
    alert("Original error: " + e.cause);
  } else {
    throw e;
  }
}
```

Trong mã trên, `readUser` hoạt động chính xác như mô tả – catches syntax và validation errors và throw `ReadError` errors thay thế (unknown errors được rethrow như thường lệ).

Vì vậy outer code chỉ check `instanceof ReadError` và thế là xong. Không cần liệt kê tất cả các possible error types.

Cách tiếp cận này được gọi là "wrapping exceptions", vì chúng ta lấy "low level" exceptions và "wrap" chúng vào `ReadError` abstract hơn. Nó được sử dụng rộng rãi trong object-oriented programming.

## [Summary](#summary)

- Chúng ta có thể inherit từ `Error` và các built-in error classes khác bình thường. Chúng ta chỉ cần chú ý property `name` và đừng quên gọi `super`.
- Chúng ta có thể dùng `instanceof` để check cho particular errors. Nó cũng hoạt động với inheritance. Nhưng đôi khi chúng ta có một error object từ 3rd-party library và không có cách dễ dàng để lấy class của nó. Lúc đó property `name` có thể dùng cho các checks như vậy.
- Wrapping exceptions là một kỹ thuật phổ biến: một function xử lý low-level exceptions và tạo higher-level errors thay vì các low-level ones khác nhau. Low-level exceptions đôi khi trở thành properties của object đó như `err.cause` trong các ví dụ trên, nhưng không bắt buộc phải vậy.

---

---

## Bài tập

## [Các bài tập](#tasks)

### [Inherit from SyntaxError](#inherit-from-syntaxerror)

importance: 5

Tạo class `FormatError` inherit từ built-in `SyntaxError` class.

Nó nên support `message`, `name` và `stack` properties.

Ví dụ sử dụng:

```
let err = new FormatError("formatting error");

alert( err.message ); // formatting error
alert( err.name ); // FormatError
alert( err.stack ); // stack

alert( err instanceof FormatError ); // true
alert( err instanceof SyntaxError ); // true (because inherits from SyntaxError)
```

solution

```
class FormatError extends SyntaxError {
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
  }
}

let err = new FormatError("formatting error");

alert( err.message ); // formatting error
alert( err.name ); // FormatError
alert( err.stack ); // stack

alert( err instanceof SyntaxError ); // true
```