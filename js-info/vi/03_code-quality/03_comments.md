# Comments (Nhận xét)

> Source: [https://javascript.info/comments](https://javascript.info/comments)

<!-- fetched: 2026-09-14 -->

Như chúng ta đã biết từ chương [Cấu trúc code](/structure), comments có thể là single-line: bắt đầu với `//` và multiline: `/* ... */`.

Chúng ta thường sử dụng chúng để mô tả cách code hoạt động và tại sao.

Thoạt nhìn, comments có vẻ rõ ràng, nhưng những người mới lập trình thường sử dụng chúng sai cách.

## [Comments xấu](#bad-comments)

Người mới có xu hướng sử dụng comments để giải thích "đang xảy ra gì trong code". Như thế này:

```
// Code này sẽ làm điều này (...) và điều kia (...)
// ...và không ai biết còn gì nữa...
very;
complex;
code;
```

Nhưng trong code tốt, lượng comments "giải thích" như vậy nên tối thiểu. Nghiêm túc mà nói, code nên dễ hiểu mà không cần chúng.

Có một quy tắc tuyệt vời về điều đó: "Nếu code không rõ ràng đến mức cần một comment, thì có lẽ nên viết lại thay thế".

### [Công thức: trích xuất thành hàm](#recipe-factor-out-functions)

Đôi khi có lợi khi thay thế một đoạn code bằng một hàm, như ở đây:

```
function showPrimes(n) {
  nextPrime:
  for (let i = 2; i < n; i++) {

    // kiểm tra xem i có phải là số nguyên tố không
    for (let j = 2; j < i; j++) {
      if (i % j == 0) continue nextPrime;
    }

    alert(i);
  }
}
```

Biến thể tốt hơn, với hàm được trích xuất `isPrime`:

```
function showPrimes(n) {

  for (let i = 2; i < n; i++) {
    if (!isPrime(i)) continue;

    alert(i);
  }
}

function isPrime(n) {
  for (let i = 2; i < n; i++) {
    if (n % i == 0) return false;
  }

  return true;
}
```

Bây giờ chúng ta có thể hiểu code một cách dễ dàng. Bản thân hàm trở thành comment. Loại code như vậy được gọi là *self-descriptive*.

### [Công thức: tạo hàm](#recipe-create-functions)

Và nếu chúng ta có một "tờ code" dài như thế này:

```
// ở đây chúng ta thêm whiskey
for(let i = 0; i < 10; i++) {
  let drop = getWhiskey();
  smell(drop);
  add(drop, glass);
}

// ở đây chúng ta thêm nước ép
for(let t = 0; t < 3; t++) {
  let tomato = getTomato();
  examine(tomato);
  let juice = press(tomato);
  add(juice, glass);
}

// ...
```

Thì có lẽ biến thể tốt hơn là refactor nó thành các hàm như:

```
addWhiskey(glass);
addJuice(glass);

function addWhiskey(container) {
  for(let i = 0; i < 10; i++) {
    let drop = getWhiskey();
    //...
  }
}

function addJuice(container) {
  for(let t = 0; t < 3; t++) {
    let tomato = getTomato();
    //...
  }
}
```

Một lần nữa, chính các hàm cho biết những gì đang xảy ra. Không có gì cần comment. Và cấu trúc code cũng tốt hơn khi được chia ra. Rõ ràng mỗi hàm làm gì, nhận gì và trả về gì.

Trong thực tế, chúng ta không thể tránh hoàn toàn các comment "giải thích". Có những thuật toán phức tạp. Và có những "mẹo" thông minh cho mục đích tối ưu hóa. Nhưng nói chung chúng ta nên cố gắng giữ code đơn giản và self-descriptive.

## [Comments tốt](#good-comments)

Vậy, comments giải thích thường là xấu. Comments nào là tốt?

Mô tả kiến trúc
:   Cung cấp cái nhìn tổng quan cấp cao về các component, cách chúng tương tác, luồng điều khiển trong các tình huống khác nhau... Nói ngắn gọn – tầm nhìn tổng thể của code. Có một ngôn ngữ đặc biệt [UML](http://wikipedia.org/wiki/Unified_Modeling_Language) để xây dựng sơ đồ kiến trúc cấp cao giải thích code. Nhất định nên học.

Ghi chú tài liệu cho các tham số hàm và cách sử dụng
:   Có một cú pháp đặc biệt [JSDoc](http://en.wikipedia.org/wiki/JSDoc) để tài liệu hóa một hàm: cách sử dụng, tham số, giá trị trả về.

Ví dụ:

```
/**
 * Trả về x nâng lên lũy thừa n.
 *
 * @param {number} x Số cần nâng.
 * @param {number} n Lũy thừa, phải là số tự nhiên.
 * @return {number} x nâng lên lũy thừa n.
 */
function pow(x, n) {
  ...
}
```

Những comments như vậy cho phép chúng ta hiểu mục đích của hàm và sử dụng nó đúng cách mà không cần xem trong code của nó.

Nhân tiện, nhiều trình soạn thảo như [WebStorm](https://www.jetbrains.com/webstorm/) cũng có thể hiểu chúng và sử dụng chúng để cung cấp autocomplete và một số kiểm tra code tự động.

Ngoài ra, có các công cụ như [JSDoc 3](https://github.com/jsdoc/jsdoc) có thể tạo HTML-documentation từ các comment. Bạn có thể đọc thêm thông tin về JSDoc tại <https://jsdoc.app>.

Tại sao nhiệm vụ được giải quyết theo cách này?
:   Những gì được viết quan trọng. Nhưng những gì *không* được viết thậm chí còn quan trọng hơn để hiểu những gì đang xảy ra. Tại sao nhiệm vụ được giải quyết chính xác theo cách này? Code không đưa ra câu trả lời.

    Nếu có nhiều cách để giải quyết nhiệm vụ, tại sao lại là cách này? Đặc biệt khi nó không phải là cách rõ ràng nhất.

    Không có những comments như vậy, tình huống sau đây có thể xảy ra:

    1. Bạn (hoặc đồng nghiệp của bạn) mở code được viết từ một thời điểm nào đó, và thấy rằng nó là "suboptimal".
    2. Bạn nghĩ: "Tôi đã ngu ngốc thế nào khi đó, và tôi thông minh thế nào bây giờ", và viết lại bằng biến thể "rõ ràng và đúng đắn hơn".
    3. …Sự thúc đẩy để viết lại là tốt. Nhưng trong quá trình bạn thấy rằng giải pháp "rõ ràng hơn" thực sự thiếu sót. Bạn thậm chí còn nhớ mơ hồ tại sao, vì bạn đã thử nó từ lâu. Bạn revert về biến thể đúng, nhưng thời gian đã bị lãng phí.

    Comments giải thích giải pháp rất quan trọng. Chúng giúp tiếp tục phát triển theo cách đúng đắn.

Có tính năng tinh tế nào trong code? Chúng được sử dụng ở đâu?
:   Nếu code có gì đó tinh tế và phản trực giác, nó nhất định đáng để comment.

## [Tổng kết](#summary)

Một dấu hiệu quan trọng của một nhà phát triển giỏi là comments: sự hiện diện của chúng và thậm chí cả sự vắng mặt của chúng.

Comments tốt cho phép chúng ta duy trì code tốt, quay lại sau một khoảng thời gian và sử dụng nó hiệu quả hơn.

**Comment những điều này:**

- Kiến trúc tổng thể, tầm nhìn cấp cao.
- Cách sử dụng hàm.
- Các giải pháp quan trọng, đặc biệt khi không rõ ràng ngay lập tức.

**Tránh comments:**

- Những cái nói "code hoạt động thế nào" và "nó làm gì".
- Chỉ đặt chúng nếu không thể làm cho code đơn giản và self-descriptive đến mức không cần chúng.

Comments cũng được sử dụng cho các công cụ auto-documenting như JSDoc3: chúng đọc chúng và tạo HTML-docs (hoặc docs ở định dạng khác).
