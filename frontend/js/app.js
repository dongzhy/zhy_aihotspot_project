/**
 * AI 热点雷达 - 前端逻辑
 */

const API_BASE = 'http://localhost:8000/api';

let trendChart = null;
let categoryChart = null;

async function loadDashboard() {
    try {
        const [hotspotsRes, trendsRes, categoriesRes] = await Promise.all([
            fetch(`${API_BASE}/hotspots`),
            fetch(`${API_BASE}/trends`),
            fetch(`${API_BASE}/categories`),
        ]);

        const hotspotsData = await hotspotsRes.json();
        const trendsData = await trendsRes.json();
        const categoriesData = await categoriesRes.json();

        updateStats(hotspotsData.items);
        renderHotspots(hotspotsData.items);
        renderTrendChart(trendsData);
        renderCategoryChart(categoriesData);

        document.getElementById('update-time').textContent = new Date().toLocaleTimeString('zh-CN');

    } catch (error) {
        console.error('加载数据失败:', error);
        showOfflineMode();
    }
}

function updateStats(hotspots) {
    const total = hotspots.length;
    const avgHeat = hotspots.length > 0
        ? (hotspots.reduce((sum, h) => sum + h.heat_score, 0) / hotspots.length).toFixed(1)
        : 0;
    const positiveCount = hotspots.filter(h => h.sentiment === 'positive').length;
    const positivePct = total > 0 ? ((positiveCount / total) * 100).toFixed(0) : 0;

    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-avg-heat').textContent = avgHeat;
    document.getElementById('stat-positive').textContent = positivePct + '%';
}

function renderHotspots(hotspots) {
    const container = document.getElementById('hotspots-container');
    container.innerHTML = '';

    if (!hotspots || hotspots.length === 0) {
        container.innerHTML = `
            <div class="p-8 text-center text-slate-500">
                <i class="fas fa-inbox text-4xl mb-4 opacity-30"></i>
                <p>暂无热点数据</p>
            </div>
        `;
        return;
    }

    hotspots.forEach((hotspot, index) => {
        const sentimentColor = getSentimentColor(hotspot.sentiment);
        const sentimentLabel = getSentimentLabel(hotspot.sentiment);
        const heatColor = getHeatColor(hotspot.heat_score);

        const card = document.createElement('div');
        card.className = `hotspot-card bg-slate-800/30 border border-slate-700/30 rounded-xl p-5 mb-4 hover:bg-slate-800/50 hover:border-slate-600 transition-all cursor-pointer group`;
        card.onclick = () => viewHotspotDetail(hotspot.id);

        card.innerHTML = `
            <div class="flex justify-between items-start mb-3">
                <span class="text-xs font-mono text-slate-500">#${hotspot.id}</span>
                <span class="text-xs font-bold ${sentimentColor} bg-${sentimentColor.replace('text-', '')}/10 px-2 py-0.5 rounded">
                    ${sentimentLabel}
                </span>
            </div>
            <h4 class="text-lg font-bold text-white mb-2 group-hover:text-cyan-400 transition-colors line-clamp-2">
                ${hotspot.title}
            </h4>
            <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2">
                    <span class="text-xs text-slate-400 flex items-center gap-1">
                        <i class="fas fa-fire"></i>
                        <span class="font-mono text-${heatColor}">${hotspot.heat_score}</span>
                    </span>
                    <span class="text-xs text-slate-500">· ${hotspot.source}</span>
                </div>
            </div>
            <div class="w-full bg-slate-700/50 h-1.5 rounded-full overflow-hidden">
                <div class="heat-bar h-full rounded-full" style="width: ${hotspot.heat_score}%"></div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-700/30">
                <p class="text-xs text-slate-400 italic max-h-[3em] overflow-hidden">
                    ${hotspot.ai_summary || 'AI 正在分析该热点...'}
                </p>
            </div>
        `;
        container.appendChild(card);
    });
}

function renderTrendChart(data) {
    const ctx = document.getElementById('trendChart').getContext('2d');

    if (trendChart) {
        trendChart.destroy();
    }

    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: '热度指数',
                data: data.map(d => d.heat_score),
                borderColor: '#06b6d4',
                backgroundColor: 'rgba(6, 182, 212, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointHoverRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1,
                }
            },
            scales: {
                x: {
                    grid: { color: '#1e293b' },
                    ticks: { color: '#94a3b8', font: { size: 11 } }
                },
                y: {
                    grid: { color: '#1e293b' },
                    ticks: { color: '#94a3b8', font: { size: 11 } },
                    min: 0,
                    max: 100
                }
            }
        }
    });
}

function renderCategoryChart(data) {
    const ctx = document.getElementById('categoryChart').getContext('2d');

    if (categoryChart) {
        categoryChart.destroy();
    }

    const colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16'];

    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.category),
            datasets: [{
                data: data.map(d => d.count),
                backgroundColor: colors.slice(0, data.length),
                borderWidth: 0,
                hoverOffset: 20,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 11 },
                        padding: 15,
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#cbd5e1',
                    borderColor: '#334155',
                    borderWidth: 1,
                    callbacks: {
                        label: (ctx) => `${ctx.label}: ${ctx.parsed} 个`
                    }
                }
            }
        }
    });
}

function getSentimentColor(sentiment) {
    switch (sentiment) {
        case 'positive': return 'text-emerald-400';
        case 'neutral': return 'text-slate-400';
        case 'negative': return 'text-rose-400';
        default: return 'text-slate-400';
    }
}

function getSentimentLabel(sentiment) {
    switch (sentiment) {
        case 'positive': return '正面';
        case 'neutral': return '中性';
        case 'negative': return '负面';
        default: return '未知';
    }
}

function getHeatColor(score) {
    if (score >= 80) return 'rose-400';
    if (score >= 60) return 'amber-400';
    return 'emerald-400';
}

async function refreshData() {
    const btn = document.querySelector('button[onclick="refreshData()"]');
    const originalHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> 加载中...';
    btn.disabled = true;

    await loadDashboard();

    btn.innerHTML = originalHtml;
    btn.disabled = false;
}

async function viewHotspotDetail(hotspotId) {
    try {
        const res = await fetch(`${API_BASE}/hotspots/${hotspotId}/analyze`, {
            method: 'POST',
        });
        const data = await res.json();

        alert(
            `热点分析结果\n\n` +
            `情感：${data.analysis.sentiment}\n` +
            `情感得分：${data.analysis.sentiment_score}\n` +
            `摘要：${data.analysis.summary}\n` +
            `关键词：${data.analysis.keywords.join(', ')}\n` +
            `预测：${data.analysis.prediction}`
        );
    } catch (error) {
        console.error('分析失败:', error);
        alert('AI 分析暂时不可用，请配置 OpenRouter API Key');
    }
}

async function generateReport() {
    try {
        const modal = document.getElementById('report-modal');
        const content = document.getElementById('report-content');

        modal.classList.remove('hidden');
        content.innerHTML = `
            <div class="flex justify-center py-10">
                <div class="loader"></div>
                <span class="ml-2 text-slate-400">AI 正在生成报告...</span>
            </div>
        `;

        const res = await fetch(`${API_BASE}/report/daily`);
        const data = await res.json();

        content.innerHTML = data.report || '<p class="text-center text-slate-500">报告生成失败</p>';
    } catch (error) {
        console.error('生成报告失败:', error);
        document.getElementById('report-content').innerHTML = `
            <p class="text-center text-slate-500 py-10">
                AI 报告生成失败<br>
                <span class="text-xs mt-2 block">请检查 OpenRouter API Key 配置</span>
            </p>
        `;
    }
}

function closeReportModal() {
    document.getElementById('report-modal').classList.add('hidden');
}

function startClock() {
    setInterval(() => {
        document.getElementById('update-time').textContent = new Date().toLocaleTimeString('zh-CN');
    }, 1000);
}

function showOfflineMode() {
    document.getElementById('hotspots-container').innerHTML = `
        <div class="p-8 text-center">
            <div class="bg-slate-800 border border-amber-500/30 rounded-xl p-6 inline-block">
                <i class="fas fa-wifi text-amber-400 text-2xl mb-3"></i>
                <h4 class="text-amber-300 font-bold mb-2">后端服务未启动</h4>
                <p class="text-sm text-slate-400 mb-4">请先启动 FastAPI 后端服务</p>
                <button onclick="refreshData()" class="bg-amber-600 hover:bg-amber-500 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all">
                    启动后刷新
                </button>
            </div>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', async () => {
    await loadDashboard();
    startClock();
    setInterval(loadDashboard, 30000);
});
