# TypeScript 高级类型系统详解

TypeScript 的类型系统是其最强大的特性之一，它不仅提供了基本的类型检查，还支持许多高级类型特性，让我们能够编写更安全、更可维护的代码。

标签：TypeScript, 类型系统, 前端开发, JavaScript

## 联合类型与交叉类型

### 联合类型 (Union Types)

联合类型表示一个值可以是几种类型之一：

```typescript
type StringOrNumber = string | number;

function formatValue(value: StringOrNumber): string {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  return value.toString();
}
```

### 交叉类型 (Intersection Types)

交叉类型将多个类型合并为一个类型：

```typescript
interface Person {
  name: string;
  age: number;
}

interface Employee {
  employeeId: string;
  department: string;
}

type PersonEmployee = Person & Employee;

const employee: PersonEmployee = {
  name: "张三",
  age: 30,
  employeeId: "E001",
  department: "开发部"
};
```

## 泛型 (Generics)

泛型允许我们创建可重用的组件，这些组件可以处理多种类型：

```typescript
function identity<T>(arg: T): T {
  return arg;
}

// 使用泛型
const stringResult = identity<string>("hello");
const numberResult = identity<number>(42);

// 类型推断
const autoResult = identity("world"); // TypeScript 自动推断为 string
```

### 泛型约束

```typescript
interface Lengthwise {
  length: number;
}

function loggingIdentity<T extends Lengthwise>(arg: T): T {
  console.log(arg.length); // 现在我们知道它有 length 属性
  return arg;
}

loggingIdentity("hello"); // ✅ 字符串有 length 属性
loggingIdentity([1, 2, 3]); // ✅ 数组有 length 属性
// loggingIdentity(3); // ❌ 数字没有 length 属性
```

## 条件类型 (Conditional Types)

条件类型根据条件选择类型：

```typescript
type NonNullable<T> = T extends null | undefined ? never : T;

type Example1 = NonNullable<string | null>; // string
type Example2 = NonNullable<number | undefined>; // number
```

### 分布式条件类型

```typescript
type ToArray<T> = T extends any ? T[] : never;

type StringArray = ToArray<string>; // string[]
type NumberArray = ToArray<number>; // number[]
type UnionArray = ToArray<string | number>; // string[] | number[]
```

## 映射类型 (Mapped Types)

映射类型基于旧类型创建新类型：

```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

type Partial<T> = {
  [P in keyof T]?: T[P];
};

interface User {
  id: number;
  name: string;
  email: string;
}

type ReadonlyUser = Readonly<User>;
type PartialUser = Partial<User>;
```

### 自定义映射类型

```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<User>;
// {
//   getId: () => number;
//   getName: () => string;
//   getEmail: () => string;
// }
```

## 模板字面量类型

TypeScript 4.1 引入了模板字面量类型：

```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;

type ClickEvent = EventName<"click">; // "onClick"
type HoverEvent = EventName<"hover">; // "onHover"

// 更复杂的例子
type CSSProperty = "margin" | "padding" | "border";
type CSSDirection = "top" | "right" | "bottom" | "left";

type CSSPropertyWithDirection = `${CSSProperty}-${CSSDirection}`;
// "margin-top" | "margin-right" | "margin-bottom" | "margin-left" | 
// "padding-top" | "padding-right" | "padding-bottom" | "padding-left" | 
// "border-top" | "border-right" | "border-bottom" | "border-left"
```

## 实用工具类型

TypeScript 提供了许多内置的工具类型：

```typescript
interface Todo {
  title: string;
  description: string;
  completed: boolean;
  createdAt: Date;
}

// Pick - 选择特定属性
type TodoPreview = Pick<Todo, "title" | "completed">;

// Omit - 排除特定属性
type TodoInfo = Omit<Todo, "completed" | "createdAt">;

// Record - 创建具有特定键值类型的对象类型
type PageInfo = Record<"home" | "about" | "contact", { title: string; url: string }>;

// ReturnType - 获取函数返回类型
function createUser() {
  return { id: 1, name: "张三", email: "zhangsan@example.com" };
}

type User = ReturnType<typeof createUser>; // { id: number; name: string; email: string; }
```

## 类型守卫 (Type Guards)

类型守卫帮助 TypeScript 在运行时确定类型：

```typescript
// 自定义类型守卫
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function processValue(value: unknown) {
  if (isString(value)) {
    // 在这个块中，TypeScript 知道 value 是 string
    console.log(value.toUpperCase());
  }
}

// 使用 in 操作符
interface Bird {
  fly(): void;
}

interface Fish {
  swim(): void;
}

function move(animal: Bird | Fish) {
  if ("fly" in animal) {
    animal.fly(); // TypeScript 知道这是 Bird
  } else {
    animal.swim(); // TypeScript 知道这是 Fish
  }
}
```

## 最佳实践

1. **优先使用类型推断**：让 TypeScript 自动推断类型，只在必要时显式声明。

2. **使用严格模式**：在 `tsconfig.json` 中启用 `strict` 模式。

3. **避免使用 `any`**：尽量使用更具体的类型或 `unknown`。

4. **合理使用泛型**：不要过度使用泛型，保持代码的可读性。

5. **利用工具类型**：充分利用 TypeScript 内置的工具类型。

## 总结

TypeScript 的高级类型系统为我们提供了强大的工具来编写类型安全的代码。通过掌握联合类型、交叉类型、泛型、条件类型、映射类型等特性，我们可以构建更加健壮和可维护的应用程序。

记住，类型系统的目标是在编译时捕获错误，提高代码质量，而不是增加复杂性。合理使用这些高级特性，可以让我们的代码既安全又优雅。
