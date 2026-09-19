# 第三方组件声明 / Third-Party Notices

`graph-3d.html` 是一个自包含的单文件页面，其中**内嵌**了以下第三方开源库的压缩代码。
根据各自许可证的要求，其版权声明与许可条款在此一并列出。

> 说明：这些库的许可证都要求「在软件的所有副本或实质性部分中保留上述版权声明和许可声明」。
> 由于本项目的 HTML 文件内嵌了它们的代码，因此本文件即是对该要求的履行。

---

## 1. three.js

- **版本**：r183
- **许可证**：MIT
- **项目地址**：https://github.com/mrdoob/three.js

```
The MIT License

Copyright © 2010-2026 three.js authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

## 2. 3d-force-graph

- **版本**：v1.80.0
- **许可证**：MIT
- **项目地址**：https://github.com/vasturiano/3d-force-graph
- **说明**：该库的 standalone 构建已打包 three.js、d3-force-3d 等依赖

```
MIT License

Copyright (c) 2017 Vasco Asturiano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 3. 工具致谢（未随本仓库分发）

以下工具用于**生成**图谱数据，其代码并未包含在本仓库中，此处仅作来源说明：

- **[Graphify](https://github.com/Graphify-Labs/graphify)** —— Apache-2.0 —— 从知识树抽取知识图谱
- **Python / NetworkX / tree-sitter** —— 由 Graphify 内部使用

---

## 自有代码

除上述第三方组件外，本项目中由作者编写的部分（页面结构、样式、交互逻辑、星场与标签层实现、3D 视图构建脚本）以 MIT 许可证发布，详见 [`LICENSE`](./LICENSE)。
