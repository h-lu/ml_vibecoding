// 侧边栏折叠功能 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // 初始化侧边栏折叠功能
    function initSidebarCollapse() {
        const sidebar = document.querySelector('.sidebar');
        if (!sidebar) return;
        
        // 查找所有章节链接
        const chapterLinks = sidebar.querySelectorAll('.sidebar-item .sidebar-link');
        const currentPath = window.location.pathname;
        
        // 为每个链接添加数据属性和事件监听器
        chapterLinks.forEach((link, index) => {
            const item = link.closest('.sidebar-item');
            const href = link.getAttribute('href') || '';
            
            // 判断是否为章节首页 (如 ch01/index.html)
            const isChapterIndex = href.includes('/index.html') || href.match(/ch\d+\/$/);
            
            if (isChapterIndex) {
                // 标记为章节首页
                item.setAttribute('data-bs-level', '1');
                item.classList.add('chapter-header');
                
                // 检查是否为当前章节
                const chapterMatch = href.match(/ch(\d+)/);
                const currentChapterMatch = currentPath.match(/ch(\d+)/);
                
                if (chapterMatch && currentChapterMatch && 
                    chapterMatch[1] === currentChapterMatch[1]) {
                    item.classList.add('current-chapter', 'expanded');
                }
                
                // 添加点击事件
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    toggleChapter(item);
                    
                    // 如果点击的是当前页面，不需要跳转
                    if (href !== currentPath) {
                        setTimeout(() => {
                            window.location.href = href;
                        }, 150);
                    }
                });
                
            } else {
                // 标记为子章节
                item.setAttribute('data-bs-level', '2');
                item.classList.add('chapter-section');
                
                // 检查是否为当前页面
                if (href === currentPath || currentPath.includes(href)) {
                    item.classList.add('active');
                    
                    // 确保父章节展开
                    const parentChapter = findParentChapter(item);
                    if (parentChapter) {
                        parentChapter.classList.add('expanded', 'current-chapter');
                    }
                }
            }
        });
        
        // 初始化：隐藏所有非当前章节的子项
        hideNonCurrentChapterSections();
    }
    
    // 切换章节展开/折叠状态
    function toggleChapter(chapterItem) {
        const isExpanded = chapterItem.classList.contains('expanded');
        
        // 首先折叠所有其他章节
        document.querySelectorAll('.sidebar-item[data-bs-level="1"]').forEach(item => {
            if (item !== chapterItem) {
                item.classList.remove('expanded');
            }
        });
        
        // 切换当前章节状态
        if (isExpanded) {
            chapterItem.classList.remove('expanded');
        } else {
            chapterItem.classList.add('expanded');
        }
        
        // 更新当前章节标记
        document.querySelectorAll('.sidebar-item[data-bs-level="1"]').forEach(item => {
            item.classList.remove('current-chapter');
        });
        chapterItem.classList.add('current-chapter');
    }
    
    // 查找父章节
    function findParentChapter(sectionItem) {
        let current = sectionItem.previousElementSibling;
        while (current) {
            if (current.classList.contains('sidebar-item') && 
                current.getAttribute('data-bs-level') === '1') {
                return current;
            }
            current = current.previousElementSibling;
        }
        return null;
    }
    
    // 隐藏非当前章节的子项
    function hideNonCurrentChapterSections() {
        const allSections = document.querySelectorAll('.sidebar-item[data-bs-level="2"]');
        allSections.forEach(section => {
            const parentChapter = findParentChapter(section);
            if (parentChapter && !parentChapter.classList.contains('expanded')) {
                section.style.display = 'none';
            } else {
                section.style.display = 'block';
            }
        });
    }
    
    // 监听展开状态变化
    function observeExpansionChanges() {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && 
                    mutation.attributeName === 'class') {
                    const target = mutation.target;
                    if (target.getAttribute('data-bs-level') === '1') {
                        updateSectionVisibility(target);
                    }
                }
            });
        });
        
        document.querySelectorAll('.sidebar-item[data-bs-level="1"]').forEach(item => {
            observer.observe(item, { attributes: true });
        });
    }
    
    // 更新子章节显示状态
    function updateSectionVisibility(chapterItem) {
        const isExpanded = chapterItem.classList.contains('expanded');
        let nextSibling = chapterItem.nextElementSibling;
        
        while (nextSibling && nextSibling.getAttribute('data-bs-level') === '2') {
            if (isExpanded) {
                nextSibling.style.display = 'block';
                setTimeout(() => {
                    nextSibling.style.opacity = '1';
                    nextSibling.style.maxHeight = '50px';
                }, 10);
            } else {
                nextSibling.style.opacity = '0';
                nextSibling.style.maxHeight = '0';
                setTimeout(() => {
                    nextSibling.style.display = 'none';
                }, 300);
            }
            nextSibling = nextSibling.nextElementSibling;
        }
    }
    
    // 键盘导航支持
    function addKeyboardSupport() {
        document.addEventListener('keydown', function(e) {
            if (e.target.closest('.sidebar')) {
                if (e.key === 'Enter' || e.key === ' ') {
                    const focusedLink = document.activeElement;
                    if (focusedLink && focusedLink.closest('.sidebar-item[data-bs-level="1"]')) {
                        e.preventDefault();
                        focusedLink.click();
                    }
                }
            }
        });
    }
    
    // 初始化所有功能
    function initialize() {
        // 等待侧边栏渲染完成
        setTimeout(() => {
            initSidebarCollapse();
            observeExpansionChanges();
            addKeyboardSupport();
        }, 100);
    }
    
    // 如果页面已经加载完成，直接初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }
});

// 页面导航时保持状态
window.addEventListener('beforeunload', function() {
    const expandedChapters = [];
    document.querySelectorAll('.sidebar-item[data-bs-level="1"].expanded').forEach(item => {
        const link = item.querySelector('.sidebar-link');
        if (link) {
            expandedChapters.push(link.getAttribute('href'));
        }
    });
    localStorage.setItem('quarto-sidebar-expanded', JSON.stringify(expandedChapters));
});

// 页面加载时恢复状态
window.addEventListener('load', function() {
    const expandedChapters = JSON.parse(localStorage.getItem('quarto-sidebar-expanded') || '[]');
    expandedChapters.forEach(href => {
        const link = document.querySelector(`.sidebar-link[href="${href}"]`);
        if (link) {
            const item = link.closest('.sidebar-item');
            if (item) {
                item.classList.add('expanded');
            }
        }
    });
});
