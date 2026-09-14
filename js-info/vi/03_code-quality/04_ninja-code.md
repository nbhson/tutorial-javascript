# Ninja code

> Source: [https://javascript.info/ninja-code](https://javascript.info/ninja-code)

<!-- fetched: 2026-09-14 -->

> Học mà không suy nghĩ thì vất vã vô ích; suy nghĩ mà không học thì hiểm nguy.
>
> Khổng Tử (Luận Ngữ)

Các ninja lập trình viên trong quá khứ đã sử dụng những thủ thuật này để rèn luyện tư duy của người bảo trì code.

Các chuyên gia review code tìm kiếm chúng trong các bài test.

Nhà phát triển mới đôi khi còn sử dụng chúng tốt hơn cả ninja lập trình viên.

Hãy đọc kỹ và tìm hiểu bạn là ai – một ninja, một người mới, hay có lẽ là một người review code?

Phát hiện mỉa mai

Nhiều người cố gắng đi theo con đường ninja. Số ít thành công.

## [Cô đọng là linh hồn của sự tinh anh](#brevity-is-the-soul-of-wit)

Làm cho code càng ngắn càng tốt. Thể hiện bạn thông minh thế nào.

Hãy để các tính năng tinh tế của ngôn ngữ dẫn dắt bạn.

Ví dụ, hãy xem toán tử ternary `'?'` này:

```
// lấy từ một thư viện javascript nổi tiếng
i = i ? i < 0 ? Math.max(0, len + i) : i : 0;
```

Tuyệt, đúng không? Nếu bạn viết như vậy, một nhà phát triển khác tình cờ đọc dòng này và cố gắng hiểu giá trị của `i` sẽ có một khoảng thời gian vui vẻ. Sau đó đến tìm bạn, để xin câu trả lời.

Bảo họ rằng ngắn gọn luôn luôn tốt hơn. Hướng dẫn họ vào con đường ninja.

## [Biến một chữ cái](#one-letter-variables)

> Đạo giấu mình trong sự vô ngôn. Chỉ có Đạo mới bắt đầu tốt và kết thúc tốt.
>
> Lão Tử (Đạo Đức Kinh)

Một cách khác để code ngắn hơn là sử dụng tên biến một chữ cái ở mọi nơi. Như `a`, `b` hoặc `c`.

Một biến ngắn biến mất trong code như một ninja thực thụ trong rừng. Không ai có thể tìm thấy nó bằng cách "search" của trình soạn thảo. Và ngay cả khi ai đó tìm thấy, họ cũng không thể "giải mã" ý nghĩa của tên `a` hoặc `b`.

…Nhưng có một ngoại lệ. Một ninja thực sự sẽ không bao giờ sử dụng `i` làm bộ đếm trong vòng lặp `"for"`. Ở bất cứ đâu cũng được, nhưng không phải ở đây. Nhìn xung quanh, có nhiều chữ cái kỳ lạ hơn nhiều. Ví dụ, `x` hoặc `y`.

Một biến kỳ lạ làm bộ đếm vòng lặp đặc biệt tuyệt nếu thân vòng lặp chiếm 1-2 trang (làm cho nó dài hơn nếu bạn có thể). Sau đó, nếu ai đó nhìn sâu vào bên trong vòng lặp, họ sẽ không thể nhanh chóng tìm ra rằng biến tên `x` là bộ đếm vòng lặp.

## [Sử dụng viết tắt](#use-abbreviations)

Nếu quy tắc nhóm cấm sử dụng tên một chữ cái và tên mơ hồ – hãy viết tắt chúng, tạo các viết tắt.

Như thế này:

- `list` → `lst`.
- `userAgent` → `ua`.
- `browser` → `brsr`.
- …etc

Chỉ những người có trực giác thực sự tốt mới có thể hiểu được những tên như vậy. Hãy cố gắng viết tắt mọi thứ. Chỉ có người xứng đáng mới có thể duy trì việc phát triển code của bạn.

## [Bay cao. Trừu tượng hóa.](#soar-high-be-abstract)

> Cái vuông vĩ đại không có góc  
> Cái vessel vĩ đại cuối cùng hoàn thành,  
> Âm thanh vĩ đại là âm thanh tinh túy,  
> Hình ảnh vĩ đại không có hình dạng.
>
> Lão Tử (Đạo Đức Kinh)

Trong khi chọn tên, hãy cố gắng sử dụng từ trừu tượng nhất. Như `obj`, `data`, `value`, `item`, `elem` và vân vân.

- **Tên lý tưởng cho một biến là `data`.** Sử dụng nó ở bất cứ đâu bạn có thể. Đúng vậy, mọi biến đều chứa *data*, phải không?

  …Nhưng phải làm gì nếu `data` đã bị chiếm? Hãy thử `value`, nó cũng phổ quát. Sau tất cả, một biến cuối cùng có được một *value*.
- **Đặt tên cho một biến theo type của nó: `str`, `num`…**

  Hãy thử chúng. Một học viên trẻ có thể tự hỏi – những tên như vậy thực sự hữu ích cho một ninja sao? Đúng vậy, chúng hữu ích!

  Chắc chắn, tên biến vẫn có nghĩa gì đó. Nó nói rằng bên trong biến là gì: một string, một number hoặc thứ gì đó khác. Nhưng khi một người outsider cố gắng hiểu code, họ sẽ ngạc nhiên khi thấy rằng thực sự không có thông tin nào cả! Và cuối cùng sẽ thất bại trong việc sửa đổi code được suy nghĩ kỹ lưỡng của bạn.

  Type của giá trị dễ dàng tìm thấy bằng debugging. Nhưng ý nghĩa của biến là gì? String/number nào nó lưu trữ?

  Không có cách nào để tìm ra mà không có một sự thiền định tốt!
- **…Nhưng nếu không còn tên như vậy thì sao?** Chỉ cần thêm một số: `data1, item2, elem5`…

## [Kiểm tra sự chú ý](#attention-test)

Chỉ có một lập trình viên thực sự chú ý mới có thể hiểu code của bạn. Nhưng làm thế nào để kiểm tra điều đó?

**Một trong những cách – sử dụng các tên biến tương tự, như `date` và `data`.**

Trộn chúng ở bất cứ đâu bạn có thể.

Việc đọc nhanh code như vậy trở nên bất khả thi. Và khi có lỗi chính tả… Ummm… Chúng ta bị mắc kẹt lâu, đến lúc uống trà.

## [Synonyms thông minh](#smart-synonyms)

> Đạo mà có thể nói ra không phải là Đạo vĩnh cửu. Tên mà có thể đặt tên không phải là tên vĩnh cửu.
>
> Lão Tử (Đạo Đức Kinh)

Sử dụng các tên *tương tự* cho cùng một thứ làm cho cuộc sống thú vị hơn và thể hiện sự sáng tạo của bạn với công chúng.

Ví dụ, xem xét các tiền tố hàm. Nếu một hàm hiển thị thông báo trên màn hình – bắt đầu nó với `display...`, như `displayMessage`. Và sau đó nếu một hàm khác hiển thị trên màn hình thứ gì đó khác, như tên người dùng, bắt đầu nó với `show...` (như `showName`).

Gợi ý rằng có một sự khác biệt tinh tế giữa các hàm như vậy, trong khi không có sự khác biệt nào.

Làm một thỏa thuận với các ninja đồng nghiệp trong nhóm: nếu John bắt đầu "hiển thị" các hàm với `display...` trong code của anh ấy, thì Peter có thể sử dụng `render..`, và Ann – `paint...`. Hãy xem code trở nên thú vị và đa dạng hơn như thế nào.

…Và bây giờ là hat trick!

Đối với hai hàm có sự khác biệt quan trọng – hãy sử dụng cùng một tiền tố!

Ví dụ, hàm `printPage(page)` sẽ sử dụng máy in. Và hàm `printText(text)` sẽ đặt text lên màn hình. Hãy để một người đọc không quen thuộc suy nghĩ kỹ về hàm tên tương tự `printMessage`: "Nó đặt thông báo ở đâu? Đến máy in hay lên màn hình?". Để làm cho nó thực sự nổi bật, `printMessage(message)` nên output nó trong cửa sổ mới!

## [Tái sử dụng tên](#reuse-names)

> Một khi toàn thể được chia tách, các phần  
> cần tên.  
> Đã có đủ tên.  
> Một người phải biết khi nào nên dừng lại.
>
> Lão Tử (Đạo Đức Kinh)

Chỉ thêm biến mới khi thực sự cần thiết.

Thay vào đó, tái sử dụng các tên hiện có. Chỉ cần ghi các giá trị mới vào chúng.

Trong một hàm, hãy cố gắng chỉ sử dụng các biến được truyền như các tham số.

Điều đó sẽ làm cho nó thực sự khó xác định những gì chính xác đang có trong biến *giờ đây*. Và cũng như nó đến từ đâu. Mục đích là phát triển trực giác và trí nhớ của người đọc code. Một người có trực giác yếu sẽ phải phân tích code từng dòng và theo dõi những thay đổi qua mọi nhánh code.

**Biến thể nâng cao của phương pháp là thay thế giá trị một cách bí mật (!) bằng một thứ tương tự ở giữa một vòng lặp hoặc một hàm.**

Ví dụ:

```
function ninjaFunction(elem) {
  // 20 dòng code làm việc với elem

  elem = clone(elem);

  // 20 dòng nữa, giờ làm việc với clone của elem!
}
```

Một lập trình viên đồng nghiệp muốn làm việc với `elem` trong nửa sau của hàm sẽ ngạc nhiên… Chỉ trong quá trình debugging, sau khi xem xét code họ sẽ phát hiện ra rằng họ đang làm việc với một clone!

Thấy trong code thường xuyên. Cực kỳ hiệu quả ngay cả đối với một ninja có kinh nghiệm.

## [Dấu gạch dưới cho vui](#underscores-for-fun)

Đặt dấu gạch dưới `_` và `__` trước tên biến. Như `_name` hoặc `__value`. Sẽ tuyệt nếu chỉ có bạn biết ý nghĩa của chúng. Hoặc, tốt hơn, thêm chúng chỉ để vui, không có ý nghĩa đặc biệt nào cả. Hoặc các ý nghĩa khác nhau ở các nơi khác nhau.

Bạn giết hai chú thỏ bằng một viên đạn. Thứ nhất, code trở nên dài hơn và khó đọc hơn, và thứ hai, một nhà phát triển đồng nghiệp có thể dành nhiều thời gian cố gắng tìm ra ý nghĩa của các dấu gạch dưới.

Một ninja thông minh đặt dấu gạch dưới ở một chỗ của code và tránh chúng ở các nơi khác. Điều đó làm cho code giòn hơn nữa và tăng xác suất lỗi trong tương lai.

## [Thể hiện tình yêu của bạn](#show-your-love)

Hãy để mọi người thấy các entity của bạn vĩ đại thế nào! Các tên như `superElement`, `megaFrame` và `niceItem` chắc chắn sẽ soi sáng một người đọc.

Thật vậy, từ một phía, có điều gì đó được viết: `super..`, `mega..`, `nice..`. Nhưng từ phía kia – điều đó không mang lại chi tiết. Một người đọc có thể quyết định tìm kiếm ý nghĩa ẩn và thiền trong một hoặc hai giờ làm việc được trả lương của họ.

## [Che khuất các biến outer](#overlap-outer-variables)

> Khi ở trong ánh sáng, không thể thấy gì trong bóng tối.  
> Khi ở trong bóng tối, có thể thấy mọi thứ trong ánh sáng.
>
> Quan Âm Tử

Sử dụng cùng tên cho các biến bên trong và bên ngoài một hàm. Đơn giản vậy thôi. Không nỗ lực tạo tên mới.

```
let user = authenticateUser();

function render() {
  let user = anotherValue();
  ...
  ...nhiều dòng...
  ...
  ... // <-- một lập trình viên muốn làm việc với user ở đây và...
  ...
}
```

Một lập trình viên nhảy vào bên trong `render` có lẽ sẽ không nhận ra rằng có một biến cục bộ `user` đang shadow biến outer.

Sau đó họ sẽ cố gắng làm việc với `user` với giả định rằng đó là biến external, kết quả của `authenticateUser()`… Cái bẫy đã giăng! Xin chào, debugger…

## [Side-effects ở mọi nơi!](#side-effects-everywhere)

Có những hàm trông như thể chúng không thay đổi gì. Như `isReady()`, `checkPermission()`, `findTags()`… Chúng được giả định là thực hiện các phép tính, tìm và trả về data, mà không thay đổi bất cứ thứ gì bên ngoài chúng. Nói cách khác, không có "side-effects".

**Một thủ thuật đẹp thực sự là thêm một hành động "hữu ích" vào chúng, bên cạnh nhiệm vụ chính.**

Biểu hiện của sự ngạc nhiên hoang mang trên khuôn mặt của đồng nghiệp khi họ thấy một hàm tên `is..`, `check..` hoặc `find...` đang thay đổi thứ gì đó – chắc chắn sẽ mở rộng ranh giới lý trí của bạn.

**Một cách khác để gây bất ngờ là trả về một kết quả không tiêu chuẩn.**

Thể hiện tư duy độc đáo của bạn! Hãy để gọi `checkPermission` trả về không phải `true/false`, mà là một object phức tạp với kết quả của phép kiểm tra.

Những nhà phát triển cố gắng viết `if (checkPermission(..))`, sẽ tự hỏi tại sao nó không hoạt động. Bảo họ: "Đọc docs!". Và đưa bài viết này.

## [Hàm mạnh mẽ!](#powerful-functions)

> Đạo lớn chảy khắp nơi,  
> cả sang trái và sang phải.
>
> Lão Tử (Đạo Đức Kinh)

Đừng giới hạn hàm bằng những gì được viết trong tên của nó. Hãy rộng hơn.

Ví dụ, một hàm `validateEmail(email)` có thể (bên cạnh việc kiểm tra email có đúng không) hiển thị thông báo lỗi và yêu cầu nhập lại email.

Các hành động bổ sung không nên rõ ràng từ tên hàm. Một ninja coder thực thụ sẽ làm cho chúng không rõ ràng từ code.

**Việc kết hợp nhiều hành động thành một bảo vệ code của bạn khỏi việc tái sử dụng.**

Hãy tưởng tượng, một nhà phát triển khác chỉ muốn kiểm tra email, và không xuất bất kỳ thông báo nào. Hàm `validateEmail(email)` của bạn làm cả hai sẽ không phù hợp với họ. Vì vậy, họ sẽ không làm phiền Meditation của bạn bằng cách hỏi bất cứ điều gì về nó.

## [Tổng kết](#summary)

Tất cả "lời khuyên" ở trên là từ code thực tế… Đôi khi, được viết bởi các nhà phát triển có kinh nghiệm. Có lẽ thậm chí còn có kinh nghiệm hơn bạn ;)

- Hãy làm theo một số trong số chúng, và code của bạn sẽ trở nên đầy bất ngờ.
- Làm theo nhiều trong số chúng, và code của bạn sẽ trở nên thực sự của bạn, không ai muốn thay đổi nó.
- Làm theo tất cả, và code của bạn sẽ trở thành một bài học quý giá cho các nhà phát triển trẻ đang tìm kiếm sự khai sáng.
