# Tham chiếu và sao chép object

> Nguồn: [https://javascript.info/object-copy](https://javascript.info/object-copy)

<!-- fetched: 2026-09-14 -->

Một trong những khác biệt cơ bản giữa objects và primitives là objects được lưu trữ và sao chép "bằng tham chiếu", trong khi các giá trị primitive: chuỗi, số, boolean, v.v. – luôn được sao chép "nguyên giá trị".

Điều đó dễ hiểu nếu chúng ta nhìn sâu hơn vào những gì xảy ra khi chúng ta sao chép một giá trị.

Hãy bắt đầu với một primitive, chẳng hạn như một chuỗi.

Ở đây chúng ta đặt một bản sao của `message` vào `phrase`:

```
let message = "Xin chào!";
let phrase = message;
```

Kết quả là chúng ta có hai biến độc lập, mỗi biến lưu trữ chuỗi `"Xin chào!"`.

![](/article/object-copy/variable-copy-value.svg)

Kết quả khá hiển nhiên, phải không?

Objects thì không như vậy.

**Một biến được gán cho một object lưu trữ không phải objectbản thân, mà là "địa chỉ trong bộ nhớ" – hay nói cách khác là "tham chiếu" đến nó.**

Hãy xem mộtví dụví dụ về biến như vậy:

```
let user = {
  name: "John"
};
```

Và đây là cách nó được lưu trữ trong bộ nhớ:

![](/article/object-copy/variable-contains-reference.svg)

Object được lưu trữ ở đâu đó trong bộ nhớ (ở bên phải của hình), trong khi biến `user` (ở bên trái) có một "tham chiếu" đến nó.

Chúng ta có thể nghĩ về một biến object, chẳng hạn như `user`, như một tờ giấy có địa chỉ của object trên đó.

Khi chúng ta thực hiện các thao tác với object,ví dụví dụ, lấy property `user.name`, động cơ JavaScript nhìn vào những gì ở địa chỉ đó và thực hiện thao tác trên object thực tế.

Giờ đây, đây là lý do tại sao điều đó quan trọng.

**Khi một biến object được sao chép, tham chiếu được sao chép, nhưng objectbản thân không được nhân bản.**

Ví dụ:

```
let user = { name: "John" };

let admin = user; // sao chép tham chiếu
```

Bây giờ chúng ta có hai biến, mỗi biến lưu trữ một tham chiếu đến cùng một object:

![](/article/object-copy/variable-copy-reference.svg)

Như bạn có thể thấy, vẫn chỉ có một object, nhưng bây giờ có hai biến tham chiếu đến nó.

Chúng ta có thể sử dụng bất kỳ biến nào để truy cập object và sửa đổi nội dung của nó:

```
let user = { name: 'John' };

let admin = user;

admin.name = 'Pete'; // bị thay đổi bởi tham chiếu "admin"

alert(user.name); // 'Pete', các thay đổi được nhìn thấy từ tham chiếu "user"
```

Nó giống như chúng ta có một tủ với hai chìa khóa và sử dụng một trong số chúng (`admin`) để mở và thực hiện các thay đổi. Sau đó, nếu chúng ta sau đó sử dụng một chìa khóa khác (`user`), chúng ta vẫn đang mở cùng một tủ và có thể truy cập nội dung đã được sửa đổi.

## [So sánh theo tham chiếu](#comparison-by-reference)

Hai object bằng nhau chỉ khi chúng là cùng một object.

Ví dụ, ở đây `a` và `b` tham chiếu đến cùng một object, vì vậy chúng bằng nhau:

```
let a = {};
let b = a; // sao chép tham chiếu

alert( a == b ); // true, cả hai biến tham chiếu đến cùng một object
alert( a === b ); // true
```

Và ở đây hai object độc lập không bằng nhau, ngay cả khi chúng trông giống nhau (cả hai đều trống):

```
let a = {};
let b = {}; // hai object độc lập

alert( a == b ); // false
```

Đối với các phép so sánh như `obj1 > obj2` hoặc so sánh với một primitive `obj == 5`, các object được chuyển đổi sang primitives. Chúng ta sẽ tìm hiểu cách chuyển đổi object hoạt động rất sớm, nhưng thật sự, những phép so sánh như vậy được sử dụng rất hiếm – thường chúng xuất hiện như là kết quả của lỗi lập trình.

Object const có thể được sửa đổi

Một tác dụng phụ quan trọng của việc lưu trữ objects như các tham chiếu là một object được khai báo là `const` *có thể* được sửa đổi.

Ví dụ:

```
const user = {
  name: "John"
};

user.name = "Pete"; // (*)

alert(user.name); // Pete
```

Có thể trông như dòng `(*)` sẽ gây ra lỗi, nhưng nó không phải. Giá trị của `user` là không đổi, nó phải luôn tham chiếu đến cùng một object, nhưng các property của object đó có thể thay đổi tự do.

Nói cách khác, `const user` chỉ gây lỗi nếu chúng ta cố gắng gán `user=...` như một thể thống nhất.

Tuy nhiên, nếu chúng ta thực sự cần làm cho các property object là constant, thì cũng có thể, nhưng sử dụng các phương pháp hoàn toàn khác. Chúng ta sẽ đề cập đến điều đó trong chương [Property flags and descriptors](/property-descriptors).

## [Clone và merge, Object.assign](#cloning-and-merging-object-assign)

Vì vậy, sao chép một biến object tạo ra một tham chiếu nữa đến cùng một object.

Nhưng nếu chúng ta cần nhân bản một object thì sao?

Chúng ta có thể tạo một object mới và sao chép cấu trúc của object hiện có, bằng cách lặp qua các property của nó và sao chép chúng ở cấp primitive.

Như thế này:

```
let user = {
  name: "John",
  age: 30
};

let clone = {}; // object trống mới

// hãy sao chép tất cả các property của user vào đó
for (let key in user) {
  clone[key] = user[key];
}

// giờ clone là một object hoàn toàn độc lập với cùng nội dung
clone.name = "Pete"; // đã thay đổi dữ liệu trong đó

alert( user.name ); // vẫn là John trong object gốc
```

Chúng ta cũng có thể sử dụng method [Object.assign](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign).

Cú pháp là:

```
Object.assign(dest, ...sources)
```

- Đối số thứ nhất `dest` là một object đích.
- Các đối số further là một danh sách các object nguồn.

Nó sao chép các property của tất cả các object nguồn vào target `dest`, và sau đó trả về nó như là kết quả.

Ví dụ, chúng ta có object `user`, hãy thêm một vài quyền vào nó:

```
let user = { name: "John" };

let permissions1 = { canView: true };
let permissions2 = { canEdit: true };

// sao chép tất cả các property từ permissions1 và permissions2 vào user
Object.assign(user, permissions1, permissions2);

// giờ user = { name: "John", canView: true, canEdit: true }
alert(user.name); // John
alert(user.canView); // true
alert(user.canEdit); // true
```

Nếu tên property được sao chép đã tồn tại, nó sẽ bị ghi đè:

```
let user = { name: "John" };

Object.assign(user, { name: "Pete" });

alert(user.name); // giờ user = { name: "Pete" }
```

Chúng ta cũng có thể sử dụng `Object.assign` để thực hiện một object clone đơn giản:

```
let user = {
  name: "John",
  age: 30
};

let clone = Object.assign({}, user);

alert(clone.name); // John
alert(clone.age); // 30
```

Ở đây nó sao chép tất cả các property của `user` vào object trống và trả về nó.

Cũng có các phương pháp khác để clone một object,ví dụví dụ sử dụng [spread syntax](/rest-parameters-spread) `clone = {...user}`, sẽ được đề cập sau trong tutorial.

## [Nested cloning](#nested-cloning)

Cho đến giờ chúng ta giả sử rằng tất cả các property của `user` là primitives. Nhưng các property có thể là các tham chiếu đến các object khác.

Như thế này:

```
let user = {
  name: "John",
  sizes: {
    height: 182,
    width: 50
  }
};

alert( user.sizes.height ); // 182
```

Bây giờ chỉ cần sao chép `clone.sizes = user.sizes` là không đủ, vì `user.sizes` là một object, và sẽ được sao chép theo tham chiếu, vì vậy `clone` và `user` sẽ chia sẻ cùng sizes:

```
let user = {
  name: "John",
  sizes: {
    height: 182,
    width: 50
  }
};

let clone = Object.assign({}, user);

alert( user.sizes === clone.sizes ); // true, cùng object

// user và clone chia sẻ sizes
user.sizes.width = 60;    // thay đổi một property từ một chỗ
alert(clone.sizes.width); // 60, lấy kết quả từ chỗ khác
```

Để sửa lỗi đó và làm cho `user` và `clone` thực sự là các object riêng biệt, chúng ta nên sử dụng vòng lặp clone kiểm tra từng giá trị của `user[key]` và, nếu nó là một object, thì sao chép cả cấu trúc của nó. Điều đó được gọi là "deep cloning" hoặc "structured cloning". Có method [structuredClone](https://developer.mozilla.org/en-US/docs/Web/API/structuredClone) triển khai deep cloning.

### [structuredClone](#structuredclone)

Lệnh gọi `structuredClone(object)` clone `object` với tất cả các nested properties.

Đây là cách chúng ta có thể sử dụng nó trongví dụví dụ của chúng ta:

```
let user = {
  name: "John",
  sizes: {
    height: 182,
    width: 50
  }
};

let clone = structuredClone(user);

alert( user.sizes === clone.sizes ); // false, các object khác nhau

// user và clone hoàn toàn không liên quan giờ
user.sizes.width = 60;    // thay đổi một property từ một chỗ
alert(clone.sizes.width); // 50, không liên quan
```

Method `structuredClone` có thể clone hầu hết các types dữ liệu, chẳng hạn như objects, arrays, primitive values.

Nó cũng hỗ trợ circular references, khi một object property tham chiếu đến objectbản thân (trực tiếp hoặc thông qua một chain của references).

Ví dụ:

```
let user = {};
// hãy tạo một circular reference:
// user.me tham chiếu đến userbản thân
user.me = user;

let clone = structuredClone(user);
alert(clone.me === clone); // true
```

Như bạn có thể thấy, `clone.me` tham chiếu đến `clone`, không phải `user`! Vì vậy circular reference đã được clone chính xác.

Tuy nhiên, có những trường hợp khi `structuredClone` fail.

Ví dụ, khi một object có một function property:

```
// error
structuredClone({
  f: function() {}
});
```

Function properties không được hỗ trợ.

Để xử lý các trường hợp phức tạp như vậy, chúng ta có thể cần sử dụng sự kết hợp của các phương pháp clone, viết mã custom hoặc, để không phải re-invent the wheel, sử dụng một implementation hiện có, chẳng hạn như [\_.cloneDeep(obj)](https://lodash.com/docs#cloneDeep) từ thư viện JavaScript [lodash](https://lodash.com).

## [Tổng kết](#summary)

Objects được gán và sao chép bằng tham chiếu. Nói cách khác, một biến lưu trữ không phải là "giá trị object", mà là một "tham chiếu" (địa chỉ trong bộ nhớ) cho giá trị. Vì vậy, sao chép biến như vậy hoặc truyền nó như một đối số hàm sao chép tham chiếu đó, không phải objectbản thân.

Tất cả các thao tác thông qua các tham chiếu được sao chép (như thêm/xóa properties) được thực hiện trên cùng một object duy nhất.

Để tạo một "bản sao thực sự" (một clone) chúng ta có thể sử dụng `Object.assign` cho cái được gọi là "shallow copy" (các nested objects được sao chép theo tham chiếu) hoặc một hàm "deep cloning" `structuredClone` hoặc sử dụng một implementation clone custom, chẳng hạn như [\_.cloneDeep(obj)](https://lodash.com/docs#cloneDeep).
