/**
 * 字体大小选择器 - 为Quarto Book添加动态字体大小调节功能
 * 类似 ChatGPT 页面的阅读设置
 */

(function() {
    'use strict';

    // 配置选项
    const CONFIG = {
        // 可选字体大小（以rem为单位）
        fontSizes: [
            { label: '极小', value: '0.875', key: 'xs' },
            { label: '小', value: '1.0', key: 'sm' },
            { label: '正常', value: '1.125', key: 'md' },
            { label: '大', value: '1.25', key: 'lg' },
            { label: '极大', value: '1.5', key: 'xl' }
        ],
        defaultSize: 'md',
        storageKey: 'quarto-font-size-preference',
        // CSS变量前缀
        cssPrefix: '--font-size-'
    };

    // 状态管理
    let currentFontSize = CONFIG.defaultSize;
    let fontSelectorPanel = null;

    /**
     * 初始化字体大小选择器
     */
    function initFontSizeSelector() {
        // 从localStorage恢复用户设置
        loadUserPreference();
        
        // 创建字体大小控制面板
        createFontSizePanel();
        
        // 应用当前字体大小
        applyFontSize(currentFontSize);
        
        // 绑定事件监听器
        bindEventListeners();
        
        console.log('[字体选择器] 初始化完成');
    }

    /**
     * 从localStorage加载用户偏好设置
     */
    function loadUserPreference() {
        const saved = localStorage.getItem(CONFIG.storageKey);
        if (saved && CONFIG.fontSizes.find(size => size.key === saved)) {
            currentFontSize = saved;
        }
    }

    /**
     * 保存用户偏好设置到localStorage
     */
    function saveUserPreference(sizeKey) {
        localStorage.setItem(CONFIG.storageKey, sizeKey);
    }

    /**
     * 创建字体大小控制面板
     */
    function createFontSizePanel() {
        // 创建按钮容器
        const controlsContainer = document.createElement('div');
        controlsContainer.className = 'font-size-controls';
        controlsContainer.innerHTML = `
            <button class="font-size-toggle-btn" 
                    title="调整字体大小" 
                    aria-label="字体大小设置">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M7 20V4h9.5M7 8h8M15 20V8h6M19 8H15"/>
                </svg>
            </button>
        `;

        // 创建字体大小面板
        const panel = document.createElement('div');
        panel.className = 'font-size-selector-panel';
        panel.innerHTML = `
            <div class="font-size-panel-header">
                <span class="panel-title">字体大小</span>
                <button class="panel-close" aria-label="关闭面板">×</button>
            </div>
            <div class="font-size-options">
                ${CONFIG.fontSizes.map(size => `
                    <button class="font-size-option ${size.key === currentFontSize ? 'active' : ''}" 
                            data-size="${size.key}" 
                            title="设置为${size.label}字体">
                        <span class="size-label">${size.label}</span>
                        <span class="size-preview" style="font-size: ${parseFloat(size.value) * 0.8}rem;">文</span>
                    </button>
                `).join('')}
            </div>
            <div class="font-size-panel-footer">
                <button class="reset-font-size" title="重置为默认字体大小">
                    重置默认
                </button>
            </div>
        `;

        // 添加到页面合适位置
        addToPage(controlsContainer, panel);
        
        fontSelectorPanel = panel;
    }

    /**
     * 将控件添加到页面
     */
    function addToPage(controlsContainer, panel) {
        // 尝试添加到导航栏
        const navbar = document.querySelector('.navbar .navbar-nav, .quarto-title-banner .quarto-title-tools, .sidebar .sidebar-tools');
        
        if (navbar) {
            // 添加到导航工具区域
            navbar.appendChild(controlsContainer);
        } else {
            // 创建浮动控件
            controlsContainer.classList.add('floating-font-controls');
            document.body.appendChild(controlsContainer);
        }

        // 将面板添加到body
        document.body.appendChild(panel);
    }

    /**
     * 绑定事件监听器
     */
    function bindEventListeners() {
        const toggleBtn = document.querySelector('.font-size-toggle-btn');
        const closeBtn = fontSelectorPanel.querySelector('.panel-close');
        const resetBtn = fontSelectorPanel.querySelector('.reset-font-size');
        const optionBtns = fontSelectorPanel.querySelectorAll('.font-size-option');

        // 切换面板显示
        toggleBtn?.addEventListener('click', togglePanel);
        closeBtn?.addEventListener('click', hidePanel);

        // 字体大小选项
        optionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const sizeKey = e.currentTarget.dataset.size;
                selectFontSize(sizeKey);
            });
        });

        // 重置按钮
        resetBtn?.addEventListener('click', () => {
            selectFontSize(CONFIG.defaultSize);
        });

        // 点击外部关闭面板
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.font-size-selector-panel') && 
                !e.target.closest('.font-size-toggle-btn')) {
                hidePanel();
            }
        });

        // 键盘快捷键支持
        document.addEventListener('keydown', handleKeyboardShortcuts);
    }

    /**
     * 处理键盘快捷键
     */
    function handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + 加号：增大字体
        if ((e.ctrlKey || e.metaKey) && (e.key === '=' || e.key === '+')) {
            e.preventDefault();
            increaseFontSize();
        }
        
        // Ctrl/Cmd + 减号：减小字体
        if ((e.ctrlKey || e.metaKey) && e.key === '-') {
            e.preventDefault();
            decreaseFontSize();
        }
        
        // Ctrl/Cmd + 0：重置字体大小
        if ((e.ctrlKey || e.metaKey) && e.key === '0') {
            e.preventDefault();
            selectFontSize(CONFIG.defaultSize);
        }

        // Esc键关闭面板
        if (e.key === 'Escape') {
            hidePanel();
        }
    }

    /**
     * 增大字体大小
     */
    function increaseFontSize() {
        const currentIndex = CONFIG.fontSizes.findIndex(size => size.key === currentFontSize);
        if (currentIndex < CONFIG.fontSizes.length - 1) {
            selectFontSize(CONFIG.fontSizes[currentIndex + 1].key);
        }
    }

    /**
     * 减小字体大小
     */
    function decreaseFontSize() {
        const currentIndex = CONFIG.fontSizes.findIndex(size => size.key === currentFontSize);
        if (currentIndex > 0) {
            selectFontSize(CONFIG.fontSizes[currentIndex - 1].key);
        }
    }

    /**
     * 选择字体大小
     */
    function selectFontSize(sizeKey) {
        const size = CONFIG.fontSizes.find(s => s.key === sizeKey);
        if (!size) return;

        currentFontSize = sizeKey;
        applyFontSize(sizeKey);
        updateUI(sizeKey);
        saveUserPreference(sizeKey);

        // 触发自定义事件
        document.dispatchEvent(new CustomEvent('fontSizeChanged', {
            detail: { size: size.value, key: sizeKey, label: size.label }
        }));
    }

    /**
     * 应用字体大小到页面
     */
    function applyFontSize(sizeKey) {
        const size = CONFIG.fontSizes.find(s => s.key === sizeKey);
        if (!size) return;

        const root = document.documentElement;
        
        // 设置主要字体大小变量
        root.style.setProperty('--quarto-font-size-base', `${size.value}rem`);
        
        // 设置各级标题的比例字体大小
        const headingSizes = {
            h1: parseFloat(size.value) * 2.25,
            h2: parseFloat(size.value) * 1.875,
            h3: parseFloat(size.value) * 1.5,
            h4: parseFloat(size.value) * 1.25,
            h5: parseFloat(size.value) * 1.125,
            h6: parseFloat(size.value) * 1.0
        };

        Object.entries(headingSizes).forEach(([tag, fontSize]) => {
            root.style.setProperty(`--quarto-${tag}-font-size`, `${fontSize}rem`);
        });

        // 设置其他元素的字体大小
        root.style.setProperty('--quarto-small-font-size', `${parseFloat(size.value) * 0.875}rem`);
        root.style.setProperty('--quarto-code-font-size', `${parseFloat(size.value) * 0.875}rem`);

        // 添加字体大小类到body
        document.body.className = document.body.className.replace(/font-size-\w+/g, '');
        document.body.classList.add(`font-size-${sizeKey}`);
    }

    /**
     * 更新UI状态
     */
    function updateUI(sizeKey) {
        const options = fontSelectorPanel.querySelectorAll('.font-size-option');
        options.forEach(option => {
            option.classList.toggle('active', option.dataset.size === sizeKey);
        });
    }

    /**
     * 切换面板显示
     */
    function togglePanel() {
        fontSelectorPanel.classList.toggle('show');
    }

    /**
     * 隐藏面板
     */
    function hidePanel() {
        fontSelectorPanel.classList.remove('show');
    }

    /**
     * 显示面板
     */
    function showPanel() {
        fontSelectorPanel.classList.add('show');
    }

    // 等待DOM加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFontSizeSelector);
    } else {
        initFontSizeSelector();
    }

    // 暴露全局API（可选）
    window.QuartoFontSizeSelector = {
        increaseFontSize,
        decreaseFontSize,
        selectFontSize,
        getCurrentFontSize: () => currentFontSize,
        showPanel,
        hidePanel,
        togglePanel
    };

})();
