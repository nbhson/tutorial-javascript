# Thuộc tính và phương thức Private và Protected

> Nguồn: [https://javascript.info/private-protected-properties-methods](https://javascript.info/private-protected-properties-methods)

<!-- fetched: 2026-09-14 -->

Một trong những nguyên tắc quan trọng nhất của lập trình hướng đối tượng – phân biệt interface nội bộ với interface bên ngoài.

Đó là thực hành "bắt buộc" trong phát triển bất cứ thứ gì phức tạp hơn ứng dụng "hello world".

Để hiểu điều này, hãy rời bỏ phát triển và hướng mắt của chúng ta vào thế giới thực.

Thông thường, các thiết bị chúng ta đang sử dụng khá phức tạp. Nhưng phân biệt interface nội bộ với interface bên ngoài cho phép sử dụng chúng mà không có vấn đề.

## [Một ví dụ thực tế](#mot-vi-du-thuc-te)

Ví dụ, một máy pha cà phê. Đơn giản từ bên ngoài: một nút bấm, một màn hình, vài lỗ…Và, chắc chắn, kết quả – cà phê tuyệt vời! :)

![](/article/private-protected-properties-methods/coffee.jpg)

Nhưng bên trong… (một hình ảnh từ hướng dẫn sửa chữa)

![](/article/private-protected-properties-methods/coffee-inside.jpg)

Rất nhiều chi tiết. Nhưng chúng ta có thể sử dụng nó mà không biết gì.

Máy pha cà phê khá đáng tin cậy, phải không? Chúng ta có thể sử dụng một cái trong nhiều năm, và chỉ nếu có gì đó sai – mang nó đi sửa chữa.

Bí quyết độ tin cậy và sự đơn giản của một máy pha cà phê – tất cả các chi tiết được điều chỉnh tốt và *ẩn* bên trong.

Nếu chúng ta tháo nắp bảo vệ khỏi máy pha cà phê, sau đó sử dụng nó sẽ phức tạp hơn nhiều (phải nhấn ở đâu?), và nguy hiểm (nó có thể gây điện giật).

Như chúng ta sẽ thấy, trong lập trình các objects giống như máy pha cà phê.

Nhưng để ẩn các chi tiết nội bộ, chúng ta sẽ không sử dụng nắp bảo vệ, mà là cú pháp đặc biệt của ngôn ngữ và các quy ước.

## [Interface nội bộ và bên ngoài](#interface-noi-bo-va-ben-ngoai)

Trong lập trình hướng đối tượng, các properties và methods được chia thành hai nhóm:

- *Internal interface* – các methods và properties, có thể truy cập từ các methods khác của class, nhưng không từ bên ngoài.
- *External interface* – các methods và properties, có thể truy cập từ bên ngoài class.

Nếu chúng ta tiếp tục phép ẩn dụ với máy pha cà phê – những gì được ẩn bên trong: một ống boiler, heating element, v.v. – là internal interface của nó.

Internal interface được sử dụng để object hoạt động, các chi tiết của nó sử dụng nhau. Ví dụ, một ống boiler được gắn vào heating element.

Nhưng từ bên ngoài một máy pha cà phê được đóng bởi nắp bảo vệ, vì vậy không ai có thể với tới những thứ đó. Các chi tiết được ẩn và không thể truy cập. Chúng ta có thể sử dụng các tính năng của nó thông qua external interface.

Vì vậy, tất cả những gì chúng ta cần để sử dụng một object là biết external interface của nó. Chúng ta có thể hoàn toàn không biết nó hoạt động như thế nào bên trong, và đó là điều tuyệt vời.

Đó là phần giới thiệu chung.

Trong JavaScript, có hai loại fields object (properties và methods):

- Public: có thể truy cập từ bất cứ đâu. Chúng tạo thành external interface. Cho đến nay chúng ta chỉ đang sử dụng các properties và methods public.
- Private: chỉ có thể truy cập từ bên trong class. Những thứ này dành cho internal interface.

Trong nhiều ngôn ngữ khác cũng tồn tại các fields "protected": chỉ có thể truy cập từ bên trong class và các class kế thừa nó (giống như private, nhưng thêm quyền truy cập từ các class con). Chúng cũng hữu ích cho internal interface. Chúng theo một nghĩa nào đó phổ biến hơn các private, vì chúng ta thường muốn các class con có quyền truy cập vào chúng.

Các fields protected không được triển khai ở cấp ngôn ngữ trong JavaScript, nhưng trong thực tế chúng rất tiện lợi, vì vậy chúng được emulate.

Bây giờ chúng ta sẽ tạo một máy pha cà phê trong JavaScript với tất cả các loại properties này. Một máy pha cà phê có nhiều chi tiết, chúng ta sẽ không model chúng để giữ đơn giản (dù chúng ta có thể).

## [Bảo vệ "waterAmount"]( #bao-ve-wateramount)

Hãy tạo một class máy pha cà phê đơn giản trước:

```
class CoffeeMachine {
  waterAmount = 0; // the amount of water inside

  constructor(power) {
    this.power = power;
    alert( `Created a coffee-machine, power: ${power}` );
  }

}

// create the coffee machine
let coffeeMachine = new CoffeeMachine(100);

// add water
coffeeMachine.waterAmount = 200;
```

Hiện tại các properties `waterAmount` và `power` là public. Chúng ta có thể dễ dàng get/set chúng từ bên ngoài thành bất kỳ giá trị nào.

Hãy thay đổi property `waterAmount` thành protected để có nhiều kiểm soát hơn về nó. Ví dụ, chúng ta không muốn ai đó đặt nó dưới 0.

**Các thuộc tính protected thường được tiền tố bằng dấu gạch dưới `_`.**

Điều đó không được enforcement ở cấp ngôn ngữ, nhưng có một quy ước đã biết giữa các programmer rằng các properties và methods như vậy không nên được truy cập từ bên ngoài.

Vì vậy property của chúng ta sẽ được gọi là `_waterAmount`:

```
class CoffeeMachine {
  _waterAmount = 0;

  set waterAmount(value) {
    if (value < 0) {
      value = 0;
    }
    this._waterAmount = value;
  }

  get waterAmount() {
    return this._waterAmount;
  }

  constructor(power) {
    this._power = power;
  }

}

// create the coffee machine
let coffeeMachine = new CoffeeMachine(100);

// add water
coffeeMachine.waterAmount = -10; // _waterAmount will become 0, not -10
```

Bây giờ quyền truy cập được kiểm soát, vì vậy việc đặt water amount dưới 0 trở nên bất khả thi.

## [Thuộc tính "power" chỉ đọc](#read-only-power)

Đối với property `power`, hãy làm cho nó read-only. Đôi khi điều đó xảy ra rằng một property phải được đặt chỉ tại thời điểm tạo, và sau đó không bao giờ bị sửa đổi.

Đó chính là trường hợp của một máy pha cà phê: power never changes.

Để làm điều đó, chúng ta chỉ cần tạo getter, nhưng không tạo setter:

```
class CoffeeMachine {
  // ...

  constructor(power) {
    this._power = power;
  }

  get power() {
    return this._power;
  }

}

// create the coffee machine
let coffeeMachine = new CoffeeMachine(100);

alert(`Power is: ${coffeeMachine.power}W`); // Power is: 100W

coffeeMachine.power = 25; // Error (no setter)
```

Getter/setter functions

Ở đây chúng ta đã sử dụng cú pháp getter/setter.

Nhưng phần lớn thời gian các hàm `get.../set...` được ưa thích hơn, như thế này:

```
class CoffeeMachine {
  _waterAmount = 0;

  setWaterAmount(value) {
    if (value < 0) value = 0;
    this._waterAmount = value;
  }

  getWaterAmount() {
    return this._waterAmount;
  }
}

new CoffeeMachine().setWaterAmount(100);
```

Nó trông hơi dài hơn, nhưng các functions linh hoạt hơn. Chúng có thể chấp nhận nhiều đối số (ngay cả khi chúng ta không cần chúng ngay bây giờ).

Mặt khác, cú pháp get/set ngắn hơn, vì vậy cuối cùng không có quy tắc nghiêm ngặt, đó là tùy bạn quyết định.

Các fields protected được thừa kế

Nếu chúng ta inherit `class MegaMachine extends CoffeeMachine`, thì không gì ngăn cản chúng ta truy cập `this._waterAmount` hoặc `this._power` từ các methods của class mới.

Vì vậy các fields protected được kế thừa một cách tự nhiên. Khác với các private mà chúng ta sẽ thấy bên dưới.

## [Thuộc tính private "#waterLimit"]( #private-waterlimit)

Một bổ sung gần đây

Đây là một bổ sung gần đây cho ngôn ngữ.
Không được hỗ trợ trong các JavaScript engines, hoặc chỉ hỗ trợ một phần, yêu cầu [polyfilling](https://javascript.info/polyfills).

Có một proposal JavaScript hoàn chỉnh, gần như trong standard, cung cấp support ở cấp ngôn ngữ cho các properties và methods private.

Các private nên bắt đầu bằng `#`. Chúng chỉ có thể truy cập từ bên trong class.

Ví dụ, đây là property private `#waterLimit` và phương thức kiểm tra nước private `#fixWaterAmount`:

```
class CoffeeMachine {
  #waterLimit = 200;

  #fixWaterAmount(value) {
    if (value < 0) return 0;
    if (value > this.#waterLimit) return this.#waterLimit;
  }

  setWaterAmount(value) {
    this.#waterLimit = this.#fixWaterAmount(value);
  }

}

let coffeeMachine = new CoffeeMachine();

// can't access privates from outside of the class
coffeeMachine.#fixWaterAmount(123); // Error
coffeeMachine.#waterLimit = 1000; // Error
```

Ở cấp ngôn ngữ, `#` là một dấu hiệu đặc biệt cho biết field là private. Chúng ta không thể truy cập nó từ bên ngoài hoặc từ các class kế thừa.

Các private fields không xung đột với các public ones. Chúng ta có thể có cả private `#waterAmount` và public `waterAmount` fields cùng lúc.

Ví dụ, hãy làm cho `waterAmount` là một accessor cho `#waterAmount`:

```
class CoffeeMachine {

  #waterAmount = 0;

  get waterAmount() {
    return this.#waterAmount;
  }

  set waterAmount(value) {
    if (value < 0) value = 0;
    this.#waterAmount = value;
  }
}

let machine = new CoffeeMachine();

machine.waterAmount = 100;
alert(machine.#waterAmount); // Error
```

Khác với các protected, các private fields được enforcement bởi chính ngôn ngữ. Đó là một điều tốt.

Nhưng nếu chúng ta kế thừa từ `CoffeeMachine`, thì chúng ta sẽ không có quyền truy cập trực tiếp vào `#waterAmount`. Chúng ta sẽ cần dựa vào getter/setter `waterAmount`:

```
class MegaCoffeeMachine extends CoffeeMachine {
  method() {
    alert( this.#waterAmount ); // Error: can only access from CoffeeMachine
  }
}
```

Trong nhiều scenario như hạn chế đó quá nghiêm trọng. Nếu chúng ta extend một `CoffeeMachine`, chúng ta có thể có lý do chính đáng để truy cập các internals của nó. Đó là lý do tại sao các fields protected được sử dụng thường xuyên hơn, ngay cả khi chúng không được hỗ trợ bởi cú pháp ngôn ngữ.

Private fields không khả dụng như this[name]

Các private fields là đặc biệt.

Như chúng ta đã biết, thông thường chúng ta có thể truy cập các fields sử dụng `this[name]`:

```
class User {
  ...
  sayHi() {
    let fieldName = "name";
    alert(`Hello, ${this[fieldName]}`);
  }
}
```

Với các private fields thì không thể: `this['#name']` không hoạt động. Đó là một limitation cú pháp để đảm bảo privacy.

## [Tóm tắt](#summary)

Về mặt OOP, việc phân biệt interface nội bộ với interface bên ngoài được gọi là [encapsulation](https://en.wikipedia.org/wiki/Encapsulation_(computer_programming)).

Nó mang lại các lợi ích sau:

Bảo vệ cho users, vì vậy họ không tự bắn vào chân mình
:   Hãy tưởng tượng, có một team developers sử dụng một máy pha cà phê. Nó được tạo bởi công ty "Best CoffeeMachine", và hoạt động tốt, nhưng nắp bảo vệ đã bị tháo. Vì vậy internal interface được expose.

   Tất cả developers đều là civilized – họ sử dụng máy pha cà phê như dự định. Nhưng một trong số họ, John, quyết định anh ta là người thông minh nhất, và đã thực hiện một số tweaks trong internals của máy pha cà phê. Vì vậy máy pha cà phê hỏng hai ngày sau.

   Đó chắc chắn không phải là lỗi của John, mà là của người đã tháo nắp bảo vệ và để John làm các thao tác của anh ta.

   Cũng giống trong lập trình. Nếu một user của một class sẽ thay đổi những thứ không nên thay đổi từ bên ngoài – hậu quả là không thể dự đoán được.

Hỗ trợ được
:   Tình huống trong lập trình phức tạp hơn so với máy pha cà phê thực tế, vì chúng ta không chỉ mua nó một lần. Mã liên tục trải qua development và improvement.

   **Nếu chúng ta nghiêm ngặt phân biệt internal interface, thì developer của class có thể tự do thay đổi các properties và methods nội bộ của nó, ngay cả mà không thông báo cho users.**

   Nếu bạn là developer của class như vậy, thật tuyệt khi biết rằng các private methods có thể được rename một cách an toàn, các parameters của chúng có thể được thay đổi, và thậm chí bị xóa, vì không có external code nào phụ thuộc vào chúng.

   Đối với users, khi một phiên bản mới ra mắt, nó có thể là một cuộc cách mạng hoàn toàn nội bộ, nhưng vẫn dễ dàng nâng cấp nếu external interface vẫn giống nhau.

Giấu complexity
:   Mọi người thích sử dụng những thứ đơn giản. Ít nhất là từ bên ngoài. Những gì ở bên trong là một câu chuyện khác.

   Các programmers không phải là ngoại lệ.

   **Luôn tiện lợi khi các chi tiết implementation được ẩn đi, và một external interface đơn giản, được tài liệu kỹ lưỡng có sẵn.**

Để ẩn internal interface chúng ta sử dụng các properties protected hoặc private:

- Các protected fields bắt đầu bằng `_`. Đó là một quy ước đã biết, không được enforcement ở cấp ngôn ngữ. Các programmers nên chỉ truy cập một field bắt đầu bằng `_` từ class của nó và các class kế thừa từ nó.
- Các private fields bắt đầu bằng `#`. JavaScript đảm bảo chúng ta chỉ có thể truy cập những thứ đó từ bên trong class.

Hiện tại, các private fields không được hỗ trợ tốt giữa các browsers, nhưng có thể được polyfill.
