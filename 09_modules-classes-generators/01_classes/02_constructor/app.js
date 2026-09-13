class User {
  constructor(name, age){ this.name=name; this.age=age; console.log("constructor", name); }
}
const u = new User("An", 20);
console.log(u);
// subclass must call super
class Admin extends User {
  constructor(name, age, role){ super(name, age); this.role=role; }
}
console.log(new Admin("B", 25, "admin"));
