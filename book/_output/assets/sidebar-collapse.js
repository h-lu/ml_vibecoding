/**
 * 侧边栏手风琴效果 - ChatGPT 风格
 * 为 Quarto Book 侧边栏添加手风琴折叠功能
 */

(function() {
    'use strict';
    
    // 等待DOM加载完成
    document.addEventListener('DOMContentLoaded', function() {
        initSidebarAccordion();
    });
    
    function initSidebarAccordion() {
        // 查找侧边栏容器
        const sidebar = document.querySelector('.sidebar-navigation, .quarto-sidebar, .sidebar');
        if (!sidebar) {
            console.log('Sidebar not found, retrying...');
            // 如果侧边栏还没有加载，稍后重试
            setTimeout(initSidebarAccordion, 500);
            return;
        }
        
        console.log('Initializing sidebar accordion...');
        
        // 处理现有的 Quarto 导航结构
        setupQuartoAccordion(sidebar);
        
        // 如果Quarto还没有完全加载，监听变化
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    setupQuartoAccordion(sidebar);
                }
            });
        });
        
        observer.observe(sidebar, {
            childList: true,
            subtree: true
        });
    }
    
    function setupQuartoAccordion(sidebar) {
        // 查找所有的章节容器
        const sectionItems = sidebar.querySelectorAll('.sidebar-item');
        const processedSections = new Set();
        
        sectionItems.forEach(function(item, index) {
            // 跳过已处理的项目
            if (processedSections.has(item)) return;
            
            const link = item.querySelector('a');
            if (!link) return;
            
            const href = link.getAttribute('href');
            
            // 检查这是否是一个章节标题（通常以 index.html 结尾或者是主要章节）
            if (href && (href.includes('/index.html') || isChapterHeader(link.textContent))) {
                processedSections.add(item);
                convertToAccordionSection(item, index);
            }
        });
        
        // 默认折叠所有章节，除了当前活动的章节
        collapseAllSections(sidebar);
        
        // 展开包含当前页面的章节
        expandCurrentSection(sidebar);
    }
    
    function isChapterHeader(text) {
        // 检查文本是否像章节标题（包含"第"字或"Chapter"或只有数字等）
        const chapterPatterns = [
            /第\s*\d+\s*章/,     // 第1章
            /Chapter\s*\d+/i,   // Chapter 1
            /^\d+\s*[\.、]\s*/,  // 1. 或 1、
            /^\d+\s*$/          // 纯数字
        ];
        
        return chapterPatterns.some(pattern => pattern.test(text.trim()));
    }
    
    function convertToAccordionSection(sectionItem, index) {
        // 如果已经处理过，跳过
        if (sectionItem.classList.contains('accordion-processed')) {
            return;
        }
        
        sectionItem.classList.add('accordion-processed');
        sectionItem.classList.add('sidebar-section-header');
        
        // 添加展开/收起图标
        const chevron = document.createElement('span');
        chevron.className = 'chevron';
        chevron.innerHTML = '▼';
        sectionItem.appendChild(chevron);
        
        // 查找该章节的子项目
        const nextItems = [];
        let nextSibling = sectionItem.nextElementSibling;
        
        while (nextSibling) {
            const nextLink = nextSibling.querySelector('a');
            if (nextLink) {
                const nextHref = nextLink.getAttribute('href');
                // 如果下一个项目也是章节标题，停止收集
                if (nextHref && (nextHref.includes('/index.html') || isChapterHeader(nextLink.textContent))) {
                    break;
                }
                nextItems.push(nextSibling);
            }
            nextSibling = nextSibling.nextElementSibling;
        }
        
        // 创建内容容器
        if (nextItems.length > 0) {
            const contentContainer = document.createElement('div');
            contentContainer.className = 'sidebar-section-content collapsed';
            contentContainer.id = 'section-content-' + index;
            
            // 将子项目移动到容器中
            nextItems.forEach(function(item) {
                item.classList.add('sidebar-subsection-item');
                contentContainer.appendChild(item);
            });
            
            // 将容器插入到章节标题后面
            sectionItem.parentNode.insertBefore(contentContainer, sectionItem.nextSibling);
            
            // 添加点击事件
            sectionItem.style.cursor = 'pointer';
            sectionItem.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                toggleSection(sectionItem, contentContainer);
            });
            
            // 默认收起
            sectionItem.classList.add('collapsed');
        }
    }
    
    function toggleSection(headerItem, contentContainer) {
        const isCollapsed = headerItem.classList.contains('collapsed');
        
        if (isCollapsed) {
            // 展开
            headerItem.classList.remove('collapsed');
            contentContainer.classList.remove('collapsed');
            contentContainer.classList.add('expanded');
            contentContainer.style.maxHeight = contentContainer.scrollHeight + 'px';
        } else {
            // 收起
            headerItem.classList.add('collapsed');
            contentContainer.classList.remove('expanded');
            contentContainer.classList.add('collapsed');
            contentContainer.style.maxHeight = '0px';
        }
        
        // 手风琴效果：收起其他章节
        collapseOtherSections(headerItem);
    }
    
    function collapseOtherSections(currentHeader) {
        const sidebar = currentHeader.closest('.sidebar-navigation, .quarto-sidebar, .sidebar');
        if (!sidebar) return;
        
        const allHeaders = sidebar.querySelectorAll('.sidebar-section-header');
        allHeaders.forEach(function(header) {
            if (header !== currentHeader && !header.classList.contains('collapsed')) {
                const contentId = header.nextElementSibling;
                if (contentId && contentId.classList.contains('sidebar-section-content')) {
                    header.classList.add('collapsed');
                    contentId.classList.remove('expanded');
                    contentId.classList.add('collapsed');
                    contentId.style.maxHeight = '0px';
                }
            }
        });
    }
    
    function collapseAllSections(sidebar) {
        const headers = sidebar.querySelectorAll('.sidebar-section-header');
        headers.forEach(function(header) {
            header.classList.add('collapsed');
            const content = header.nextElementSibling;
            if (content && content.classList.contains('sidebar-section-content')) {
                content.classList.add('collapsed');
                content.classList.remove('expanded');
                content.style.maxHeight = '0px';
            }
        });
    }
    
    function expandCurrentSection(sidebar) {
        // 查找当前活动的页面
        const activeItem = sidebar.querySelector('.sidebar-item.active, .sidebar-item-text.active') || 
                          sidebar.querySelector('[aria-current="page"]');
        
        if (activeItem) {
            // 查找包含当前页面的章节
            let container = activeItem.closest('.sidebar-section-content');
            if (container) {
                const header = container.previousElementSibling;
                if (header && header.classList.contains('sidebar-section-header')) {
                    header.classList.remove('collapsed');
                    container.classList.remove('collapsed');
                    container.classList.add('expanded');
                    container.style.maxHeight = container.scrollHeight + 'px';
                }
            }
        }
        
        // 如果没有找到活动项目，可以根据URL来确定
        const currentPath = window.location.pathname;
        const sidebarLinks = sidebar.querySelectorAll('a[href]');
        
        sidebarLinks.forEach(function(link) {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href.replace('.html', ''))) {
                link.closest('.sidebar-item')?.classList.add('active');
                
                // 展开包含此链接的章节
                let container = link.closest('.sidebar-section-content');
                if (container) {
                    const header = container.previousElementSibling;
                    if (header && header.classList.contains('sidebar-section-header')) {
                        header.classList.remove('collapsed');
                        container.classList.remove('collapsed');
                        container.classList.add('expanded');
                        container.style.maxHeight = container.scrollHeight + 'px';
                    }
                }
            }
        });
    }
    
    // 导出函数供外部使用
    window.SidebarAccordion = {
        init: initSidebarAccordion,
        expandCurrentSection: expandCurrentSection,
        collapseAllSections: collapseAllSections
    };
    
})();

// 页面路由变化时重新初始化（单页应用场景）
if (typeof window !== 'undefined') {
    let lastUrl = location.href;
    new MutationObserver(() => {
        const url = location.href;
        if (url !== lastUrl) {
            lastUrl = url;
            setTimeout(() => {
                if (window.SidebarAccordion) {
                    window.SidebarAccordion.expandCurrentSection(
                        document.querySelector('.sidebar-navigation, .quarto-sidebar, .sidebar')
                    );
                }
            }, 100);
        }
    }).observe(document, { subtree: true, childList: true });
}