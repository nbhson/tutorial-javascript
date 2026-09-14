# Quy ước viết code

> Source: [https://javascript.info/coding-style](https://javascript.info/coding-style)

<!-- fetched: 2026-09-14 -->

Code của chúng ta phải sạch sẽ và dễ đọc nhất có thể.

Đó thực sự là nghệ thuật của lập trình – làm một nhiệm vụ phức tạp và mã hóa nó theo cách vừa đúng đắn vừa dễ đọc. Phong cách code tốt greatly hỗ trợ điều đó.

## [Cú pháp](#syntax)

Đây là một cheat sheet với một số quy tắc được đề xuất (xem bên dưới để biết thêm chi tiết):

![](/article/coding-style/code-style.svg)

Bây giờ hãy thảo luận về các quy tắc và lý do cho chúng một cách chi tiết.

Không có quy tắc "bắt buộc"

Không có gì ở đây là cố định. Đây là những sở thích về phong cách, không phải các giáo điều tôn giáo.

### [Dấu ngoặc nhọn](#curly-braces)

Trong hầu hết các dự án JavaScript, dấu ngoặc nhọn được viết theo kiểu "Ai Cập" với dấu mở `{` trên cùng dòng với từ khóa tương ứng – không phải trên dòng mới. Cũng nên có một khoảng trống trước dấu mở, như thế này:

```
if (condition) {
  // làm điều này
  // ...và cái kia
  // ...và cái kia nữa
}
```

Một cấu trúc một dòng, như `if (condition) doSomething()`, là một trường hợp đặc biệt quan trọng. Liệu chúng ta có nên sử dụng dấu ngoặc nhọn hay không?

Đây là các biến thể được chú thích để bạn có thể tự đánh giá tính dễ đọc:

1. 😠 Người mới thường làm như vậy. Không tốt! Dấu ngoặc nhọn không cần thiết:

   ```
   if (n < 0) {alert(`Power ${n} is not supported`);}
   ```
2. 😠 Chia thành dòng riêng mà không có dấu ngoặc nhọn. Đừng bao giờ làm vậy, dễ mắc lỗi khi thêm các dòng mới:

   ```
   if (n < 0)
     alert(`Power ${n} is not supported`);
   ```
3. 😏 Một dòng mà không có dấu ngoặc nhọn – chấp nhận được, nếu nó ngắn:

   ```
   if (n < 0) alert(`Power ${n} is not supported`);
   ```
4. 😃 Biến thể tốt nhất:

   ```
   if (n < 0) {
     alert(`Power ${n} is not supported`);
   }
   ```

Đối với code rất ngắn, một dòng được phép, ví dụ `if (cond) return null`. Nhưng một khối code (biến thể cuối cùng) thường dễ đọc hơn.

### [Độ dài dòng](#line-length)

Không ai thích đọc một dòng code dài theo chiều ngang. Thực hành tốt nhất là chia chúng.

Ví dụ:

```
// backtick quotes ` cho phép chia string thành nhiều dòng
let str = `
  ECMA International's TC39 là một nhóm các nhà phát triển JavaScript,
  người thực hiện, học giả và những người khác, hợp tác với cộng đồng
  để duy trì và phát triển định nghĩa của JavaScript.
`;
```

Và, đối với các câu lệnh `if`:

```
if (
  id === 123 &&
  moonPhase === 'Waning Gibbous' &&
  zodiacSign === 'Libra'
) {
  letTheSorceryBegin();
}
```

Độ dài dòng tối đa nên được thỏa thuận ở cấp độ nhóm. Thông thường là 80 hoặc 120 ký tự.

### [Thụt lề](#indents)

Có hai loại thụt lề:

- **Thụt lề ngang: 2 hoặc 4 khoảng trắng.**

  Thụt lề ngang được tạo bằng cách sử dụng 2 hoặc 4 khoảng trắng hoặc ký tự tab ngang (phím `Tab`). Chọn cái nào là một cuộc chiến tranh cũ. Ngày nay khoảng trắng phổ biến hơn.

  Một ưu điểm của khoảng trắng so với tab là khoảng trắng cho phép cấu hình thụt lề linh hoạt hơn so với ký tự tab.

  Ví dụ, chúng ta có thể căn chỉnh các tham số với dấu ngoặc mở, như thế này:

  ```
  show(parameters,
       aligned, // 5 khoảng trắng padding ở bên trái
       one,
       after,
       another
    ) {
    // ...
  }
  ```
- **Thụt lề dọc: dòng trống để chia code thành các khối logic.**

  Ngay cả một hàm đơn lẻ cũng thường có thể được chia thành các khối logic. Trong ví dụ dưới đây, việc khởi tạo biến, vòng lặp chính và trả về kết quả được chia theo chiều dọc:

  ```
  function pow(x, n) {
    let result = 1;
    //              <--
    for (let i = 0; i < n; i++) {
      result *= x;
    }
    //              <--
    return result;
  }
  ```

  Chèn một dòng trốngextra ở nơi giúp code dễ đọc hơn. Không nên có quá chín dòng code mà không có thụt lề dọc.

### [Dấu chấm phẩy](#semicolons)

Một dấu chấm phẩy nên có sau mỗi câu lệnh, ngay cả khi nó có thể bị bỏ qua.

Có những ngôn ngữ mà dấu chấm phẩy thực sự tùy chọn và hiếm khi được sử dụng. Tuy nhiên, trong JavaScript, có những trường hợp ngắt dòng không được hiểu là dấu chấm phẩy, khiến code dễ bị lỗi. Xem thêm về điều đó trong chương [Cấu trúc code](/structure#semicolon).

Nếu bạn là một lập trình viên JavaScript có kinh nghiệm, bạn có thể chọn phong cách code không có dấu chấm phẩy như [StandardJS](https://standardjs.com/). Nếu không, tốt nhất nên sử dụng dấu chấm phẩy để tránh các cạm bẫy có thể xảy ra. Đa số các nhà phát triển đều sử dụng dấu chấm phẩy.

### [Mức độ lồng nhau](#nesting-levels)

Hãy cố gắng tránh lồng code quá nhiều cấp.

Ví dụ, trong vòng lặp, đôi khi ý tưởng tốt là sử dụng mệnh đề [`continue`](/while-for#continue) để tránh lồng thêm.

Ví dụ, thay vì thêm một điều kiện `if` lồng nhau như thế này:

```
for (let i = 0; i < 10; i++) {
  if (cond) {
    ... // <- một mức lồng nữa
  }
}
```

Chúng ta có thể viết:

```
for (let i = 0; i < 10; i++) {
  if (!cond) continue;
  ...  // <- không có mức lồng extra
}
```

Một điều tương tự có thể được thực hiện với `if/else` và `return`.

Ví dụ, hai cấu trúc dưới đây giống hệt nhau.

Option 1:

```
function pow(x, n) {
  if (n < 0) {
    alert("Negative 'n' not supported");
  } else {
    let result = 1;

    for (let i = 0; i < n; i++) {
      result *= x;
    }

    return result;
  }
}
```

Option 2:

```
function pow(x, n) {
  if (n < 0) {
    alert("Negative 'n' not supported");
    return;
  }

  let result = 1;

  for (let i = 0; i < n; i++) {
    result *= x;
  }

  return result;
}
```

Phương án thứ hai dễ đọc hơn vì trường hợp "đặc biệt" của `n < 0` được xử lý sớm. Một khi kiểm tra được thực hiện, chúng ta có thể chuyển sang luồng code "chính" mà không cần thêm lồng nhau.

## [Vị trí đặt hàm](#function-placement)

Nếu bạn đang viết nhiều hàm "hỗ trợ" và code sử dụng chúng, có ba cách để tổ chức các hàm.

1. Khai báo các hàm *ở trên* code sử dụng chúng:

   ```
   // khai báo hàm
   function createElement() {
     ...
   }

   function setHandler(elem) {
     ...
   }

   function walkAround() {
     ...
   }

   // code sử dụng chúng
   let elem = createElement();
   setHandler(elem);
   walkAround();
   ```
2. Code trước, sau đó là các hàm

   ```
   // code sử dụng các hàm
   let elem = createElement();
   setHandler(elem);
   walkAround();

   // --- các hàm hỗ trợ ---
   function createElement() {
     ...
   }

   function setHandler(elem) {
     ...
   }

   function walkAround() {
     ...
   }
   ```
3. Hỗn hợp: một hàm được khai báo tại nơi nó được sử dụng lần đầu.

Phần lớn thời gian, biến thể thứ hai được ưa chuộng.

Lý do là khi đọc code, chúng ta muốn biết *nó làm gì* trước. Nếu code đi trước, thì nó trở nên rõ ràng từ đầu. Sau đó, có thể chúng ta không cần đọc các hàm altogether, đặc biệt nếu tên của chúng mô tả những gì chúng thực sự làm.

## [Style guides](#style-guides)

Một style guide chứa các quy tắc chung về "cách viết" code, ví dụ như sử dụng dấu ngoặc kép nào, thụt lề bao nhiêu khoảng trắng, độ dài dòng tối đa, v.v. Rất nhiều thứ nhỏ nhặt.

Khi tất cả các thành viên trong nhóm sử dụng cùng một style guide, code sẽ trông đồng nhất, bất kể thành viên nào trong nhóm viết nó.

Tất nhiên, một nhóm luôn có thể viết style guide của riêng mình, nhưng thông thường không cần thiết. Có rất nhiều guide có sẵn để lựa chọn.

Một số lựa chọn phổ biến:

- [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Idiomatic.JS](https://github.com/rwaldron/idiomatic.js)
- [StandardJS](https://standardjs.com/)
- (và nhiều hơn nữa)

Nếu bạn là một nhà phát triển mới bắt đầu, hãy bắt đầu với cheat sheet ở đầu chương này. Sau đó, bạn có thể duyệt qua các style guide khác để thu thập thêm ý tưởng và quyết định cái nào bạn thích nhất.

## [Automated Linters](#automated-linters)

Linters là các công cụ có thể tự động kiểm tra phong cách của code và đưa ra các gợi ý cải thiện.

Điều tuyệt vời về chúng là kiểm tra phong cách cũng có thể tìm thấy một số lỗi, như lỗi chính tả trong tên biến hoặc hàm. Vì đặc điểm này, việc sử dụng linter được khuyến nghị ngay cả khi bạn không muốn tuân theo một "code style" cụ thể nào.

Dưới đây là một số công cụ linting nổi tiếng:

- [JSLint](https://www.jslint.com/) – một trong những linters đầu tiên.
- [JSHint](https://jshint.com/) – nhiều cài đặt hơn JSLint.
- [ESLint](https://eslint.org/) – có lẽ là mới nhất.

Tất cả chúng đều có thể làm được việc. Tác giả sử dụng [ESLint](https://eslint.org/).

Hầu hết các linters được tích hợp với nhiều trình soạn thảo phổ biến: chỉ cần bật plugin trong trình soạn thảo và cấu hình style.

Ví dụ, đối với ESLint bạn nên làm những điều sau:

1. Cài đặt [Node.js](https://nodejs.org/).
2. Cài đặt ESLint với lệnh `npm install -g eslint` (npm là một trình cài đặt package JavaScript).
3. Tạo một file cấu hình có tên `.eslintrc` trong root của dự án JavaScript của bạn (trong thư mục chứa tất cả các file của bạn).
4. Cài đặt/bật plugin cho trình soạn thảo của bạn tích hợp với ESLint. Phần lớn các trình soạn thảo đều có một plugin như vậy.

Đây là một ví dụ về file `.eslintrc`:

```
{
  "extends": "eslint:recommended",
  "env": {
    "browser": true,
    "node": true,
    "es6": true
  },
  "rules": {
    "no-console": 0,
    "indent": 2
  }
}
```

Ở đây directive `"extends"` cho biết cấu hình dựa trên bộ cài đặt "eslint:recommended". Sau đó, chúng ta chỉ định các cài đặt của riêng mình.

Cũng có thể tải xuống các bộ quy tắc style từ web và mở rộng chúng thay thế. Xem <https://eslint.org/docs/user-guide/getting-started> để biết thêm chi tiết về cài đặt.

Ngoài ra, một số IDE có tích hợp sẵn linting, điều đó thuận tiện nhưng không linh hoạt như ESLint.

## [Tổng kết](#summary)

Tất cả các quy tắc cú pháp được mô tả trong chương này (và trong các style guide được tham chiếu) nhằm tăng khả năng đọc của code của bạn. Tất cả chúng đều có thể tranh cãi.

Khi chúng ta nghĩ về việc viết code "tốt hơn", những câu hỏi chúng ta nên tự hỏi là: "Điều gì làm cho code dễ đọc và dễ hiểu hơn?" và "Điều gì có thể giúp chúng ta tránh lỗi?" Đây là những điều chính cần ghi nhớ khi chọn và tranh luận về các phong cách code.

Đọc các style guide phổ biến sẽ cho phép bạn cập nhật với những ý tưởng mới nhất về xu hướng và thực hành tốt nhất về phong cách code.

---

---

## Tasks

## [Tasks](#tasks)

### [Phong cách xấu](#bad-style)

importance: 4

Có gì sai với phong cách code dưới đây?

```
function pow(x,n)
{
  let result=1;
  for(let i=0;i<n;i++) {result*=x;}
  return result;
}

let x=prompt("x?",''), n=prompt("n?",'')
if (n<=0)
{
  alert(`Power ${n} is not supported, please enter an integer number greater than zero`);
}
else
{
  alert(pow(x,n))
}
```

Sửa nó.

solution

Bạn có thể nhận thấy những điều sau:

```
function pow(x,n)  // <- không có khoảng trắng giữa các tham số
{  // <- dấu ngoặc nhọn trên một dòng riêng
  let result=1;   // <- không có khoảng trắng trước hoặc sau =
  for(let i=0;i<n;i++) {result*=x;}   // <- không có khoảng trắng
  // nội dung của { ... } nên ở trên dòng mới
  return result;
}

let x=prompt("x?",''), n=prompt("n?",'') // <-- về mặt kỹ thuật có thể,
// nhưng tốt hơn nên chia thành 2 dòng, cũng thiếu khoảng trắng và ;
if (n<=0)  // <- không có khoảng trắng bên trong (n <= 0), và nên có dòng extra ở trên
{   // <- dấu ngoặc nhọn trên một dòng riêng
  // bên dưới - các dòng dài có thể được chia thành nhiều dòng để cải thiện khả năng đọc
  alert(`Power ${n} is not supported, please enter an integer number greater than zero`);
}
else // <- có thể viết trên một dòng như "} else {"
{
  alert(pow(x,n))  // không có khoảng trắng và thiếu ;
}
```

Biến thể đã sửa:

```
function pow(x, n) {
  let result = 1;

  for (let i = 0; i < n; i++) {
    result *= x;
  }

  return result;
}

let x = prompt("x?", "");
let n = prompt("n?", "");

if (n <= 0) {
  alert(`Power ${n} is not supported,
    please enter an integer number greater than zero`);
} else {
  alert( pow(x, n) );
}
```
