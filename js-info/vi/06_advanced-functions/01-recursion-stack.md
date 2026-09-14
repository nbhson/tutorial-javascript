# Đệ quy và stack

> Source: [https://javascript.info/recursion](https://javascript.info/recursion)

<!-- fetched: 2026-09-14 -->

Hãy quay lại với functions và nghiên cứu chúng sâu hơn.

Chủ đề đầu tiên của chúng ta sẽ là *đệ quy (recursion)*.

Nếu bạn không phải là người mới bắt đầu lập trình, thì có lẽ nó đã quen thuộc và bạn có thể bỏ qua chương này.

Đệ quy là một mẫu thiết kế lập trình hữu ích trong các tình huống khi một tác vụ có thể được phân tách tự nhiên thành nhiều tác vụ cùng loại nhưng đơn giản hơn. Hoặc khi một tác vụ có thể được đơn giản hóa thành một hành động dễ cộng với một biến thể đơn giản hơn của cùng tác vụ đó. Hoặc, như chúng ta sẽ thấy sớm, để xử lý một số cấu trúc dữ liệu nhất định.

Khi một function giải quyết một tác vụ, trong quá trình đó nó có thể gọi nhiều function khác. Một trường hợp đặc biệt là khi một function gọi *chính nó*. Điều đó được gọi là *đệ quy*.

## [Hai cách suy nghĩ](#two-ways-of-thinking)

Bắt đầu với một điều đơn giản – hãy viết một function `pow(x, n)` nâng `x` lên lũy thừa tự nhiên `n`. Nói cách khác, nhân `x` với chính nó `n` lần.

```
pow(2, 2) = 4
pow(2, 3) = 8
pow(2, 4) = 16
```

Có hai cách để triển khai nó.

1. Suy nghĩ lặp (iterative): vòng lặp `for`:

   ```
   function pow(x, n) {
     let result = 1;

     // multiply result by x n times in the loop
     for (let i = 0; i < n; i++) {
       result *= x;
     }

     return result;
   }

   alert( pow(2, 3) ); // 8
   ```
2. Suy nghĩ đệ quy: đơn giản hóa tác vụ và gọi chính nó:

   ```
   function pow(x, n) {
     if (n == 1) {
       return x;
     } else {
       return x * pow(x, n - 1);
     }
   }

   alert( pow(2, 3) ); // 8
   ```

Xin lưu ý cách biến thể đệ quy khác biệt về bản chất.

Khi `pow(x, n)` được gọi, quá trình thực thi chia thành hai nhánh:

```
              if n==1  = x
             /
pow(x, n) =
             \
              else     = x * pow(x, n - 1)
```

1. Nếu `n == 1`, thì mọi thứ đều tầm thường. Nó được gọi là *cơ sở (base)* của đệ quy, bởi vì nó ngay lập tức tạo ra kết quả hiển nhiên: `pow(x, 1)` bằng `x`.
2. Ngược lại, chúng ta có thể biểu diễn `pow(x, n)` thành `x * pow(x, n - 1)`. Trong toán học, người ta sẽ viết `xn = x * xn-1`. Đây được gọi là *bước đệ quy*: chúng ta biến đổi tác vụ thành một hành động đơn giản hơn (nhân với `x`) và một lời gọi đơn giản hơn của cùng tác vụ (`pow` với `n` nhỏ hơn). Các bước tiếp theo đơn giản hóa nó hơn nữa cho đến khi `n` đạt đến `1`.

Chúng ta cũng có thể nói rằng `pow` *gọi đệ quy chính nó* cho đến khi `n == 1`.

![](/article/recursion/recursion-pow.svg)

Ví dụ, để tính `pow(2, 4)` biến thể đệ quy thực hiện các bước sau:

1. `pow(2, 4) = 2 * pow(2, 3)`
2. `pow(2, 3) = 2 * pow(2, 2)`
3. `pow(2, 2) = 2 * pow(2, 1)`
4. `pow(2, 1) = 2`

Vì vậy, đệ quy giảm một lời gọi function thành một lời gọi đơn giản hơn, rồi – thành đơn giản hơn nữa, cứ tiếp tục cho đến khi kết quả trở nên hiển nhiên.

Đệ quy thường ngắn hơn

Giải pháp đệ quy thường ngắn hơn giải pháp lặp.

Ở đây chúng ta có thể viết lại cùng code sử dụng toán tử điều kiện `?` thay vì `if` để làm cho `pow(x, n)` ngắn gọn hơn và vẫn rất dễ đọc:

```
function pow(x, n) {
  return (n == 1) ? x : (x * pow(x, n - 1));
}
```

Số lượng lời gọi lồng nhau tối đa (bao gồm lời gọi đầu tiên) được gọi là *độ sâu đệ quy*. Trong trường hợp của chúng ta, nó sẽ chính xác bằng `n`.

Độ sâu đệ quy tối đa bị giới hạn bởi engine JavaScript. Chúng ta có thể dựa vào nó là 10000, một số engine cho phép nhiều hơn, nhưng 100000 có lẽ vượt quá giới hạn của hầu hết chúng. Có những tối ưu tự động giúp giảm thiểu điều này ("tối ưu tail calls"), nhưng chúng chưa được hỗ trợ ở mọi nơi và chỉ hoạt động trong các trường hợp đơn giản.

Điều này giới hạn việc ứng dụng đệ quy, nhưng nó vẫn rất rộng. Có nhiều tác vụ mà cách suy nghĩ đệ quy tạo ra code đơn giản hơn, dễ bảo trì hơn.

## [Ngữ cảnh thực thi và stack](#the-execution-context-and-stack)

Bây giờ hãy xem cách các lời gọi đệ quy hoạt động. Để làm điều đó chúng ta sẽ nhìn vào bên trong của functions.

Thông tin về quá trình thực thi của một function đang chạy được lưu trữ trong *ngữ cảnh thực thi (execution context)* của nó.

[Ngữ cảnh thực thi](https://tc39.github.io/ecma262/#sec-execution-contexts) là một cấu trúc dữ liệu nội bộ chứa các chi tiết về việc thực thi một function: luồng điều khiển hiện ở đâu, các biến hiện tại, giá trị của `this` (chúng ta không sử dụng nó ở đây) và một vài chi tiết nội bộ khác.

Một lời gọi function có chính xác một ngữ cảnh thực thi liên kết với nó.

Khi một function thực hiện lời gọi lồng nhau, những điều sau xảy ra:

- Function hiện tại bị tạm dừng.
- Ngữ cảnh thực thi liên kết với nó được ghi nhớ trong một cấu trúc dữ liệu đặc biệt gọi là *stack ngữ cảnh thực thi*.
- Lời gọi lồng nhau được thực thi.
- Sau khi nó kết thúc, ngữ cảnh thực thi cũ được lấy lại từ stack, và function bên ngoài được tiếp tục từ nơi nó dừng lại.

Hãy xem điều gì xảy ra trong quá trình gọi `pow(2, 3)`.

### [pow(2, 3)](#pow-2-3)

Khi bắt đầu gọi `pow(2, 3)`, ngữ cảnh thực thi sẽ lưu trữ các biến: `x = 2, n = 3`, luồng thực thi ở dòng `1` của function.

Chúng ta có thể vẽ nó như sau:

- Context: { x: 2, n: 3, at line 1 }
  pow(2, 3)

Đó là khi function bắt đầu thực thi. Điều kiện `n == 1` là falsy, vì vậy luồng tiếp tục vào nhánh thứ hai của `if`:

```
function pow(x, n) {
  if (n == 1) {
    return x;
  } else {
    return x * pow(x, n - 1);
  }
}

alert( pow(2, 3) );
```

Các biến vẫn giống nhau, nhưng dòng thay đổi, vì vậy ngữ cảnh bây giờ là:

- Context: { x: 2, n: 3, at line 5 }
  pow(2, 3)

Để tính `x * pow(x, n - 1)`, chúng ta cần thực hiện một lời gọi subcall của `pow` với các đối số mới `pow(2, 2)`.

### [pow(2, 2)](#pow-2-2)

Để thực hiện lời gọi lồng nhau, JavaScript ghi nhớ ngữ cảnh thực thi hiện tại trong *stack ngữ cảnh thực thi*.

Ở đây chúng ta gọi cùng function `pow`, nhưng điều đó hoàn toàn không quan trọng. Quá trình là giống nhau cho tất cả các functions:

1. Ngữ cảnh hiện tại được "ghi nhớ" trên đỉnh stack.
2. Ngữ cảnh mới được tạo cho subcall.
3. Khi subcall hoàn thành – ngữ cảnh trước được pop khỏi stack, và việc thực thi của nó tiếp tục.

Đây là stack ngữ cảnh khi chúng ta vào subcall `pow(2, 2)`:

- Context: { x: 2, n: 2, at line 1 }
  pow(2, 2)
- Context: { x: 2, n: 3, at line 5 }
  pow(2, 3)

Ngữ cảnh thực thi hiện tại mới ở trên cùng (và in đậm), và các ngữ cảnh trước được ghi nhớ ở bên dưới.

Khi chúng ta hoàn thành subcall – việc tiếp tục ngữ cảnh trước rất dễ dàng, vì nó giữ cả hai biến và vị trí chính xác của code nơi nó dừng lại.

Xin lưu ý:

Ở đây trong hình chúng ta sử dụng từ "dòng", vì trong ví dụ của chúng ta chỉ có một subcall trong mỗi dòng, nhưng nhìn chung một dòng code có thể chứa nhiều subcall, như `pow(…) + pow(…) + somethingElse(…)`.

Vì vậy, sẽ chính xác hơn khi nói rằng việc thực thi tiếp tục "ngay sau subcall".

### [pow(2, 1)](#pow-2-1)

Quá trình lặp lại: một subcall mới được thực hiện ở dòng `5`, bây giờ với các đối số `x=2`, `n=1`.

Một ngữ cảnh thực thi mới được tạo, ngữ cảnh trước được đẩy lên đỉnh stack:

- Context: { x: 2, n: 1, at line 1 }
  pow(2, 1)
- Context: { x: 2, n: 2, at line 5 }
  pow(2, 2)
- Context: { x: 2, n: 3, at line 5 }
  pow(2, 3)

Có 2 ngữ cảnh cũ và 1 đang chạy cho `pow(2, 1)`.

### [Thoát](#the-exit)

Trong quá trình thực thi `pow(2, 1)`, không giống như trước, điều kiện `n == 1` là truthy, vì vậy nhánh đầu tiên của `if` hoạt động:

```
function pow(x, n) {
  if (n == 1) {
    return x;
  } else {
    return x * pow(x, n - 1);
  }
}
```

Không còn lời gọi lồng nhau nào nữa, vì vậy function hoàn thành, trả về `2`.

Khi function hoàn thành, ngữ cảnh thực thi của nó không còn cần thiết nữa, vì vậy nó được gỡ khỏi bộ nhớ. Ngữ cảnh trước được khôi phục từ đỉnh stack:

- Context: { x: 2, n: 2, at line 5 }
  pow(2, 2)
- Context: { x: 2, n: 3, at line 5 }
  pow(2, 3)

Việc thực thi `pow(2, 2)` tiếp tục. Nó có kết quả của subcall `pow(2, 1)`, vì vậy nó cũng có thể hoàn thành đánh giá `x * pow(x, n - 1)`, trả về `4`.

Sau đó ngữ cảnh trước được khôi phục:

- Context: { x: 2, n: 3, at line 5 }
  pow(2, 3)

Khi nó hoàn thành, chúng ta có kết quả `pow(2, 3) = 8`.

Độ sâu đệ quy trong trường hợp này là: **3**.

Như chúng ta có thể thấy từ các hình minh họa ở trên, độ sâu đệ quy bằng số lượng ngữ cảnh tối đa trong stack.

Lưu ý yêu cầu bộ nhớ. Các ngữ cảnh chiếm bộ nhớ. Trong trường hợp của chúng ta, nâng lên lũy thừa `n` thực sự cần bộ nhớ cho `n` ngữ cảnh, cho tất cả các giá trị nhỏ hơn của `n`.

Thuật toán dựa trên vòng lặp tiết kiệm bộ nhớ hơn:

```
function pow(x, n) {
  let result = 1;

  for (let i = 0; i < n; i++) {
    result *= x;
  }

  return result;
}
```

`pow` lặp sử dụng một ngữ cảnh duy nhất thay đổi `i` và `result` trong quá trình. Yêu cầu bộ nhớ của nó nhỏ, cố định và không phụ thuộc vào `n`.

**Bất kỳ đệ quy nào cũng có thể được viết lại thành vòng lặp. Biến thể vòng lặp thường có thể hiệu quả hơn.**

…Nhưng đôi khi việc viết lại không tầm thường, đặc biệt khi một function sử dụng các subcall đệ quy khác nhau tùy thuộc vào điều kiện và kết hợp kết quả của chúng hoặc khi phân nhánh phức tạp hơn. Và việc tối ưu có thể không cần thiết và hoàn toàn không xứng đáng với công sức.

Đệ quy có thể tạo ra code ngắn hơn, dễ hiểu và dễ hỗ trợ hơn. Tối ưu hóa không bắt buộc ở mọi nơi, chủ yếu chúng ta cần code tốt, đó là lý do tại sao nó được sử dụng.

## [Duyệt đệ quy](#recursive-traversals)

Một ứng dụng tuyệt vời khác của đệ quy là duyệt đệ quy.

Hãy tưởng tượng, chúng ta có một công ty. Cấu trúc nhân sự có thể được biểu diễn như một object:

```
let company = {
  sales: [{
    name: 'John',
    salary: 1000
  }, {
    name: 'Alice',
    salary: 1600
  }],

  development: {
    sites: [{
      name: 'Peter',
      salary: 2000
    }, {
      name: 'Alex',
      salary: 1800
    }],

    internals: [{
      name: 'Jack',
      salary: 1300
    }]
  }
};
```

Nói cách khác, một công ty có các phòng ban.

- Một phòng ban có thể có một mảng nhân viên. Ví dụ, phòng ban `sales` có 2 nhân viên: John và Alice.
- Hoặc một phòng ban có thể chia thành các phòng ban con, như `development` có hai nhánh: `sites` và `internals`. Mỗi nhánh có nhân viên riêng.
- Cũng có thể khi một phòng ban con phát triển, nó chia thành các phòng ban con-con (hoặc nhóm).

  Ví dụ, phòng ban `sites` trong tương lai có thể được chia thành các nhóm cho `siteA` và `siteB`. Và chúng, có khả năng, có thể chia nhỏ hơn nữa. Điều đó không có trong hình, chỉ là điều cần ghi nhớ.

Bây giờ hãy nói chúng ta muốn một function để tính tổng tất cả lương. Chúng ta có thể làm điều đó như thế nào?

Cách tiếp cận lặp không dễ, vì cấu trúc không đơn giản. Ý tưởng đầu tiên có thể là tạo một vòng lặp `for` trên `company` với vòng lặp con lồng nhau qua các phòng ban cấp 1. Nhưng sau đó chúng ta cần nhiều vòng lặp con lồng nhau hơn để duyệt qua nhân viên trong các phòng ban cấp 2 như `sites`… Và sau đó một vòng lặp con khác bên trong chúng cho các phòng ban cấp 3 có thể xuất hiện trong tương lai? Nếu chúng ta đặt 3-4 vòng lặp con lồng nhau trong code để duyệt một object, nó trở nên khá xấu.

Hãy thử đệ quy.

Như chúng ta có thể thấy, khi function của chúng ta nhận một phòng ban để tính tổng, có hai trường hợp có thể:

1. Hoặc đó là một phòng ban "đơn giản" với một *mảng* người – thì chúng ta có thể tính tổng lương trong một vòng lặp đơn giản.
2. Hoặc đó là một *object* với `N` phòng ban con – thì chúng ta có thể thực hiện `N` lời gọi đệ quy để tính tổng cho mỗi phòng ban con và kết hợp các kết quả.

Trường hợp 1 là cơ sở của đệ quy, trường hợp tầm thường, khi chúng ta nhận một mảng.

Trường hợp 2 khi chúng ta nhận một object là bước đệ quy. Một tác vụ phức tạp được chia thành các tác vụ con cho các phòng ban nhỏ hơn. Chúng có thể lần lượt chia nhỏ again, nhưng sớm hay muộn việc chia nhỏ sẽ kết thúc ở (1).

Thuật toán có lẽ thậm chí dễ đọc hơn từ code:

```
let company = { // the same object, compressed for brevity
  sales: [{name: 'John', salary: 1000}, {name: 'Alice', salary: 1600 }],
  development: {
    sites: [{name: 'Peter', salary: 2000}, {name: 'Alex', salary: 1800 }],
    internals: [{name: 'Jack', salary: 1300}]
  }
};

// The function to do the job
function sumSalaries(department) {
  if (Array.isArray(department)) { // case (1)
    return department.reduce((prev, current) => prev + current.salary, 0); // sum the array
  } else { // case (2)
    let sum = 0;
    for (let subdep of Object.values(department)) {
      sum += sumSalaries(subdep); // recursively call for subdepartments, sum the results
    }
    return sum;
  }
}

alert(sumSalaries(company)); // 7700
```

Code ngắn và dễ hiểu (hy vọng vậy?). Đó là sức mạnh của đệ quy. Nó cũng hoạt động cho bất kỳ mức độ lồng phòng ban con nào.

Đây là biểu đồ các lời gọi:

![](/article/recursion/recursive-salaries.svg)

Chúng ta có thể dễ dàng thấy nguyên tắc: đối với một object `{...}` các subcall được thực hiện, trong khi các mảng `[...]` là các "lá" của cây đệ quy, chúng cho kết quả trực tiếp.

Lưu ý rằng code sử dụng các tính năng thông minh mà chúng ta đã tìm hiểu trước đó:

- Phương thức `arr.reduce` được giải thích trong chương [Array methods](/array-methods) để tính tổng mảng.
- Vòng lặp `for(val of Object.values(obj))` để duyệt qua các giá trị object: `Object.values` trả về một mảng các giá trị đó.

## [Cấu trúc đệ quy](#recursive-structures)

Một cấu trúc dữ liệu đệ quy (được định nghĩa đệ quy) là một cấu trúc tự sao chép một phần của chính nó.

Chúng ta vừa thấy nó trong ví dụ về cấu trúc công ty ở trên.

Một *phòng ban* công ty là:

- Hoặc một mảng người.
- Hoặc một object với các *phòng ban*.

Đối với các nhà phát triển web, có những ví dụ được biết đến nhiều hơn: tài liệu HTML và XML.

Trong tài liệu HTML, một *thẻ HTML* có thể chứa một danh sách:

- Các đoạn văn bản.
- Các comment HTML.
- Các *thẻ HTML* khác (mà đến lượt chúng có thể chứa các đoạn văn bản/comment hoặc các thẻ khác v.v.).

Đó lại là một định nghĩa đệ quy.

Để hiểu rõ hơn, chúng ta sẽ tìm hiểu thêm một cấu trúc đệ quy có tên "Danh sách liên kết (Linked list)" có thể là một giải pháp thay thế tốt hơn cho mảng trong một số trường hợp.

### [Danh sách liên kết](#linked-list)

Hãy tưởng tượng, chúng ta muốn lưu trữ một danh sách đối tượng có thứ tự.

Lựa chọn tự nhiên sẽ là một mảng:

```
let arr = [obj1, obj2, obj3];
```

…Nhưng có một vấn đề với mảng. Các thao tác "xóa phần tử" và "chèn phần tử" tốn kém. Ví dụ, thao tác `arr.unshift(obj)` phải đánh số lại tất cả các phần tử để tạo chỗ cho `obj` mới, và nếu mảng lớn, nó mất thời gian. Tương tự với `arr.shift()`.

Chỉ có những sửa đổi cấu trúc không yêu cầu đánh số lại hàng loạt là những thao tác ở cuối mảng: `arr.push/pop`. Vì vậy mảng có thể khá chậm với hàng đợi lớn, khi chúng ta phải làm việc với phần đầu.

Thay vào đó, nếu chúng ta thực sự cần chèn/xóa nhanh, chúng ta có thể chọn một cấu trúc dữ liệu khác gọi là [danh sách liên kết](https://en.wikipedia.org/wiki/Linked_list).

*Phần tử danh sách liên kết* được định nghĩa đệ quy là một object với:

- `value`.
- Thuộc tính `next` tham chiếu đến *phần tử danh sách liên kết* tiếp theo hoặc `null` nếu đó là phần tử cuối.

Ví dụ:

```
let list = {
  value: 1,
  next: {
    value: 2,
    next: {
      value: 3,
      next: {
        value: 4,
        next: null
      }
    }
  }
};
```

Biểu diễn đồ họa của danh sách:

![](/article/recursion/linked-list.svg)

Code thay thế để tạo:

```
let list = { value: 1 };
list.next = { value: 2 };
list.next.next = { value: 3 };
list.next.next.next = { value: 4 };
list.next.next.next.next = null;
```

Ở đây chúng ta thậm chí có thể thấy rõ hơn rằng có nhiều object, mỗi object có `value` và `next` trỏ đến phần tử lân cận. Biến `list` là object đầu tiên trong chuỗi, vì vậy đi theo các con trỏ `next` từ nó chúng ta có thể đến bất kỳ phần tử nào.

Danh sách có thể dễ dàng chia thành nhiều phần và sau đó ghép lại:

```
let secondList = list.next.next;
list.next.next = null;
```

![](/article/recursion/linked-list-split.svg)

Để ghép:

```
list.next.next = secondList;
```

Và chắc chắn chúng ta có thể chèn hoặc xóa các mục ở bất kỳ vị trí nào.

Ví dụ, để thêm một giá trị mới vào đầu, chúng ta cần cập nhật head của danh sách:

```
let list = { value: 1 };
list.next = { value: 2 };
list.next.next = { value: 3 };
list.next.next.next = { value: 4 };

// prepend the new value to the list
list = { value: "new item", next: list };
```

![](/article/recursion/linked-list-0.svg)

Để xóa một giá trị từ giữa, thay đổi `next` của phần tử trước:

```
list.next = list.next.next;
```

![](/article/recursion/linked-list-remove-1.svg)

Chúng ta đã làm cho `list.next` nhảy qua `1` đến giá trị `2`. Giá trị `1` bây giờ bị loại khỏi chuỗi. Nếu nó không được lưu trữ ở bất kỳ đâu khác, nó sẽ tự động được gỡ khỏi bộ nhớ.

Không giống như mảng, không có đánh số lại hàng loạt, chúng ta có thể dễ dàng sắp xếp lại các phần tử.

Tự nhiên, danh sách không phải lúc nào cũng tốt hơn mảng. Nếu không mọi người sẽ chỉ sử dụng danh sách.

Nhược điểm chính là chúng ta không thể dễ dàng truy cập một phần tử theo số thứ tự. Trong mảng thì dễ: `arr[n]` là tham chiếu trực tiếp. Nhưng trong danh sách chúng ta cần bắt đầu từ phần tử đầu tiên và đi `next` `N` lần để lấy phần tử thứ N.

…Nhưng chúng ta không luôn cần các thao tác như vậy. Ví dụ, khi chúng ta cần một hàng đợi hoặc thậm chí một [deque](https://en.wikipedia.org/wiki/Double-ended_queue) – cấu trúc có thứ tự phải cho phép thêm/xóa phần tử rất nhanh từ cả hai đầu, nhưng truy cập vào giữa không cần thiết.

Danh sách có thể được nâng cao:

- Chúng ta có thể thêm thuộc tính `prev` ngoài `next` để tham chiếu phần tử trước, để di chuyển ngược dễ dàng.
- Chúng ta cũng có thể thêm một biến tên `tail` tham chiếu phần tử cuối cùng của danh sách (và cập nhật nó khi thêm/xóa phần tử từ cuối).
- …Cấu trúc dữ liệu có thể thay đổi theo nhu cầu của chúng ta.

## [Tổng kết](#summary)

Các thuật ngữ:

- *Đệ quy* là một thuật ngữ lập trình có nghĩa là gọi một function từ chính nó. Các function đệ quy có thể được sử dụng để giải quyết các tác vụ theo cách thanh lịch.

  Khi một function gọi chính nó, đó được gọi là *bước đệ quy*. *Cơ sở* của đệ quy là các đối số function làm cho tác vụ đơn giản đến mức function không thực hiện thêm lời gọi nào.
- Một [cấu trúc dữ liệu đệ quy](https://en.wikipedia.org/wiki/Recursive_data_type) là một cấu trúc dữ liệu có thể được định nghĩa bằng cách sử dụng chính nó.

  Ví dụ, danh sách liên kết có thể được định nghĩa là một cấu trúc dữ liệu bao gồm một object tham chiếu đến một danh sách (hoặc null).

  ```
  list = { value, next -> list }
  ```

  Các cây như cây phần tử HTML hoặc cây phòng ban từ chương này cũng tự nhiên đệ quy: chúng có các nhánh và mỗi nhánh có thể có các nhánh khác.

  Các function đệ quy có thể được sử dụng để duyệt chúng như chúng ta đã thấy trong ví dụ `sumSalary`.

Bất kỳ function đệ quy nào cũng có thể được viết lại thành function lặp. Và điều đó đôi khi cần thiết để tối ưu hóa. Nhưng đối với nhiều tác vụ, giải pháp đệ quy đủ nhanh và dễ viết, dễ hỗ trợ hơn.

---

---

## [Bài tập](#tasks)

### [Tính tổng tất cả các số đến số đã cho](#sum-all-numbers-till-the-given-one)

importance: 5

Viết một function `sumTo(n)` tính tổng các số `1 + 2 + ... + n`.

Ví dụ:

```
sumTo(1) = 1
sumTo(2) = 2 + 1 = 3
sumTo(3) = 3 + 2 + 1 = 6
sumTo(4) = 4 + 3 + 2 + 1 = 10
...
sumTo(100) = 100 + 99 + ... + 2 + 1 = 5050
```

Tạo 3 biến thể giải pháp:

1. Sử dụng vòng lặp for.
2. Sử dụng đệ quy, vì `sumTo(n) = n + sumTo(n-1)` cho `n > 1`.
3. Sử dụng [công thức cấp số cộng](https://en.wikipedia.org/wiki/Arithmetic_progression).

Ví dụ về kết quả:

```
function sumTo(n) { /*... your code ... */ }

alert( sumTo(100) ); // 5050
```

P.S. Biến thể giải pháp nào nhanh nhất? Chậm nhất? Tại sao?

P.P.S. Chúng ta có thể sử dụng đệ quy để tính `sumTo(100000)`?

solution

Giải pháp sử dụng vòng lặp:

```
function sumTo(n) {
  let sum = 0;
  for (let i = 1; i <= n; i++) {
    sum += i;
  }
  return sum;
}

alert( sumTo(100) );
```

Giải pháp sử dụng đệ quy:

```
function sumTo(n) {
  if (n == 1) return 1;
  return n + sumTo(n - 1);
}

alert( sumTo(100) );
```

Giải pháp sử dụng công thức: `sumTo(n) = n*(n+1)/2`:

```
function sumTo(n) {
  return n * (n + 1) / 2;
}

alert( sumTo(100) );
```

P.S. Tự nhiên, công thức là giải pháp nhanh nhất. Nó chỉ sử dụng 3 phép toán cho bất kỳ số `n` nào. Toán học giúp ích!

Biến thể vòng lặp đứng thứ hai về tốc độ. Trong cả biến thể đệ quy và vòng lặp chúng ta cộng cùng các số. Nhưng đệ quy liên quan đến các lời gọi lồng nhau và quản lý stack thực thi. Điều đó cũng tốn tài nguyên, vì vậy nó chậm hơn.

P.P.S. Một số engine hỗ trợ tối ưu hóa "tail call": nếu một lời gọi đệ quy là lời gọi cuối cùng trong function, không có tính toán nào khác được thực hiện, thì function bên ngoài sẽ không cần tiếp tục thực thi, vì vậy engine không cần ghi nhớ ngữ cảnh thực thi của nó. Điều đó loại bỏ gánh nặng bộ nhớ. Nhưng nếu engine JavaScript không hỗ trợ tối ưu hóa tail call (hầu hết không hỗ trợ), sẽ có lỗi: maximum stack size exceeded, vì thường có giới hạn về tổng kích thước stack.

### [Tính giai thừa](#calculate-factorial)

importance: 4

[Giai thừa](https://en.wikipedia.org/wiki/Factorial) của một số tự nhiên là số đó nhân với `"số trừ một"`, sau đó với `"số trừ hai"`, cứ tiếp tục cho đến `1`. Giai thừa của `n` được ký hiệu là `n!`

Chúng ta có thể viết định nghĩa giai thừa như sau:

```
n! = n * (n - 1) * (n - 2) * ...*1
```

Giá trị giai thừa cho các `n` khác nhau:

```
1! = 1
2! = 2 * 1 = 2
3! = 3 * 2 * 1 = 6
4! = 4 * 3 * 2 * 1 = 24
5! = 5 * 4 * 3 * 2 * 1 = 120
```

Tác vụ là viết một function `factorial(n)` tính `n!` sử dụng các lời gọi đệ quy.

```
alert( factorial(5) ); // 120
```

P.S. Gợi ý: `n!` có thể được viết là `n * (n-1)!` Ví dụ: `3! = 3*2! = 3*2*1! = 6`

solution

Theo định nghĩa, giai thừa `n!` có thể được viết là `n * (n-1)!`.

Nói cách khác, kết quả của `factorial(n)` có thể được tính bằng `n` nhân với kết quả của `factorial(n-1)`. Và lời gọi cho `n-1` có thể đệ quy xuống thấp hơn, thấp hơn, cho đến `1`.

```
function factorial(n) {
  return (n != 1) ? n * factorial(n - 1) : 1;
}

alert( factorial(5) ); // 120
```

Cơ sở của đệ quy là giá trị `1`. Chúng ta cũng có thể làm `0` thành cơ sở ở đây, không quan trọng lắm, nhưng cho thêm một bước đệ quy:

```
function factorial(n) {
  return n ? n * factorial(n - 1) : 1;
}

alert( factorial(5) ); // 120
```

### [Số Fibonacci](#fibonacci-numbers)

importance: 5

Dãy [số Fibonacci](https://en.wikipedia.org/wiki/Fibonacci_number) có công thức `Fn = Fn-1 + Fn-2`. Nói cách khác, số tiếp theo là tổng của hai số trước đó.

Hai số đầu tiên là `1`, sau đó `2(1+1)`, rồi `3(1+2)`, `5(2+3)` cứ tiếp tục: `1, 1, 2, 3, 5, 8, 13, 21...`.

Số Fibonacci liên quan đến [tỷ lệ vàng](https://en.wikipedia.org/wiki/Golden_ratio) và nhiều hiện tượng tự nhiên xung quanh chúng ta.

Viết một function `fib(n)` trả về số Fibonacci thứ `n`.

Ví dụ hoạt động:

```
function fib(n) { /* your code */ }

alert(fib(3)); // 2
alert(fib(7)); // 13
alert(fib(77)); // 5527939700884757
```

P.S. Function phải nhanh. Lời gọi `fib(77)` nên không quá một phần giây.

solution

Giải pháp đầu tiên chúng ta có thể thử ở đây là đệ quy.

Số Fibonacci là đệ quy theo định nghĩa:

```
function fib(n) {
  return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}

alert( fib(3) ); // 2
alert( fib(7) ); // 13
// fib(77); // will be extremely slow!
```

…Nhưng với các giá trị lớn của `n` nó rất chậm. Ví dụ, `fib(77)` có thể làm treo engine trong một thời gian, ăn hết tài nguyên CPU.

Đó là vì function thực hiện quá nhiều subcall. Các giá trị giống nhau được đánh giá lại nhiều lần.

Ví dụ, hãy xem một phần tính toán cho `fib(5)`:

```
...
fib(5) = fib(4) + fib(3)
fib(4) = fib(3) + fib(2)
...
```

Ở đây chúng ta có thể thấy rằng giá trị của `fib(3)` được cần cho cả `fib(5)` và `fib(4)`. Vì vậy `fib(3)` sẽ được gọi và đánh giá hai lần hoàn toàn độc lập.

Đây là toàn bộ cây đệ quy:

![](/task/fibonacci-numbers/fibonacci-recursion-tree.svg)

Chúng ta có thể thấy rõ ràng rằng `fib(3)` được đánh giá hai lần và `fib(2)` được đánh giá ba lần. Tổng lượng tính toán tăng nhanh hơn nhiều so với `n`, trở nên khổng lồ thậm chí cho `n=77`.

Chúng ta có thể tối ưu điều đó bằng cách ghi nhớ các giá trị đã được đánh giá: nếu giá trị của `fib(3)` được tính một lần, thì chúng ta có thể tái sử dụng nó trong các tính toán tương lai.

Một biến thể khác là từ bỏ đệ quy và sử dụng một thuật toán vòng lặp hoàn toàn khác.

Thay vì đi từ `n` xuống các giá trị thấp hơn, chúng ta có thể tạo một vòng lặp bắt đầu từ `1` và `2`, sau đó lấy `fib(3)` làm tổng của chúng, rồi `fib(4)` làm tổng của hai giá trị trước đó, rồi `fib(5)` và đi lên, cho đến khi nó đạt đến giá trị cần. Ở mỗi bước chúng ta chỉ cần ghi nhớ hai giá trị trước đó.

Đây là các bước của thuật toán mới chi tiết.

Bắt đầu:

```
// a = fib(1), b = fib(2), these values are by definition 1
let a = 1, b = 1;

// get c = fib(3) as their sum
let c = a + b;

/* we now have fib(1), fib(2), fib(3)
a  b  c
1, 1, 2
*/
```

Bây giờ chúng ta muốn lấy `fib(4) = fib(2) + fib(3)`.

Hãy dịch chuyển các biến: `a,b` sẽ là `fib(2),fib(3)`, và `c` sẽ là tổng của chúng:

```
a = b; // now a = fib(2)
b = c; // now b = fib(3)
c = a + b; // c = fib(4)

/* now we have the sequence:
   a  b  c
1, 1, 2, 3
*/
```

Bước tiếp theo cho một số thứ tự khác:

```
a = b; // now a = fib(3)
b = c; // now b = fib(4)
c = a + b; // c = fib(5)

/* now the sequence is (one more number):
      a  b  c
1, 1, 2, 3, 5
*/
```

…Cứ tiếp tục cho đến khi chúng ta lấy được giá trị cần. Điều đó nhanh hơn nhiều so với đệ quy và không liên quan đến tính toán trùng lặp.

Code đầy đủ:

```
function fib(n) {
  let a = 1;
  let b = 1;
  for (let i = 3; i <= n; i++) {
    let c = a + b;
    a = b;
    b = c;
  }
  return b;
}

alert( fib(3) ); // 2
alert( fib(7) ); // 13
alert( fib(77) ); // 5527939700884757
```

Vòng lặp bắt đầu với `i=3`, vì giá trị thứ nhất và thứ hai của dãy được hard-code vào các biến `a=1`, `b=1`.

Cách tiếp cận này được gọi là [dynamic programming bottom-up](https://en.wikipedia.org/wiki/Dynamic_programming).

### [Xuất danh sách liên kết đơn](#output-a-single-linked-list)

importance: 5

Hãy nói chúng ta có một danh sách liên kết đơn (như được mô tả trong chương [Đệ quy và stack](/recursion)):

```
let list = {
  value: 1,
  next: {
    value: 2,
    next: {
      value: 3,
      next: {
        value: 4,
        next: null
      }
    }
  }
};
```

Viết một function `printList(list)` xuất các mục danh sách từng cái một.

Tạo hai biến thể giải pháp: sử dụng vòng lặp và sử dụng đệ quy.

Cái nào tốt hơn: có đệ quy hay không có?

solution

Giải pháp dựa trên vòng lặp

#### Giải pháp dựa trên vòng lặp

Biến thể giải pháp dựa trên vòng lặp:

```
let list = {
  value: 1,
  next: {
    value: 2,
    next: {
      value: 3,
      next: {
        value: 4,
        next: null
      }
    }
  }
};

function printList(list) {
  let tmp = list;

  while (tmp) {
    alert(tmp.value);
    tmp = tmp.next;
  }

}

printList(list);
```

Xin lưu ý rằng chúng ta sử dụng một biến tạm thời `tmp` để duyệt qua danh sách. Về mặt kỹ thuật, chúng ta có thể sử dụng tham số function `list` thay vào đó:

```
function printList(list) {

  while(list) {
    alert(list.value);
    list = list.next;
  }

}
```

…Nhưng điều đó sẽ không khôn ngoan. Trong tương lai chúng ta có thể cần mở rộng một function, làm điều gì đó khác với danh sách. Nếu chúng ta thay đổi `list`, chúng ta mất khả năng đó.

Nói về tên biến tốt, `list` ở đây là bản thân danh sách. Phần tử đầu tiên của nó. Và nó nên giữ nguyên như vậy. Điều đó rõ ràng và đáng tin cậy.

Mặt khác, vai trò của `tmp` là duyệt danh sách, giống như `i` trong vòng lặp `for`.

Giải pháp đệ quy

#### Giải pháp đệ quy

Biến thể đệ quy của `printList(list)` theo logic đơn giản: để xuất một danh sách chúng ta nên xuất phần tử hiện tại `list`, sau đó làm tương tự cho `list.next`:

```
let list = {
  value: 1,
  next: {
    value: 2,
    next: {
      value: 3,
      next: {
        value: 4,
        next: null
      }
    }
  }
};

function printList(list) {

  alert(list.value); // output the current item

  if (list.next) {
    printList(list.next); // do the same for the rest of the list
  }

}

printList(list);
```

Bây giờ cái nào tốt hơn?

Về mặt kỹ thuật, vòng lặp hiệu quả hơn. Hai biến thể làm điều tương tự, nhưng vòng lặp không tốn tài nguyên cho các lời gọi function lồng nhau.

Mặt khác, biến thể đệ quy ngắn hơn và đôi khi dễ hiểu hơn.

### [Xuất danh sách liên kết đơn theo thứ tự ngược](#output-a-single-linked-list-in-the-reverse-order)

importance: 5

Xuất danh sách liên kết đơn từ tác vụ trước [Xuất danh sách liên kết đơn](/task/output-single-linked-list) theo thứ tự ngược.

Tạo hai giải pháp: sử dụng vòng lặp và sử dụng đệ quy.

solution

Sử dụng đệ quy

#### Sử dụng đệ quy

Logic đệ quy hơi phức tạp ở đây.

Chúng ta cần xuất phần còn lại của danh sách trước *sau đó* xuất phần hiện tại:

```
let list = {
  value: 1,
  next: {
    value: 2,
    next: {
      value: 3,
      next: {
        value: 4,
        next: null
      }
    }
  }
};

function printReverseList(list) {

  if (list.next) {
    printReverseList(list.next);
  }

  alert(list.value);
}

printReverseList(list);
```

Sử dụng vòng lặp

#### Sử dụng vòng lặp

Biến thể vòng lặp cũng hơi phức tạp hơn xuất trực tiếp.

Không có cách nào để lấy giá trị cuối cùng trong `list` của chúng ta. Chúng ta cũng không thể "đi ngược lại".

Vì vậy, điều chúng ta có thể làm là đi qua các mục theo thứ tự trực tiếp và ghi nhớ chúng trong một mảng, sau đó xuất những gì chúng ta đã ghi nhớ theo thứ tự ngược:

```
let list = {
  value: 1,
  next: {
    value: 2,
    next: {
      value: 3,
      next: {
        value: 4,
        next: null
      }
    }
  }
};

function printReverseList(list) {
  let arr = [];
  let tmp = list;

  while (tmp) {
    arr.push(tmp.value);
    tmp = tmp.next;
  }

  for (let i = arr.length - 1; i >= 0; i--) {
    alert( arr[i] );
  }
}

printReverseList(list);
```

Xin lưu ý rằng giải pháp đệ quy thực sự làm chính xác điều tương tự: nó duyệt danh sách, ghi nhớ các mục trong chuỗi các lời gọi lồng nhau (trong stack ngữ cảnh thực thi), và sau đó xuất chúng.
