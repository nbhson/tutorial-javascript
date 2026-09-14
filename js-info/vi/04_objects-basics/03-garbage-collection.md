# Garbage collection

> Nguồn: [https://javascript.info/garbage-collection](https://javascript.info/garbage-collection)

<!-- fetched: 2026-09-14 -->

Quản lý bộ nhớ trong JavaScript được thực hiện tự động và vô hình đối với chúng ta. Chúng ta tạo primitives, objects, functions… Tất cả những thứ đó chiếm bộ nhớ.

Những gì xảy ra khi thứ gì đó không còn cần thiết nữa? Làm thế nào để động cơ JavaScript phát hiện ra và dọn dẹp nó?

## [Reachability](#reachability)

Khái niệm chính của quản lý bộ nhớ trong JavaScript là *reachability*.

Nói một cách đơn giản, các giá trị "reachable" là những giá trị có thể truy cập được hoặc usable theo cách nào đó. Chúng được đảm bảo sẽ được lưu trữ trong bộ nhớ.

1. Có một tập hợp cơ bản các giá trị inherently reachable, không thể bị xóa vì những lý do hiển nhiên.

   Ví dụ:

   - Function đang thực thi hiện tại, các biến cục bộ và parameters của nó.
   - Các hàm khác trên chain của nested calls hiện tại, các biến cục bộ và parameters của chúng.
   - Global variables.
   - (cũng có một số cái internal khác)

   Các giá trị này được gọi là *roots*.

2. Bất kỳ giá trị nào khác được coi là reachable nếu nó reachable từ một root bằng một tham chiếu hoặc bằng một chain của các tham chiếu.

   Ví dụ, nếu có một object trong một global variable, và object đó có một property tham chiếu đến một object khác, *object đó* được coi là reachable. Và những object mà nó tham chiếu đến cũng reachable. Cácví dụví dụ chi tiết sẽ theo sau.

Có một quá trình background trong động cơ JavaScript được gọi là [garbage collector](https://en.wikipedia.org/wiki/Garbage_collection_(computer_science)). Nó giám sát tất cả các object và xóa những object đã trở nên unreachable.

## [Mộtví dụví dụ đơn giản](#a-simple-example)

Đây làví dụví dụ đơn giản nhất:

```
// user có một tham chiếu đến object
let user = {
  name: "John"
};
```

![](/article/garbage-collection/memory-user-john.svg)

Ở đây arrow depicts một object reference. Global variable `"user"` tham chiếu đến object `{name: "John"}` (chúng ta sẽ gọi nó là John để ngắn gọn). Property `"name"` của John lưu trữ một primitive, vì vậy nó được vẽ bên trong object.

Nếu giá trị của `user` bị ghi đè, tham chiếu bị mất:

```
user = null;
```

![](/article/garbage-collection/memory-user-john-lost.svg)

Bây giờ John trở nên unreachable. Không có cách nào để truy cập nó, không có tham chiếu nào đến nó. Garbage collector sẽ junk the data và giải phóng bộ nhớ.

## [Hai references](#two-references)

Giờ hãy tưởng tượng chúng ta sao chép reference từ `user` sang `admin`:

```
// user có một tham chiếu đến object
let user = {
  name: "John"
};

let admin = user;
```

![](/article/garbage-collection/memory-user-john-admin.svg)

Bây giờ nếu chúng ta làm tương tự:

```
user = null;
```

…Thì object vẫn reachable thông qua global variable `admin`, vì vậy nó phải ở lại trong bộ nhớ. Nếu chúng ta ghi đè `admin` quá, thì nó có thể bị xóa.

## [Interlinked objects](#interlinked-objects)

Giờ mộtví dụví dụ phức tạp hơn. Family:

```
function marry(man, woman) {
  woman.husband = man;
  man.wife = woman;

  return {
    father: man,
    mother: woman
  }
}

let family = marry({
  name: "John"
}, {
  name: "Ann"
});
```

Function `marry` "marry" hai object bằng cách cho chúng các tham chiếu đến nhau và trả về một object mới chứa cả hai.

Cấu trúc bộ nhớ resulting:

![](/article/garbage-collection/family.svg)

Tính đến thời điểm này, tất cả các object đều reachable.

Bây giờ hãy xóa hai references:

```
delete family.father;
delete family.mother.husband;
```

![](/article/garbage-collection/family-delete-refs.svg)

Không đủ để chỉ xóa một trong hai references này, vì tất cả các object vẫn sẽ reachable.

Nhưng nếu chúng ta xóa cả hai, thì chúng ta có thể thấy rằng John không còn incoming reference nào nữa:

![](/article/garbage-collection/family-no-father.svg)

 outgoing references không quan trọng. Chỉ incoming ones có thể làm cho một object reachable. Vì vậy, John giờ là unreachable và sẽ bị xóa khỏi bộ nhớ cùng với tất cả dữ liệu của nó mà cũng trở nên unaccessible.

Sau garbage collection:

![](/article/garbage-collection/family-no-father-2.svg)

## [Unreachable island](#unreachable-island)

Có thể một whole island của interlinked objects trở nên unreachable và bị xóa khỏi bộ nhớ.

Source object là giống như ở trên. Sau đó:

```
family = null;
```

Bức tranh trong bộ nhớ trở thành:

![](/article/garbage-collection/family-no-family.svg)

Ví dụ này minh họa tầm quan trọng của khái niệm reachability.

Rõ ràng là John và Ann vẫn được liên kết, cả hai đều có incoming references. Nhưng điều đó không đủ.

Object `"family"` trước đó đã bị unlink khỏi root, không có reference nào đến nó nữa, vì vậy cả island trở nên unreachable và sẽ bị xóa.

## [Internal algorithms](#internal-algorithms)

Thuật toán garbage collection cơ bản được gọi là "mark-and-sweep".

Các bước "garbage collection" sau được thực hiện định kỳ:

- Garbage collector lấy roots và "mark" (nhớ) chúng.
- Sau đó nó visit và "mark" tất cả các references từ chúng.
- Sau đó nó visit các marked objects và mark *their* references. Tất cả các visited objects được nhớ, để không visit cùng một object hai lần trong tương lai.
- …Và cứ thế cho đến khi mọi reachable (từ các roots) references đều được visit.
- Tất cả các object ngoại trừ những marked ones bị xóa.

Ví dụ, hãy tưởng tượng object structure của chúng ta trông như thế này:

![](/article/garbage-collection/garbage-collection-1.svg)

Chúng ta có thể thấy rõ một "unreachable island" ở bên phải. Giờ hãy xem garbage collector "mark-and-sweep" xử lý nó như thế nào.

Bước đầu tiên mark các roots:

![](/article/garbage-collection/garbage-collection-2.svg)

Sau đó chúng ta follow their references và mark referenced objects:

![](/article/garbage-collection/garbage-collection-3.svg)

…Và tiếp tục follow further references, trong khi có thể:

![](/article/garbage-collection/garbage-collection-4.svg)

Bây giờ các objects không thể được visit trong quá trình được coi là unreachable và sẽ bị xóa:

![](/article/garbage-collection/garbage-collection-5.svg)

Chúng ta cũng có thể tưởng tượng quá trình như đang đổ một big bucket of paint từ các roots, chảy qua tất cả các references và mark tất cả các objects reachable. Những cái không được mark sau đó bị xóa.

Đó là khái niệm về cách garbage collection hoạt động. Các động cơ JavaScript áp dụng nhiều optimizations để làm cho nó chạy nhanh hơn và không giới thiệu bất kỳ delays nào vào code execution.

Một số optimizations:

- **Generational collection** – objects được chia thành hai sets: "new ones" và "old ones". Trong typical code, nhiều objects có short life span: chúng xuất hiện, làm việc của chúng và chết nhanh, vì vậy có ý nghĩa để track new objects và clear memory từ chúng nếu đó là trường hợp. Những cái tồn tại đủ lâu, trở thành "old" và được examine ít often hơn.
- **Incremental collection** – nếu có nhiều objects, và chúng ta cố gắng walk và mark toàn bộ object set cùng một lúc, nó có thể tốn một số thời gian và giới thiệu visible delays trong execution. Vì vậy engine chia small set of existing objects thành nhiều parts. Và sau đó clear these parts một sauanother. Có nhiều small garbage collections thay vì một total one. Điều đó yêu cầu một số extra bookkeeping giữa chúng để track changes, nhưng chúng ta có nhiều tiny delays thay vì một big one.
- **Idle-time collection** – garbage collector cố gắng chạy chỉ trong khi CPU idle, để giảm thiểu possible effect lên execution.

Có các optimizations và flavours khác của các thuật toán garbage collection. Như nhiều như tôi muốn mô tả chúng ở đây, tôi phải hold off, vì các engines khác nhau triển khai các tweaks và techniques khác nhau. Và, quan trọng hơn, mọi thứ thay đổi khi các engines phát triển, vì vậy studying deeper "in advance", mà không có real need là probably không worth that. Trừ khi, tất nhiên, đó là một matter of pure interest, sau đó sẽ có một số links cho bạn bên dưới.

## [Tổng kết](#summary)

Những điều chính cần biết:

- Garbage collection được thực hiện tự động. Chúng ta không thể force hoặc prevent it.
- Objects được retained trong bộ nhớ trong khi chúng reachable.
- Being referenced không giống như being reachable (từ một root): một pack của interlinked objects có thể trở nên unreachable như một whole, như chúng ta đã thấy trongví dụví dụ ở trên.

Các engines hiện đại triển khai các algorithms garbage collection advanced.

Cuốn sách tổng quát "The Garbage Collection Handbook: The Art of Automatic Memory Management" (R. Jones et al) bao phủ một số algorithms trong số chúng.

Nếu bạn familiar với low-level programming, thông tin chi tiết hơn về V8's garbage collector là trong article [A tour of V8: Garbage Collection](https://jayconrod.com/posts/55/a-tour-of-v8-garbage-collection).

[V8 blog](https://v8.dev/) cũng publishes articles về các changes trong memory management from time to time. Naturally, để learn more về garbage collection, bạn nên chuẩn bị bằng cách học về V8 internals nói chung và đọc blog của [Vyacheslav Egorov](https://mrale.ph) who worked as one of the V8 engineers. Tôi đang nói: "V8", vì nó được covered best bởi các articles trên internet. Đối với các engines khác, nhiều approaches là similar, nhưng garbage collection differs in many aspects.

In-depth knowledge of engines là good khi bạn cần low-level optimizations. Nó sẽ là wise để plan that như là bước tiếp theo sau khi bạn familiar với language.
