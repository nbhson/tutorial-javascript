class Animal { constructor(name){ this.name=name; } speak(){ console.log(this.name+" makes noise"); } }
class Dog extends Animal { speak(){ super.speak(); console.log(this.name+" barks"); } }
new Dog("Rex").speak();
console.log(Dog.prototype instanceof Animal);
