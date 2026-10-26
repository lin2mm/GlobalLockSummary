# -*- coding: utf-8 -*-
import json, re

with open("build.mjs", "r", encoding="utf-8") as f:
    code = f.read()

# 目标：在 lockPage(fam, lang) 中，当 matchedSamples 存在时，根据样本的分类为每个卡片打上分类锚点与类别属性，并在顶部生成极简工业微导航条。

# 我们先写一个函数注入或者替换 lockPage 中 matchedSamples 的部分
# 查看原本的：
# let gallerySectionHtml = '';
# if (matchedSamples.length > 0) {
#   const sampleCards = matchedSamples.map((s) => { ...
