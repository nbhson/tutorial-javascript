# Getter và setter thuộc tính

> Source: [https://javascript.info/property-accessors](https://javascript.info/property-accessors)

<!-- fetched: 2026-09-14 -->

Có hai loại thuộc tính đối tượng.

Loại đầu tiên là *thuộc tính dữ liệu*. Chúng ta đã biết cách làm việc với chúng. Tất cả các thuộc tính mà chúng ta đã sử dụng cho đến nay đều là thuộc tính dữ liệu.

Loại thứ hai của thuộc tính là một thứ mới. Đó là *thuộc tính truy cập*. Về bản chất, chúng là các hàm thực thi khi đọc và gán giá trị, nhưng trông giống như các thuộc tính thông thường đối với mã bên ngoài.

## [Getter và setter](#getters-and-setters)

Các thuộc tính truy cập được đại diện bởi các phương thức "getter" và "setter". Trong một đối tượng literal, chúng được ký hiệu bằng `get` và `set`:

```
let obj = {
  get propName() {
    // getter, mã được thực thi khi đọc obj.propName
  },

  set propName(value) {
    // setter, mã được thực thi khi gán obj.propName = value
  }
};
```

Getter hoạt động khi `obj.propName` được đọc, setter – khi nó được gán.

Ví dụ, chúng ta có một đối tượng `user` với `name` và `surname`:

```
let user = {
  name: "John",
  surname: "Smith"
};
```

Bây giờ chúng ta muốn thêm thuộc tính `fullName`, giá trị sẽ là `"John Smith"`. Tất nhiên, chúng ta không muốn sao chép-dán thông tin hiện có, vì vậy chúng ta có thể triển khai nó như một thuộc tính truy cập:

```
let user = {
  name: "John",
  surname: "Smith",

  get fullName() {
    return `${this.name} ${this.surname}`;
  }
};

alert(user.fullName); // John Smith
```

Từ bên ngoài, một thuộc tính truy cập trông giống như một thuộc tính thông thường. Đó là ý tưởng của các thuộc tính truy cập. Chúng ta không *gọi* `user.fullName` như một hàm, chúng ta *đọc* nó bình thường: getter chạy ngầm phía sau.

Cho đến nay, `fullName` chỉ có getter. Nếu chúng ta cố gắng gán `user.fullName=`, sẽ có lỗi:

```
let user = {
  get fullName() {
    return `...`;
  }
};

user.fullName = "Test"; // Error (property has only a getter)
```

Hãy sửa nó bằng cách thêm setter cho `user.fullName`:

```
let user = {
  name: "John",
  surname: "Smith",

  get fullName() {
    return `${this.name} ${this.surname}`;
  },

  set fullName(value) {
    [this.name, this.surname] = value.split(" ");
  }
};

// set fullName is executed with the given value.
user.fullName = "Alice Cooper";

alert(user.name); // Alice
alert(user.surname); // Cooper
```

Kết quả là chúng ta có thuộc tính "ảo" `fullName`. Nó có thể đọc và ghi được.

## [Mô tả thuộc tính truy cập](#accessor-descriptors)

Mô tả cho các thuộc tính truy cập khác với mô tả cho thuộc tính dữ liệu.

Đối với thuộc tính truy cập, không có `value` hoặc `writable`, nhưng thay vào đó là các hàm `get` và `set`.

 nghĩa là, một mô tả thuộc tính truy cập có thể có:

- **`get`** – một hàm không có đối số, hoạt động khi thuộc tính được đọc,
- **`set`** – một hàm có một đối số, được gọi khi thuộc tính được gán,
- **`enumerable`** – giống như cho thuộc tính dữ liệu,
- **`configurable`** – giống như cho thuộc tính dữ liệu.

Ví dụ, để tạo một thuộc tính truy cập `fullName` với `defineProperty`, chúng ta có thể truyền một mô tả với `get` và `set`:

```
let user = {
  name: "John",
  surname: "Smith"
};

Object.defineProperty(user, 'fullName', {
  get() {
    return `${this.name} ${this.surname}`;
  },

  set(value) {
    [this.name, this.surname] = value.split(" ");
  }
});

alert(user.fullName); // John Smith

for(let key in user) alert(key); // name, surname
```

Xin lưu ý rằng một thuộc tính có thể là thuộc tính truy cập (có `get/set`) hoặc thuộc tính dữ liệu (có `value`), không phải cả hai.

Nếu chúng ta cố gắng cung cấp cả `get` và `value` trong cùng một mô tả, sẽ có lỗi:

```
// Error: Invalid property descriptor.
Object.defineProperty({}, 'prop', {
  get() {
    return 1
  },

  value: 2
});
```

## [Getter/setter thông minh hơn](#smarter-getters-setters)

Getter/setter có thể được sử dụng như các bộ bao bọc quanh các giá trị thuộc tính "thực" để kiểm soát tốt hơn các thao tác với chúng.

Ví dụ, nếu chúng ta muốn cấm các tên quá ngắn cho `user`, chúng ta có thể có setter `name` và giữ giá trị trong một thuộc tính riêng `_name`:

```
let user = {
  get name() {
    return this._name;
  },

  set name(value) {
    if (value.length < 4) {
      alert("Name is too short, need at least 4 characters");
      return;
    }
    this._name = value;
  }
};

user.name = "Pete";
alert(user.name); // Pete

user.name = ""; // Name is too short...
```

Vì vậy, tên được lưu trong thuộc tính `_name`, và truy cập được thực hiện thông qua getter và setter.

Về mặt kỹ thuật, mã bên ngoài có thể truy cập trực tiếp tên bằng cách sử dụng `user._name`. Nhưng có một quy ước được biết đến rộng rãi rằng các thuộc tính bắt đầu bằng dấu gạch dưới `"_"` là thuộc tính nội bộ và không nên chạm vào từ bên ngoài đối tượng.

## [Sử dụng cho tương thích](#using-for-compatibility)

Một trong những công dụng tuyệt vời của các thuộc tính truy cập là chúng cho phép kiểm soát một thuộc tính dữ liệu "thông thường" bất cứ lúc nào bằng cách thay thế nó bằng getter và setter và tinh chỉnh hành vi của nó.

Hãy tưởng tượng chúng ta bắt đầu triển khai các đối tượng user bằng cách sử dụng thuộc tính dữ liệu `name` và `age`:

```
function User(name, age) {
  this.name = name;
  this.age = age;
}

let john = new User("John", 25);

alert( john.age ); // 25
```

…Nhưng sớm hay muộn, mọi thứ có thể thay đổi. Thay vì `age`, chúng ta có thể quyết định lưu `birthday`, vì nó chính xác và thuận tiện hơn:

```
function User(name, birthday) {
  this.name = name;
  this.birthday = birthday;
}

let john = new User("John", new Date(1992, 6, 1));
```

Giờ phải làm gì với mã cũ vẫn sử dụng thuộc tính `age`?

Chúng ta có thể cố gắng tìm tất cả các vị trí như vậy và sửa chúng, nhưng điều đó tốn thời gian và có thể khó thực hiện nếu mã đó được sử dụng bởi nhiều người khác. Và bên cạnh đó, `age` là một thứ tốt nên có trong `user`, đúng không?

Hãy giữ nó.

Thêm getter cho `age` giải quyết vấn đề:

```
function User(name, birthday) {
  this.name = name;
  this.birthday = birthday;

  // age is calculated from the current date and birthday
  Object.defineProperty(this, "age", {
    get() {
      let todayYear = new Date().getFullYear();
      return todayYear - this.birthday.getFullYear();
    }
  });
}

let john = new User("John", new Date(1992, 6, 1));

alert( john.birthday ); // birthday is available
alert( john.age );      // ...as well as the age
```

Giờ mã cũ cũng hoạt động và chúng ta có thêm một thuộc tính đẹp.
