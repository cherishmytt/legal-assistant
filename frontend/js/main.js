// ==================== 全局变量 ====================
let currentReport = null;
let consultationHistory = [];

// ==================== 页面加载 ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成');
    
    // 初始化
    initNavigation();
    initEventListeners();
    loadHistory();
});

// ==================== 导航功能 ====================
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 更新导航状态
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // 切换页面
            const targetId = this.getAttribute('href').substring(1);
            showSection(targetId);
        });
    });
}

function showSection(sectionId) {
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }
}

// ==================== 事件监听 ====================
function initEventListeners() {
    // 提交按钮
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.addEventListener('click', handleSubmit);
    
    // 回车提交
    const questionInput = document.getElementById('questionInput');
    questionInput.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            handleSubmit();
        }
    });
    
    // 清空历史
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearHistory);
    }
}

// ==================== 提交处理 ====================
async function handleSubmit() {
    const questionInput = document.getElementById('questionInput');
    const question = questionInput.value.trim();
    
    if (!question) {
        showToast('请输入您的法律问题', 'warning');
        return;
    }
    
    // 禁用按钮
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<div class="progress-spinner"></div><span>分析中...</span>';
    
    // 显示进度条
    showProgress();
    
    try {
        // 模拟进度更新
        updateProgress(1, 25);
        await sleep(500);
        
        updateProgress(2, 50);
        await sleep(500);
        
        updateProgress(3, 75);
        
        // 调用API
        const response = await fetch('http://localhost:5000/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });
        
        if (!response.ok) {
            throw new Error('服务器响应错误');
        }
        
        const data = await response.json();
        
        updateProgress(4, 100);
        await sleep(500);
        
        // 隐藏进度条
        hideProgress();
        
        // 显示结果
        currentReport = data;
        displayResult(data);
        
        // 保存到历史
        saveToHistory(question, data);
        
        showToast('分析完成！', 'success');
        
    } catch (error) {
        console.error('分析失败:', error);
        hideProgress();
        showToast('分析失败，请稍后重试', 'error');
    } finally {
        // 恢复按钮
        submitBtn.disabled = false;
        submitBtn.innerHTML = `
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>开始分析</span>
        `;
    }
}

// ==================== 进度条控制 ====================
function showProgress() {
    const progressSection = document.getElementById('progressSection');
    const resultSection = document.getElementById('resultSection');
    
    progressSection.style.display = 'block';
    resultSection.style.display = 'none';
    
    // 重置进度
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = '0%';
    
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach(step => {
        step.classList.remove('active', 'completed');
    });
}

function updateProgress(step, percentage) {
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = percentage + '%';
    
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach((stepEl, index) => {
        if (index < step - 1) {
            stepEl.classList.add('completed');
            stepEl.classList.remove('active');
        } else if (index === step - 1) {
            stepEl.classList.add('active');
            stepEl.classList.remove('completed');
        } else {
            stepEl.classList.remove('active', 'completed');
        }
    });
}

function hideProgress() {
    const progressSection = document.getElementById('progressSection');
    setTimeout(() => {
        progressSection.style.display = 'none';
    }, 500);
}

// ==================== 显示结果 ====================
function displayResult(data) {
    console.log('显示结果，数据:', data);
    
    const resultSection = document.getElementById('resultSection');
    resultSection.style.display = 'flex';
    
    // 滚动到结果区域
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // 验证数据结构
    if (!data || !data.ai_analysis) {
        console.error('数据格式错误:', data);
        showToast('数据格式错误', 'error');
        return;
    }
    
    console.log('AI分析数据:', data.ai_analysis);
    
    // 显示行动建议（增强版）
    displayActionSuggestions(data.ai_analysis);
    
    // 显示案由分析
    displayCaseAnalysis(data.ai_analysis);
    
    // 显示争议点
    displayDisputePoints(data.ai_analysis);
    
    // 显示法律依据
    displayRelevantLaws(data.relevant_laws);
}

function displayActionSuggestions(aiAnalysis) {
    console.log('显示行动建议，数据:', aiAnalysis);
    
    const container = document.getElementById('actionSuggestions');
    
    // 安全获取行动建议
    const suggestions = aiAnalysis['行动建议'] || aiAnalysis['action_suggestions'] || aiAnalysis.suggestions || [];
    
    console.log('行动建议列表:', suggestions);
    
    if (!Array.isArray(suggestions) || suggestions.length === 0) {
        container.innerHTML = `
            <div class="action-item">
                <div class="action-number">1</div>
                <div class="action-content">
                    <div class="action-title">📋 收集证据材料</div>
                    <div class="action-description">收集和保存所有相关证据材料</div>
                </div>
            </div>
            <div class="action-item">
                <div class="action-number">2</div>
                <div class="action-content">
                    <div class="action-title">👨‍⚖️ 寻求专业帮助</div>
                    <div class="action-description">咨询专业律师，了解详细的法律规定</div>
                </div>
            </div>
            <div class="action-item">
                <div class="action-number">3</div>
                <div class="action-content">
                    <div class="action-title">⚖️ 法律程序</div>
                    <div class="action-description">根据具体情况选择协商、调解、仲裁或诉讼</div>
                </div>
            </div>
        `;
        return;
    }
    
    // 增强的行动建议内容
    const enhancedSuggestions = suggestions.map((suggestion, index) => {
        let title = '';
        let description = String(suggestion);
        
        // 根据内容生成标题和描述
        if (description.includes('证据')) {
            title = '📋 收集证据材料';
        } else if (description.includes('律师') || description.includes('咨询')) {
            title = '👨‍⚖️ 寻求专业帮助';
        } else if (description.includes('协商') || description.includes('调解')) {
            title = '🤝 尝试协商解决';
        } else if (description.includes('仲裁') || description.includes('诉讼')) {
            title = '⚖️ 法律程序';
        } else if (description.includes('时效')) {
            title = '⏰ 注意时效';
        } else {
            title = `📌 建议 ${index + 1}`;
        }
        
        return { title, description };
    });
    
    container.innerHTML = enhancedSuggestions.map((item, index) => `
        <div class="action-item">
            <div class="action-number">${index + 1}</div>
            <div class="action-content">
                <div class="action-title">${item.title}</div>
                <div class="action-description">${item.description}</div>
            </div>
        </div>
    `).join('');
}

function displayCaseAnalysis(aiAnalysis) {
    console.log('显示案由分析，数据:', aiAnalysis);
    
    const container = document.getElementById('caseAnalysis');
    const analysis = aiAnalysis['案由分析'] || aiAnalysis['case_analysis'] || aiAnalysis.analysis || '暂无分析';
    container.innerHTML = `<p>${analysis}</p>`;
}

function displayDisputePoints(aiAnalysis) {
    console.log('显示争议点，数据:', aiAnalysis);
    
    const container = document.getElementById('disputePoints');
    const points = aiAnalysis['核心争议点'] || aiAnalysis['dispute_points'] || aiAnalysis.points || [];
    
    if (!Array.isArray(points) || points.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary);">暂无争议点分析</p>';
        return;
    }
    
    container.innerHTML = points.map(point => `
        <div class="dispute-item">
            <svg class="dispute-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div class="dispute-text">${point}</div>
        </div>
    `).join('');
}

function displayRelevantLaws(laws) {
    console.log('显示法律依据，数据:', laws);
    
    const container = document.getElementById('relevantLaws');
    
    if (!laws || !Array.isArray(laws) || laws.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary);">暂无相关法律依据</p>';
        return;
    }
    
    container.innerHTML = laws.map(law => {
        // 安全获取属性
        const category = law.category || '法律依据';
        const title = law.title || law.name || '相关法律';
        const lawsList = law.laws || [];
        const procedures = law.procedures || [];
        
        return `
            <div class="law-item">
                <div class="law-header">
                    <span class="law-category">${category}</span>
                    <h3 class="law-title">${title}</h3>
                </div>
                <div class="law-content">
                    ${lawsList.length > 0 ? lawsList.map(lawDoc => `
                        <div class="law-section">
                            <div class="law-section-title">${lawDoc.name || '法律条文'}</div>
                            <div class="law-articles">
                                ${(lawDoc.articles || []).map(article => `
                                    <div class="law-article">
                                        <div class="article-number">${article.number || ''}</div>
                                        <div class="article-content">${article.content || ''}</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('') : '<p style="color: var(--text-secondary); padding: 1rem;">暂无具体法律条文</p>'}
                    
                    ${procedures.length > 0 ? `
                        <div class="law-section">
                            <div class="law-section-title">处理流程</div>
                            <div class="law-procedures">
                                ${procedures.map(proc => `
                                    <div class="procedure-item">
                                        <svg class="procedure-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                        <div class="procedure-text">${proc}</div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

// ==================== 历史记录 ====================
function saveToHistory(question, report) {
    const historyItem = {
        id: Date.now(),
        question: question,
        report: report,
        timestamp: new Date().toLocaleString('zh-CN')
    };
    
    consultationHistory.unshift(historyItem);
    
    // 限制历史记录数量
    if (consultationHistory.length > 50) {
        consultationHistory = consultationHistory.slice(0, 50);
    }
    
    // 保存到localStorage
    try {
        localStorage.setItem('consultationHistory', JSON.stringify(consultationHistory));
        console.log('历史记录已保存');
    } catch (e) {
        console.error('保存历史记录失败:', e);
    }
    
    // 更新历史列表显示
    displayHistory();
}

function loadHistory() {
    try {
        const saved = localStorage.getItem('consultationHistory');
        if (saved) {
            consultationHistory = JSON.parse(saved);
            console.log(`加载了 ${consultationHistory.length} 条历史记录`);
        }
    } catch (e) {
        console.error('加载历史记录失败:', e);
        consultationHistory = [];
    }
    displayHistory();
}

function displayHistory() {
    const container = document.getElementById('historyList');
    
    if (!container) {
        console.warn('历史记录容器不存在');
        return;
    }
    
    if (consultationHistory.length === 0) {
        container.innerHTML = `
            <div class="history-empty">
                <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <p class="empty-text">暂无咨询历史</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = consultationHistory.map(item => {
        // 安全获取数据
        const question = item.question || '未知问题';
        const timestamp = item.timestamp || '';
        
        // 安全获取预览内容
        let preview = '暂无分析';
        try {
            if (item.report && item.report.ai_analysis) {
                preview = item.report.ai_analysis['案由分析'] || 
                         item.report.ai_analysis['case_analysis'] || 
                         item.report.summary || 
                         '暂无分析';
            }
        } catch (e) {
            console.warn('获取预览内容失败:', e);
        }
        
        // 截断预览文本
        if (preview.length > 100) {
            preview = preview.substring(0, 100) + '...';
        }
        
        return `
            <div class="history-item" data-id="${item.id}">
                <div class="history-header">
                    <div class="history-question">${escapeHtml(question)}</div>
                    <div class="history-time">${escapeHtml(timestamp)}</div>
                </div>
                <div class="history-preview">
                    ${escapeHtml(preview)}
                </div>
                <div class="history-actions">
                    <button class="history-btn view-btn" onclick="viewHistory(${item.id})">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" stroke-width="2"/>
                            <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" stroke-width="2"/>
                        </svg>
                        查看详情
                    </button>
                    <button class="history-btn delete-btn" onclick="deleteHistory(${item.id})">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        删除
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function viewHistory(id) {
    const item = consultationHistory.find(h => h.id === id);
    if (!item) {
        showToast('历史记录不存在', 'error');
        return;
    }
    
    try {
        // 切换到首页
        showSection('home');
        document.querySelector('.nav-link[href="#home"]').classList.add('active');
        document.querySelector('.nav-link[href="#history"]').classList.remove('active');
        
        // 填充问题
        document.getElementById('questionInput').value = item.question;
        
        // 显示结果
        currentReport = item.report;
        displayResult(item.report);
        
        // 滚动到结果
        setTimeout(() => {
            const resultSection = document.getElementById('resultSection');
            if (resultSection) {
                resultSection.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            }
        }, 300);
        
        showToast('已加载历史记录', 'success');
    } catch (e) {
        console.error('查看历史记录失败:', e);
        showToast('加载失败', 'error');
    }
}

function deleteHistory(id) {
    if (confirm('确定要删除这条记录吗？')) {
        try {
            consultationHistory = consultationHistory.filter(h => h.id !== id);
            localStorage.setItem('consultationHistory', JSON.stringify(consultationHistory));
            displayHistory();
            showToast('已删除', 'success');
        } catch (e) {
            console.error('删除历史记录失败:', e);
            showToast('删除失败', 'error');
        }
    }
}

function clearHistory() {
    if (confirm('确定要清空所有历史记录吗？此操作不可恢复。')) {
        try {
            consultationHistory = [];
            localStorage.removeItem('consultationHistory');
            displayHistory();
            showToast('历史记录已清空', 'success');
        } catch (e) {
            console.error('清空历史记录失败:', e);
            showToast('清空失败', 'error');
        }
    }
}

// ==================== 工具函数 ====================
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ==================== Toast 提示 ====================
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ==================== 工具函数 ====================
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function displayQuestionAssessment(aiAnalysis) {
    const assessment = aiAnalysis['问题评估'] || {};
    
    if (assessment['需要澄清']) {
        // 在结果区域顶部显示提示
        const resultSection = document.getElementById('resultSection');
        const existingAlert = resultSection.querySelector('.clarification-alert');
        
        if (existingAlert) {
            existingAlert.remove();
        }
        
        const clarificationQuestions = assessment['澄清问题'] || [];
        
        const alertHtml = `
            <div class="clarification-alert" style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; align-items: start; gap: 1rem;">
                    <svg style="width: 24px; height: 24px; flex-shrink: 0; margin-top: 2px;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <div style="flex: 1;">
                        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem; font-weight: 600;">
                            ⚠️ 需要补充信息
                        </h3>
                        <p style="margin: 0 0 1rem 0; opacity: 0.95;">
                            您的问题信息不够完整，为了给您提供更准确的法律建议，请补充以下信息：
                        </p>
                        ${clarificationQuestions.length > 0 ? `
                            <ul style="margin: 0; padding-left: 1.5rem; opacity: 0.95;">
                                ${clarificationQuestions.map(q => `<li style="margin: 0.5rem 0;">${escapeHtml(q)}</li>`).join('')}
                            </ul>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
        
        resultSection.insertAdjacentHTML('afterbegin', alertHtml);
    }
}

function displayRiskWarnings(aiAnalysis) {
    const warnings = aiAnalysis['风险提示'] || [];
    
    if (warnings.length === 0) {
        return;
    }
    
    // 查找或创建风险提示容器
    let container = document.getElementById('riskWarnings');
    
    if (!container) {
        // 在行动建议后面创建风险提示区域
        const actionCard = document.querySelector('.result-card');
        if (actionCard) {
            const warningCard = document.createElement('div');
            warningCard.className = 'result-card';
            warningCard.innerHTML = `
                <div class="card-header">
                    <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <h2 class="card-title">风险提示</h2>
                </div>
                <div class="card-content" id="riskWarnings"></div>
            `;
            actionCard.parentNode.insertBefore(warningCard, actionCard.nextSibling);
            container = document.getElementById('riskWarnings');
        }
    }
    
    if (container) {
        container.innerHTML = warnings.map(warning => `
            <div class="risk-item" style="
                display: flex;
                align-items: start;
                gap: 1rem;
                padding: 1rem;
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                border-radius: 8px;
                margin-bottom: 1rem;
            ">
                <svg style="width: 20px; height: 20px; color: #ff9800; flex-shrink: 0; margin-top: 2px;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <div style="flex: 1; color: #856404;">
                    ${escapeHtml(warning)}
                </div>
            </div>
        `).join('');
    }
}
