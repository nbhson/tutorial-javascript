# Cookies và document.cookie

> Source: [https://javascript.info/cookie](https://javascript.info/cookie)

<!-- fetched: 2026-09-14 -->

Cookies là những chuỗi dữ liệu nhỏ được lưu trữ trực tiếp trong trình duyệt. Chúng là một phần của giao thức HTTP, được định nghĩa bởi đặc tả [RFC 6265](https://tools.ietf.org/html/rfc6265).

Cookies thường được đặt bởi máy chủ web qua HTTP header `Set-Cookie` trong phản hồi. Sau đó, trình duyệt tự động thêm chúng vào (gần như) mọi request tới cùng domain bằng HTTP header `Cookie`.

Một trong những trường hợp sử dụng phổ biến nhất là xác thực:

1. Khi đăng nhập, server sử dụng HTTP header `Set-Cookie` trong phản hồi để đặt một cookie chứa "định danh phiên" duy nhất.
2. Lần tiếp theo khi request được gửi tới cùng domain, trình duyệt gửi cookie qua mạng bằng HTTP header `Cookie`.
3. Vì vậy, server biết ai đã thực hiện request.

Chúng ta cũng có thể truy cập cookies từ trình duyệt bằng thuộc tính `document.cookie`.

Có nhiều điều đáng chú ý về cookies và các thuộc tính của chúng. Trong chương này, chúng ta sẽ tìm hiểu chi tiết về chúng.

## [Đọc từ document.cookie](#reading-from-document-cookie)

Trình duyệt của bạn có lưu trữ cookie nào từ trang web này không? Hãy cùng xem:

```
// At javascript.info, we use Google Analytics for statistics,
// so there should be some cookies
alert( document.cookie ); // cookie1=value1; cookie2=value2;...
```

Giá trị của `document.cookie` gồm các cặp `name=value`, ngăn cách bằng `;`. Mỗi cặp là một cookie riêng biệt.

Để tìm một cookie cụ thể, chúng ta có thể tách `document.cookie` bằng `;`, sau đó tìm đúng tên. Chúng ta có thể dùng biểu thức chính quy hoặc các phương thức mảng để làm điều đó.

Chúng ta để lại việc này như một bài tập cho người đọc. Ngoài ra, ở cuối chương, bạn sẽ tìm thấy các hàm tiện ích để thao tác với cookies.

## [Viết vào document.cookie](#writing-to-document-cookie)

Chúng ta có thể viết vào `document.cookie`. Nhưng nó không phải là thuộc tính dữ liệu, mà là [accessor (getter/setter)](/property-accessors). Việc gán giá trị cho nó được xử lý đặc biệt.

**Thao tác viết vào `document.cookie` chỉ cập nhật cookie được nêu trong nó và không đụng chạm đến các cookie khác.**

Ví dụ, lệnh gọi này đặt một cookie với tên `user` và giá trị `John`:

```
document.cookie = "user=John"; // update only cookie named 'user'
alert(document.cookie); // show all cookies
```

Nếu bạn chạy, bạn có thể thấy nhiều cookie. Đó là vì thao tác `document.cookie=` không ghi đè toàn bộ cookies. Nó chỉ đặt cookie `user` được nêu.

Về mặt kỹ thuật, tên và giá trị có thể chứa bất kỳ ký tự nào. Để giữ định dạng hợp lệ, chúng nên được escape bằng hàm `encodeURIComponent` có sẵn:

```
// special characters (spaces) need encoding
let name = "my name";
let value = "John Smith"

// encodes the cookie as my%20name=John%20Smith
document.cookie = encodeURIComponent(name) + '=' + encodeURIComponent(value);

alert(document.cookie); // ...; my%20name=John%20Smith
```

Hạn chế

Có một vài hạn chế:

- Bạn chỉ có thể đặt/cập nhật một cookie tại một thời điểm bằng `document.cookie`.
- Cặp `name=value`, sau `encodeURIComponent`, không nên vượt quá 4KB. Vì vậy chúng ta không thể lưu bất kỳ thứ gì quá lớn trong cookie.
- Tổng số cookie trên mỗi domain bị giới hạn ở khoảng 20+, giới hạn cụ thể phụ thuộc vào trình duyệt.

Cookies có nhiều thuộc tính, nhiều trong số đó quan trọng và nên được đặt.

Các thuộc tính được liệt kê sau `key=value`, ngăn cách bằng `;`, như sau:

```
document.cookie = "user=John; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT"
```

## [domain](#domain)

- **`domain=site.com`**

Domain định nghĩa nơi cookie có thể được truy cập. Tuy nhiên, trên thực tế có những hạn chế. Chúng ta không thể đặt bất kỳ domain nào.

**Không có cách nào để cookie có thể được truy cập từ domain cấp 2 khác, vì vậy `other.com` sẽ không bao giờ nhận được cookie được đặt tại `site.com`.**

Đó là một hạn chế bảo mật, cho phép chúng ta lưu dữ liệu nhạy cảm trong cookies chỉ nên có sẵn trên một trang web.

Mặc định, cookie chỉ có thể được truy cập tại domain đã đặt nó.

Vui lòng lưu ý, mặc định, cookie không được chia sẻ với subdomain, chẳng hạn như `forum.site.com`.

```
// if we set a cookie at site.com website...
document.cookie = "user=John"

// ...we won't see it at forum.site.com
alert(document.cookie); // no user
```

…Nhưng điều này có thể thay đổi. Nếu chúng ta muốn cho phép các subdomain như `forum.site.com` nhận cookie được đặt tại `site.com`, điều đó hoàn toàn khả thi.

Để làm được điều đó, khi đặt cookie tại `site.com`, chúng ta nên đặt rõ thuộc tính `domain` thành domain gốc: `domain=site.com`. Khi đó tất cả subdomains sẽ thấy cookie đó.

Ví dụ:

```
// at site.com
// make the cookie accessible on any subdomain *.site.com:
document.cookie = "user=John; domain=site.com"

// later

// at forum.site.com
alert(document.cookie); // has cookie user=John
```

Cú pháp cũ

Về mặt lịch sử, `domain=.site.com` (với dấu chấm trước `site.com`) trước đây hoạt động theo cách tương tự, cho phép truy cập cookie từ các subdomain. Dấu chấm đầu trong tên domain bây giờ bị bỏ qua, nhưng một số trình duyệt có thể từ chối đặt cookie chứa các dấu chấm như vậy.

Tóm lại, thuộc tính `domain` cho phép cookie được truy cập tại các subdomain.

## [path](#path)

- **`path=/mypath`**

Tiền tố path trong URL phải là tuyệt đối. Nó khiến cookie có thể được truy cập cho các trang dưới path đó. Mặc định, đó là path hiện tại.

Nếu cookie được đặt với `path=/admin`, nó hiển thị trên các trang `/admin` và `/admin/something`, nhưng không phải tại `/home`, `/home/admin` hoặc `/`.

Thông thường, chúng ta nên đặt `path` thành gốc: `path=/` để cookie có thể được truy cập từ tất cả trang của website. Nếu thuộc tính này không được đặt, giá trị mặc định được tính bằng [phương pháp này](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#path_default_value).

## [expires, max-age](#expires-max-age)

Mặc định, nếu cookie không có một trong các thuộc tính này, nó sẽ biến mất khi trình duyệt/cửa sổ tab đóng lại. Những cookie như vậy được gọi là "session cookies".

Để cookie tồn tại khi trình duyệt đóng, chúng ta có thể đặt thuộc tính `expires` hoặc `max-age`. `max-age` có ưu tiên cao hơn nếu cả hai đều được đặt.

- **`expires=Tue, 19 Jan 2038 03:14:07 GMT`**

Ngày hết hạn của cookie định nghĩa thời điểm trình duyệt sẽ tự động xóa nó (theo múi giờ của trình duyệt).

Ngày tháng phải đúng định dạng này, trong múi giờ GMT. Chúng ta có thể dùng `date.toUTCString` để lấy nó. Ví dụ, chúng ta có thể đặt cookie hết hạn sau 1 ngày:

```
// +1 day from now
let date = new Date(Date.now() + 86400e3);
date = date.toUTCString();
document.cookie = "user=John; expires=" + date;
```

Nếu chúng ta đặt `expires` thành ngày trong quá khứ, cookie sẽ bị xóa.

- **`max-age=3600`**

Đây là lựa chọn thay thế cho `expires` và chỉ định thời gian hết hạn của cookie tính bằng giây từ hiện tại.

Nếu đặt bằng 0 hoặc giá trị âm, cookie sẽ bị xóa:

```
// cookie will die in +1 hour from now
document.cookie = "user=John; max-age=3600";

// delete cookie (let it expire right now)
document.cookie = "user=John; max-age=0";
```

## [secure](#secure)

- **`secure`**

Cookie chỉ nên được truyền qua HTTPS.

**Mặc định, nếu chúng ta đặt cookie tại `http://site.com`, thì nó cũng xuất hiện tại `https://site.com` và ngược lại.**

Nghĩa là, cookies dựa trên domain, chúng không phân biệt giữa các giao thức.

Với thuộc tính này, nếu cookie được đặt bởi `https://site.com`, thì nó không xuất hiện khi cùng trang web đó được truy cập bằng HTTP, như `http://site.com`. Vì vậy, nếu cookie chứa nội dung nhạy cảm không bao giờ nên gửi qua HTTP không mã hóa, cờ `secure` là điều đúng đắn.

```
// assuming we're on https:// now
// set the cookie to be secure (only accessible over HTTPS)
document.cookie = "user=John; secure";
```

## [samesite](#samesite)

Đây là thuộc tính bảo mật khác `samesite`. Nó được thiết kế để bảo vệ khỏi các cuộc tấn công XSRF (cross-site request forgery).

Để hiểu cách nó hoạt động và khi nào hữu ích, hãy xem xét các cuộc tấn công XSRF.

### [Tấn công XSRF](#xsrf-attack)

Hãy tưởng tượng bạn đã đăng nhập vào trang web `bank.com`. Nghĩa là: bạn có cookie xác thực từ trang đó. Trình duyệt của bạn gửi nó đến `bank.com` với mỗi request để nó nhận diện bạn và thực hiện tất cả các giao dịch tài chính nhạy cảm.

Giờ đây, khi đang duyệt web trong một cửa sổ khác, bạn vô tình đến trang web khác `evil.com`. Trang đó có mã JavaScript gửi một form `<form action="https://bank.com/pay">` đến `bank.com` với các trường khởi tạo giao dịch chuyển tiền vào tài khoản của hacker.

Trình duyệt gửi cookies mỗi khi bạn truy cập trang `bank.com`, kể cả khi form được gửi từ `evil.com`. Vì vậy, ngân hàng nhận diện bạn và thực hiện thanh toán.

![](/article/cookie/cookie-xsrf.svg)

Đây là cuộc tấn công "Cross-Site Request Forgery" (viết tắt là XSRF).

Các ngân hàng thực tế đương nhiên được bảo vệ khỏi điều này. Tất cả các form được tạo bởi `bank.com` đều có một trường đặc biệt, gọi là "token bảo vệ XSRF", mà trang độc hại không thể tạo ra hoặc trích xuất từ trang xa. Nó có thể gửi form ở đó, nhưng không thể nhận lại dữ liệu. Trang `bank.com` kiểm tra token như vậy trong mọi form nó nhận được.

Tuy nhiên, việc bảo vệ như vậy mất thời gian để triển khai. Chúng ta cần đảm bảo rằng mọi form đều có trường token yêu cầu, và cũng phải kiểm tra tất cả các request.

### [Sử dụng thuộc tính samesite của cookie](#use-cookie-samesite-attribute)

Thuộc tính `samesite` của cookie cung cấp một cách khác để bảo vệ khỏi các cuộc tấn công như vậy, mà (về mặt lý thuyết) không nên yêu cầu "token bảo vệ xsrf".

Nó có hai giá trị có thể:

- **`samesite=strict`**

Cookie với `samesite=strict` không bao giờ được gửi nếu người dùng đến từ bên ngoài cùng trang web.

Nói cách khác, bất kể người dùng theo dõi link từ email của họ, gửi form từ `evil.com`, hoặc thực hiện bất kỳ thao tác nào có nguồn gốc từ domain khác, cookie sẽ không được gửi.

Nếu cookie xác thực có thuộc tính `samesite=strict`, thì cuộc tấn công XSRF không có cơ hội thành công, vì việc gửi từ `evil.com` diễn ra mà không có cookies. Vì vậy `bank.com` sẽ không nhận diện được người dùng và không tiếp tục thanh toán.

Bảo vệ khá tin cậy. Chỉ các thao tác đến từ `bank.com` mới gửi cookie `samesite=strict`, chẳng hạn như gửi form từ trang khác tại `bank.com`.

Tuy nhiên, có một bất tiện nhỏ.

Khi người dùng theo dõi link hợp lệ đến `bank.com`, chẳng hạn như từ ghi chú của họ, họ sẽ ngạc nhiên khi thấy `bank.com` không nhận ra họ. Đúng vậy, cookie `samesite=strict` không được gửi trong trường hợp đó.

Chúng ta có thể khắc phục bằng cách sử dụng hai cookies: một cho "nhận diện chung chung", chỉ để nói: "Xin chào, John", và cái khác cho các thao tác thay đổi dữ liệu với `samesite=strict`. Khi đó, người đến từ bên ngoài trang web sẽ thấy lời chào mừng, nhưng thanh toán phải được khởi tạo từ trang web ngân hàng để cookie thứ hai được gửi.

- **`samesite=lax` (tương đương `samesite` không có giá trị)**

Cách tiếp cận linh hoạt hơn, cũng bảo vệ khỏi XSRF và không phá vỡ trải nghiệm người dùng.

Chế độ Lax, giống như `strict`, cấm trình duyệt gửi cookies khi đến từ bên ngoài trang web, nhưng thêm một ngoại lệ.

Cookie `samesite=lax` được gửi nếu cả hai điều kiện sau đúng:

1. HTTP method là "an toàn" (ví dụ: GET, nhưng không phải POST).

   Danh sách đầy đủ các HTTP method an toàn nằm trong [đặc tả RFC7231](https://tools.ietf.org/html/rfc7231#section-4.2.1). Đây là các method nên dùng để đọc, không phải để ghi dữ liệu. Chúng không được thực hiện bất kỳ thao tác nào thay đổi dữ liệu. Theo link luôn là GET, method an toàn.
2. Thao tác thực hiện điều hướng cấp cao nhất (đổi URL trong thanh địa chỉ trình duyệt).

   Điều này thường đúng, nhưng nếu điều hướng được thực hiện trong `<iframe>`, thì không phải cấp cao nhất. Ngoài ra, các phương thức JavaScript cho request mạng không thực hiện bất kỳ điều hướng nào.

Vì vậy, thứ mà `samesite=lax` làm, là cho phép thao tác phổ biến nhất "đi tới URL" có cookies. Ví dụ mở link website từ ghi chú thỏa mãn các điều kiện này.

Nhưng bất kỳ điều gì phức tạp hơn, như request mạng từ trang web khác hoặc gửi form, sẽ mất cookies.

Nếu điều đó ổn với bạn, thì thêm `samesite=lax` có thể sẽ không phá vỡ trải nghiệm người dùng và thêm bảo vệ.

Nhìn chung, `samesite` là thuộc tính tuyệt vời.

Có một nhược điểm:

- `samesite` bị bỏ qua (không được hỗ trợ) bởi các trình duyệt rất cũ, khoảng năm 2017.

**Vì vậy nếu chúng ta chỉ dựa vào `samesite` để cung cấp bảo vệ, thì các trình duyệt cũ sẽ dễ bị tổn thương.**

Nhưng chúng ta có thể dùng `samesite` cùng với các biện pháp bảo vệ khác, như token xsrf, để thêm một lớp phòng thủ và sau đó, trong tương lai, khi các trình duyệt cũ biến mất, chúng ta có thể bỏ token xsrf.

## [httpOnly](#httponly)

Thuộc tính này không liên quan gì đến JavaScript, nhưng chúng ta phải đề cập để hoàn chỉnh.

Máy chủ web sử dụng header `Set-Cookie` để đặt cookie. Ngoài ra, nó cũng có thể đặt thuộc tính `httpOnly`.

Thuộc tính này cấm bất kỳ truy cập JavaScript nào đến cookie. Chúng ta không thể thấy cookie như vậy hay thao tác với nó bằng `document.cookie`.

Điều này được dùng như một biện pháp phòng ngừa, để bảo vệ khỏi một số cuộc tấn công khi hacker tiêm mã JavaScript của riêng anh ta vào trang và chờ người dùng truy cập trang đó. Theo lý thuyết, điều đó không nên có thể xảy ra, hacker không nên có thể tiêm mã của họ vào trang web của chúng ta, nhưng có thể có lỗi cho phép họ làm vậy.

Thông thường, nếu điều đó xảy ra, và người dùng truy cập trang web có mã JavaScript của hacker, thì mã đó được thực thi và truy cập được `document.cookie` với cookies của người dùng chứa thông tin xác thực. Đó là điều tồi tệ.

Nhưng nếu cookie là `httpOnly`, thì `document.cookie` không thấy nó, vì vậy nó được bảo vệ.

## [Phụ lục: Các hàm cookie](#appendix-cookie-functions)

Đây là một bộ hàm nhỏ để làm việc với cookies, tiện lợi hơn việc chỉnh sửa thủ công `document.cookie`.

Có nhiều thư viện cookie cho mục đích đó, vì vậy đây chỉ mang tính minh họa. Hoàn toàn hoạt động được.

### [getCookie(name)](#getcookie-name)

Cách ngắn nhất để truy cập cookie là sử dụng [biểu thức chính quy](/regular-expressions).

Hàm `getCookie(name)` trả về cookie với `name` được cho:

```
// returns the cookie with the given name,
// or undefined if not found
function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
```

Ở đây `new RegExp` được tạo động, để khớp với `; name=<value>`.

Vui lòng lưu ý rằng giá trị cookie được mã hóa, vì vậy `getCookie` sử dụng hàm `decodeURIComponent` có sẵn để giải mã.

### [setCookie(name, value, attributes)](#setcookie-name-value-attributes)

Đặt `name` của cookie thành `value` được cho, mặc định là `path=/` (có thể chỉnh sửa để thêm các giá trị mặc định khác):

```
function setCookie(name, value, attributes = {}) {

  attributes = {
    path: '/',
    // add other defaults here if necessary
    ...attributes
  };

  if (attributes.expires instanceof Date) {
    attributes.expires = attributes.expires.toUTCString();
  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let attributeKey in attributes) {
    updatedCookie += "; " + attributeKey;
    let attributeValue = attributes[attributeKey];
    if (attributeValue !== true) {
      updatedCookie += "=" + attributeValue;
    }
  }

  document.cookie = updatedCookie;
}

// Example of use:
setCookie('user', 'John', {secure: true, 'max-age': 3600});
```

### [deleteCookie(name)](#deletecookie-name)

Để xóa cookie, chúng ta có thể gọi nó với ngày hết hạn âm:

```
function deleteCookie(name) {
  setCookie(name, "", {
    'max-age': -1
  })
}
```

Cập nhật hoặc xóa phải sử dụng cùng path và domain

Vui lòng lưu ý: khi chúng ta cập nhật hoặc xóa cookie, chúng ta nên sử dụng chính xác cùng thuộc tính path và domain như khi đặt nó.

Gộp lại: [cookie.js](/article/cookie/cookie.js).

## [Phụ lục: Cookies bên thứ ba](#appendix-third-party-cookies)

Cookie được gọi là "bên thứ ba" nếu nó được đặt bởi domain khác với trang mà người dùng đang truy cập.

Ví dụ:

1. Một trang tại `site.com` tải banner từ trang web khác: `<img src="https://ads.com/banner.png">`.
2. Cùng với banner, máy chủ xa tại `ads.com` có thể đặt header `Set-Cookie` với cookie như `id=1234`. Cookie đó đến từ domain `ads.com`, và chỉ hiển thị tại `ads.com`:

   ![](/article/cookie/cookie-third-party.svg)
3. Lần tiếp theo khi `ads.com` được truy cập, máy chủ xa nhận được cookie `id` và nhận diện người dùng:

   ![](/article/cookie/cookie-third-party-2.svg)
4. Quan trọng hơn nữa, khi người dùng chuyển từ `site.com` sang trang web khác `other.com`, cũng có banner, thì `ads.com` nhận được cookie, vì nó thuộc về `ads.com`, từ đó nhận diện khách truy cập và theo dõi anh ta khi di chuyển giữa các trang web:

   ![](/article/cookie/cookie-third-party-3.svg)

Cookies bên thứ ba truyền thống được dùng cho dịch vụ theo dõi và quảng cáo, do bản chất của chúng. Chúng gắn với domain nguồn gốc, vì vậy `ads.com` có thể theo dõi cùng người dùng giữa các trang web khác nhau, nếu tất cả chúng đều truy cập nó.

Tất nhiên, một số người không thích bị theo dõi, vì vậy các trình duyệt cho phép họ vô hiệu hóa các cookie như vậy.

Ngoài ra, một số trình duyệt hiện đại áp dụng các chính sách đặc biệt cho cookies như vậy:

- Safari không cho phép cookies bên thứ ba hoàn toàn.
- Firefox đi kèm "danh sách đen" các domain bên thứ ba nơi nó chặn cookies bên thứ ba.

Vui lòng lưu ý:

Nếu chúng ta tải script từ domain bên thứ ba, như `<script src="https://google-analytics.com/analytics.js">`, và script đó sử dụng `document.cookie` để đặt cookie, thì cookie đó không phải bên thứ ba.

Nếu một script đặt cookie, thì bất kể script đến từ đâu – cookie thuộc về domain của trang web hiện tại.

## [Phụ lục: GDPR](#appendix-gdpr)

Chủ đề này không liên quan gì đến JavaScript, nó chỉ là điều cần ghi nhớ khi đặt cookies.

Có một luật ở Châu Âu gọi là GDPR, thực thi một bộ quy tắc để các trang web tôn trọng quyền riêng tư của người dùng. Một trong những quy tắc này là yêu cầu sự cho phép rõ ràng cho cookies theo dõi từ người dùng.

Vui lòng lưu ý, điều đó chỉ liên quan đến cookies theo dõi/xác định/xác thực.

Vì vậy, nếu chúng ta đặt cookie chỉ lưu một số thông tin, nhưng không theo dõi hay xác định người dùng, thì chúng ta tự do làm điều đó.

Nhưng nếu chúng ta sắp đặt cookie chứa phiên xác thực hoặc ID theo dõi, thì người dùng phải cho phép điều đó.

Các trang web thường có hai phương án tuân thủ GDPR. Có thể bạn đã thấy cả hai trên web:

1. Nếu một trang web muốn đặt cookies theo dõi chỉ cho người dùng đã xác thực.

   Để làm vậy, form đăng ký nên có hộp kiểm như "chấp nhận chính sách riêng tư" (miêu tả cách cookies được sử dụng), người dùng phải kiểm tra nó, và sau đó trang web có thể đặt cookies xác thực.
2. Nếu một trang web muốn đặt cookies theo dõi cho tất cả mọi người.

   Để làm vậy hợp pháp, trang web hiển thị màn hình modal "splash" cho khách mới và yêu cầu họ đồng ý với cookies. Sau đó trang web có thể đặt chúng và để mọi người xem nội dung. Điều đó có thể gây khó chịu cho khách mới. Không ai thích thấy các màn hình modal "bắt buộc nhấp" như vậy thay vì nội dung. Nhưng GDPR yêu cầu sự đồng ý rõ ràng.

GDPR không chỉ về cookies, mà còn về các vấn đề liên quan đến quyền riêng tư khác, nhưng điều đó nằm ngoài phạm vi của chúng ta.

## [Tóm tắt](#summary)

`document.cookie` cung cấp truy cập đến cookies.

- Thao tác viết chỉ sửa đổi cookie được nêu trong đó.
- Tên/giá trị phải được mã hóa.
- Một cookie không được vượt quá 4KB về kích thước. Số lượng cookie cho phép trên một domain là khoảng 20+ (khác nhau theo trình duyệt).

Các thuộc tính của cookie:

- `path=/`, mặc định là path hiện tại, khiến cookie chỉ hiển thị dưới path đó.
- `domain=site.com`, mặc định cookie chỉ hiển thị trên domain hiện tại. Nếu domain được đặt rõ, cookie trở nên hiển thị trên các subdomain.
- `expires` hoặc `max-age` đặt thời gian hết hạn của cookie. Không có chúng, cookie sẽ chết khi trình duyệt đóng.
- `secure` khiến cookie chỉ dùng cho HTTPS.
- `samesite` cấm trình duyệt gửi cookie với các request đến từ bên ngoài trang web. Điều này giúp ngăn chặn các cuộc tấn công XSRF.

Ngoài ra:

- Trình duyệt có thể cấm cookies bên thứ ba, ví dụ: Safari làm điều đó mặc định. Cũng có công việc đang triển khai để thực hiện điều này trong Chrome.
- Khi đặt cookie theo dõi cho công dân EU, GDPR yêu cầu phải xin phép.
