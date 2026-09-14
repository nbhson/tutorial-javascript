# Polyfills và transpilers

> Source: [https://javascript.info/polyfills](https://javascript.info/polyfills)

<!-- fetched: 2026-09-14 -->

Ngôn ngữ JavaScript liên tục phát triển. Các đề xuất mới cho ngôn ngữ xuất hiện thường xuyên, chúng được phân tích và, nếu được coi là đáng giá, được bổ sung vào danh sách tại <https://tc39.github.io/ecma262/> và sau đó tiến tới [specification](https://www.ecma-international.org/publications-and-standards/standards/ecma-262/).

Các nhóm đứng sau các JavaScript engine có ý tưởng riêng về những gì cần implement trước. Họ có thể quyết định implement các đề xuất đang trong draft và hoãn những thứ đã có trong spec, vì chúng ít thú vị hơn hoặc đơn giản khó thực hiện hơn.

Vì vậy, khá phổ biến cho một engine chỉ implement một phần của standard.

Một trang tốt để xem trạng thái hiện tại của support cho các tính năng ngôn ngữ là <https://compat-table.github.io/compat-table/es6/> (nó khá lớn, chúng ta còn nhiều thứ để học).

Là các lập trình viên, chúng ta muốn sử dụng các tính năng mới nhất. Càng nhiều thứ tốt – càng tốt!

Mặt khác, làm thế nào để làm cho code hiện đại của chúng ta hoạt động trên các engine cũ không hiểu các tính năng gần đây?

Có hai công cụ cho việc đó:

1. Transpilers.
2. Polyfills.

Ở đây, trong chương này, mục đích của chúng ta là nắm được cách chúng hoạt động, và vị trí của chúng trong web development.

## [Transpilers](#transpilers)

Một [transpiler](https://en.wikipedia.org/wiki/Source-to-source_compiler) là một piece software đặc biệt dịch source code sang source code khác. Nó có thể parse ("đọc và hiểu") code hiện đại và viết lại nó bằng các construct cú pháp cũ hơn, để nó cũng hoạt động trên các engine lỗi thời.

Ví dụ, JavaScript trước năm 2020 không có "nullish coalescing operator" `??`. Vì vậy, nếu một visitor sử dụng trình duyệt lỗi thời, nó có thể không hiểu code như `height = height ?? 100`.

Một transpiler sẽ phân tích code của chúng ta và viết lại `height ?? 100` thành `(height !== undefined && height !== null) ? height : 100`.

```
// trước khi chạy transpiler
height = height ?? 100;

// sau khi chạy transpiler
height = (height !== undefined && height !== null) ? height : 100;
```

Giờ code đã viết lại phù hợp cho các engine JavaScript cũ.

Thông thường, một nhà phát triển chạy transpiler trên máy tính của họ, sau đó deploy code đã transpile lên server.

Nói về tên, [Babel](https://babeljs.io) là một trong những transpilers nổi tiếng nhất.

Các hệ thống build project hiện đại, như [webpack](https://webpack.js.org/), cung cấp một cách để chạy transpiler tự động trên mỗi thay đổi code, vì vậy rất dễ tích hợp vào quy trình phát triển.

## [Polyfills](#polyfills)

Các tính năng ngôn ngữ mới có thể bao gồm không chỉ các construct cú pháp và operators, mà còn các hàm built-in.

Ví dụ, `Math.trunc(n)` là một hàm "cắt bỏ" phần thập phân của một số, ví dụ `Math.trunc(1.23)` trả về `1`.

Trong một số (rất lỗi thời) engine JavaScript, không có `Math.trunc`, vì vậy code như vậy sẽ fail.

Vì chúng ta đang nói về các hàm mới, không phải thay đổi cú pháp, không cần transpile gì ở đây. Chúng ta chỉ cần khai báo hàm bị thiếu.

Một script cập nhật/thêm các hàm mới được gọi là "polyfill". Nó "điền vào" khoảng trống và thêm các implementation bị thiếu.

Đối với trường hợp đặc biệt này, polyfill cho `Math.trunc` là một script implement nó, như thế này:

```
if (!Math.trunc) { // nếu không có hàm như vậy
  // implement nó
  Math.trunc = function(number) {
    // Math.ceil và Math.floor tồn tại ngay cả trong các engine JavaScript cổ xưa
    // chúng được cover sau trong tutorial
    return number < 0 ? Math.ceil(number) : Math.floor(number);
  };
}
```

JavaScript là một ngôn ngữ highly dynamic. Các script có thể thêm/sửa đổi bất kỳ hàm nào, ngay cả các hàm built-in.

Một thư viện polyfill thú vị là [core-js](https://github.com/zloirock/core-js), hỗ trợ một phạm vi rộng các tính năng và cho phép bạn chỉ include những thứ bạn cần.

## [Tổng kết](#summary)

Trong chương này chúng ta muốn khuyến khích bạn nghiên cứu các tính năng ngôn ngữ hiện đại và thậm chí "bleeding-edge", ngay cả khi chúng chưa được support tốt bởi các engine JavaScript.

Chỉ đừng quên sử dụng transpiler (nếu sử dụng cú pháp hoặc operators hiện đại) và polyfills (để thêm các hàm có thể bị thiếu). Chúng sẽ đảm bảo rằng code hoạt động.

Ví dụ, sau này khi bạn quen thuộc với JavaScript, bạn có thể setup một hệ thống build code dựa trên [webpack](https://webpack.js.org/) với plugin [babel-loader](https://github.com/babel/babel-loader).

Các nguồn tài liệu tốt hiển thị trạng thái hiện tại của support cho các tính năng khác nhau:

- <https://compat-table.github.io/compat-table/es6/> – cho JavaScript thuần túy.
- <https://caniuse.com/> – cho các hàm liên quan đến trình duyệt.

P.S. Google Chrome thường cập nhật nhất về các tính năng ngôn ngữ, hãy thử nó nếu demo trong tutorial fail. Hầu hết các demo trong tutorial hoạt động với bất kỳ trình duyệt hiện đại nào.
