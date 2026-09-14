# Kiểm thử tự động với Mocha

> Source: [https://javascript.info/testing-mocha](https://javascript.info/testing-mocha)

<!-- fetched: 2026-09-14 -->

Kiểm thử tự động sẽ được sử dụng trong các task sau này, và nó cũng được sử dụng rộng rãi trong các dự án thực tế.

## [Tại sao chúng ta cần tests?](#why-do-we-need-tests)

Khi chúng ta viết một hàm, chúng ta thường có thể tưởng tượng ra những gì nó nên làm: tham số nào cho kết quả nào.

Trong quá trình phát triển, chúng ta có thể kiểm tra hàm bằng cách chạy nó và so sánh kết quả với kết quả mong đợi. Ví dụ, chúng ta có thể làm điều đó trong console.

Nếu có gì đó sai – thì chúng ta sửa code, chạy lại, kiểm tra kết quả – và cứ như vậy cho đến khi nó hoạt động.

Nhưng việc "chạy lại" thủ công như vậy là không hoàn hảo.

**Khi kiểm thử code bằng cách chạy lại thủ công, rất dễ bỏ sót điều gì đó.**

Ví dụ, chúng ta đang tạo một hàm `f`. Viết một số code, kiểm thử: `f(1)` hoạt động, nhưng `f(2)` không hoạt động. Chúng ta sửa code và giờ `f(2)` hoạt động. Có vẻ như đã hoàn chỉnh? Nhưng chúng ta quên kiểm tra lại `f(1)`. Điều đó có thể dẫn đến lỗi.

Điều đó rất điển hình. Khi chúng ta phát triển thứ gì đó, chúng ta giữ rất nhiều trường hợp sử dụng có thể trong tâm trí. Nhưng khó có thể mong đợi một lập trình viên kiểm tra tất cả chúng một cách thủ công sau mỗi thay đổi. Vì vậy, trở nên dễ dàng sửa một thứ và phá hỏng thứ khác.

**Kiểm thử tự động có nghĩa là tests được viết riêng biệt, bên cạnh code. Chúng chạy các hàm của chúng ta theo nhiều cách khác nhau và so sánh kết quả với kết quả mong đợi.**

## [Behavior Driven Development (BDD)](#behavior-driven-development-bdd)

Hãy bắt đầu với một kỹ thuật có tên [Behavior Driven Development](http://en.wikipedia.org/wiki/Behavior-driven_development) hoặc, ngắn gọn, BDD.

**BDD là ba thứ trong một: tests VÀ tài liệu VÀ ví dụ.**

Để hiểu BDD, chúng ta sẽ xem xét một trường hợp phát triển thực tế.

## [Phát triển "pow": spec](#development-of-pow-the-spec)

Giả sử chúng ta muốn tạo một hàm `pow(x, n)` nâng `x` lên lũy thừa nguyên `n`. Chúng ta giả sử rằng `n≥0`.

Nhiệm vụ này chỉ là một ví dụ: có toán tử `**` trong JavaScript có thể làm điều đó, nhưng ở đây chúng ta tập trung vào quy trình phát triển có thể áp dụng cho các nhiệm vụ phức tạp hơn.

Trước khi tạo code của `pow`, chúng ta có thể tưởng tượng hàm nên làm gì và mô tả nó.

Sự mô tả như vậy được gọi là *specification* hoặc, ngắn gọn, spec, và chứa các mô tả về các trường hợp sử dụng cùng với các tests cho chúng, như thế này:

```
describe("pow", function() {

  it("raises to n-th power", function() {
    assert.equal(pow(2, 3), 8);
  });

});
```

Một spec có ba khối xây dựng chính mà bạn có thể thấy ở trên:

`describe("title", function() { ... })`
:   Chúng ta đang mô tả functionality nào? Trong trường hợp của chúng ta, chúng ta đang mô tả hàm `pow`. Được sử dụng để nhóm các "worker" – các block `it`.

`it("use case description", function() { ... })`
:   Trong tiêu đề của `it` chúng ta *theo cách dễ đọc bằng ngôn ngữ tự nhiên* mô tả trường hợp sử dụng cụ thể, và đối số thứ hai là một hàm kiểm tra nó.

`assert.equal(value1, value2)`
:   Code bên trong block `it`, nếu implementation đúng, sẽ thực thi mà không có lỗi.

    Các hàm `assert.*` được sử dụng để kiểm tra xem `pow` có hoạt động như mong đợi không. Ngay tại đây chúng ta đang sử dụng một trong số chúng – `assert.equal`, nó so sánh các đối số và tạo lỗi nếu chúng không bằng nhau. Ở đây nó kiểm tra rằng kết quả của `pow(2, 3)` bằng `8`. Có các loại so sánh và kiểm tra khác, chúng ta sẽ thêm sau.

Spec có thể được thực thi, và nó sẽ chạy test được chỉ định trong block `it`. Chúng ta sẽ thấy điều đó sau.

## [Quy trình phát triển](#the-development-flow)

Quy trình phát triển thường trông như thế này:

1. Một spec ban đầu được viết, với các tests cho functionality cơ bản nhất.
2. Một implementation ban đầu được tạo.
3. Để kiểm tra xem nó có hoạt động không, chúng ta chạy framework kiểm thử [Mocha](https://mochajs.org/) (chi tiết hơn sớm) chạy spec. Trong khi functionality chưa hoàn chỉnh, các lỗi được hiển thị. Chúng ta thực hiện các sửa đổi cho đến khi mọi thứ hoạt động.
4. Giờ chúng ta có một implementation ban đầu hoạt động với tests.
5. Chúng ta thêm nhiều trường hợp sử dụng hơn vào spec, có lẽ chưa được support bởi implementations. Tests bắt đầu fail.
6. Quay lại bước 3, cập nhật implementation cho đến khi tests không cho lỗi.
7. Lặp lại các bước 3-6 cho đến khi functionality sẵn sàng.

Vì vậy, phát triển là *iterative*. Chúng ta viết spec, implement nó, đảm bảo tests pass, sau đó viết nhiều tests hơn, đảm bảo chúng hoạt động v.v. Vào cuối chúng ta có cả implementation hoạt động và tests cho nó.

Hãy xem quy trình phát triển này trong trường hợp thực tế của chúng ta.

Bước đầu tiên đã hoàn thành: chúng ta có spec ban đầu cho `pow`. Giờ, trước khi tạo implementation, hãy sử dụng một vài thư viện JavaScript để chạy các tests, chỉ để xem chúng có hoạt động không (tất cả sẽ fail).

## [Spec trong hành động](#the-spec-in-action)

Ở đây trong tutorial chúng ta sẽ sử dụng các thư viện JavaScript sau cho tests:

- [Mocha](https://mochajs.org/) – framework cốt lõi: nó cung cấp các hàm kiểm thử chung bao gồm `describe` và `it` và hàm chính chạy tests.
- [Chai](https://www.chaijs.com/) – thư viện với nhiều assertions. Nó cho phép sử dụng rất nhiều assertions khác nhau, giờ chúng ta chỉ cần `assert.equal`.
- [Sinon](https://sinonjs.org/) – thư viện để spy over functions, emulate built-in functions và nhiều hơn nữa, chúng ta sẽ cần nó sau này.

Các thư viện này phù hợp cho cả kiểm thử trong browser và server-side. Ở đây chúng ta sẽ xem xét biến thể browser.

Trang HTML đầy đủ với các frameworks và spec `pow`:

```
<!DOCTYPE html>
<html>
<head>
  <!-- thêm mocha css, để hiển thị kết quả -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mocha/3.2.0/mocha.css">
  <!-- thêm mocha framework code -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/mocha/3.2.0/mocha.js"></script>
  <script>
    mocha.setup('bdd'); // setup tối thiểu
  </script>
  <!-- thêm chai -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/chai/3.5.0/chai.js"></script>
  <script>
    // chai có nhiều thứ, hãy làm assert global
    let assert = chai.assert;
  </script>
</head>

<body>

  <script>
    function pow(x, n) {
      /* function code cần được viết, đang trống */
    }
  </script>

  <!-- script với tests (describe, it...) -->
  <script src="test.js"></script>

  <!-- element với id="mocha" sẽ chứa kết quả tests -->
  <div id="mocha"></div>

  <!-- chạy tests! -->
  <script>
    mocha.run();
  </script>
</body>

</html>
```

Trang có thể được chia thành năm phần:

1. `<head>` – thêm các thư viện third-party và styles cho tests.
2. `<script>` với hàm để kiểm tra, trong trường hợp của chúng ta – với code cho `pow`.
3. Các tests – trong trường hợp của chúng ta là một script bên ngoài `test.js` có `describe("pow", ...)` từ ở trên.
4. Element HTML `<div id="mocha">` sẽ được Mocha sử dụng để output kết quả.
5. Các tests được bắt đầu bằng lệnh `mocha.run()`.

Kết quả:

Tính đến giờ, test fail, có một lỗi. Điều đó hợp lý: chúng ta có code hàm rỗng trong `pow`, vì vậy `pow(2,3)` trả về `undefined` thay vì `8`.

Về sau, hãy lưu ý rằng có các test-runners cấp cao hơn, như [karma](https://karma-runner.github.io/) và những cái khác, làm cho việc autorun nhiều tests khác nhau trở nên dễ dàng.

## [Initial implementation](#initial-implementation)

Hãy tạo một implementation đơn giản của `pow`, để tests pass:

```
function pow(x, n) {
  return 8; // :) chúng ta gian lận!
}
```

Wow, giờ nó hoạt động rồi!

## [Cải thiện spec](#improving-the-spec)

Những gì chúng ta đã làm chắc chắn là gian lận. Hàm không hoạt động: một nỗ lực tính toán `pow(3,4)` sẽ cho kết quả sai, nhưng tests pass.

…Nhưng tình huống khá điển hình, nó xảy ra trong thực tế. Tests pass, nhưng hàm hoạt động sai. Spec của chúng ta không hoàn hảo. Chúng ta cần thêm nhiều trường hợp sử dụng hơn vào nó.

Hãy thêm một test nữa để kiểm tra rằng `pow(3, 4) = 81`.

Chúng ta có thể chọn một trong hai cách để tổ chức test ở đây:

1. Biến thể đầu tiên – thêm một `assert` nữa vào cùng `it`:

   ```
   describe("pow", function() {

     it("raises to n-th power", function() {
       assert.equal(pow(2, 3), 8);
       assert.equal(pow(3, 4), 81);
     });

   });
   ```
2. Biến thể thứ hai – tạo hai tests:

   ```
   describe("pow", function() {

     it("2 raised to power 3 is 8", function() {
       assert.equal(pow(2, 3), 8);
     });

     it("3 raised to power 4 is 81", function() {
       assert.equal(pow(3, 4), 81);
     });

   });
   ```

Sự khác biệt chính là khi `assert` kích hoạt một lỗi, block `it` ngay lập tức kết thúc. Vì vậy, trong biến thể đầu tiên nếu `assert` đầu tiên fail, thì chúng ta sẽ không bao giờ thấy kết quả của `assert` thứ hai.

Tạo các tests riêng biệt hữu ích để có nhiều thông tin hơn về những gì đang xảy ra, vì vậy biến thể thứ hai tốt hơn.

Và ngoài ra, có một quy tắc nữa nên tuân theo.

**Một test kiểm tra một thứ.**

Nếu chúng ta nhìn vào test và thấy hai checks độc lập trong đó, tốt hơn là chia nó thành hai cái đơn giản hơn.

Vì vậy, hãy tiếp tục với biến thể thứ hai.

Kết quả:

Như chúng ta có thể mong đợi, test thứ hai đã fail. Chắc chắn, hàm của chúng ta luôn trả về `8`, trong khi `assert` mong đợi `81`.

## [Cải thiện implementation](#improving-the-implementation)

Hãy viết một thứ gì đó thực tế hơn để tests pass:

```
function pow(x, n) {
  let result = 1;

  for (let i = 0; i < n; i++) {
    result *= x;
  }

  return result;
}
```

Để chắc chắn rằng hàm hoạt động tốt, hãy kiểm thử nó cho nhiều giá trị hơn. Thay vì viết thủ công các block `it`, chúng ta có thể tạo chúng trong `for`:

```
describe("pow", function() {

  function makeTest(x) {
    let expected = x * x * x;
    it(`${x} in the power 3 is ${expected}`, function() {
      assert.equal(pow(x, 3), expected);
    });
  }

  for (let x = 1; x <= 5; x++) {
    makeTest(x);
  }

});
```

Kết quả:

## [Nested describe](#nested-describe)

Chúng ta sẽ thêm nhiều tests hơn. Nhưng trước đó hãy lưu ý rằng hàm helper `makeTest` và `for` nên được nhóm lại. Chúng ta sẽ không cần `makeTest` trong các tests khác, nó chỉ cần trong `for`: nhiệm vụ chung của chúng là kiểm tra cách `pow` nâng lên lũy thừa cho trước.

Grouping được thực hiện với một `describe` nested:

```
describe("pow", function() {

  describe("raises x to power 3", function() {

    function makeTest(x) {
      let expected = x * x * x;
      it(`${x} in the power 3 is ${expected}`, function() {
        assert.equal(pow(x, 3), expected);
      });
    }

    for (let x = 1; x <= 5; x++) {
      makeTest(x);
    }

  });

  // ... thêm nhiều tests nữa ở đây, cả describe và it có thể được thêm
});
```

`describe` nested xác định một "subgroup" tests mới. Trong output chúng ta có thể thấy indentation được đánh dấu:

Trong tương lai chúng ta có thể thêm nhiều `it` và `describe` ở cấp cao nhất với các hàm helper của riêng chúng, chúng sẽ không thấy `makeTest`.

`before/after` và `beforeEach/afterEach`

Chúng ta có thể setup các hàm `before/after` thực thi trước/sau khi chạy tests, và cũng các hàm `beforeEach/afterEach` thực thi trước/sau *mỗi* `it`.

Ví dụ:

```
describe("test", function() {

  before(() => alert("Testing started – before all tests"));
  after(() => alert("Testing finished – after all tests"));

  beforeEach(() => alert("Before a test – enter a test"));
  afterEach(() => alert("After a test – exit a test"));

  it('test 1', () => alert(1));
  it('test 2', () => alert(2));

});
```

Thứ tự thực hiện sẽ là:

```
Testing started – before all tests (before)
Before a test – enter a test (beforeEach)
1
After a test – exit a test   (afterEach)
Before a test – enter a test (beforeEach)
2
After a test – exit a test   (afterEach)
Testing finished – after all tests (after)
```

[Mở ví dụ trong sandbox.](https://plnkr.co/edit/qDrAVgw2asod4sRo?p=preview)

Thông thường, `beforeEach/afterEach` và `before/after` được sử dụng để thực hiện khởi tạo, zero out counters hoặc làm điều gì đó khác giữa các tests (hoặc các nhóm tests).

## [Mở rộng spec](#extending-the-spec)

Functionality cơ bản của `pow` đã hoàn thành. Vòng lặp phát triển đầu tiên đã hoàn tất. Khi chúng ta kết thúc ăn mừng và uống champagne – hãy tiếp tục và cải thiện nó.

Như đã nói, hàm `pow(x, n)` được thiết kế để làm việc với các giá trị nguyên dương `n`.

Để biểu thị một lỗi toán học, các hàm JavaScript thường trả về `NaN`. Hãy làm tương tự đối với các giá trị không hợp lệ của `n`.

Trước tiên hãy thêm behavior vào spec(!):

```
describe("pow", function() {

  // ...

  it("for negative n the result is NaN", function() {
    assert.isNaN(pow(2, -1));
  });

  it("for non-integer n the result is NaN", function() {
    assert.isNaN(pow(2, 1.5));
  });

});
```

Kết quả với các tests mới:

Các tests mới được thêm vào fail, vì implementation của chúng ta không support chúng. Đó là cách BDD được thực hiện: trước tiên chúng ta viết các tests fail, sau đó tạo implementation cho chúng.

Các assertions khác

Xin lưu ý assertion `assert.isNaN`: nó kiểm tra `NaN`.

Cũng có các assertions khác trong [Chai](https://www.chaijs.com/), ví dụ:

- `assert.equal(value1, value2)` – kiểm tra Equality `value1 == value2`.
- `assert.strictEqual(value1, value2)` – kiểm tra strict Equality `value1 === value2`.
- `assert.notEqual`, `assert.notStrictEqual` – các checks ngược lại với các checks ở trên.
- `assert.isTrue(value)` – kiểm tra rằng `value === true`
- `assert.isFalse(value)` – kiểm tra rằng `value === false`
- …danh sách đầy đủ có trong [docs](https://www.chaijs.com/api/assert/)

Vì vậy, chúng ta nên thêm một vài dòng vào `pow`:

```
function pow(x, n) {
  if (n < 0) return NaN;
  if (Math.round(n) != n) return NaN;

  let result = 1;

  for (let i = 0; i < n; i++) {
    result *= x;
  }

  return result;
}
```

Giờ nó hoạt động, tất cả tests đều pass:

[Mở ví dụ cuối cùng đầy đủ trong sandbox.](https://plnkr.co/edit/pAczWMe5ms4IXPwO?p=preview)

## [Tổng kết](#summary)

Trong BDD, spec đi trước, sau đó là implementation. Vào cuối chúng ta có cả spec và code.

Spec có thể được sử dụng theo ba cách:

1. Như **Tests** – chúng đảm bảo rằng code hoạt động đúng.
2. Như **Docs** – tiêu đề của `describe` và `it` cho biết hàm làm gì.
3. Như **Examples** – các tests thực sự là các ví dụ hoạt động cho thấy cách một hàm có thể được sử dụng.

Với spec, chúng ta có thể an toàn cải thiện, thay đổi, thậm chí viết lại hàm từ đầu và đảm bảo rằng nó vẫn hoạt động đúng.

Điều đó đặc biệt quan trọng trong các dự án lớn khi một hàm được sử dụng ở nhiều nơi. Khi chúng ta thay đổi một hàm như vậy, thực sự không có cách nào thủ công để kiểm tra xem mọi nơi sử dụng nó có còn hoạt động đúng không.

Không có tests, mọi người có hai cách:

1. Thực hiện thay đổi, bất kể điều gì. Và sau đó người dùng của chúng ta gặp phải các lỗi, vì chúng ta có thể đã thất bại trong việc kiểm tra thứ gì đó bằng tay.
2. Hoặc, nếu hình phạt cho lỗi là nghiêm khắc, vì không có tests, mọi người trở nên sợ sửa đổi các hàm như vậy, và sau đó code trở nên lỗi thời, không ai muốn đi vào nó. Không tốt cho phát triển.

**Kiểm thử tự động giúp tránh những vấn đề này!**

Nếu dự án được bao phủ với tests, thì thực sự không có vấn đề như vậy. Sau bất kỳ thay đổi nào, chúng ta có thể chạy tests và thấy rất nhiều checks được thực hiện trong vài giây.

**Hơn nữa, code được kiểm thử kỹ có kiến trúc tốt hơn.**

Tất nhiên, đó là vì code được kiểm thử tự động dễ sửa đổi và cải thiện hơn. Nhưng cũng có một lý do khác.

Để viết tests, code nên được tổ chức theo cách mà mọi hàm có một nhiệm vụ được mô tả rõ ràng, input và output xác định rõ. Điều đó có nghĩa là kiến trúc tốt ngay từ đầu.

Trong thực tế, điều đó đôi khi không dễ dàng như vậy. Đôi khi khó viết spec trước code thực tế, vì chưa rõ ràng nó nên hoạt động như thế nào. Nhưng nói chung viết tests làm cho phát triển nhanh hơn và ổn định hơn.

Sau này trong tutorial bạn sẽ gặp nhiều task với tests baked-in. Vì vậy bạn sẽ thấy nhiều ví dụ thực tiễn hơn.

Viết tests đòi hỏi kiến thức JavaScript tốt. Nhưng chúng ta mới bắt đầu học nó. Vì vậy, để ổn định mọi thứ, cho đến nay bạn không được yêu cầu viết tests, nhưng bạn đã có thể đọc chúng ngay cả khi chúng hơi phức tạp hơn trong chương này.

---

---

## Tasks

## [Tasks](#tasks)

### [Có gì sai trong test?](#what-s-wrong-in-the-test)

importance: 5

Có gì sai trong test của `pow` dưới đây?

```
it("Raises x to the power n", function() {
  let x = 5;

  let result = x;
  assert.equal(pow(x, 1), result);

  result *= x;
  assert.equal(pow(x, 2), result);

  result *= x;
  assert.equal(pow(x, 3), result);
});
```

P.S. Về mặt cú pháp test đúng và pass.

solution

TestDemonstrate một trong những cám dỗ mà nhà phát triển gặp phải khi viết tests.

Những gì chúng ta có ở đây thực sự là 3 tests, nhưng được arrange như một hàm single với 3 asserts.

Đôi khi dễ dàng hơn để viết như vậy, nhưng nếu có lỗi xảy ra, nó ít rõ ràng hơn về những gì đã sai.

Nếu một lỗi xảy ra ở giữa một luồng thực thi phức tạp, thì chúng ta sẽ phải xác định dữ liệu tại điểm đó. Chúng ta thực sự phải *gỡ lỗi test*.

Tốt hơn nhiều là chia test thành nhiều block `it` với các input và output được viết rõ ràng.

Như thế này:

```
describe("Raises x to power n", function() {
  it("5 in the power of 1 equals 5", function() {
    assert.equal(pow(5, 1), 5);
  });

  it("5 in the power of 2 equals 25", function() {
    assert.equal(pow(5, 2), 25);
  });

  it("5 in the power of 3 equals 125", function() {
    assert.equal(pow(5, 3), 125);
  });
});
```

Chúng ta đã thay thế `it` single với `describe` và một nhóm các block `it`. Giờ nếu có gì đó fail chúng ta sẽ thấy rõ ràng dữ liệu là gì.

Chúng ta cũng có thể cô lập một test duy nhất và chạy nó ở chế độ standalone bằng cách viết `it.only` thay vì `it`:

```
describe("Raises x to power n", function() {
  it("5 in the power of 1 equals 5", function() {
    assert.equal(pow(5, 1), 5);
  });

  // Mocha will run only this block
  it.only("5 in the power of 2 equals 25", function() {
    assert.equal(pow(5, 2), 25);
  });

  it("5 in the power of 3 equals 125", function() {
    assert.equal(pow(5, 3), 125);
  });
});
```
