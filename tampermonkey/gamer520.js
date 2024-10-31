// ==UserScript==
// @name         Gamer520 enhancement
// @namespace    http://tampermonkey.net/
// @version      1.1
// @description  游戏详情页快速搜索 steam 详情
// @author       xp9477
// @match        https://www.gamer520.com/*.html
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gamer520.com
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 获取<title>标签中的内容
    var fullTitle = document.title;
    // 提取第一个|前面的文本
    var gameTitle = fullTitle.split('|')[0].trim();

    // 创建按钮元素
    var button = document.createElement('button');
    button.innerHTML = 'Steam'; // 文本
    button.style.position = 'fixed'; // 位置固定
    button.style.bottom = '20px';
    button.style.left = '20px';
    button.style.padding = '10px 20px'; // 内边距
    button.style.backgroundColor = '#0078d7'; // 蓝色背景
    button.style.color = 'white'; // 白色文字
    button.style.border = 'none'; // 无边框
    button.style.borderRadius = '5px'; // 圆角
    button.style.cursor = 'pointer'; // 鼠标指针变"手指"
    button.style.zIndex = '9999'; // 处于页面顶层，避免遮挡

    // 按钮点击事件，跳转到Steam搜索页面
    button.onclick = function() {
        window.open('https://store.steampowered.com/search/?term=' + encodeURIComponent(gameTitle));
    };

    // 将按钮添加到页面上
    document.body.appendChild(button);
})();
